# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Arpeggiator settings and deterministic note-sequence generation.

The module is intentionally independent from the GUI. It converts one chord
symbol and one arpeggiator configuration into timed single-note events that can
be rendered by LilyPond and MIDI.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import random
from typing import Any

from .chords import (
    chord_symbol_to_arpeggio_semitones,
    pitch_semitone_to_lilypond,
)

ARP_PATTERN_DOWN_UP = "down_up"
ARP_PATTERN_UP_DOWN = "up_down"
ARP_PATTERN_RANDOM = "random"

ARP_PATTERN_LABELS: dict[str, str] = {
    ARP_PATTERN_DOWN_UP: "Descendre puis remonter",
    ARP_PATTERN_UP_DOWN: "Monter puis redescendre",
    ARP_PATTERN_RANDOM: "Notes au hasard",
}
ARP_PATTERN_LABEL_TO_VALUE = {label: value for value, label in ARP_PATTERN_LABELS.items()}
SUPPORTED_ARP_PATTERNS = frozenset(ARP_PATTERN_LABELS)

ARP_RHYTHM_SIXTEENTH = "sixteenth"
ARP_RHYTHM_EIGHTH = "eighth"
ARP_RHYTHM_QUARTER = "quarter"
ARP_RHYTHM_HALF = "half"
ARP_RHYTHM_WHOLE = "whole"

ARP_RHYTHM_LABELS: dict[str, str] = {
    ARP_RHYTHM_SIXTEENTH: "Double croche",
    ARP_RHYTHM_EIGHTH: "Croche",
    ARP_RHYTHM_QUARTER: "Noire",
    ARP_RHYTHM_HALF: "Blanche",
    ARP_RHYTHM_WHOLE: "Ronde",
}
ARP_RHYTHM_LABEL_TO_VALUE = {label: value for value, label in ARP_RHYTHM_LABELS.items()}
ARP_RHYTHM_DURATIONS: dict[str, Fraction] = {
    ARP_RHYTHM_SIXTEENTH: Fraction(1, 16),
    ARP_RHYTHM_EIGHTH: Fraction(1, 8),
    ARP_RHYTHM_QUARTER: Fraction(1, 4),
    ARP_RHYTHM_HALF: Fraction(1, 2),
    ARP_RHYTHM_WHOLE: Fraction(1, 1),
}
SUPPORTED_ARP_RHYTHMS = frozenset(ARP_RHYTHM_DURATIONS)

MAX_ARPEGGIATOR_OCTAVES = 8
MAX_TUPLET_COUNT = 32
MAX_ARPEGGIO_STEPS = 4096


class ArpeggiatorError(ValueError):
    """Raised when an arpeggiator setting or sequence is invalid."""


def _greatest_power_of_two_not_exceeding(value: int) -> int:
    """Return the conventional binary note count used by a tuplet ratio.

    Examples: 3 -> 2, 5 -> 4, 7 -> 4, 9 -> 8. This produces conventional
    LilyPond ratios such as 3/2, 5/4, 7/4 and 9/8 while preserving the user's
    requested total duration for the complete group.
    """
    if value < 1:
        raise ValueError("La valeur doit être positive.")
    return 1 << (value.bit_length() - 1)


