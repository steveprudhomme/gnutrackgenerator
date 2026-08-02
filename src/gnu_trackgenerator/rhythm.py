# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Rhythmic subdivision helpers for chord grids.

The module is deliberately independent from the GUI and the project models. It
uses :class:`fractions.Fraction` so complex meters and triplet subdivisions are
calculated without floating-point rounding errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .arpeggiator import ArpeggiatorSettings

RHYTHM_HALF = "half"
RHYTHM_DOTTED_HALF = "dotted_half"
RHYTHM_QUARTER = "quarter"
RHYTHM_DOTTED_QUARTER = "dotted_quarter"
RHYTHM_EIGHTH = "eighth"
RHYTHM_WHOLE_TRIPLET = "whole_triplet"
RHYTHM_HALF_TRIPLET = "half_triplet"
RHYTHM_QUARTER_TRIPLET = "quarter_triplet"
RHYTHM_EIGHTH_TRIPLET = "eighth_triplet"

RHYTHM_UNIT_LABELS: dict[str, str] = {
    RHYTHM_HALF: "Blanche",
    RHYTHM_DOTTED_HALF: "Blanche pointée",
    RHYTHM_QUARTER: "Noire",
    RHYTHM_DOTTED_QUARTER: "Noire pointée",
    RHYTHM_EIGHTH: "Croche",
    RHYTHM_WHOLE_TRIPLET: "Triolet de ronde",
    RHYTHM_HALF_TRIPLET: "Triolet de blanche",
    RHYTHM_QUARTER_TRIPLET: "Triolet de noire",
    RHYTHM_EIGHTH_TRIPLET: "Triolet de croche",
}

RHYTHM_LABEL_TO_UNIT: dict[str, str] = {
    label: value for value, label in RHYTHM_UNIT_LABELS.items()
}

# Duration of one grid cell, expressed as a fraction of a whole note.
# In a triplet, three notes occupy the duration normally used by two notes of
# the same written value. A quarter-note triplet therefore lasts 1/6 of a whole
# note and an eighth-note triplet lasts 1/12.
RHYTHM_UNIT_DURATIONS: dict[str, Fraction] = {
    RHYTHM_HALF: Fraction(1, 2),
    RHYTHM_DOTTED_HALF: Fraction(3, 4),
    RHYTHM_QUARTER: Fraction(1, 4),
    RHYTHM_DOTTED_QUARTER: Fraction(3, 8),
    RHYTHM_EIGHTH: Fraction(1, 8),
    RHYTHM_WHOLE_TRIPLET: Fraction(2, 3),
    RHYTHM_HALF_TRIPLET: Fraction(1, 3),
    RHYTHM_QUARTER_TRIPLET: Fraction(1, 6),
    RHYTHM_EIGHTH_TRIPLET: Fraction(1, 12),
}

SUPPORTED_RHYTHM_UNITS = frozenset(RHYTHM_UNIT_DURATIONS)
MAX_CHORD_GRID_SLOTS = 512


@dataclass(frozen=True)
class ChordTimelineEvent:
    """One audible chord attack or one silent region on a timeline."""

    symbol: str | None
    duration: Fraction
    arpeggiator: "ArpeggiatorSettings | None" = None


@dataclass(frozen=True)
class ChordTimelineChunk:
    """Part of an event split at a measure boundary."""

    symbol: str | None
    duration: Fraction
    show_label: bool
    continues_after: bool
    ends_measure: bool
    arpeggiator: "ArpeggiatorSettings | None" = None


def line_duration(numerator: int, denominator: int, measures: int) -> Fraction:
    """Return the complete line duration in whole-note units."""
    return Fraction(numerator * measures, denominator)


def measure_duration(numerator: int, denominator: int) -> Fraction:
    """Return one measure duration in whole-note units."""
    return Fraction(numerator, denominator)


def chord_grid_durations(
    numerator: int,
    denominator: int,
    measures: int,
    rhythm_unit: str,
) -> tuple[Fraction, ...]:
    """Return one exact duration for every required chord-grid cell.

    Most grids divide the line exactly. When a dotted value does not divide the
    complete line evenly, a final shortened cell is created so the generated
    music always ends exactly at the line boundary rather than overflowing it.
    """
    if rhythm_unit not in RHYTHM_UNIT_DURATIONS:
        raise ValueError(f"Subdivision rythmique inconnue: {rhythm_unit}")
    if numerator <= 0 or denominator <= 0 or measures <= 0:
        raise ValueError("La signature et le nombre de mesures doivent être positifs.")

    remaining = line_duration(numerator, denominator, measures)
    nominal = RHYTHM_UNIT_DURATIONS[rhythm_unit]
    durations: list[Fraction] = []
    while remaining > 0:
        if len(durations) >= MAX_CHORD_GRID_SLOTS:
            raise ValueError(
                f"La grille dépasserait la limite de {MAX_CHORD_GRID_SLOTS} cases. "
                "Réduisez le nombre de mesures ou choisissez une subdivision plus grande."
            )
        current = min(nominal, remaining)
        durations.append(current)
        remaining -= current
    return tuple(durations)


