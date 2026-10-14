"""Checks for the game-jam-ai-rules dataset: the CSVs are well formed and every number in the README matches them."""
import csv
import math
import os
import re
import unittest
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "page1": os.path.join(HERE, "data", "itch-jams-2026-10-14.csv"),
    "page2": os.path.join(HERE, "data", "itch-jams-2026-10-14-page2.csv"),
}
HISTORY_FILE = os.path.join(HERE, "data", "recurring-jams-history-2026-10-14.csv")
COLUMNS = ["slug", "name", "url", "joined", "submissions_open_utc_as_listed", "policy", "scope", "quote",
           "cash_prize", "prize_notes"]
HISTORY_COLUMNS = ["series", "slug", "name", "url", "host", "start_utc", "entries", "policy", "scope", "quote", "note"]
POLICIES = ["banned_all", "banned_assets", "discouraged", "allowed_disclose", "allowed", "required", "not_stated"]
HISTORY_POLICIES = POLICIES + ["banned_most"]
ALLOWING = {"allowed_disclose", "allowed", "required"}
PRIZES = {"no", "cash", "gift_card", "store_credit", "funding", "trip", "unclear"}
READ_ON = "2026-10-14"


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


ROWS = {k: load(p) for k, p in FILES.items()}
ALL = ROWS["page1"] + ROWS["page2"]
HISTORY = load(HISTORY_FILE)
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


def by_year(rows):
    """{year: [editions, editions with a ban, entries, entries under a ban]} for ended editions."""
    out = defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        if not r["entries"]:
            continue
        y, n, banned = int(r["start_utc"][:4]), int(r["entries"]), r["policy"].startswith("banned")
        t = out[y]
        t[0] += 1
        t[1] += banned
        t[2] += n
        t[3] += n if banned else 0
    return dict(out)


def series_editions():
    s = defaultdict(list)
    for r in HISTORY:
        s[r["series"]].append(r)
    for v in s.values():
        v.sort(key=lambda r: r["start_utc"])
    return s


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


class History(unittest.TestCase):
    def test_columns_and_rows(self):
        with open(HISTORY_FILE, encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), HISTORY_COLUMNS)
        slugs = [r["slug"] for r in HISTORY]
        self.assertEqual(len(slugs), len(set(slugs)), "an edition appears twice")
        for r in HISTORY:
            self.assertNotIn(None, r, r["slug"])
            self.assertNotIn(None, r.values(), r["slug"])
            self.assertEqual(r["url"], "https://itch.io/jam/" + r["slug"])
            self.assertIn(r["policy"], HISTORY_POLICIES, r["slug"])
            self.assertRegex(r["start_utc"], r"^\d{4}-\d\d-\d\d$")
            # only editions that had not started when the pages were read lack an entry count
            if r["entries"]:
                self.assertRegex(r["entries"], r"^\d+$")
                self.assertLess(r["start_utc"], READ_ON, r["slug"])
            else:
                self.assertGreater(r["start_utc"], READ_ON, r["slug"])
            self.assertEqual(r["policy"] == "not_stated", r["quote"] == "", r["slug"])

    def test_counts(self):
        self.assertEqual(len(HISTORY), 55)
        self.assertEqual(len(series_editions()), 11)
        self.assertEqual(sum(bool(r["entries"]) for r in HISTORY), 51)
        self.assertIn("**11 recurring jam series**", README)
        self.assertIn("**55\neditions**", README)
        self.assertIn("51 editions have ended", README)

    def test_year_table_matches(self):
        got = {}
        for m in re.finditer(r"^\| (\d{4}) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+)% \|$", README, re.M):
            got[int(m.group(1))] = [int(x) for x in m.groups()[1:]]
        want = {y: t + [round(100 * t[3] / t[2])] for y, t in by_year(HISTORY).items()}
        self.assertEqual(got, want)
        self.assertEqual(want[2022], [4, 0, 6688, 0, 0])
        self.assertEqual(want[2023], [14, 4, 11169, 699, 6])
        self.assertEqual(want[2024], [12, 4, 16083, 4465, 28])
        self.assertEqual(want[2025], [12, 8, 20687, 18452, 89])
        self.assertEqual(want[2026], [8, 5, 15814, 14814, 94])

    def test_without_gmtk(self):
        rest = by_year([r for r in HISTORY if r["series"] != "GMTK Game Jam"])
        shares = {y: round(100 * t[3] / t[2]) for y, t in rest.items() if y >= 2023}
        self.assertEqual(shares, {2023: 16, 2024: 52, 2025: 80, 2026: 81})
        self.assertIn("the share is 16% (2023), 52% (2024), 80% (2025) and 81% (2026)", README)
        gmtk26 = [r for r in HISTORY if r["slug"] == "gmtk-jam-2026"][0]
        self.assertEqual(gmtk26["entries"], "10531")
        self.assertIn("10,531 entries in\n  2026", README)

    def test_transitions(self):
        adopted, allowing = [], []
        for name, eds in series_editions().items():
            policies = [r["policy"] for r in eds]
            restrict = [p.startswith("banned") or p == "discouraged" for p in policies]
            if policies[0] == "not_stated" and any(restrict):
                adopted.append(name)
            if any(p in ALLOWING for p in policies):
                allowing.append(name)
            # no series allows AI after it has banned it
            first_ban = next((i for i, p in enumerate(policies) if p.startswith("banned")), None)
            if first_ban is not None:
                self.assertFalse(any(p in ALLOWING for p in policies[first_ban:]), name)
        self.assertEqual(sorted(adopted), ["Boss Rush Jam", "Brackeys Game Jam", "GMTK Game Jam",
                                           "Godot Wild Jam", "Kenney Jam", "SCREAM JAM"])
        self.assertEqual(sorted(allowing), ["Game Off", "Gamedev.js Jam"])
        self.assertIn("Six series adopted a restriction", README)
        self.assertIn("No series went from a ban back to allowing AI", README)
        # the earliest adoption found: Godot Wild Jam between #53 and #54
        gwj = {r["slug"]: r["policy"] for r in HISTORY if r["series"] == "Godot Wild Jam"}
        self.assertEqual((gwj["godot-wild-jam-53"], gwj["godot-wild-jam-54"]), ("not_stated", "banned_all"))


if __name__ == "__main__":
    unittest.main()
