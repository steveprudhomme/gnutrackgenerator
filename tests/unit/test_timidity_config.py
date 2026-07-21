# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Unit tests for TiMidity++ SoundFont configuration generation."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from gnu_trackgenerator.generator import _write_timidity_soundfont_config


class TimidityConfigTests(unittest.TestCase):
    def test_soundfont_config_uses_selected_sf2(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            soundfont = root / "CrisisGeneralMidi301.sf2"
            soundfont.write_bytes(b"dummy")
            wav = root / "test.wav"

            cfg = _write_timidity_soundfont_config(soundfont, wav)
            content = cfg.read_text(encoding="utf-8")

            self.assertEqual(cfg.name, "test.timidity.cfg")
            self.assertIn("soundfont", content)
            self.assertIn("CrisisGeneralMidi301.sf2", content)
            self.assertIn("order=0", content)
            self.assertIn("amp=120", content)


if __name__ == "__main__":
    unittest.main()
