# Copyright 2026 MV2 of Munim, Inc. Licensed under the Apache License, Version 2.0 (Apache-2.0).
"""Checks for the 2026-10-30 re-check: the CSV is well formed and every number in RECHECK-2026-10-30.md matches it."""
import csv
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "data", "no-rule-recheck-2026-10-30.csv")
DOC_PATH = os.path.join(HERE, "RECHECK-2026-10-30.md")

COLUMNS = ["slug", "name", "url", "joined_2026_10_14", "policy_2026_10_14", "policy_2026_10_30",
           "scope_2026_10_30", "quote_2026_10_30", "joined_2026_10_30", "entries_2026_10_30",
           "status_2026_10_30", "cash_prize_2026_10_30", "note"]
POLICIES = {"banned_all", "banned_most", "banned_assets", "discouraged", "allowed_disclose", "allowed",
            "required", "not_stated"}


def load():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def num(value):
    return int(value) if value else 0


class Recheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fields, cls.rows = load()
        with open(DOC_PATH, encoding="utf-8") as f:
            cls.doc = f.read()

    def test_format(self):
        self.assertEqual(self.fields, COLUMNS)
        slugs = [r["slug"] for r in self.rows]
        self.assertEqual(len(slugs), len(set(slugs)))
        for r in self.rows:
            self.assertEqual(r["url"], "https://itch.io/jam/" + r["slug"])
            self.assertEqual(r["policy_2026_10_14"], "not_stated")
            self.assertIn(r["policy_2026_10_30"], POLICIES)
            self.assertIn(r["status_2026_10_30"], {"ended", "running", "upcoming"})
            self.assertIn(r["cash_prize_2026_10_30"], {"yes", "no"})
            # a stated rule needs its source sentence; no rule means no quote
            if r["policy_2026_10_30"] == "not_stated":
                self.assertEqual(r["quote_2026_10_30"], "")
            else:
                self.assertTrue(r["quote_2026_10_30"])
                self.assertTrue(r["scope_2026_10_30"])

    def test_headline_table(self):
        self.assertEqual(len(self.rows), 21)
        silent = [r for r in self.rows if r["policy_2026_10_30"] == "not_stated"]
        changed = {r["slug"]: r["policy_2026_10_30"] for r in self.rows if r["policy_2026_10_30"] != "not_stated"}
        self.assertEqual(len(silent), 19)
        self.assertEqual(changed, {"mini-jame-gam-60": "banned_all", "bezi-jam-14": "allowed"})
        self.assertEqual(round(100 * len(silent) / len(self.rows)), 90)
        self.assertIn("| Still no sentence about AI on the page | 19 |", self.doc)
        self.assertIn("| **Total re-read** | **21** |", self.doc)
        self.assertIn("19 of the 21 jams (90%)", self.doc)

    def test_ended(self):
        ended = [r for r in self.rows if r["status_2026_10_30"] == "ended"]
        silent_ended = [r for r in ended if r["policy_2026_10_30"] == "not_stated"]
        self.assertEqual(len(ended), 10)
        self.assertEqual(len(silent_ended), 8)
        self.assertEqual(sum(num(r["entries_2026_10_30"]) for r in silent_ended), 311)
        self.assertIn("10 of the 21 jams have now ended. 8 of those 10", self.doc)
        self.assertIn("they took 311 entries", self.doc)

    def test_upcoming(self):
        upcoming = [r for r in self.rows if r["status_2026_10_30"] == "upcoming"]
        self.assertEqual(len(upcoming), 6)
        self.assertTrue(all(r["policy_2026_10_30"] == "not_stated" for r in upcoming))
        now = sum(num(r["joined_2026_10_30"]) for r in upcoming)
        then = sum(num(r["joined_2026_10_14"]) for r in upcoming)
        self.assertEqual((now, then), (4975, 2419))
        self.assertEqual(round(now / then, 1), 2.1)
        self.assertIn("they have 4,975 joined, up from 2,419 on 14 October (2.1x)", self.doc)

    def test_new_ban(self):
        row = next(r for r in self.rows if r["slug"] == "mini-jame-gam-60")
        self.assertEqual(row["entries_2026_10_30"], "126")
        self.assertIn('"' + row["quote_2026_10_30"] + '"', self.doc)
        self.assertIn("Mini Jame Gam #60 (126 entries)", self.doc)

    def test_cash_and_silent(self):
        cash = sorted(r["slug"] for r in self.rows
                      if r["policy_2026_10_30"] == "not_stated" and r["cash_prize_2026_10_30"] == "yes")
        self.assertEqual(cash, ["braincloud-jam", "game-jam-europe-starting", "gdevelop-big-game-jam-10"])
        self.assertIn("3 of the 19 silent jams offer cash", self.doc)

    def test_licence(self):
        self.assertIn("CC BY 4.0", self.doc)
        self.assertIn("Apache-2.0", self.doc)
        self.assertNotIn("MIT", self.doc)


if __name__ == "__main__":
    unittest.main()
