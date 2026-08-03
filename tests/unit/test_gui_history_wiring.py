# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Static regression checks for GUI-to-history event wiring."""

from pathlib import Path
import unittest


class GuiHistoryWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "gnu_trackgenerator"
            / "gui.py"
        ).read_text(encoding="utf-8")

    def test_main_fields_are_registered_for_history(self) -> None:
        for field in (
            "self.bpm_var",
            "self.numerator_var",
            "self.denominator_var",
            "self.measures_var",
            "self.chord_symbol_var",
            "self.chord_instrument_var",
            "self.chord_grid_unit_var",
        ):
            self.assertIn(field, self.source)
        self.assertIn("self._register_history_var(variable)", self.source)

    def test_chord_mode_and_arpeggiator_changes_notify_history(self) -> None:
        for method in (
            "def show_line_chord_area",
            "def show_measure_chord_area",
            "def show_grid_chord_area",
            "def disable_chords",
            "def _edit_line_arpeggiator",
            "def _edit_measure_arpeggiator",
            "def _edit_grid_arpeggiator",
        ):
            start = self.source.index(method)
            block = self.source[start:start + 1400]
            self.assertIn("_notify_change()", block, method)

    def test_structural_actions_commit_one_snapshot(self) -> None:
        for method in ("def add_row", "def remove_row", "def duplicate_row", "def _end_row_drag"):
            start = self.source.index(method)
            block = self.source[start:start + 1800]
            self.assertIn("_commit_history_snapshot()", block, method)

    def test_global_click_track_is_traced_and_snapshotted(self) -> None:
        self.assertIn("self.click_track_enabled_var.trace_add", self.source)
        self.assertIn("click_track_enabled=bool(self.click_track_enabled_var.get())", self.source)
        self.assertIn("self.click_track_enabled_var.set", self.source)

    def test_snapshot_schema_is_validated_on_capture_and_restore(self) -> None:
        self.assertIn("build_project_history_snapshot(", self.source)
        self.assertIn("validate_row_history_state(", self.source)
        self.assertIn("validate_project_history_snapshot(snapshot)", self.source)


if __name__ == "__main__":
    unittest.main()
