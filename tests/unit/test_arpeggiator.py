# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

from fractions import Fraction
import unittest

from gnu_trackgenerator.arpeggiator import (
    ARP_PATTERN_DOWN_UP,
    ARP_PATTERN_RANDOM,
    ARP_PATTERN_UP_DOWN,
    ARP_RHYTHM_EIGHTH,
    ARP_RHYTHM_QUARTER,
    ArpeggiatorError,
    ArpeggiatorSettings,
    generate_arpeggio_steps,
)
from gnu_trackgenerator.generator import build_lilypond_source
from gnu_trackgenerator.models import (
    CHORD_MODE_GRID,
    CHORD_MODE_LINE,
    CHORD_MODE_MEASURE,
    ProjectData,
    Segment,
)
from gnu_trackgenerator.rhythm import RHYTHM_QUARTER, chord_grid_durations, resolve_grid_events


class ArpeggiatorSettingsTests(unittest.TestCase):
    def test_dotted_quarter_duration(self):
        settings = ArpeggiatorSettings(enabled=True, rhythm=ARP_RHYTHM_QUARTER, dotted=True)
        self.assertEqual(settings.step_duration, Fraction(3, 8))

    def test_five_tuplet_uses_five_in_the_time_of_four(self):
        settings = ArpeggiatorSettings(
            enabled=True,
            rhythm=ARP_RHYTHM_EIGHTH,
            tuplet_count=5,
        )
        self.assertEqual(settings.step_duration, Fraction(1, 10))

    def test_round_trip(self):
        settings = ArpeggiatorSettings(
            enabled=True,
            pattern=ARP_PATTERN_DOWN_UP,
            octaves=3,
            rhythm=ARP_RHYTHM_QUARTER,
            dotted=True,
            tuplet_count=7,
        )
        self.assertEqual(ArpeggiatorSettings.from_dict(settings.to_dict()), settings)

    def test_tuplet_count_one_or_two_is_rejected(self):
        for count in (1, 2):
            with self.subTest(count=count):
                with self.assertRaises(ArpeggiatorError):
                    ArpeggiatorSettings(enabled=True, tuplet_count=count).validate()


class ArpeggioSequenceTests(unittest.TestCase):
    def test_up_down_sequence(self):
        settings = ArpeggiatorSettings(
            enabled=True,
            pattern=ARP_PATTERN_UP_DOWN,
            octaves=1,
            rhythm=ARP_RHYTHM_EIGHTH,
        )
        steps = generate_arpeggio_steps("C", Fraction(5, 8), settings)
        self.assertEqual([step.note for step in steps], ["c", "e", "g", "e", "c"])

    def test_down_up_sequence(self):
        settings = ArpeggiatorSettings(
            enabled=True,
            pattern=ARP_PATTERN_DOWN_UP,
            octaves=1,
            rhythm=ARP_RHYTHM_EIGHTH,
        )
        steps = generate_arpeggio_steps("C", Fraction(5, 8), settings)
        self.assertEqual([step.note for step in steps], ["g", "e", "c", "e", "g"])

    def test_random_sequence_is_reproducible(self):
        settings = ArpeggiatorSettings(
            enabled=True,
            pattern=ARP_PATTERN_RANDOM,
            octaves=2,
            rhythm=ARP_RHYTHM_EIGHTH,
        )
        first = generate_arpeggio_steps("Am7", Fraction(1, 1), settings, seed_key="same")
        second = generate_arpeggio_steps("Am7", Fraction(1, 1), settings, seed_key="same")
        self.assertEqual(first, second)


class ArpeggiatorModelTests(unittest.TestCase):
    def test_line_mode_serializes_one_arpeggiator(self):
        settings = ArpeggiatorSettings(enabled=True, octaves=2)
        segment = Segment(
            bpm=120,
            numerator=4,
            denominator=4,
            measures=2,
            chord_symbol="C",
            chord_mode=CHORD_MODE_LINE,
            chord_arpeggiator=settings,
        )
        payload = segment.to_dict()
        self.assertEqual(payload["arpeggiator"]["octaves"], 2)
        self.assertEqual(Segment.from_dict(payload), segment)

    def test_measure_mode_serializes_one_setting_per_measure(self):
        enabled = ArpeggiatorSettings(enabled=True)
        disabled = ArpeggiatorSettings()
        segment = Segment(
            bpm=100,
            numerator=3,
            denominator=4,
            measures=2,
            chord_mode=CHORD_MODE_MEASURE,
            measure_chords=("C", "G"),
            measure_arpeggiators=(enabled, disabled),
        )
        restored = Segment.from_dict(segment.to_dict())
        self.assertTrue(restored.measure_arpeggiators[0].enabled)
        self.assertFalse(restored.measure_arpeggiators[1].enabled)

    def test_grid_comma_inherits_previous_arpeggiator(self):
        durations = chord_grid_durations(4, 4, 1, RHYTHM_QUARTER)
        enabled = ArpeggiatorSettings(enabled=True, octaves=2)
        events = resolve_grid_events(
            ("C", ",", None, "G"),
            durations,
            (enabled, ArpeggiatorSettings(), ArpeggiatorSettings(), ArpeggiatorSettings()),
        )
        self.assertEqual(events[0].duration, Fraction(1, 2))
        self.assertEqual(events[0].arpeggiator, enabled)


class ArpeggiatorLilyPondTests(unittest.TestCase):
    def test_triplet_arpeggio_generates_single_notes_and_tuplets(self):
        segment = Segment(
            bpm=120,
            numerator=4,
            denominator=4,
            measures=1,
            chord_symbol="Cmaj7",
            chord_mode=CHORD_MODE_LINE,
            chord_arpeggiator=ArpeggiatorSettings(
                enabled=True,
                pattern=ARP_PATTERN_UP_DOWN,
                octaves=2,
                rhythm=ARP_RHYTHM_EIGHTH,
                tuplet_count=3,
            ),
        )
        source = build_lilypond_source(ProjectData([segment]), "arp-test")
        self.assertIn(r"\tuplet 3/2 {", source)
        self.assertIn("c8", source)
        self.assertNotIn("<c e g b>1", source)
        self.assertIn(r'\bold "Cmaj7"', source)

    def test_grid_arpeggiator_is_saved_and_rendered(self):
        enabled = ArpeggiatorSettings(enabled=True, rhythm=ARP_RHYTHM_QUARTER)
        segment = Segment(
            bpm=120,
            numerator=4,
            denominator=4,
            measures=1,
            chord_mode=CHORD_MODE_GRID,
            chord_grid_unit=RHYTHM_QUARTER,
            grid_chords=("C", ",", "G", None),
            grid_arpeggiators=(enabled, ArpeggiatorSettings(), enabled, ArpeggiatorSettings()),
        )
        source = build_lilypond_source(ProjectData([segment]), "grid-arp")
        self.assertIn("% Arpégiateur:", source)
        self.assertIn("r4", source)


if __name__ == "__main__":
    unittest.main()
