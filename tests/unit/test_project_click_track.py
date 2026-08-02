# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for the project-wide click-track switch."""

import unittest

from gnu_trackgenerator.generator import build_lilypond_source
from gnu_trackgenerator.models import ProjectData, Segment, ValidationError


class ProjectClickTrackTests(unittest.TestCase):
    def test_click_track_state_round_trips_in_gen_payload(self) -> None:
        project = ProjectData(
            segments=[Segment(120, 4, 4, 2)],
            click_track_enabled=False,
        )
        payload = project.to_dict()
        restored = ProjectData.from_dict(payload)

        self.assertFalse(payload["click_track_enabled"])
        self.assertFalse(restored.click_track_enabled)

    def test_legacy_project_defaults_to_enabled_click_track(self) -> None:
        restored = ProjectData.from_dict(
            {
                "app": "GNU TrackGenerator",
                "version": "0.6.0",
                "segments": [
                    {"bpm": 120, "numerator": 4, "denominator": 4, "measures": 1}
                ],
            }
        )
        self.assertTrue(restored.click_track_enabled)

    def test_enabled_click_track_generates_drum_attacks(self) -> None:
        source = build_lilypond_source(
            ProjectData([Segment(120, 4, 4, 1)], click_track_enabled=True),
            title="clic-actif",
        )
        self.assertIn("bd4 sn4 sn4 sn4", source)

    def test_disabled_click_track_preserves_timing_with_silent_skips(self) -> None:
        source = build_lilypond_source(
            ProjectData([Segment(120, 7, 8, 2)], click_track_enabled=False),
            title="clic-inactif",
        )
        self.assertIn("\\tempo 8 = 120", source)
        self.assertIn("\\repeat unfold 2 { s1*7/8 | }", source)
        self.assertNotIn("bd8", source)
        self.assertNotIn("sn8", source)

    def test_non_boolean_click_track_state_is_rejected(self) -> None:
        payload = {
            "segments": [
                {"bpm": 120, "numerator": 4, "denominator": 4, "measures": 1}
            ],
            "click_track_enabled": "false",
        }
        with self.assertRaises(ValidationError):
            ProjectData.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
