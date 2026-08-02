# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

import unittest

from gnu_trackgenerator.sequence import duplicate_row_state, move_item


class SequenceHelpersTests(unittest.TestCase):
    def test_duplicate_row_state_is_deep_copy(self) -> None:
        original = {
            "bpm": "120",
            "measure_chords": ["C", "Am7"],
            "measure_arpeggiators": [{"enabled": True, "octaves": 2}],
        }
        duplicate = duplicate_row_state(original)
        duplicate["measure_chords"][0] = "F"
        duplicate["measure_arpeggiators"][0]["octaves"] = 3

        self.assertEqual(original["measure_chords"][0], "C")
        self.assertEqual(original["measure_arpeggiators"][0]["octaves"], 2)

    def test_move_item_down(self) -> None:
        values = ["intro", "verse", "chorus", "outro"]
        move_item(values, 0, 2)
        self.assertEqual(values, ["verse", "chorus", "intro", "outro"])

    def test_move_item_up(self) -> None:
        values = ["intro", "verse", "chorus", "outro"]
        move_item(values, 3, 1)
        self.assertEqual(values, ["intro", "outro", "verse", "chorus"])

    def test_move_item_same_position_is_noop(self) -> None:
        values = [1, 2, 3]
        move_item(values, 1, 1)
        self.assertEqual(values, [1, 2, 3])

    def test_move_item_rejects_invalid_index(self) -> None:
        with self.assertRaises(IndexError):
            move_item(["a"], 0, 1)


if __name__ == "__main__":
    unittest.main()
