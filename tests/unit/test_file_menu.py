# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Static regression tests for the standard File menu."""

from pathlib import Path
import unittest


class FileMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "gnu_trackgenerator"
            / "gui.py"
        ).read_text(encoding="utf-8")

    def test_standard_file_menu_commands_are_present(self) -> None:
        for label in (
            'label="Ouvrir…"',
            'label="Enregistrer"',
            'label="Enregistrer sous…"',
            'label="Exporter…"',
        ):
            self.assertIn(label, self.source)
        self.assertIn('label="Fichier"', self.source)

    def test_file_shortcuts_are_bound(self) -> None:
        self.assertIn('accelerator="Ctrl+O"', self.source)
        self.assertIn('accelerator="Ctrl+S"', self.source)
        self.assertIn('accelerator="Ctrl+Maj+S"', self.source)
        self.assertIn('self.bind_all("<Control-o>", self.open_project)', self.source)
        self.assertIn('self.bind_all("<Control-s>", self.save_project)', self.source)
        self.assertIn('self.bind_all("<Control-Shift-s>", self.save_project_as)', self.source)

    def test_save_uses_current_path_and_save_as_sets_it(self) -> None:
        self.assertIn('self.current_project_path: Path | None = None', self.source)
        self.assertIn('if self.current_project_path is None:', self.source)
        self.assertIn('return self.save_project_as(_event)', self.source)
        self.assertIn('self._set_current_project_path(target)', self.source)

    def test_open_sets_current_file_and_resets_history(self) -> None:
        start = self.source.index('def open_project')
        block = self.source[start:start + 2600]
        self.assertIn('self._set_current_project_path(path)', block)
        self.assertIn('self.history.reset(self._capture_history_snapshot())', block)

    def test_export_produces_all_project_artifacts(self) -> None:
        start = self.source.index('def export_project')
        block = self.source[start:start + 3000]
        self.assertIn('generate_project(', block)
        self.assertIn('result.gen_path', block)
        self.assertIn('result.lilypond_path', block)
        self.assertIn('result.pdf_path', block)
        self.assertIn('result.midi_path', block)
        self.assertIn('result.wav_path', block)
        self.assertIn('result.command_log_path', block)

    def test_old_project_buttons_are_removed_from_action_bar(self) -> None:
        self.assertNotIn('text="Sauvegarder le projet"', self.source)
        self.assertNotIn('text="Charger un projet"', self.source)
        self.assertNotIn('text="Générer"', self.source)

    def test_undo_redo_buttons_are_removed_from_bottom_bar(self) -> None:
        self.assertNotIn('text="Annuler (Ctrl+Z)"', self.source)
        self.assertNotIn('text="Rétablir (Ctrl+Y)"', self.source)
        self.assertIn('label="Annuler"', self.source)
        self.assertIn('label="Rétablir"', self.source)



if __name__ == "__main__":
    unittest.main()
