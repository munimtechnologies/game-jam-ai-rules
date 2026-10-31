# Copyright 2026 MV2 of Munim, Inc. Licensed under the Apache License, Version 2.0 (Apache-2.0).
"""Checks for RESULTS-agent-clauses.md: the grades and every number in it follow from the files in data/."""
import json
import os
import statistics
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grade_agent_clauses as gr  # noqa: E402

SUMMARY = os.path.join(HERE, "data", "agent-clauses-2026-10-31-summary.json")
HAND = os.path.join(HERE, "data", "agent-clauses-2026-10-31-hand.csv")
DOC = os.path.join(HERE, "RESULTS-agent-clauses.md")


class Results(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SUMMARY, encoding="utf-8") as f:
            cls.s = json.load(f)
        cls.hand = gr.read_hand(HAND)
        cls.out = gr.grade(cls.s, cls.hand)
        with open(DOC, encoding="utf-8") as f:
            cls.doc = f.read()

    def test_grades(self):
        v = {k: p["verdict"] for k, p in self.out["predictions"].items()}
        self.assertEqual(v, {"P1": "holds", "P2": "fails", "P3": "fails", "P4": "holds", "P5": "holds",
                             "P6": "holds", "P7": "holds"})
        self.assertEqual(self.out["core_held"], "2 of 3")
        self.assertIn("Core predictions: 2 of 3 held", self.doc)
        self.assertIn("All seven: 5 held, 2 failed.", self.doc)

    def test_summary_is_consistent(self):
        s = self.s
        self.assertEqual(s["jams_read"], s["listed"])
        self.assertEqual(sum(s["by_listing"].values()), s["jams_read"])
        self.assertEqual(len(s["agent_jams"]), s["mentions_agent"])
        self.assertEqual(sum(1 for j in s["agent_jams"] if j["agent_restrict"]), s["agent_restrict"])
        self.assertEqual(s["agent_restrict"] + s["agent_not_restrict"], s["mentions_agent"])
        self.assertEqual(statistics.median(j["joined"] for j in s["agent_jams"]), s["median_joined_agent"])
        self.assertEqual(round(s["mentions_ai"] / s["jams_read"], 4), s["mentions_ai_share"])

    def test_table_numbers(self):
        s = self.s
        self.assertIn("| 6 of 590 (1.0%) | holds |", self.doc)
        self.assertIn("| 384 of 590 (65.1%) | holds |", self.doc)
        self.assertIn("| 277.5 against 16.5 | holds |", self.doc)
        self.assertIn("| 1 against 5 | fails |", self.doc)
        self.assertEqual(round(100 * s["mentions_agent"] / s["jams_read"], 1), 1.0)
        self.assertEqual(round(100 * s["mentions_ai"] / s["jams_read"], 1), 65.1)
        self.assertIn("(332 in progress and 258 upcoming)", self.doc)

    def test_hand_codes(self):
        self.assertEqual(self.out["p7"]["unhand_coded"], [])
        self.assertEqual(self.out["p7"]["share"], 1.0)
        self.assertEqual(self.out["p7"]["hand_counts"], {"allow": 3, "none": 1, "restrict": 1, "tools": 1})
        for j in self.s["agent_jams"]:
            self.assertIn("| %s | %s | %s |" % (j["title"], format(j["joined"], ","), self.hand[j["slug"]]), self.doc)

    def test_hand_corrected_figures(self):
        rules = [j for j in self.s["agent_jams"] if self.hand[j["slug"]] != "none"]
        self.assertEqual(len(rules), 5)
        self.assertTrue(all(j["host_sentences"] for j in rules))
        self.assertEqual(round(100 * len(rules) / self.s["jams_read"], 1), 0.8)
        self.assertEqual(statistics.median(j["joined"] for j in rules), 314)
        self.assertIn("**5 of 590 pages (0.8%)**", self.doc)
        self.assertIn("The median joined count of those 5 is 314.", self.doc)
        named = [j for j in self.s["agent_jams"] if any("iLands" in t for t in j["host_sentences"])]
        self.assertEqual([j["slug"] for j in named], ["20-second-game-jam-2026"])

    def test_quotes_come_from_the_data(self):
        for j in self.s["agent_jams"]:
            if j["slug"] in ("20-second-game-jam-2026", "slapjam-ai-2"):
                self.assertIn('"' + j["host_sentences"][0] + '"', self.doc)

    def test_privacy_and_licence(self):
        # no entrant addresses; the publish lane separately refuses any postal address
        text = self.doc + json.dumps(self.s) + open(HAND, encoding="utf-8").read()
        self.assertNotIn(".itch.io", text)
        self.assertIn("CC BY 4.0", self.doc)
        self.assertIn("Apache-2.0", self.doc)
        self.assertNotIn("MIT", self.doc)


if __name__ == "__main__":
    unittest.main()
