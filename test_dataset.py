"""Checks for the game-jam-ai-rules dataset: the CSV is well formed and the README's table matches it."""
import csv
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "data", "itch-jams-2026-10-14.csv")
COLUMNS = ["slug", "name", "url", "joined", "submissions_open_utc_as_listed", "policy", "scope", "quote",
           "cash_prize", "prize_notes"]
POLICIES = {"banned_all", "banned_assets", "allowed_disclose", "required", "not_stated"}
PRIZES = {"no", "cash", "gift_card", "store_credit", "funding", "trip", "unclear"}

with open(CSV, encoding="utf-8", newline="") as f:
    ROWS = list(csv.DictReader(f))
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    README = f.read()


class Dataset(unittest.TestCase):
    def test_columns(self):
        with open(CSV, encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), COLUMNS)
        for r in ROWS:
            self.assertNotIn(None, r, r["slug"])
            self.assertNotIn(None, r.values(), r["slug"])

    def test_rows(self):
        slugs = [r["slug"] for r in ROWS]
        self.assertEqual(len(slugs), len(set(slugs)))
        for r in ROWS:
            self.assertEqual(r["url"], "https://itch.io/jam/" + r["slug"])
            self.assertIn(r["policy"], POLICIES, r["slug"])
            self.assertIn(r["cash_prize"], PRIZES, r["slug"])
            self.assertRegex(r["joined"], r"^\d+$")
            self.assertRegex(r["submissions_open_utc_as_listed"], r"^\d{4}-\d\d-\d\d to \d{4}-\d\d-\d\d$")
            # every ban rests on a quoted sentence
            if r["policy"].startswith("banned") or r["policy"] == "required":
                self.assertTrue(r["quote"], r["slug"])
            if r["policy"] == "not_stated":
                self.assertEqual(r["quote"], "", r["slug"])

    def test_readme_table_matches(self):
        for policy in POLICIES:
            m = re.search(r"^\| %s \|[^|]*\| *(\d+) \| *(\d+) \|$" % policy, README, re.M)
            self.assertIsNotNone(m, policy)
            rows = [r for r in ROWS if r["policy"] == policy]
            self.assertEqual(int(m.group(1)), len(rows), policy)
            self.assertEqual(int(m.group(2)), sum(int(r["joined"]) for r in rows), policy)
        self.assertIn("**33 video-game jams**", README)
        self.assertEqual(len(ROWS), 33)

    def test_headline_numbers(self):
        stated = [r for r in ROWS if r["policy"] != "not_stated"]
        bans = [r for r in stated if r["policy"].startswith("banned")]
        self.assertEqual((len(bans), len(stated)), (18, 25))
        self.assertEqual(sum(r["policy"] == "banned_all" for r in stated), 10)
        joined_bans = sum(int(r["joined"]) for r in bans)
        joined_stated = sum(int(r["joined"]) for r in stated)
        self.assertEqual((joined_bans, joined_stated), (5081, 7153))
        self.assertEqual(round(100 * joined_bans / joined_stated), 71)
        money = [r for r in ROWS if r["cash_prize"] in ("cash", "gift_card")]
        self.assertEqual(len(money), 5)
        self.assertEqual(sorted(r["policy"] for r in money),
                         ["allowed_disclose", "allowed_disclose", "banned_all", "banned_all", "not_stated"])


if __name__ == "__main__":
    unittest.main()
