# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Unit tests for generated LilyPond source."""

import unittest

from gnu_trackgenerator.generator import build_lilypond_source
from gnu_trackgenerator.models import (
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
    CHORD_INSTRUMENT_PIANO,
    ProjectData,
    Segment,
)


class LilyPondOutputTests(unittest.TestCase):
    def test_chord_symbol_is_printed_above_click_staff(self) -> None:
        project = ProjectData([Segment(120, 4, 4, 1, chord_symbol="C7#9")])
        source = build_lilypond_source(project, title="test")
        self.assertIn('bd4^\\markup { \\bold "C7#9" }', source)

    def test_guitar_fretboards_are_added_when_guitar_chords_exist(self) -> None:
        project = ProjectData([
            Segment(120, 4, 4, 1, chord_symbol="C", chord_instrument=CHORD_INSTRUMENT_ACOUSTIC_GUITAR)
        ])
        source = build_lilypond_source(project, title="test")
        self.assertIn('\\include "predefined-guitar-fretboards.ly"', source)
        self.assertIn('\\new FretBoards', source)
        self.assertIn('\\repeat unfold 1 { c1*4/4 | }', source)

    def test_fretboard_chord_quality_duration_order_is_lilypond_valid(self) -> None:
        project = ProjectData([
            Segment(120, 7, 4, 1, chord_symbol="Am", chord_instrument=CHORD_INSTRUMENT_ACOUSTIC_GUITAR),
            Segment(120, 5, 8, 1, chord_symbol="Dm", chord_instrument=CHORD_INSTRUMENT_ACOUSTIC_GUITAR),
        ])
        source = build_lilypond_source(project, title="test")
        self.assertIn('\\repeat unfold 1 { a1*7/4:m | }', source)
        self.assertIn('\\repeat unfold 1 { d1*5/8:m | }', source)
        self.assertNotIn('a:m1*7/4', source)
        self.assertNotIn('d:m1*5/8', source)

    def test_non_guitar_chords_do_not_add_fretboards(self) -> None:
        project = ProjectData([
            Segment(120, 4, 4, 1, chord_symbol="Cm7", chord_instrument=CHORD_INSTRUMENT_PIANO)
        ])
        source = build_lilypond_source(project, title="test")
        self.assertNotIn('\\new FretBoards', source)


if __name__ == "__main__":
    unittest.main()
