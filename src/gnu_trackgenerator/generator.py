# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Generation engine for GNU TrackGenerator.

The GUI calls this module, but this module never imports the GUI. It owns the
local generation pipeline:

1. Save .gen project JSON.
2. Generate .ly LilyPond source.
3. Run LilyPond through subprocess to produce MIDI.
4. Run TiMidity or FluidSynth through subprocess to produce WAV.

The engine can report every generated file and every external command to a log
callback. This is intentionally useful for troubleshooting local installations
of LilyPond, TiMidity and FluidSynth.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .chords import (
    ChordParseError,
    chord_symbol_to_lilypond_chord,
    chord_symbol_to_lilypond_fretboard_chord,
)
from .models import (
    APP_NAME,
    APP_VERSION,
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
    CHORD_INSTRUMENT_PIANO,
    CHORD_INSTRUMENT_STRINGS,
    ProjectData,
    Segment,
)
from .project_io import save_project


class GenerationError(RuntimeError):
    """Raised when a subprocess or external dependency fails."""


LogCallback = Callable[[str], None]


@dataclass(frozen=True)
class GenerationResult:
    """Paths created by one successful generation run."""

    gen_path: Path
    lilypond_path: Path
    midi_path: Path
    wav_path: Path
    command_log_path: Path


@dataclass(frozen=True)
class WavDiagnostics:
    """Small diagnostic summary for a generated PCM WAV file."""

    duration_seconds: float
    channels: int
    frame_rate: int
    sample_width: int
    peak: float


LILYPOND_MIDI_INSTRUMENTS: dict[str, str] = {
    CHORD_INSTRUMENT_PIANO: "acoustic grand",
    CHORD_INSTRUMENT_STRINGS: "string ensemble 1",
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR: "acoustic guitar (steel)",
}


LILYPOND_INSTRUMENT_NAMES: dict[str, str] = {
    CHORD_INSTRUMENT_PIANO: "Piano",
    CHORD_INSTRUMENT_STRINGS: "Strings",
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR: "Guitare",
}


def _safe_stem(name: str) -> str:
    """Return a filesystem-friendly file stem."""
    cleaned = "".join(char if char.isalnum() or char in "-_" else "_" for char in name.strip())
    return cleaned or "gnu_trackgenerator_click"


def _format_command(command: list[str]) -> str:
    """Format a command so the user can copy it in a terminal.

    subprocess.list2cmdline uses Windows-friendly quoting, which is useful for
    the main target environment of this desktop application while remaining
    readable on other platforms.
    """
    return subprocess.list2cmdline([str(part) for part in command])


def _emit(on_log: LogCallback | None, message: str) -> None:
    """Send one message to the optional generation log."""
    if on_log:
        on_log(message)


def _require_executable(binary_name: str, on_log: LogCallback | None = None) -> str:
    """Return the executable path or raise a helpful error."""
    executable = shutil.which(binary_name)
    if not executable:
        raise GenerationError(
            f"Impossible de trouver '{binary_name}' sur le PATH de l'OS. "
            "Installez l'outil ou ajoutez-le au PATH avant de générer."
        )
    _emit(on_log, f"[outil trouvé] {binary_name} -> {executable}")
    return executable


