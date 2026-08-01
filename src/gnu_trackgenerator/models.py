# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Domain models for GNU TrackGenerator.

This module intentionally contains no GUI code and no subprocess calls.  It is
safe to unit-test in isolation and represents the musical/project data model.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

APP_NAME = "GNU TrackGenerator"
APP_VERSION = "0.2.0"

# LilyPond note durations are represented by powers of two: 1, 2, 4, 8, 16...
# Keeping the denominator in this set supports common and complex meters such as
# 7/8, 11/16, 27/16, 5/4, etc.
SUPPORTED_DENOMINATORS = {1, 2, 4, 8, 16, 32, 64}

CHORD_INSTRUMENT_PIANO = "piano"
CHORD_INSTRUMENT_STRINGS = "strings"
CHORD_INSTRUMENT_ACOUSTIC_GUITAR = "acoustic_guitar"

SUPPORTED_CHORD_INSTRUMENTS = {
    CHORD_INSTRUMENT_PIANO,
    CHORD_INSTRUMENT_STRINGS,
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
}

CHORD_MODE_NONE = "none"
CHORD_MODE_LINE = "line"
CHORD_MODE_MEASURE = "measure"

SUPPORTED_CHORD_MODES = {
    CHORD_MODE_NONE,
    CHORD_MODE_LINE,
    CHORD_MODE_MEASURE,
}


class ValidationError(ValueError):
    """Raised when the project or one of its musical segments is invalid."""


