# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Regression checks for planned safe application shutdown."""

from pathlib import Path
import unittest


class RoadmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.roadmap = (
            Path(__file__).resolve().parents[2] / "ROADMAP.md"
        ).read_text(encoding="utf-8")

    def test_safe_quit_workflow_is_planned(self) -> None:
        for phrase in (
            "commande **Quitter**",
            "bouton de fermeture `X`",
            "**Enregistrer**",
            "**Ne pas enregistrer**",
            "**Annuler**",
            "`WM_DELETE_WINDOW`",
        ):
            self.assertIn(phrase, self.roadmap)


if __name__ == "__main__":
    unittest.main()
