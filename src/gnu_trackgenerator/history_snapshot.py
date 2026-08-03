# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Validated project snapshots used by Undo and Redo.

This module keeps the history schema independent from CustomTkinter so every
editable project property can be covered by deterministic unit tests.  The GUI
stores raw strings rather than validated musical values, which allows Undo to
restore an incomplete value while the user is typing.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import Any


REQUIRED_ROW_HISTORY_KEYS = frozenset(
    {
        "bpm",
        "numerator",
        "denominator",
        "measures",
        "chord_mode",
        "chord_symbol",
        "chord_instrument_label",
        "chord_grid_unit_label",
        "measure_chords",
        "grid_chords",
        "line_arpeggiator",
        "measure_arpeggiators",
        "grid_arpeggiators",
    }
)

REQUIRED_PROJECT_HISTORY_KEYS = frozenset(
    {
        "soundfont",
        "click_track_enabled",
        "rows",
    }
)


class HistorySnapshotError(ValueError):
    """Raised when an Undo/Redo snapshot is incomplete or malformed."""


def validate_row_history_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Return a deep copy of a complete row state.

    Extra keys are intentionally retained for forward compatibility.  Required
    keys protect existing editing actions from silently disappearing from the
    Undo/Redo snapshot when the GUI is refactored.
    """
    missing = REQUIRED_ROW_HISTORY_KEYS.difference(state.keys())
    if missing:
        names = ", ".join(sorted(missing))
        raise HistorySnapshotError(
            f"Instantané de ligne incomplet; champ(s) manquant(s) : {names}."
        )
    return deepcopy(dict(state))


def build_project_history_snapshot(
    *,
    soundfont: str,
    click_track_enabled: bool,
    rows: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build and validate one complete project history snapshot."""
    return {
        "soundfont": str(soundfont),
        "click_track_enabled": bool(click_track_enabled),
        "rows": [validate_row_history_state(row) for row in rows],
    }


def validate_project_history_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a stored project snapshot before restoring it."""
    missing = REQUIRED_PROJECT_HISTORY_KEYS.difference(snapshot.keys())
    if missing:
        names = ", ".join(sorted(missing))
        raise HistorySnapshotError(
            f"Instantané de projet incomplet; champ(s) manquant(s) : {names}."
        )

    click_track_enabled = snapshot["click_track_enabled"]
    if not isinstance(click_track_enabled, bool):
        raise HistorySnapshotError("click_track_enabled doit être un booléen.")

    rows = snapshot["rows"]
    if not isinstance(rows, list):
        raise HistorySnapshotError("rows doit être une liste.")

    return build_project_history_snapshot(
        soundfont=str(snapshot["soundfont"]),
        click_track_enabled=click_track_enabled,
        rows=rows,
    )
