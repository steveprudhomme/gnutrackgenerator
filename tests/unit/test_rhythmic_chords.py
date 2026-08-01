# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for rhythmic chord-grid calculations and continuation semantics."""

from fractions import Fraction
import unittest

from gnu_trackgenerator.generator import build_lilypond_source
from gnu_trackgenerator.models import CHORD_MODE_GRID, ProjectData, Segment, ValidationError
from gnu_trackgenerator.rhythm import (
    RHYTHM_DOTTED_HALF,
    RHYTHM_DOTTED_QUARTER,
    RHYTHM_EIGHTH,
    RHYTHM_EIGHTH_TRIPLET,
    RHYTHM_HALF,
    RHYTHM_HALF_TRIPLET,
    RHYTHM_QUARTER,
    RHYTHM_QUARTER_TRIPLET,
    RHYTHM_WHOLE_TRIPLET,
    chord_grid_durations,
)


class RhythmicGridCalculationTests(unittest.TestCase):
    def test_all_requested_units_create_expected_cell_counts_in_four_four(self) -> None:
        expected_counts = {
            RHYTHM_HALF: 8,
            RHYTHM_DOTTED_HALF: 6,
            RHYTHM_QUARTER: 16,
            RHYTHM_DOTTED_QUARTER: 11,
            RHYTHM_EIGHTH: 32,
            RHYTHM_WHOLE_TRIPLET: 6,
            RHYTHM_HALF_TRIPLET: 12,
            RHYTHM_QUARTER_TRIPLET: 24,
            RHYTHM_EIGHTH_TRIPLET: 48,
        }
        for unit, expected in expected_counts.items():
            with self.subTest(unit=unit):
                durations = chord_grid_durations(4, 4, 4, unit)
                self.assertEqual(len(durations), expected)
                self.assertEqual(sum(durations), Fraction(4, 1))

    def test_four_measures_of_four_four_at_quarters_create_sixteen_cells(self) -> None:
        durations = chord_grid_durations(4, 4, 4, RHYTHM_QUARTER)
        self.assertEqual(len(durations), 16)
        self.assertTrue(all(duration == Fraction(1, 4) for duration in durations))

    def test_quarter_triplets_create_twenty_four_cells(self) -> None:
        durations = chord_grid_durations(4, 4, 4, RHYTHM_QUARTER_TRIPLET)
        self.assertEqual(len(durations), 24)
        self.assertTrue(all(duration == Fraction(1, 6) for duration in durations))

    def test_eighth_triplets_create_forty_eight_cells(self) -> None:
        durations = chord_grid_durations(4, 4, 4, RHYTHM_EIGHTH_TRIPLET)
        self.assertEqual(len(durations), 48)

    def test_non_divisible_dotted_value_uses_shortened_final_cell(self) -> None:
        durations = chord_grid_durations(4, 4, 4, RHYTHM_DOTTED_HALF)
        self.assertEqual(len(durations), 6)
        self.assertEqual(durations[-1], Fraction(1, 4))
        self.assertEqual(sum(durations), Fraction(4, 1))


class RhythmicGridModelTests(unittest.TestCase):
    def test_grid_mode_round_trip(self) -> None:
        values = ("C", ",", "G", None) * 4
        segment = Segment(
            120,
            4,
            4,
            4,
            chord_mode=CHORD_MODE_GRID,
            chord_grid_unit=RHYTHM_QUARTER,
            grid_chords=values,
        )
        payload = segment.to_dict()
        restored = Segment.from_dict(payload)
        self.assertEqual(payload["chord_mode"], CHORD_MODE_GRID)
        self.assertEqual(payload["chord_grid_unit"], RHYTHM_QUARTER)
        self.assertEqual(restored.grid_chords, values)

    def test_leading_comma_is_rejected(self) -> None:
        segment = Segment(
            120,
            4,
            4,
            1,
            chord_mode=CHORD_MODE_GRID,
            chord_grid_unit=RHYTHM_QUARTER,
            grid_chords=(",", None, None, None),
        )
        with self.assertRaises(ValidationError):
            segment.validate()


class RhythmicGridLilyPondTests(unittest.TestCase):
    def test_comma_extends_previous_chord_without_retriggering(self) -> None:
        segment = Segment(
            120,
            4,
            4,
            1,
            chord_mode=CHORD_MODE_GRID,
            chord_grid_unit=RHYTHM_QUARTER,
            grid_chords=("C", ",", "G", None),
        )
        source = build_lilypond_source(ProjectData([segment]), title="grille")
        self.assertIn("<c e g>2", source)
        self.assertIn("<g b d'>4", source)
        self.assertIn("r4 |", source)
        self.assertEqual(source.count('\\bold "C"'), 1)
        self.assertEqual(source.count('\\bold "G"'), 1)
        self.assertNotIn('\\bold ","', source)

    def test_continuation_can_cross_a_measure_boundary_with_a_tie(self) -> None:
        segment = Segment(
            120,
            4,
            4,
            2,
            chord_mode=CHORD_MODE_GRID,
            chord_grid_unit=RHYTHM_DOTTED_HALF,
            grid_chords=("C", ",", ","),
        )
        source = build_lilypond_source(ProjectData([segment]), title="liaison")
        self.assertIn("<c e g>1~ |", source)
        self.assertIn("<c e g>1 |", source)
        self.assertEqual(source.count('\\bold "C"'), 1)


if __name__ == "__main__":
    unittest.main()