def resolve_grid_events(
    values: tuple[str | None, ...],
    durations: tuple[Fraction, ...],
    arpeggiators: tuple["ArpeggiatorSettings", ...] | None = None,
) -> tuple[ChordTimelineEvent, ...]:
    """Resolve chord cells into attacks, silences, and comma continuations.

    A comma extends the immediately preceding audible chord without retriggering
    it. An empty cell creates silence. Consecutive silent cells are merged.
    """
    if len(values) != len(durations):
        raise ValueError("Le nombre de valeurs doit correspondre au nombre de cases rythmiques.")
    if arpeggiators is not None and len(arpeggiators) != len(values):
        raise ValueError("Le nombre de réglages d'arpégiateur doit correspondre au nombre de cases rythmiques.")

    events: list[ChordTimelineEvent] = []
    active_symbol: str | None = None

    for index, (raw_value, duration) in enumerate(zip(values, durations), start=1):
        value = raw_value.strip() if raw_value else None
        arpeggiator = arpeggiators[index - 1] if arpeggiators is not None else None

        if value == ",":
            if active_symbol is None or not events or events[-1].symbol is None:
                raise ValueError(
                    f"La case {index} contient une virgule, mais aucun accord précédent ne peut être prolongé."
                )
            previous = events[-1]
            events[-1] = ChordTimelineEvent(
                symbol=previous.symbol,
                duration=previous.duration + duration,
                arpeggiator=previous.arpeggiator,
            )
            continue

        if value is None:
            active_symbol = None
            if events and events[-1].symbol is None:
                previous = events[-1]
                events[-1] = ChordTimelineEvent(None, previous.duration + duration, None)
            else:
                events.append(ChordTimelineEvent(None, duration, None))
            continue

        active_symbol = value
        events.append(ChordTimelineEvent(value, duration, arpeggiator))

    return tuple(events)


def split_events_at_measure_boundaries(
    events: tuple[ChordTimelineEvent, ...],
    one_measure: Fraction,
) -> tuple[ChordTimelineChunk, ...]:
    """Split timeline events at bar lines while retaining sustain information."""
    if one_measure <= 0:
        raise ValueError("La durée d'une mesure doit être positive.")

    chunks: list[ChordTimelineChunk] = []
    offset = Fraction(0, 1)

    for event in events:
        remaining = event.duration
        first_chunk = True
        while remaining > 0:
            available = one_measure - offset
            current = min(remaining, available)
            remaining_after = remaining - current
            ends_measure = current == available
            chunks.append(
                ChordTimelineChunk(
                    symbol=event.symbol,
                    duration=current,
                    show_label=first_chunk and event.symbol is not None,
                    continues_after=remaining_after > 0,
                    ends_measure=ends_measure,
                    arpeggiator=event.arpeggiator,
                )
            )
            remaining = remaining_after
            offset += current
            if ends_measure:
                offset = Fraction(0, 1)
            first_chunk = False

    if offset != 0:
        raise ValueError("La séquence rythmique ne remplit pas un nombre entier de mesures.")
    return tuple(chunks)


# Prefer conventional LilyPond durations where possible. Multipliers are used
# for tuplets and uncommon durations produced by continuation or a shortened
# final cell.
_STANDARD_LILYPOND_DURATIONS: dict[Fraction, str] = {
    Fraction(1, 1): "1",
    Fraction(3, 4): "2.",
    Fraction(2, 3): "1*2/3",
    Fraction(1, 2): "2",
    Fraction(3, 8): "4.",
    Fraction(1, 3): "2*2/3",
    Fraction(1, 4): "4",
    Fraction(1, 6): "4*2/3",
    Fraction(3, 16): "8.",
    Fraction(1, 8): "8",
    Fraction(3, 32): "16.",
    Fraction(1, 12): "8*2/3",
    Fraction(1, 16): "16",
    Fraction(3, 64): "32.",
    Fraction(1, 32): "32",
    Fraction(3, 128): "64.",
    Fraction(1, 64): "64",
}


def lilypond_duration(duration: Fraction) -> str:
    """Convert an exact whole-note fraction to LilyPond duration syntax."""
    if duration <= 0:
        raise ValueError("Une durée LilyPond doit être positive.")
    if duration in _STANDARD_LILYPOND_DURATIONS:
        return _STANDARD_LILYPOND_DURATIONS[duration]
    return f"1*{duration.numerator}/{duration.denominator}"
