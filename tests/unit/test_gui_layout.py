"""Regression tests for the row action-button layout."""

from pathlib import Path
import unittest


class SegmentRowLayoutTests(unittest.TestCase):
    """Protect the direct-access duplication button requested for v0.6.0."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.source = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "gnu_trackgenerator"
            / "gui.py"
        ).read_text(encoding="utf-8")

    def test_duplicate_button_is_to_the_right_of_remove_button(self) -> None:
        add_index = self.source.index('text="+"')
        remove_index = self.source.index('text="−"', add_index)
        duplicate_index = self.source.index('text="D"', remove_index)
        menu_index = self.source.index('text="☰"', duplicate_index)

        self.assertLess(add_index, remove_index)
        self.assertLess(remove_index, duplicate_index)
        self.assertLess(duplicate_index, menu_index)
        self.assertIn("column=10", self.source[duplicate_index:duplicate_index + 300])

    def test_duplicate_command_is_not_in_row_menu(self) -> None:
        self.assertNotIn("⧉ Dupliquer la ligne", self.source)


if __name__ == "__main__":
    unittest.main()