def _run_command(command: list[str], cwd: Path, on_log: LogCallback | None = None) -> subprocess.CompletedProcess[str]:
    """Run a command and convert subprocess failures into GenerationError."""
    display = _format_command(command)
    _emit(on_log, "")
    _emit(on_log, f"[répertoire] {cwd}")
    _emit(on_log, f"[commande] {display}")

    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise GenerationError(f"Commande introuvable: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        stdout = (exc.stdout or "").strip()
        stderr = (exc.stderr or "").strip()
        if stdout:
            _emit(on_log, f"[stdout]\n{stdout}")
        if stderr:
            _emit(on_log, f"[stderr]\n{stderr}")
        _emit(on_log, f"[code retour] {exc.returncode}")
        details = "\n".join(part for part in [stdout, stderr] if part)
        raise GenerationError(
            f"La commande a échoué: {display}\n{details}"
        ) from exc

    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()
    if stdout:
        _emit(on_log, f"[stdout]\n{stdout}")
    if stderr:
        # LilyPond and audio tools sometimes report useful warnings on stderr
        # even when the command succeeds. We intentionally show them.
        _emit(on_log, f"[stderr]\n{stderr}")
    _emit(on_log, f"[code retour] {completed.returncode}")
    return completed


def _timidity_cfg_path_for(wav_path: Path) -> Path:
    """Return the generated TiMidity++ configuration path for one output file."""
    return wav_path.with_suffix(".timidity.cfg")


def _timidity_cfg_escape(path: Path) -> str:
    """Return a TiMidity++-friendly path string.

    TiMidity++ configuration files can be sensitive to Windows backslashes.
    Forward slashes are accepted by Windows APIs and avoid accidental escape-like
    sequences in the generated `.cfg` file.
    """
    return str(path.resolve()).replace("\\", "/")


def _write_timidity_soundfont_config(
    soundfont_path: Path,
    wav_path: Path,
    on_log: LogCallback | None = None,
) -> Path:
    """Write a small TiMidity++ config that loads the selected SoundFont.

    The application deliberately generates this file next to the WAV so the
    troubleshooting log shows exactly which SoundFont was used. This avoids
    depending on a hidden global `timidity.cfg` installation.
    """
    cfg_path = _timidity_cfg_path_for(wav_path)
    cfg_content = (
        "# Auto-generated by GNU TrackGenerator.\n"
        "# This file tells TiMidity++ which SoundFont to use for this render.\n"
        f'soundfont "{_timidity_cfg_escape(soundfont_path)}" order=0 amp=120\n'
    )
    cfg_path.write_text(cfg_content, encoding="utf-8")
    _emit(on_log, f"[fichier écrit] {cfg_path}")
    _emit(on_log, f"[SoundFont TiMidity] {soundfont_path}")
    _emit(on_log, f"[configuration TiMidity]\n{cfg_content.rstrip()}")
    return cfg_path


def _segment_measure_pattern(segment: Segment) -> str:
    """Build one measure of click-track drum notes for a segment.

    Rule required by the specification:
    - first subdivision: bass drum, LilyPond abbreviated name `bd`
    - all other subdivisions: snare, LilyPond abbreviated name `sn`

    If the user entered a chord symbol, it is printed above the first click of
    every measure. This keeps the PDF readable even when a complex chord is not
    available in LilyPond's predefined guitar-fretboard table.
    """
    duration = str(segment.denominator)
    notes = [f"bd{duration}{_chord_symbol_markup(segment)}"]
    notes.extend(f"sn{duration}" for _ in range(segment.numerator - 1))
    return " ".join(notes)


def _measure_duration_multiplier(segment: Segment) -> str:
    """Return a LilyPond multiplier representing one full measure."""
    return f"1*{segment.numerator}/{segment.denominator}"


def _lilypond_string_literal(value: str) -> str:
    """Escape a Python string so it can be used inside LilyPond quotes."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _chord_symbol_markup(segment: Segment) -> str:
    """Return the exact chord symbol markup printed above the click staff."""
    if not segment.chord_symbol:
        return ""
    symbol = _lilypond_string_literal(segment.chord_symbol.strip())
    return f'^\\markup {{ \\bold "{symbol}" }}'


def _segment_chord_measure_pattern(segment: Segment, segment_index: int) -> str:
    """Build one chord measure for the optional harmony staff."""
    duration = _measure_duration_multiplier(segment)
    if not segment.chord_symbol:
        return f"r{duration}"

    try:
        chord = chord_symbol_to_lilypond_chord(segment.chord_symbol)
    except ChordParseError as exc:
        raise GenerationError(f"Accord invalide à la rangée {segment_index}: {exc}") from exc

    # Guitar chords are rendered as strummed/arpeggiated chords. LilyPond's
    # \arpeggio produces a visual strum marker and a more idiomatic guitar score.
    if segment.chord_instrument == CHORD_INSTRUMENT_ACOUSTIC_GUITAR:
        return f"{chord}{duration}\\arpeggio"
    return f"{chord}{duration}"


def _build_click_music(project: ProjectData) -> str:
    """Build the DrumStaff music body."""
    music_lines: list[str] = []
    for index, segment in enumerate(project.segments, start=1):
        pattern = _segment_measure_pattern(segment)
        music_lines.extend(
            [
                f"  % Segment {index}: {segment.numerator}/{segment.denominator}, "
                f"{segment.bpm} BPM, {segment.measures} mesure(s)",
                f"  \\time {segment.numerator}/{segment.denominator}",
                # BPM is interpreted on the denominator beat unit.
                # Example: 7/8 at 120 => eighth-note = 120.
                f"  \\tempo {segment.denominator} = {segment.bpm}",
                f"  \\repeat unfold {segment.measures} {{ {pattern} | }}",
                "",
            ]
        )
    return "\n".join(music_lines).rstrip()


def _build_chord_music(project: ProjectData) -> str:
    """Build the optional chord staff music body."""
    music_lines: list[str] = []
    current_instrument: str | None = None

    for index, segment in enumerate(project.segments, start=1):
        instrument = segment.chord_instrument
        midi_instrument = LILYPOND_MIDI_INSTRUMENTS.get(instrument, "acoustic grand")
        instrument_name = LILYPOND_INSTRUMENT_NAMES.get(instrument, "Accords")
        pattern = _segment_chord_measure_pattern(segment, index)

        music_lines.extend(
            [
                f"  % Accords segment {index}: {segment.chord_symbol or 'silence'}",
                f"  \\time {segment.numerator}/{segment.denominator}",
                f"  \\tempo {segment.denominator} = {segment.bpm}",
            ]
        )
        if instrument != current_instrument:
            music_lines.extend(
                [
                    f"  \\set Staff.instrumentName = #\"{instrument_name}\"",
                    f"  \\set Staff.midiInstrument = #\"{midi_instrument}\"",
                ]
            )
            current_instrument = instrument

        if segment.chord_instrument == CHORD_INSTRUMENT_ACOUSTIC_GUITAR:
            music_lines.append("  \\arpeggioArrowUp")

        music_lines.extend(
            [
                f"  \\repeat unfold {segment.measures} {{ {pattern} | }}",
                "",
            ]
        )

    return "\n".join(music_lines).rstrip()


def _segment_fretboard_measure_pattern(segment: Segment, segment_index: int) -> str:
    """Build one measure for the optional guitar fretboard diagram track."""
    duration = _measure_duration_multiplier(segment)
    if segment.chord_instrument != CHORD_INSTRUMENT_ACOUSTIC_GUITAR or not segment.chord_symbol:
        return f"s{duration}"

    try:
        chordmode_token = chord_symbol_to_lilypond_fretboard_chord(segment.chord_symbol)
    except ChordParseError as exc:
        raise GenerationError(f"Accord invalide à la rangée {segment_index}: {exc}") from exc

    if chordmode_token is None:
        # The exact text symbol still appears above the DrumStaff. We skip the
        # diagram here because LilyPond's predefined guitar table does not cover
        # every extended or altered chord.
        return f"s{duration}"

    # LilyPond chordmode expects the duration immediately after the root, before
    # the chord quality. For example, A minor over a 7/4 measure must be written
    # as `a1*7/4:m`, not `a:m1*7/4`. The latter causes the exact syntax error
    # reported by LilyPond: "unexpected '*'".
    if ":" in chordmode_token:
        root, quality = chordmode_token.split(":", 1)
        return f"{root}{duration}:{quality}"
    return f"{chordmode_token}{duration}"


def _build_fretboard_music(project: ProjectData) -> str:
    """Build the optional FretBoards music body for acoustic-guitar chords."""
    music_lines: list[str] = []
    for index, segment in enumerate(project.segments, start=1):
        pattern = _segment_fretboard_measure_pattern(segment, index)
        music_lines.extend(
            [
                f"  % Diagrammes guitare segment {index}: {segment.chord_symbol or 'aucun'}",
                f"  \\time {segment.numerator}/{segment.denominator}",
                f"  \\repeat unfold {segment.measures} {{ {pattern} | }}",
                "",
            ]
        )
    return "\n".join(music_lines).rstrip()


def build_lilypond_source(project: ProjectData, title: str = APP_NAME) -> str:
    """Generate the full LilyPond source for a project."""
    project.validate()

    click_music = _build_click_music(project)
    has_chords = any(segment.chord_symbol for segment in project.segments)
    has_guitar_chords = any(
        segment.chord_symbol and segment.chord_instrument == CHORD_INSTRUMENT_ACOUSTIC_GUITAR
        for segment in project.segments
    )
    chord_music = _build_chord_music(project) if has_chords else ""
    fretboard_music = _build_fretboard_music(project) if has_guitar_chords else ""

    include_fretboards = '\n\\include "predefined-guitar-fretboards.ly"\n' if has_guitar_chords else ""

    if has_chords:
        chord_definition = f"""
chordTrack = {{
{chord_music}
}}
"""
    else:
        chord_definition = ""

    if has_guitar_chords:
        fretboard_definition = f"""
fretBoardTrack = \\chordmode {{
{fretboard_music}
}}
"""
    else:
        fretboard_definition = ""

    if has_chords:
        contexts = """    \\new DrumStaff \\with {
      instrumentName = "Click"
    } {
      \\clickTrack
    }
    \\new Staff \\with {
      instrumentName = "Accords"
      midiInstrument = "acoustic grand"
    } {
      \\chordTrack
    }"""
        if has_guitar_chords:
            contexts = """    \\new FretBoards {
      \\fretBoardTrack
    }
""" + contexts
        score_body = f"""<<
{contexts}
  >>"""
    else:
        score_body = """\\new DrumStaff \\with {
    instrumentName = "Click"
  } {
    \\clickTrack
  }"""

    return f"""% Auto-generated by {APP_NAME} {APP_VERSION}
% Do not edit this file manually unless you know what you are doing.

\\version "2.24.0"{include_fretboards}
\\header {{
  title = "{title}"
  composer = "{APP_NAME}"
  tagline = "Generated with {APP_NAME} {APP_VERSION}"
}}

clickTrack = \\drummode {{
{click_music}
}}
{chord_definition}{fretboard_definition}\\score {{
  {score_body}
  \\layout {{ }}
  \\midi {{ }}
}}
"""


def write_lilypond_file(
    project: ProjectData,
    path: str | Path,
    title: str = APP_NAME,
    on_log: LogCallback | None = None,
) -> Path:
    """Write a .ly file and return its path."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_lilypond_source(project, title=title), encoding="utf-8")
    _emit(on_log, f"[fichier écrit] {target}")
    return target


def compile_lilypond_to_midi(
    lilypond_path: str | Path,
    output_stem: str | Path,
    lilypond_binary: str = "lilypond",
    on_log: LogCallback | None = None,
) -> Path:
    """Compile a LilyPond file to MIDI and return the .mid path.

    LilyPond commonly writes `.midi`. The application normalizes the result to
    `.mid` because the user-facing specification asks for a .mid file.
    """
    lilypond_executable = _require_executable(lilypond_binary, on_log=on_log)
    ly_path = Path(lilypond_path)
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)

    command = [
        lilypond_executable,
        "-dno-point-and-click",
        "-o",
        str(stem),
        str(ly_path),
    ]
    _run_command(command, cwd=stem.parent, on_log=on_log)

    midi_candidates = [stem.with_suffix(".midi"), stem.with_suffix(".mid")]
    produced = next((candidate for candidate in midi_candidates if candidate.exists()), None)
    if produced is None:
        raise GenerationError("LilyPond a terminé sans produire de fichier MIDI attendu.")

    normalized = stem.with_suffix(".mid")
    if produced != normalized:
        if normalized.exists():
            normalized.unlink()
        produced.rename(normalized)
    _emit(on_log, f"[fichier MIDI] {normalized} ({normalized.stat().st_size} octets)")
    return normalized


