import sys
import unittest
from pathlib import Path

from reportlab.lib.units import inch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Source"))

from ProxiesFromDeck import CARD_H, CARD_W, get_layout_config, get_page_size


class LayoutConfigTests(unittest.TestCase):
    def test_portrait_layout_defaults_to_3x3(self):
        cols, rows = get_layout_config(False)
        self.assertEqual((cols, rows), (3, 3))

    def test_landscape_layout_uses_2x4(self):
        cols, rows = get_layout_config(True)
        self.assertEqual((cols, rows), (4, 2))

    def test_page_size_includes_gap_between_cards(self):
        width, height = get_page_size(3, 3, 0.25 * inch)
        self.assertAlmostEqual(width, 3 * CARD_W + 2 * 0.25 * inch)
        self.assertAlmostEqual(height, 3 * CARD_H + 2 * 0.25 * inch)


if __name__ == "__main__":
    unittest.main()
