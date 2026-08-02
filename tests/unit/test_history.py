# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

import unittest

from gnu_trackgenerator.history import UndoHistory


class UndoHistoryTests(unittest.TestCase):
    def test_record_then_undo_returns_previous_state(self):
        history = UndoHistory(max_entries=10)
        history.reset({"value": "initial"})
        history.record({"value": "edited"})

        self.assertTrue(history.can_undo)
        self.assertEqual(history.undo(), {"value": "initial"})
        self.assertFalse(history.can_undo)

    def test_identical_state_is_not_recorded(self):
        history = UndoHistory(max_entries=10)
        history.reset([1, 2, 3])

        self.assertFalse(history.record([1, 2, 3]))
        self.assertEqual(history.depth, 0)

    def test_history_is_bounded(self):
        history = UndoHistory(max_entries=2)
        history.reset(0)
        history.record(1)
        history.record(2)
        history.record(3)

        self.assertEqual(history.depth, 2)
        self.assertEqual(history.undo(), 2)
        self.assertEqual(history.undo(), 1)
        self.assertIsNone(history.undo())

    def test_snapshots_are_deep_copied(self):
        initial = {"rows": [{"bpm": "120"}]}
        history = UndoHistory(max_entries=10)
        history.reset(initial)
        initial["rows"][0]["bpm"] = "999"
        history.record({"rows": [{"bpm": "140"}]})

        restored = history.undo()
        self.assertEqual(restored, {"rows": [{"bpm": "120"}]})


if __name__ == "__main__":
    unittest.main()