@dataclass(frozen=True)
class ArpeggiatorSettings:
    """Configuration attached to one chord-entry field.

    When ``tuplet_count`` is zero, ``rhythm`` is the duration of each generated
    arpeggio note, as in earlier project versions.

    When ``tuplet_count`` is ``N`` (3 to 32), ``rhythm`` is instead the total
    duration of one complete N-olet group. The engine generates exactly ``N``
    attacks inside that duration. For example, ``rhythm='whole'`` and
    ``tuplet_count=7`` creates seven notes spanning one whole note, represented
    conventionally as ``\\tuplet 7/4`` with seven written quarter notes.
    """

    enabled: bool = False
    pattern: str = ARP_PATTERN_UP_DOWN
    octaves: int = 1
    rhythm: str = ARP_RHYTHM_EIGHTH
    dotted: bool = False
    tuplet_count: int = 0

    def validate(self) -> None:
        if self.pattern not in SUPPORTED_ARP_PATTERNS:
            raise ArpeggiatorError("Motif d'arpégiateur invalide.")
        if not 1 <= self.octaves <= MAX_ARPEGGIATOR_OCTAVES:
            raise ArpeggiatorError(
                f"Le nombre d'octaves doit être compris entre 1 et {MAX_ARPEGGIATOR_OCTAVES}."
            )
        if self.rhythm not in SUPPORTED_ARP_RHYTHMS:
            raise ArpeggiatorError("Valeur rythmique d'arpégiateur invalide.")
        if self.tuplet_count != 0 and not 3 <= self.tuplet_count <= MAX_TUPLET_COUNT:
            raise ArpeggiatorError(
                f"Le N-olet doit être 0 (désactivé) ou un nombre de 3 à {MAX_TUPLET_COUNT}."
            )

    @property
    def normalized_tuplet_count(self) -> int:
        """Return the validated N-olet count, or 0 when disabled."""
        self.validate()
        return self.tuplet_count

    @property
    def selected_rhythm_duration(self) -> Fraction:
        """Return the duration selected in the UI, including a possible dot."""
        self.validate()
        duration = ARP_RHYTHM_DURATIONS[self.rhythm]
        if self.dotted:
            duration *= Fraction(3, 2)
        return duration

    @property
    def tuplet_normal_count(self) -> int:
        """Return the denominator of the conventional LilyPond tuplet ratio.

        For example, 7 notes use a 7/4 ratio, while 9 notes use a 9/8 ratio.
        Zero means that N-olet mode is disabled.
        """
        count = self.normalized_tuplet_count
        if not count:
            return 0
        return _greatest_power_of_two_not_exceeding(count)

    @property
    def tuplet_scale(self) -> Fraction:
        """Return actual-duration / written-duration for one tuplet note."""
        count = self.normalized_tuplet_count
        if not count:
            return Fraction(1, 1)
        return Fraction(self.tuplet_normal_count, count)

    @property
    def written_note_duration(self) -> Fraction:
        """Return the notated duration of each generated arpeggio note.

        Outside N-olet mode, this is simply the selected note value. In N-olet
        mode, the selected value is the whole group duration and is divided by
        the conventional binary count. A whole-note septuplet therefore writes
        seven quarter notes under ``\\tuplet 7/4``.
        """
        count = self.normalized_tuplet_count
        if not count:
            return self.selected_rhythm_duration
        return self.selected_rhythm_duration / self.tuplet_normal_count

    @property
    def step_duration(self) -> Fraction:
        """Return the audible duration of one generated arpeggio note.

        With N-olet mode enabled, exactly N equal attacks fill the selected
        rhythmic duration. Thus a whole-note septuplet has a step duration of
        1/7 of a whole note.
        """
        count = self.normalized_tuplet_count
        if not count:
            return self.selected_rhythm_duration
        return self.selected_rhythm_duration / count

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "enabled": self.enabled,
            "pattern": self.pattern,
            "octaves": self.octaves,
            "rhythm": self.rhythm,
            "dotted": self.dotted,
            "tuplet_count": self.normalized_tuplet_count,
        }

    @classmethod
    def from_dict(cls, payload: Any) -> "ArpeggiatorSettings":
        if payload is None or payload == "":
            return cls()
        if not isinstance(payload, dict):
            raise ArpeggiatorError("La configuration d'arpégiateur doit être un objet JSON.")
        try:
            settings = cls(
                enabled=bool(payload.get("enabled", False)),
                pattern=str(payload.get("pattern", ARP_PATTERN_UP_DOWN)),
                octaves=int(payload.get("octaves", 1)),
                rhythm=str(payload.get("rhythm", ARP_RHYTHM_EIGHTH)),
                dotted=bool(payload.get("dotted", False)),
                tuplet_count=int(payload.get("tuplet_count", 0)),
            )
        except (TypeError, ValueError) as exc:
            raise ArpeggiatorError("Configuration d'arpégiateur invalide.") from exc
        settings.validate()
        return settings


@dataclass(frozen=True)
class ArpeggioStep:
    """One arpeggiated note with actual and written durations."""

    note: str
    actual_duration: Fraction
    written_duration: Fraction
    starts_tuplet: bool = False
    ends_tuplet: bool = False


