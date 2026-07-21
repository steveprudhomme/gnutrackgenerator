# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Chord symbol parsing and LilyPond conversion utilities.

The GUI lets users enter common chord symbols such as C, Cm7, F#dim7 or C7#9.
This module converts those symbols into LilyPond chord note lists.  It avoids
GUI and subprocess dependencies so the mapping can be tested independently.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


class ChordParseError(ValueError):
    """Raised when a chord symbol cannot be understood."""


@dataclass(frozen=True)
class ChordQuality:
    """Chord quality represented by scale degrees."""

    name: str
    degrees: tuple[str, ...]


# Intervals in semitones relative to the root.  Compound extensions are kept
# above the octave so LilyPond can write them as d', f', a', etc.
DEGREE_TO_SEMITONES: dict[str, int] = {
    "1": 0,
    "2": 2,
    "b3": 3,
    "3": 4,
    "4": 5,
    "b5": 6,
    "5": 7,
    "#5": 8,
    "6": 9,
    "bb7": 9,
    "b7": 10,
    "7": 11,
    "9": 14,
    "#9": 15,
    "11": 17,
    "13": 21,
}

# LilyPond's English note names.  The chosen spellings favor readability and
# validity over perfect enharmonic spelling for every theoretical context.
PITCH_CLASS_TO_LILYPOND: dict[int, str] = {
    0: "c",
    1: "cis",
    2: "d",
    3: "ees",
    4: "e",
    5: "f",
    6: "fis",
    7: "g",
    8: "aes",
    9: "a",
    10: "bes",
    11: "b",
}

ROOT_TO_PITCH_CLASS: dict[str, int] = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

# LilyPond chordmode roots. These spellings are used only for visual guitar
# fretboard diagrams, not for the audible chord notes.
ROOT_TO_LILYPOND_CHORDMODE: dict[tuple[str, str], str] = {
    ("C", ""): "c",
    ("C", "#"): "cis",
    ("C", "b"): "ces",
    ("D", ""): "d",
    ("D", "#"): "dis",
    ("D", "b"): "des",
    ("E", ""): "e",
    ("E", "#"): "eis",
    ("E", "b"): "ees",
    ("F", ""): "f",
    ("F", "#"): "fis",
    ("F", "b"): "fes",
    ("G", ""): "g",
    ("G", "#"): "gis",
    ("G", "b"): "ges",
    ("A", ""): "a",
    ("A", "#"): "ais",
    ("A", "b"): "aes",
    ("B", ""): "b",
    ("B", "#"): "bis",
    ("B", "b"): "bes",
}

# Supported symbols requested in the project roadmap/discussion.  Synonyms are
# intentionally explicit so future contributors can add more chord types safely.
CHORD_QUALITIES: dict[str, ChordQuality] = {
    "5": ChordQuality("quinte", ("1", "5")),
    "(b5)": ChordQuality("quinte diminuée", ("1", "b5")),
    "": ChordQuality("majeur", ("1", "3", "5")),
    "m": ChordQuality("mineur", ("1", "b3", "5")),
    "dim": ChordQuality("diminué", ("1", "b3", "b5")),
    "°": ChordQuality("diminué", ("1", "b3", "b5")),
    "aug": ChordQuality("augmenté", ("1", "3", "#5")),
    "+": ChordQuality("augmenté", ("1", "3", "#5")),
    "sus2": ChordQuality("suspendu 2", ("1", "2", "5")),
    "sus4": ChordQuality("suspendu 4", ("1", "4", "5")),
    "7sus4": ChordQuality("septième suspendu 4", ("1", "4", "5", "b7")),
    "add2": ChordQuality("ajout 2", ("1", "2", "3", "5")),
    "μ": ChordQuality("ajout 2", ("1", "2", "3", "5")),
    "add9": ChordQuality("ajout 9", ("1", "3", "5", "9")),
    "6": ChordQuality("sixte", ("1", "3", "5", "6")),
    "m6": ChordQuality("mineur sixte", ("1", "b3", "5", "6")),
    "maj7": ChordQuality("majeur septième", ("1", "3", "5", "7")),
    "7": ChordQuality("septième", ("1", "3", "5", "b7")),
    "m7": ChordQuality("mineur septième", ("1", "b3", "5", "b7")),
    "m7b5": ChordQuality("mineur septième quinte diminuée", ("1", "b3", "b5", "b7")),
    "ø": ChordQuality("demi-diminué", ("1", "b3", "b5", "b7")),
    "dim7": ChordQuality("diminué septième", ("1", "b3", "b5", "bb7")),
    "mM7": ChordQuality("mineur majeur septième", ("1", "b3", "5", "7")),
    "maj9": ChordQuality("majeur neuvième", ("1", "3", "5", "7", "9")),
    "9": ChordQuality("neuvième", ("1", "3", "5", "b7", "9")),
    "m9": ChordQuality("mineur neuvième", ("1", "b3", "5", "b7", "9")),
    "m11": ChordQuality("mineur onzième", ("1", "b3", "5", "b7", "9", "11")),
    "13": ChordQuality("treizième", ("1", "3", "5", "b7", "9", "11", "13")),
    "maj13": ChordQuality("majeur treizième", ("1", "3", "5", "7", "9", "11", "13")),
    "7#9": ChordQuality("septième dièse neuf", ("1", "3", "5", "b7", "#9")),
}

