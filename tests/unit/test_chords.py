# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Unit tests for chord symbol conversion."""

import unittest

from gnu_trackgenerator.chords import chord_symbol_to_lilypond_chord


class ChordConversionTests(unittest.TestCase):
    def test_basic_major_chord(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("C"), "<c e g>")

    def test_minor_seventh_chord(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("Cm7"), "<c ees g bes>")

    def test_altered_dominant_chord(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("C7#9"), "<c e g bes ees'>")

    def test_flat_root_chord(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("Bb9"), "<bes d' f' aes' c''>")

    def test_sharp_root_chord(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("F#m7"), "<fis a cis' e'>")


if __name__ == "__main__":
    unittest.main()

from gnu_trackgenerator.chords import chord_symbol_to_lilypond_fretboard_chord


class GuitarFretboardChordTests(unittest.TestCase):
    def test_major_chordmode_for_fretboard(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_fretboard_chord("C"), "c")

    def test_flat_root_chordmode_for_fretboard(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_fretboard_chord("Bb7"), "bes:7")

    def test_unsupported_extended_chord_skips_fretboard(self) -> None:
        self.assertIsNone(chord_symbol_to_lilypond_fretboard_chord("C7#9"))

from gnu_trackgenerator.chords import ChordParseError, normalize_chord_symbol


class GenericAddedDegreeChordTests(unittest.TestCase):
    def test_add11_is_calculated_without_hard_coded_quality(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("Dadd11"), "<d fis a g'>")

    def test_minor_chord_can_receive_an_added_degree(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("Cmadd9"), "<c ees g d'>")

    def test_seventh_chord_can_receive_an_added_extension(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("C7add13"), "<c e g bes a'>")

    def test_altered_added_degree_is_supported(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("Fadd#11"), "<f a c' b'>")

    def test_parenthesized_add_notation_is_supported(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("D(add11)"), "<d fis a g'>")

    def test_add_keyword_is_case_insensitive(self) -> None:
        self.assertEqual(chord_symbol_to_lilypond_chord("DADD11"), "<d fis a g'>")

    def test_unknown_base_quality_before_add_is_rejected(self) -> None:
        with self.assertRaises(ChordParseError):
            normalize_chord_symbol("Cfooadd11")
