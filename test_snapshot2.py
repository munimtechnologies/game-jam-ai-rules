# SPDX-License-Identifier: Apache-2.0
# MV2 of Munim, Inc. (made with AI agents).
"""Recompute every number in snapshot-2/RESULTS.md from snapshot-2/itch-jams-2026-11-16.csv."""
import csv
import math
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "snapshot-2"
CSV_PATH = SNAP / "itch-jams-2026-11-16.csv"
RESULTS_PATH = SNAP / "RESULTS.md"

POLICIES = {
    "banned_all", "banned_most", "banned_assets", "discouraged", "allowed_disclose",
    "allowed", "required", "required_tool", "not_stated", "mixed",
}
BANS = {"banned_all", "banned_most", "banned_assets"}
ALLOWS = {"allowed", "allowed_disclose", "required", "required_tool"}
EXCLUDED_RANKS = {5, 8, 11, 25, 27, 29}


def load():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fisher_two_sided(a, b, c, d):
    """Two-sided Fisher exact test for [[a, b], [c, d]] (sum of tables no more likely than observed)."""
    row1, col1, n = a + b, a + c, a + b + c + d

    def p(k):
        return math.comb(col1, k) * math.comb(n - col1, row1 - k) / math.comb(n, row1)

    lo, hi = max(0, row1 - (n - col1)), min(row1, col1)
    observed = p(a)
    return sum(p(k) for k in range(lo, hi + 1) if p(k) <= observed * (1 + 1e-9))


class TestSnapshot2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load()
        cls.results = RESULTS_PATH.read_text(encoding="utf-8")

    def test_shape(self):
        rows = self.rows
        self.assertEqual(len(rows), 44)
        slugs = [r["slug"] for r in rows]
        self.assertEqual(len(set(slugs)), 44)
        ranks = [int(r["rank"]) for r in rows]
        self.assertEqual(len(set(ranks)), 44)
        self.assertEqual(set(range(1, 51)) - set(ranks), EXCLUDED_RANKS)
        for r in rows:
            self.assertEqual(r["url"], "https://itch.io/jam/" + r["slug"])
            self.assertIn(r["policy"], POLICIES)
            self.assertIn(r["main_track_policy"], POLICIES - {"mixed"})
            if r["policy"] != "mixed":
                self.assertEqual(r["main_track_policy"], r["policy"], r["slug"])
            self.assertIn(r["cash_prize"], {"cash", "no"})
            self.assertIn(r["read_before_prereg"], {"yes", "no"})
            self.assertGreater(int(r["joined"]), 0)
            if r["policy"] == "not_stated":
                self.assertEqual(r["quote"], "", r["slug"])
            else:
                self.assertNotEqual(r["quote"], "", r["slug"])
        self.assertEqual(sum(r["read_before_prereg"] == "yes" for r in rows), 4)

    def test_counts(self):
        counts = Counter(r["policy"] for r in self.rows)
        self.assertEqual(dict(counts), {
            "banned_all": 22, "banned_assets": 6, "discouraged": 1, "mixed": 2,
            "allowed": 2, "allowed_disclose": 2, "required": 1, "not_stated": 8,
        })
        total = sum(int(r["joined"]) for r in self.rows)
        self.assertEqual(total, 9577)
        self.assertIn("9,577 joined in total", self.results)

    def test_main_track_shares(self):
        stated = [r for r in self.rows if r["policy"] != "not_stated"]
        self.assertEqual(len(stated), 36)
        bans = [r for r in stated if r["main_track_policy"] in BANS]
        self.assertEqual(len(bans), 29)
        self.assertEqual(round(100 * len(bans) / len(stated)), 81)
        self.assertIn("29 of those 36 (81%)", self.results)
        permit = [r for r in self.rows if r["main_track_policy"] in ALLOWS]
        self.assertEqual(len(permit), 6)
        permit_joined = sum(int(r["joined"]) for r in permit)
        ban_joined = sum(int(r["joined"]) for r in self.rows if r["main_track_policy"] in BANS)
        self.assertEqual(permit_joined, 340)
        self.assertEqual(ban_joined, 7573)
        self.assertEqual(round(100 * permit_joined / 9577, 1), 3.6)
        self.assertEqual(round(100 * ban_joined / 9577, 1), 79.1)
        self.assertIn("340 of 9,577 joined (3.6%)", self.results)
        self.assertIn("7,573 joined (79.1%)", self.results)

    def test_biggest_jams_ban(self):
        big = [r for r in self.rows if int(r["joined"]) >= 1000]
        self.assertEqual(len(big), 3)
        for r in big:
            self.assertIn(r["main_track_policy"], BANS, r["slug"])

    def test_cash(self):
        cash = [r for r in self.rows if r["cash_prize"] == "cash"]
        nocash = [r for r in self.rows if r["cash_prize"] == "no"]
        self.assertEqual(len(cash), 9)
        a = sum(r["main_track_policy"] in ALLOWS for r in cash)
        c = sum(r["main_track_policy"] in ALLOWS for r in nocash)
        self.assertEqual((a, c), (4, 2))
        p = fisher_two_sided(a, len(cash) - a, c, len(nocash) - c)
        self.assertAlmostEqual(p, 0.011257, places=5)
        self.assertIn("p = 0.011", self.results)
        literal = sum(r["policy"] in ALLOWS for r in cash)
        self.assertEqual(literal, 3)

    def test_overlap_with_snapshot1(self):
        both = [r for r in self.rows if r["snapshot1_policy"]]
        self.assertEqual(len(both), 12)
        same = [r for r in both if r["snapshot1_policy"] == r["policy"]]
        self.assertEqual(len(same), 11)
        relaxed = [r for r in both
                   if r["snapshot1_policy"] in BANS and r["main_track_policy"] not in BANS]
        self.assertEqual(relaxed, [])
        changed = [r["slug"] for r in both if r not in same]
        self.assertEqual(changed, ["metroidvania-month-34"])
        self.assertIn("0 of 12", self.results)

    def test_p3_failed(self):
        silent = sum(r["policy"] == "not_stated" for r in self.rows)
        self.assertEqual(silent, 8)
        self.assertLess(100 * silent / 44, 20)
        self.assertIn("8 / 44 = 18%", self.results)


if __name__ == "__main__":
    unittest.main()