# LilyPond ships a predefined table of guitar fret diagrams for a limited
# family of common chords. For those symbols we can safely create a FretBoards
# track; for more complex symbols the exact chord name is still printed as text
# above the percussion staff, but no predefined guitar diagram is forced.
LILYPOND_FRETBOARD_SUFFIXES: dict[str, str] = {
    "": "",
    "m": ":m",
    "dim": ":dim",
    "°": ":dim",
    "aug": ":aug",
    "+": ":aug",
    "7": ":7",
    "maj7": ":maj7",
    "m7": ":m7",
    "9": ":9",
}

CHORD_SYMBOL_RE = re.compile(r"^\s*([A-Ga-g])([#b]?)(.*)\s*$")

# Public list used by the GUI and documentation.
SUPPORTED_CHORD_EXAMPLES: tuple[str, ...] = (
    "C5",
    "C(b5)",
    "C",
    "Cm",
    "Cdim",
    "C°",
    "Caug",
    "C+",
    "Csus2",
    "Csus4",
    "C7sus4",
    "Cadd2",
    "Cμ",
    "Cadd9",
    "C6",
    "Cm6",
    "Cmaj7",
    "C7",
    "Cm7",
    "Cm7b5",
    "Cø",
    "Cdim7",
    "CmM7",
    "Cmaj9",
    "C9",
    "Cm9",
    "Cm11",
    "C13",
    "Cmaj13",
    "C7#9",
)


def normalize_chord_symbol(symbol: str) -> tuple[str, int, str, ChordQuality]:
    """Return normalized root, root pitch class, suffix and chord quality."""
    match = CHORD_SYMBOL_RE.match(symbol or "")
    if not match:
        raise ChordParseError(
            "Accord invalide. Utilisez une fondamentale A à G, par exemple C, F#m7 ou Bbmaj7."
        )

    root_letter = match.group(1).upper()
    accidental = match.group(2)
    suffix = match.group(3).replace(" ", "")

    root_pc = ROOT_TO_PITCH_CLASS[root_letter]
    if accidental == "#":
        root_pc += 1
    elif accidental == "b":
        root_pc -= 1
    root_pc %= 12

    if suffix not in CHORD_QUALITIES:
        examples = ", ".join(SUPPORTED_CHORD_EXAMPLES[:10]) + ", ..."
        raise ChordParseError(
            f"Type d'accord non supporté: '{suffix or 'majeur'}'. Exemples: {examples}"
        )

    normalized_root = root_letter + accidental
    return normalized_root, root_pc, suffix, CHORD_QUALITIES[suffix]


def _lilypond_note_from_total_semitones(total: int) -> str:
    """Convert an absolute semitone value to a LilyPond note name."""
    pitch_class = total % 12
    octave_offset = total // 12
    note = PITCH_CLASS_TO_LILYPOND[pitch_class]
    if octave_offset > 0:
        note += "'" * octave_offset
    elif octave_offset < 0:
        note += "," * abs(octave_offset)
    return note


def chord_symbol_to_lilypond_notes(symbol: str) -> list[str]:
    """Convert a chord symbol such as 'Cmaj7' to LilyPond note names.

    Returns only the note names, without angle brackets or duration.  Example:
    C7 -> ["c", "e", "g", "bes"]
    """
    _root, root_pc, _suffix, quality = normalize_chord_symbol(symbol)
    notes: list[str] = []
    for degree in quality.degrees:
        interval = DEGREE_TO_SEMITONES[degree]
        notes.append(_lilypond_note_from_total_semitones(root_pc + interval))
    return notes


def chord_symbol_to_lilypond_chord(symbol: str) -> str:
    """Return a LilyPond chord token without duration, e.g. '<c e g>'."""
    notes = chord_symbol_to_lilypond_notes(symbol)
    return "<" + " ".join(notes) + ">"



def _split_root_for_chordmode(symbol: str) -> tuple[str, str, str]:
    """Return root letter, accidental and suffix for LilyPond chordmode uses."""
    match = CHORD_SYMBOL_RE.match(symbol or "")
    if not match:
        raise ChordParseError(
            "Accord invalide. Utilisez une fondamentale A à G, par exemple C, F#m7 ou Bbmaj7."
        )
    return match.group(1).upper(), match.group(2), match.group(3).replace(" ", "")


def chord_symbol_to_lilypond_fretboard_chord(symbol: str) -> str | None:
    """Return a LilyPond chordmode token for predefined guitar diagrams.

    Returns None when the chord is valid but outside LilyPond's predefined
    guitar-fretboard family. The caller can still print the exact text symbol
    above the staff without risking an invalid or misleading guitar diagram.
    """
    root_letter, accidental, suffix = _split_root_for_chordmode(symbol)
    # Reuse full validation so unsupported chord qualities still produce the
    # same helpful error messages as audio chord generation.
    normalize_chord_symbol(symbol)
    if suffix not in LILYPOND_FRETBOARD_SUFFIXES:
        return None
    root = ROOT_TO_LILYPOND_CHORDMODE[(root_letter, accidental)]
    return root + LILYPOND_FRETBOARD_SUFFIXES[suffix]
