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
APP_VERSION = "0.1.2"

# LilyPond note durations are represented by powers of two: 1, 2, 4, 8, 16...
# Keeping the denominator in this set supports common and complex meters such as
# 7/8, 11/16, 27/16, 5/4, etc.
SUPPORTED_DENOMINATORS = {1, 2, 4, 8, 16, 32, 64}


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
    """

    bpm: int
    numerator: int
    denominator: int
    measures: int

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

    def to_dict(self) -> dict[str, int]:
        """Serialize the segment to a JSON-friendly dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Segment":
        """Create and validate a Segment from JSON-like data."""
        try:
            segment = cls(
                bpm=int(payload["bpm"]),
                numerator=int(payload["numerator"]),
                denominator=int(payload["denominator"]),
                measures=int(payload["measures"]),
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
