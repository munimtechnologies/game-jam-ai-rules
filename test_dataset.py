"""Checks for the game-jam-ai-rules dataset: the CSVs are well formed and every number in the README matches them."""
import csv
import math
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "page1": os.path.join(HERE, "data", "itch-jams-2026-10-14.csv"),
    "page2": os.path.join(HERE, "data", "itch-jams-2026-10-14-page2.csv"),
}
COLUMNS = ["slug", "name", "url", "joined", "submissions_open_utc_as_listed", "policy", "scope", "quote",
           "cash_prize", "prize_notes"]
POLICIES = ["banned_all", "banned_assets", "discouraged", "allowed_disclose", "allowed", "required", "not_stated"]
ALLOWING = {"allowed_disclose", "allowed", "required"}
PRIZES = {"no", "cash", "gift_card", "store_credit", "funding", "trip", "unclear"}


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


ROWS = {k: load(p) for k, p in FILES.items()}
ALL = ROWS["page1"] + ROWS["page2"]
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    README = f.read()


def stated(rows):
    return [r for r in rows if r["policy"] != "not_stated"]


def bans(rows):
    return [r for r in rows if r["policy"].startswith("banned")]


def names_code(r):
    """A ban whose scope names code as banned (not 'code not mentioned', not 'code allowed')."""
    s = r["scope"]
    return "code" in s and "not mentioned" not in s and "allowed" not in s


def money(r):
    return r["cash_prize"] in ("cash", "gift_card")


def fisher_two_sided(a, b, c, d):
    """Fisher's exact test for [[a, b], [c, d]]: sum of tables no more likely than the observed one."""
    row1, col1, n = a + b, a + c, a + b + c + d
    denom = math.comb(n, row1)

    def p(x):
        return math.comb(col1, x) * math.comb(n - col1, row1 - x) / denom

    obs = p(a)
    lo, hi = max(0, row1 + col1 - n), min(row1, col1)
    return sum(p(x) for x in range(lo, hi + 1) if p(x) <= obs * (1 + 1e-9))


class Dataset(unittest.TestCase):
    def test_columns(self):
        for name, path in FILES.items():
            with open(path, encoding="utf-8", newline="") as f:
                self.assertEqual(next(csv.reader(f)), COLUMNS, name)
            for r in ROWS[name]:
                self.assertNotIn(None, r, r["slug"])
                self.assertNotIn(None, r.values(), r["slug"])

    def test_rows(self):
        slugs = [r["slug"] for r in ALL]
        self.assertEqual(len(slugs), len(set(slugs)), "a jam appears twice")
        for r in ALL:
            self.assertEqual(r["url"], "https://itch.io/jam/" + r["slug"])
            self.assertIn(r["policy"], POLICIES, r["slug"])
            self.assertIn(r["cash_prize"], PRIZES, r["slug"])
            self.assertRegex(r["joined"], r"^\d+$")
            self.assertRegex(r["submissions_open_utc_as_listed"], r"^\d{4}-\d\d-\d\d to \d{4}-\d\d-\d\d$")
            # every stated rule rests on a quoted sentence; no quote without a rule
            if r["policy"] == "not_stated":
                self.assertEqual(r["quote"], "", r["slug"])
            elif r["slug"] not in ("zoud-gamelab", "your-worst-ideas"):  # rules read from an FAQ / rules tab
                self.assertTrue(r["quote"], r["slug"])

    def test_readme_table_matches(self):
        for policy in POLICIES:
            m = re.search(r"^\| %s \|[^|]*\|" % policy + r" *(\d+) \|" * 6 + "$", README, re.M)
            self.assertIsNotNone(m, policy)
            got = [int(x) for x in m.groups()]
            want = []
            for rows in (ROWS["page1"], ROWS["page2"], ALL):
                sel = [r for r in rows if r["policy"] == policy]
                want += [len(sel), sum(int(r["joined"]) for r in sel)]
            self.assertEqual(got, want, policy)
        self.assertEqual((len(ROWS["page1"]), len(ROWS["page2"]), len(ALL)), (33, 44, 77))
        self.assertIn("**77 video-game jams**", README)

    def test_snapshot1_headlines_unchanged(self):
        p1 = ROWS["page1"]
        self.assertEqual((len(bans(stated(p1))), len(stated(p1))), (18, 25))
        self.assertEqual(sum(r["policy"] == "banned_all" for r in p1), 10)
        self.assertEqual(sum(names_code(r) for r in bans(p1)), 3)
        self.assertEqual(sum(money(r) for r in p1), 5)

    def test_combined_headlines(self):
        s = stated(ALL)
        self.assertEqual(len(s), 56)
        self.assertEqual(len(bans(s)), 36)
        self.assertEqual(round(100 * 36 / 56), 64)
        self.assertEqual(sum(r["policy"] == "banned_all" for r in s), 23)
        self.assertEqual(round(100 * 23 / 56), 41)
        self.assertEqual(sum(r["policy"] in ALLOWING for r in s), 19)
        self.assertEqual(round(100 * 19 / 56), 34)
        jb, js = sum(int(r["joined"]) for r in bans(s)), sum(int(r["joined"]) for r in s)
        self.assertEqual((jb, js), (5752, 8277))
        self.assertEqual(round(100 * jb / js), 69)
        # page 2 alone
        s2 = stated(ROWS["page2"])
        self.assertEqual((len(bans(s2)), len(s2)), (18, 31))
        self.assertEqual(round(100 * 18 / 31), 58)
        # bans that name code
        self.assertEqual(sum(names_code(r) for r in bans(ROWS["page2"])), 7)
        self.assertEqual(sum(names_code(r) for r in bans(ALL)), 10)

    def test_money_jams(self):
        s = stated(ALL)
        m = [r for r in s if money(r)]
        nm = [r for r in s if not money(r)]
        a, b = sum(r["policy"] in ALLOWING for r in m), sum(r["policy"] not in ALLOWING for r in m)
        c, d = sum(r["policy"] in ALLOWING for r in nm), sum(r["policy"] not in ALLOWING for r in nm)
        self.assertEqual((a, b, c, d), (7, 6, 12, 31))
        self.assertEqual(sum(r["policy"].startswith("banned") for r in m), 6)
        self.assertEqual(sum(money(r) for r in ALL), 16)
        p = fisher_two_sided(a, b, c, d)
        self.assertTrue(0.09 < p < 0.12, p)
        self.assertIn("p ≈ 0.10", README)


if __name__ == "__main__":
    unittest.main()
