# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for one-chord-per-measure project data and LilyPond output."""

import unittest

from gnu_trackgenerator.generator import build_lilypond_source
from gnu_trackgenerator.models import (
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
    CHORD_MODE_LINE,
    CHORD_MODE_MEASURE,
    ProjectData,
    Segment,
)


class MeasureChordModelTests(unittest.TestCase):
    def test_measure_chords_round_trip_in_gen_payload(self) -> None:
        segment = Segment(
            bpm=120,
            numerator=7,
            denominator=8,
            measures=3,
            chord_instrument=CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
            chord_mode=CHORD_MODE_MEASURE,
            measure_chords=("C", "Am7", "F"),
        )
        payload = segment.to_dict()
        restored = Segment.from_dict(payload)

        self.assertEqual(payload["chord_mode"], CHORD_MODE_MEASURE)
        self.assertEqual(payload["measure_chords"], ["C", "Am7", "F"])
        self.assertEqual(restored.measure_chords, ("C", "Am7", "F"))
        self.assertEqual(restored.chord_symbols_by_measure, ("C", "Am7", "F"))

    def test_legacy_chord_symbol_is_inferred_as_line_mode(self) -> None:
        restored = Segment.from_dict(
            {
                "bpm": 120,
                "numerator": 4,
                "denominator": 4,
                "measures": 2,
                "chord_symbol": "Cm7",
                "chord_instrument": "piano",
            }
        )
        self.assertEqual(restored.effective_chord_mode, CHORD_MODE_LINE)
        self.assertEqual(restored.chord_symbols_by_measure, ("Cm7", "Cm7"))


class MeasureChordLilyPondTests(unittest.TestCase):
    def test_each_measure_gets_its_own_symbol_and_full_measure_duration(self) -> None:
        project = ProjectData(
            [
                Segment(
                    120,
                    7,
                    8,
                    3,
                    chord_mode=CHORD_MODE_MEASURE,
                    measure_chords=("C", "Am7", "F"),
                )
            ]
        )
        source = build_lilypond_source(project, title="mesures")

        self.assertIn('s1*7/8^\\markup { \\bold "C" }', source)
        self.assertIn('s1*7/8^\\markup { \\bold "Am7" }', source)
        self.assertIn('s1*7/8^\\markup { \\bold "F" }', source)
        self.assertIn('<c e g>1*7/8', source)
        self.assertIn("<a c' e' g'>1*7/8", source)
        self.assertIn("<f a c'>1*7/8", source)

    def test_generic_add_chord_is_rendered_in_measure_mode(self) -> None:
        project = ProjectData(
            [
                Segment(
                    120,
                    4,
                    4,
                    1,
                    chord_mode=CHORD_MODE_MEASURE,
                    measure_chords=("Dadd11",),
                )
            ]
        )
        source = build_lilypond_source(project, title="add11")
        self.assertIn('s1^\\markup { \\bold "Dadd11" }', source)
        self.assertIn("<d fis a g'>1", source)

    def test_reported_power_chord_progression_generates_successfully(self) -> None:
        project = ProjectData(
            [
                Segment(
                    120,
                    4,
                    4,
                    6,
                    chord_mode=CHORD_MODE_MEASURE,
                    measure_chords=("E5", "B5", "E5", "C5m", "F#5(b5)", "B5"),
                )
            ]
        )
        source = build_lilypond_source(project, title="progression-puissance")

        self.assertIn('<e b>1', source)
        self.assertIn("<b fis'>1", source)
        self.assertIn('<c ees g>1', source)
        self.assertIn("<fis c'>1", source)
        self.assertIn('s1^\\markup { \\bold "C5m" }', source)

    def test_blank_measure_chord_generates_a_full_measure_rest(self) -> None:
        project = ProjectData(
            [
                Segment(
                    100,
                    5,
                    4,
                    3,
                    chord_mode=CHORD_MODE_MEASURE,
                    measure_chords=("C", None, "G7"),
                )
            ]
        )
        source = build_lilypond_source(project, title="silence")
        self.assertIn("r1*5/4 |", source)
        self.assertIn("s1*5/4 |", source)

    def test_per_measure_guitar_chords_generate_matching_fretboards(self) -> None:
        project = ProjectData(
            [
                Segment(
                    120,
                    4,
                    4,
                    2,
                    chord_instrument=CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
                    chord_mode=CHORD_MODE_MEASURE,
                    measure_chords=("C", "Am7"),
                )
            ]
        )
        source = build_lilypond_source(project, title="guitare")
        self.assertIn("c1 |", source)
        self.assertIn("a1:m7 |", source)
        self.assertIn("<c e g>1\\arpeggio", source)


if __name__ == "__main__":
    unittest.main()
