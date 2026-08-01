# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Domain models for GNU TrackGenerator.

This module intentionally contains no GUI code and no subprocess calls. It is
safe to unit-test in isolation and represents the musical/project data model.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .rhythm import (
    RHYTHM_QUARTER,
    SUPPORTED_RHYTHM_UNITS,
    chord_grid_durations,
    resolve_grid_events,
)

APP_NAME = "GNU TrackGenerator"
APP_VERSION = "0.3.0"

# LilyPond note durations are represented by powers of two: 1, 2, 4, 8, 16...
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
CHORD_MODE_GRID = "grid"

SUPPORTED_CHORD_MODES = {
    CHORD_MODE_NONE,
    CHORD_MODE_LINE,
    CHORD_MODE_MEASURE,
    CHORD_MODE_GRID,
}


class ValidationError(ValueError):
    """Raised when the project or one of its musical segments is invalid."""


@dataclass(frozen=True)
class Segment:
    """A programmable click-track segment.

    Chords can be disabled, repeated for the whole line, entered once per
    measure, or entered in a rhythmic grid. In grid mode, an empty cell means
    silence and a comma extends the previous chord without retriggering it.
    """

    bpm: int
    numerator: int
    denominator: int
    measures: int
    chord_symbol: str | None = None
    chord_instrument: str = CHORD_INSTRUMENT_PIANO
    chord_mode: str = CHORD_MODE_NONE
    measure_chords: tuple[str | None, ...] = ()
    chord_grid_unit: str = RHYTHM_QUARTER
    grid_chords: tuple[str | None, ...] = ()

    @property
    def effective_chord_mode(self) -> str:
        """Return a backward-compatible effective chord mode."""
        if self.chord_mode == CHORD_MODE_NONE:
            if self.grid_chords:
                return CHORD_MODE_GRID
            if self.measure_chords:
                return CHORD_MODE_MEASURE
            if self.chord_symbol:
                return CHORD_MODE_LINE
        return self.chord_mode

    @property
    def chord_symbols_by_measure(self) -> tuple[str | None, ...]:
        """Return one symbol for every measure in the legacy line/measure modes."""
        mode = self.effective_chord_mode
        if mode == CHORD_MODE_LINE:
            return tuple(self.chord_symbol for _ in range(self.measures))
        if mode == CHORD_MODE_MEASURE:
            return self.measure_chords
        return tuple(None for _ in range(self.measures))

    @property
    def chord_grid_durations(self):
        """Return exact grid-cell durations for the current segment."""
        return chord_grid_durations(
            self.numerator,
            self.denominator,
            self.measures,
            self.chord_grid_unit,
        )

    @property
    def has_any_chord(self) -> bool:
        """Return whether at least one audible chord is defined."""
        mode = self.effective_chord_mode
        if mode == CHORD_MODE_GRID:
            return any(value not in {None, "", ","} for value in self.grid_chords)
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
            if self.measure_chords or self.grid_chords:
                raise ValidationError("Un segment ne peut utiliser qu'un seul mode d'accord.")

        elif mode == CHORD_MODE_MEASURE:
            if self.chord_symbol or self.grid_chords:
                raise ValidationError("Un segment ne peut utiliser qu'un seul mode d'accord.")
            if len(self.measure_chords) != self.measures:
                raise ValidationError(
                    "Le nombre d'accords par mesure doit correspondre au nombre de mesures de la ligne."
                )

        elif mode == CHORD_MODE_GRID:
            if self.chord_symbol or self.measure_chords:
                raise ValidationError("Un segment ne peut utiliser qu'un seul mode d'accord.")
            if self.chord_grid_unit not in SUPPORTED_RHYTHM_UNITS:
                raise ValidationError("La subdivision rythmique choisie est invalide.")
            try:
                durations = self.chord_grid_durations
            except ValueError as exc:
                raise ValidationError(str(exc)) from exc
            if len(self.grid_chords) != len(durations):
                raise ValidationError(
                    "Le nombre d'accords rythmiques doit correspondre au nombre de cases calculé pour la ligne."
                )
            try:
                resolve_grid_events(self.grid_chords, durations)
            except ValueError as exc:
                raise ValidationError(str(exc)) from exc


    def to_dict(self) -> dict[str, Any]:
        """Serialize the segment to a JSON-friendly dictionary."""
        data = asdict(self)
        mode = self.effective_chord_mode
        data["chord_mode"] = mode
        data["measure_chords"] = list(self.measure_chords)
        data["grid_chords"] = list(self.grid_chords)

        if mode == CHORD_MODE_NONE:
            for key in (
                "chord_symbol",
                "chord_instrument",
                "chord_mode",
                "measure_chords",
                "chord_grid_unit",
                "grid_chords",
            ):
                data.pop(key, None)
        elif mode == CHORD_MODE_LINE:
            data.pop("measure_chords", None)
            data.pop("chord_grid_unit", None)
            data.pop("grid_chords", None)
        elif mode == CHORD_MODE_MEASURE:
            data.pop("chord_symbol", None)
            data.pop("chord_grid_unit", None)
            data.pop("grid_chords", None)
        elif mode == CHORD_MODE_GRID:
            data.pop("chord_symbol", None)
            data.pop("measure_chords", None)
        return data

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Segment":
        """Create and validate a Segment from JSON-like data."""
        try:
            chord_symbol = payload.get("chord_symbol")

            raw_measure_chords = payload.get("measure_chords", []) or []
            if not isinstance(raw_measure_chords, (list, tuple)):
                raise TypeError("measure_chords must be a list")
            measure_chords = tuple(
                str(symbol).strip() if symbol is not None and str(symbol).strip() else None
                for symbol in raw_measure_chords
            )

            raw_grid_chords = payload.get("grid_chords", []) or []
            if not isinstance(raw_grid_chords, (list, tuple)):
                raise TypeError("grid_chords must be a list")
            grid_chords = tuple(
                str(symbol).strip() if symbol is not None and str(symbol).strip() else None
                for symbol in raw_grid_chords
            )

            raw_mode = payload.get("chord_mode")
            if raw_mode is None:
                if grid_chords:
                    raw_mode = CHORD_MODE_GRID
                elif measure_chords:
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
                chord_grid_unit=str(payload.get("chord_grid_unit", RHYTHM_QUARTER)),
                grid_chords=grid_chords,
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