def _wav_peak_amplitude(wav_path: Path) -> WavDiagnostics | None:
    """Return basic PCM WAV diagnostics.

    Returns None if the WAV format cannot be analyzed by Python's wave module.
    """
    try:
        with wave.open(str(wav_path), "rb") as reader:
            channels = reader.getnchannels()
            frame_rate = reader.getframerate()
            sample_width = reader.getsampwidth()
            frame_count = reader.getnframes()
            duration = frame_count / frame_rate if frame_rate else 0.0
            peak = 0
            while True:
                chunk = reader.readframes(4096)
                if not chunk:
                    break
                if sample_width == 1:
                    chunk_peak = max((abs(byte - 128) for byte in chunk), default=0)
                elif sample_width in {2, 3, 4}:
                    values = (
                        abs(int.from_bytes(chunk[i : i + sample_width], "little", signed=True))
                        for i in range(0, len(chunk) - sample_width + 1, sample_width)
                    )
                    chunk_peak = max(values, default=0)
                else:
                    return None
                peak = max(peak, chunk_peak)
            return WavDiagnostics(duration, channels, frame_rate, sample_width, float(peak))
    except (wave.Error, OSError, EOFError):
        return None


def _log_wav_diagnostics(wav_path: Path, on_log: LogCallback | None = None) -> WavDiagnostics | None:
    """Log size and silence diagnostics for the produced WAV file."""
    if not wav_path.exists():
        _emit(on_log, f"[diagnostic WAV] Fichier absent: {wav_path}")
        return None

    size = wav_path.stat().st_size
    _emit(on_log, f"[fichier WAV] {wav_path} ({size} octets)")
    if size <= 44:
        _emit(on_log, "[avertissement] Le WAV est vide ou presque vide. Il ne contient probablement pas d'audio utile.")
        return None

    diagnostics = _wav_peak_amplitude(wav_path)
    if diagnostics is None:
        _emit(on_log, "[diagnostic WAV] Impossible d'analyser automatiquement l'amplitude du fichier WAV.")
        return None

    _emit(
        on_log,
        "[diagnostic WAV] "
        f"durée={diagnostics.duration_seconds:.2f}s, canaux={diagnostics.channels}, "
        f"fréquence={diagnostics.frame_rate}Hz, "
        f"échantillon={diagnostics.sample_width * 8} bits, pic={diagnostics.peak:.0f}",
    )
    if diagnostics.peak == 0:
        _emit(
            on_log,
            "[avertissement] Le WAV semble silencieux. Vérifiez la configuration TiMidity/FluidSynth "
            "et la présence d'une banque de sons/SoundFont valide.",
        )
    elif diagnostics.peak < 20:
        _emit(
            on_log,
            "[avertissement] Le WAV semble extrêmement faible. Le rendu MIDI fonctionne peut-être, "
            "mais le volume ou la banque de sons doit être vérifié.",
        )
    return diagnostics