@dataclass(frozen=True)
class Segment:
    """A programmable click-track segment.

    Args:
        bpm: Tempo. In this first version, the beat unit is the denominator of
            the time signature. Example: 7/8 at 120 means eighth-note = 120.
        numerator: Number of subdivisions in each measure.
        denominator: LilyPond rhythmic duration used by each subdivision.
        measures: Number of measures to repeat this pattern.
        chord_symbol: Optional chord symbol entered by the user, e.g. C, Cm7,
            F#dim7 or Bbmaj9. The symbol is parsed during generation.
        chord_instrument: Instrument used for the optional chord staff.
        chord_mode: Chord-entry mode: no chord, one chord repeated for the
            entire line, or one independently editable chord per measure.
        measure_chords: Chord symbols associated with individual measures.
            Empty entries represent silent measures.
    """

    bpm: int
    numerator: int
    denominator: int
    measures: int
    chord_symbol: str | None = None
    chord_instrument: str = CHORD_INSTRUMENT_PIANO
    chord_mode: str = CHORD_MODE_NONE
    measure_chords: tuple[str | None, ...] = ()

    @property
    def effective_chord_mode(self) -> str:
        """Return a backward-compatible effective chord mode.

        Projects created before 0.2.0 only stored ``chord_symbol``. Treat those
        projects as line-level chord projects even when ``chord_mode`` is absent.
        """
        if self.chord_mode == CHORD_MODE_NONE:
            if self.measure_chords:
                return CHORD_MODE_MEASURE
            if self.chord_symbol:
                return CHORD_MODE_LINE
        return self.chord_mode

    @property
    def chord_symbols_by_measure(self) -> tuple[str | None, ...]:
        """Return one chord symbol (or silence) for every measure."""
        mode = self.effective_chord_mode
        if mode == CHORD_MODE_LINE:
            return tuple(self.chord_symbol for _ in range(self.measures))
        if mode == CHORD_MODE_MEASURE:
            return self.measure_chords
        return tuple(None for _ in range(self.measures))

    @property
    def has_any_chord(self) -> bool:
        """Return whether at least one audible chord is defined."""
        return any(symbol for symbol in self.chord_symbols_by_measure)

    def validate(self) -> None:
        """Validate one segment and raise a readable error if invalid."""
        if self.bpm <= 0:
            raise ValidationError("Le BPM doit être un entier positif.")
        if self.numerator <= 0:
            raise ValidationError("Le numérateur doit être un entier positif.")
        if self.denominator not in SUPPORTED_DENOMINATORS:
            allowed = ", ".join(str(d) for d in sorted(SUPPORTED_DENOMINATORS))
            raise ValidationError(
                f"Le dénominateur doit être une valeur rythmique LilyPond valide: {allowed}."
            )
        if self.measures <= 0:
            raise ValidationError("Le nombre de mesures doit être un entier positif.")
        if self.chord_instrument not in SUPPORTED_CHORD_INSTRUMENTS:
            allowed = ", ".join(sorted(SUPPORTED_CHORD_INSTRUMENTS))
            raise ValidationError(f"Instrument d'accord invalide. Valeurs permises: {allowed}.")
        if self.chord_mode not in SUPPORTED_CHORD_MODES:
            allowed = ", ".join(sorted(SUPPORTED_CHORD_MODES))
            raise ValidationError(f"Mode d'accord invalide. Valeurs permises: {allowed}.")

        mode = self.effective_chord_mode
        if mode == CHORD_MODE_LINE:
            if self.chord_symbol is None or not self.chord_symbol.strip():
                raise ValidationError("Un accord doit être saisi pour le mode par ligne.")
            if self.measure_chords:
                raise ValidationError(
                    "Un segment ne peut pas utiliser simultanément un accord par ligne et des accords par mesure."
                )
        elif mode == CHORD_MODE_MEASURE:
            if self.chord_symbol:
                raise ValidationError(
                    "Un segment ne peut pas utiliser simultanément un accord par ligne et des accords par mesure."
                )
            if len(self.measure_chords) != self.measures:
                raise ValidationError(
                    "Le nombre d'accords par mesure doit correspondre au nombre de mesures de la ligne."
                )

        for measure_index, symbol in enumerate(self.measure_chords, start=1):
            if symbol is not None and not symbol.strip():
                raise ValidationError(
                    f"Le symbole d'accord de la mesure {measure_index} ne peut pas contenir uniquement des espaces."
                )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the segment to a JSON-friendly dictionary."""
        data = asdict(self)
        mode = self.effective_chord_mode
        data["chord_mode"] = mode
        data["measure_chords"] = list(self.measure_chords)

        # Keep the .gen file compact while retaining the selected chord mode.
        if mode == CHORD_MODE_NONE:
            data.pop("chord_symbol", None)
            data.pop("chord_instrument", None)
            data.pop("chord_mode", None)
            data.pop("measure_chords", None)
        elif mode == CHORD_MODE_LINE:
            data.pop("measure_chords", None)
        elif mode == CHORD_MODE_MEASURE:
            data.pop("chord_symbol", None)
        return data

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Segment":
        """Create and validate a Segment from JSON-like data."""
        try:
            chord_symbol = payload.get("chord_symbol")
            raw_measure_chords = payload.get("measure_chords", [])
            if raw_measure_chords is None:
                raw_measure_chords = []
            if not isinstance(raw_measure_chords, (list, tuple)):
                raise TypeError("measure_chords must be a list")
            measure_chords = tuple(
                str(symbol).strip() if symbol is not None and str(symbol).strip() else None
                for symbol in raw_measure_chords
            )

            raw_mode = payload.get("chord_mode")
            if raw_mode is None:
                if measure_chords:
                    raw_mode = CHORD_MODE_MEASURE
                elif chord_symbol:
                    raw_mode = CHORD_MODE_LINE
                else:
                    raw_mode = CHORD_MODE_NONE
            segment = cls(
                bpm=int(payload["bpm"]),
                numerator=int(payload["numerator"]),
                denominator=int(payload["denominator"]),
                measures=int(payload["measures"]),
                chord_symbol=str(chord_symbol).strip() if chord_symbol else None,
                chord_instrument=str(payload.get("chord_instrument", CHORD_INSTRUMENT_PIANO)),
                chord_mode=str(raw_mode),
                measure_chords=measure_chords,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValidationError("Segment invalide dans le fichier .gen.") from exc
        segment.validate()
        return segment


@dataclass(frozen=True)
class ProjectData:
    """Serializable project state for the application."""

    segments: list[Segment]
    soundfont_path: str | None = None
    app: str = APP_NAME
    version: str = APP_VERSION

    def validate(self) -> None:
        """Validate the full project."""
        if not self.segments:
            raise ValidationError("Le projet doit contenir au moins une rangée.")
        for index, segment in enumerate(self.segments, start=1):
            try:
                segment.validate()
            except ValidationError as exc:
                raise ValidationError(f"Erreur à la rangée {index}: {exc}") from exc

    def to_dict(self) -> dict[str, Any]:
        """Serialize the project to a JSON-friendly dictionary."""
        return {
            "app": self.app,
            "version": self.version,
            "soundfont_path": self.soundfont_path,
            "segments": [segment.to_dict() for segment in self.segments],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProjectData":
        """Create and validate project data from JSON-like data."""
        try:
            segments = [Segment.from_dict(item) for item in payload["segments"]]
        except (KeyError, TypeError) as exc:
            raise ValidationError("Fichier .gen invalide: la liste de segments est manquante.") from exc

        project = cls(
            segments=segments,
            soundfont_path=payload.get("soundfont_path") or None,
            app=str(payload.get("app", APP_NAME)),
            version=str(payload.get("version", APP_VERSION)),
        )
        project.validate()
        return project