def _directional_cycle(pitches: list[int], pattern: str) -> list[int]:
    if len(pitches) <= 1:
        return pitches
    if pattern == ARP_PATTERN_UP_DOWN:
        return pitches + pitches[-2:0:-1]
    if pattern == ARP_PATTERN_DOWN_UP:
        descending = list(reversed(pitches))
        return descending + pitches[1:-1]
    return pitches


def _stable_seed(seed_key: str) -> int:
    digest = hashlib.sha256(seed_key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def generate_arpeggio_steps(
    chord_symbol: str,
    duration: Fraction,
    settings: ArpeggiatorSettings,
    *,
    seed_key: str = "",
) -> tuple[ArpeggioStep, ...]:
    """Generate notes that fill ``duration`` exactly.

    Without N-olet mode, notes use the selected value until the event ends and
    the final note may be shortened.

    With N-olet mode, each complete group spans the selected rhythmic duration
    and contains exactly N attacks. If an event ends before a complete selected
    group can fit, a final shortened group still contains exactly N equally
    spaced attacks so the chord ends precisely at its timeline boundary.

    Random patterns are deterministic for the same chord, settings and seed key,
    which keeps repeated project generation reproducible.
    """
    settings.validate()
    if not settings.enabled:
        return ()
    if duration <= 0:
        raise ArpeggiatorError("La durée d'un arpège doit être positive.")

    pitches = chord_symbol_to_arpeggio_semitones(chord_symbol, settings.octaves)
    if not pitches:
        raise ArpeggiatorError("L'accord ne contient aucune note utilisable par l'arpégiateur.")

    cycle = _directional_cycle(pitches, settings.pattern)
    rng = random.Random(
        _stable_seed(
            f"{seed_key}|{chord_symbol}|{settings.pattern}|{settings.octaves}|"
            f"{settings.rhythm}|{settings.dotted}|{settings.normalized_tuplet_count}"
        )
    )

    steps: list[ArpeggioStep] = []
    previous_pitch: int | None = None
    sequence_index = 0

    def next_pitch() -> int:
        nonlocal previous_pitch, sequence_index
        if settings.pattern == ARP_PATTERN_RANDOM:
            pitch = rng.choice(pitches)
            if len(pitches) > 1 and pitch == previous_pitch:
                alternatives = [candidate for candidate in pitches if candidate != previous_pitch]
                pitch = rng.choice(alternatives)
        else:
            pitch = cycle[sequence_index % len(cycle)]
        previous_pitch = pitch
        sequence_index += 1
        return pitch

    tuplet_count = settings.normalized_tuplet_count
    if not tuplet_count:
        remaining = duration
        while remaining > 0:
            if len(steps) >= MAX_ARPEGGIO_STEPS:
                raise ArpeggiatorError(
                    f"L'arpège dépasserait la limite de {MAX_ARPEGGIO_STEPS} notes. "
                    "Choisissez une valeur rythmique plus grande ou réduisez la durée."
                )
            actual = min(settings.step_duration, remaining)
            steps.append(
                ArpeggioStep(
                    note=pitch_semitone_to_lilypond(next_pitch()),
                    actual_duration=actual,
                    written_duration=actual,
                )
            )
            remaining -= actual
        return tuple(steps)

    # N-olet mode: the selected rhythm is the total duration of one group.
    remaining = duration
    normal_count = settings.tuplet_normal_count
    while remaining > 0:
        if len(steps) + tuplet_count > MAX_ARPEGGIO_STEPS:
            raise ArpeggiatorError(
                f"L'arpège dépasserait la limite de {MAX_ARPEGGIO_STEPS} notes. "
                "Choisissez une valeur rythmique plus grande, réduisez N ou réduisez la durée."
            )

        group_duration = min(settings.selected_rhythm_duration, remaining)
        actual_per_note = group_duration / tuplet_count
        written_per_note = group_duration / normal_count

        for group_index in range(tuplet_count):
            steps.append(
                ArpeggioStep(
                    note=pitch_semitone_to_lilypond(next_pitch()),
                    actual_duration=actual_per_note,
                    written_duration=written_per_note,
                    starts_tuplet=group_index == 0,
                    ends_tuplet=group_index == tuplet_count - 1,
                )
            )
        remaining -= group_duration

    return tuple(steps)
