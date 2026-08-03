# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from gnu_trackgenerator.settings import (
    AppSettings,
    DEFAULT_HISTORY_LIMIT,
    MAX_HISTORY_LIMIT,
    MIN_HISTORY_LIMIT,
    SettingsError,
    default_settings_path,
    load_app_settings,
    save_app_settings,
    validate_history_limit,
)


class SettingsTests(unittest.TestCase):
    def test_missing_file_uses_default_history_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = load_app_settings(Path(directory) / "missing.json")
        self.assertEqual(settings.history_limit, DEFAULT_HISTORY_LIMIT)

    def test_settings_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            written = save_app_settings(AppSettings(history_limit=250), path)
            restored = load_app_settings(path)
        self.assertEqual(written, path)
        self.assertEqual(restored.history_limit, 250)

    def test_saved_file_is_readable_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_app_settings(AppSettings(history_limit=75), path)
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload, {"history_limit": 75})

    def test_malformed_or_invalid_file_falls_back_to_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("not json", encoding="utf-8")
            self.assertEqual(load_app_settings(path).history_limit, DEFAULT_HISTORY_LIMIT)
            path.write_text('{"history_limit": 0}', encoding="utf-8")
            self.assertEqual(load_app_settings(path).history_limit, DEFAULT_HISTORY_LIMIT)

    def test_validation_accepts_bounds_and_rejects_invalid_values(self):
        self.assertEqual(validate_history_limit(str(MIN_HISTORY_LIMIT)), MIN_HISTORY_LIMIT)
        self.assertEqual(validate_history_limit(MAX_HISTORY_LIMIT), MAX_HISTORY_LIMIT)
        for value in (0, MAX_HISTORY_LIMIT + 1, "abc", True):
            with self.subTest(value=value):
                with self.assertRaises(SettingsError):
                    validate_history_limit(value)

    def test_environment_override_controls_default_path(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"GNU_TRACKGENERATOR_CONFIG_DIR": directory}):
                self.assertEqual(
                    default_settings_path(),
                    Path(directory) / "settings.json",
                )


if __name__ == "__main__":
    unittest.main()