def render_midi_to_wav(
    midi_path: str | Path,
    wav_path: str | Path,
    soundfont_path: str | Path | None = None,
    prefer: str = "timidity",
    on_log: LogCallback | None = None,
) -> Path:
    """Render MIDI to WAV using TiMidity first, with FluidSynth as fallback.

    TiMidity is preferred because the project currently targets a lighter setup
    that can work when TiMidity is configured system-wide. FluidSynth remains
    available as a fallback and generally needs a SoundFont (.sf2 or .sf3).
    """
    midi = Path(midi_path)
    wav = Path(wav_path)
    wav.parent.mkdir(parents=True, exist_ok=True)

    env_soundfont = os.environ.get("TRACKGENERATOR_SOUNDFONT")
    sf2 = Path(soundfont_path or env_soundfont) if (soundfont_path or env_soundfont) else None

    fluidsynth = shutil.which("fluidsynth")
    timidity = shutil.which("timidity")

    use_fluidsynth_first = prefer.lower() == "fluidsynth"
    tools = ["fluidsynth", "timidity"] if use_fluidsynth_first else ["timidity", "fluidsynth"]

    if sf2:
        if sf2.exists():
            _emit(on_log, f"[SoundFont sélectionné] {sf2}")
        else:
            _emit(on_log, f"[avertissement] SoundFont introuvable: {sf2}")

    last_error: GenerationError | None = None
    for tool in tools:
        if tool == "timidity" and timidity:
            # Standard TiMidity++ WAV rendering. If a SoundFont was selected,
            # write and pass an explicit .timidity.cfg so TiMidity does not rely
            # on an incomplete global configuration file.
            command = [timidity]
            if sf2 and sf2.exists():
                cfg_path = _write_timidity_soundfont_config(sf2, wav, on_log=on_log)
                command.extend(["-c", str(cfg_path)])
            else:
                _emit(
                    on_log,
                    "[avertissement] Aucun SoundFont valide n'est transmis à TiMidity. "
                    "Le rendu dépendra de la configuration globale timidity.cfg.",
                )
            command.extend(["-A120", "-Ow", "-o", str(wav), str(midi)])
            _run_command(command, cwd=wav.parent, on_log=on_log)
            diagnostics = _log_wav_diagnostics(wav, on_log=on_log)
            if diagnostics is None or diagnostics.peak >= 20 or not fluidsynth or not sf2 or not sf2.exists():
                return wav

            _emit(
                on_log,
                "[repli] Le rendu TiMidity est encore trop faible. "
                "Nouvelle tentative avec FluidSynth et le même SoundFont.",
            )
            # Continue to the FluidSynth branch when available.
            continue

        if tool == "fluidsynth" and fluidsynth:
            if not sf2 or not sf2.exists():
                last_error = GenerationError(
                    "FluidSynth est installé, mais aucun SoundFont valide (.sf2/.sf3) n'a été fourni. "
                    "Sélectionnez un SoundFont dans l'interface ou définissez TRACKGENERATOR_SOUNDFONT."
                )
                _emit(on_log, f"[outil ignoré] FluidSynth: {last_error}")
                continue
            command = [
                fluidsynth,
                "-ni",
                "-T",
                "wav",
                "-F",
                str(wav),
                str(sf2),
                str(midi),
            ]
            _run_command(command, cwd=wav.parent, on_log=on_log)
            _log_wav_diagnostics(wav, on_log=on_log)
            return wav

    if last_error:
        raise last_error
    raise GenerationError(
        "Aucun moteur MIDI -> WAV trouvé. Installez TiMidity ou FluidSynth."
    )


