# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Regression coverage for every project action promised by Undo/Redo."""

from __future__ import annotations

from copy import deepcopy
import unittest

from gnu_trackgenerator.history import UndoHistory
from gnu_trackgenerator.history_snapshot import (
    HistorySnapshotError,
    REQUIRED_ROW_HISTORY_KEYS,
    build_project_history_snapshot,
    validate_project_history_snapshot,
)
from gnu_trackgenerator.sequence import duplicate_row_state, move_item


def arp(enabled: bool = False, *, octaves: int = 1) -> dict:
    return {
        "enabled": enabled,
        "pattern": "up_down",
        "octaves": octaves,
        "rhythm": "eighth",
        "dotted": False,
        "tuplet_count": 0,
    }


def row_state(label: str = "C") -> dict:
    return {
        "bpm": "120",
        "numerator": "4",
        "denominator": "4",
        "measures": "2",
        "chord_mode": "line",
        "chord_symbol": label,
        "chord_instrument_label": "Piano",
        "chord_grid_unit_label": "Noire",
        "measure_chords": ["C", "G7"],
        "grid_chords": ["C", ",", "G", ""],
        "line_arpeggiator": arp(),
        "measure_arpeggiators": [arp(), arp()],
        "grid_arpeggiators": [arp(), arp(), arp(), arp()],
    }


def project_snapshot(*rows: dict, click: bool = True) -> dict:
    return build_project_history_snapshot(
        soundfont="C:/SoundFonts/CrisisGeneralMidi301.sf2",
        click_track_enabled=click,
        rows=rows or (row_state(),),
    )


class HistoryActionCoverageTests(unittest.TestCase):
    def assertUndoRedo(self, before: dict, after: dict) -> None:  # noqa: N802
        history = UndoHistory[dict](max_entries=100)
        history.reset(before)
        self.assertTrue(history.record(after))
        self.assertEqual(history.undo(), before)
        self.assertEqual(history.redo(), after)

    def test_row_snapshot_contains_every_required_editable_field(self) -> None:
        self.assertEqual(set(row_state()), set(REQUIRED_ROW_HISTORY_KEYS))

    def test_add_and_remove_row_are_reversible(self) -> None:
        first = row_state("C")
        second = row_state("F")
        one_row = project_snapshot(first)
        two_rows = project_snapshot(first, second)
        self.assertUndoRedo(one_row, two_rows)  # add
        self.assertUndoRedo(two_rows, one_row)  # remove

    def test_tempo_signature_and_measure_count_are_reversible(self) -> None:
        before = project_snapshot(row_state())
        edited_row = row_state()
        edited_row.update({"bpm": "145", "numerator": "7", "denominator": "8", "measures": "5"})
        self.assertUndoRedo(before, project_snapshot(edited_row))

    def test_all_chord_entry_modes_are_reversible(self) -> None:
        before = project_snapshot(row_state())
        edited = row_state("Dadd11")
        edited["measure_chords"] = ["Em7", "A7"]
        edited["grid_chords"] = ["G#m7(b13)", ",", "B5", ""]
        self.assertUndoRedo(before, project_snapshot(edited))

    def test_chord_mode_change_is_reversible(self) -> None:
        before = project_snapshot(row_state())
        edited = row_state()
        edited["chord_mode"] = "grid"
        self.assertUndoRedo(before, project_snapshot(edited))

    def test_all_arpeggiator_scopes_are_reversible(self) -> None:
        before = project_snapshot(row_state())
        edited = row_state()
        edited["line_arpeggiator"] = arp(True, octaves=2)
        edited["measure_arpeggiators"][1] = arp(True, octaves=3)
        edited["grid_arpeggiators"][2] = arp(True, octaves=4)
        self.assertUndoRedo(before, project_snapshot(edited))

    def test_duplicate_row_is_reversible_and_independent(self) -> None:
        source = row_state("Cmaj7")
        duplicated = duplicate_row_state(source)
        after = project_snapshot(source, duplicated)
        self.assertUndoRedo(project_snapshot(source), after)

        duplicated["measure_chords"][0] = "F"
        self.assertEqual(source["measure_chords"][0], "C")

    def test_row_reordering_is_reversible(self) -> None:
        rows = [row_state("Intro"), row_state("Couplet"), row_state("Refrain")]
        before = project_snapshot(*rows)
        reordered = deepcopy(rows)
        move_item(reordered, 2, 0)
        self.assertUndoRedo(before, project_snapshot(*reordered))

    def test_global_click_track_toggle_is_reversible(self) -> None:
        self.assertUndoRedo(project_snapshot(click=True), project_snapshot(click=False))

    def test_incomplete_snapshot_is_rejected_before_restore(self) -> None:
        broken = project_snapshot()
        del broken["rows"][0]["grid_arpeggiators"]
        with self.assertRaises(HistorySnapshotError):
            validate_project_history_snapshot(broken)


if __name__ == "__main__":
    unittest.main()
