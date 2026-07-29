import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, r"e:\_repos\Pokemon Proxying\Source")
import ProxiesFromDeck as pd


class FakeCard:
    def __init__(self, name, number, set_code):
        self.name = name
        self.number = number
        self.set = SimpleNamespace(id=set_code.lower(), ptcgoCode=set_code)
        self.images = {"large": "https://example.test/card.png"}


class ResolveTests(unittest.TestCase):
    def test_prefers_exact_name_over_same_number_mismatch(self):
        candidates = [
            FakeCard("Paras", "150", "BKT"),
            FakeCard("Town Map", "149", "BKT"),
        ]

        resolved = pd.resolve(candidates, "Town Map", "150", "BKT")

        self.assertEqual(resolved.name, "Town Map")

    def test_rejects_unrelated_same_number_match(self):
        candidates = [
            FakeCard("Paras", "150", "BKT"),
        ]

        resolved = pd.resolve(candidates, "Town Map", "150", "BKT")

        self.assertIsNone(resolved)


if __name__ == "__main__":
    unittest.main()