def _write_command_log(log_path: Path, lines: list[str]) -> None:
    """Persist generation logs next to the generated files."""
    log_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def generate_project(
    project: ProjectData,
    output_dir: str | Path,
    base_name: str = "gnu_trackgenerator_click",
    lilypond_binary: str = "lilypond",
    on_log: LogCallback | None = None,
) -> GenerationResult:
    """Run the complete local generation pipeline."""
    project.validate()
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / _safe_stem(base_name)
    command_log_path = stem.with_suffix(".commands.txt")
    log_lines: list[str] = []

    def log(message: str) -> None:
        log_lines.append(message)
        _emit(on_log, message)

    log(f"GNU TrackGenerator {APP_VERSION} — journal de génération")
    log(f"[sortie] {out_dir}")
    log(f"[nom de base] {stem.name}")

    try:
        gen_path = save_project(project, stem.with_suffix(".gen"))
        log(f"[fichier écrit] {gen_path}")
        ly_path = write_lilypond_file(project, stem.with_suffix(".ly"), title=stem.name, on_log=log)
        midi_path = compile_lilypond_to_midi(ly_path, stem, lilypond_binary=lilypond_binary, on_log=log)
        wav_path = render_midi_to_wav(
            midi_path,
            stem.with_suffix(".wav"),
            soundfont_path=project.soundfont_path,
            prefer="timidity",
            on_log=log,
        )
        log(f"[journal écrit] {command_log_path}")
        _write_command_log(command_log_path, log_lines)
    except Exception:
        log(f"[journal écrit malgré erreur] {command_log_path}")
        try:
            _write_command_log(command_log_path, log_lines)
        except OSError:
            pass
        raise

    return GenerationResult(
        gen_path=gen_path,
        lilypond_path=ly_path,
        midi_path=midi_path,
        wav_path=wav_path,
        command_log_path=command_log_path,
    )
