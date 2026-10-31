"""Tests for grade_agent_clauses.py on made-up summaries (no network). Apache-2.0, MV2 of Munim, Inc."""
import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade_agent_clauses as gr  # noqa: E402


def summary(**kw):
    s = {"jams_read": 200, "listed": 205, "parsed_ok": True, "reader_version": "0.2", "mentions_ai": 110,
         "mentions_ai_share": 0.55, "mentions_agent": 4, "agent_restrict": 3, "agent_not_restrict": 1,
         "median_joined_agent": 120, "median_joined_other": 15, "mentions_ilands": 2,
         "agent_jams": [{"slug": "a", "agent_restrict": True}, {"slug": "b", "agent_restrict": True},
                        {"slug": "c", "agent_restrict": True}, {"slug": "d", "agent_restrict": False}]}
    s.update(kw)
    return s


def verdicts(out):
    return {k: v["verdict"] for k, v in out["predictions"].items()}


class Grade(unittest.TestCase):
    def test_all_hold(self):
        out = gr.grade(summary(), {"a": "restrict", "b": "restrict", "c": "restrict", "d": "allow"})
        self.assertEqual(set(verdicts(out).values()), {"holds"})
        self.assertEqual(out["core_held"], "3 of 3")
        self.assertEqual(out["p7"]["share"], 1.0)

    def test_thresholds_are_strict_where_written(self):
        v = verdicts(gr.grade(summary(mentions_agent=10, agent_restrict=2, agent_not_restrict=8, mentions_ilands=1,
                                      median_joined_agent=15, mentions_ai_share=0.76)))
        self.assertEqual((v["P1"], v["P2"], v["P3"], v["P4"], v["P5"], v["P6"]),
                         ("fails", "fails", "fails", "fails", "fails", "fails"))
        # P1 is "fewer than 5%": exactly 5% fails; P5 bounds are inclusive
        self.assertEqual(verdicts(gr.grade(summary(mentions_agent=10)))["P1"], "fails")
        self.assertEqual(verdicts(gr.grade(summary(mentions_ai_share=0.40)))["P5"], "holds")

    def test_missing_inputs_are_not_testable(self):
        v = verdicts(gr.grade(summary(mentions_agent=0, agent_restrict=0, agent_not_restrict=0, agent_jams=[],
                                      median_joined_agent=None)))
        self.assertEqual((v["P3"], v["P4"], v["P7"]), ("not testable", "not testable", "not testable"))
        self.assertEqual(v["P1"], "holds")

    def test_p7_needs_every_agent_jam_hand_coded(self):
        out = gr.grade(summary(), {"a": "restrict", "b": "restrict", "c": "restrict"})
        self.assertEqual(out["predictions"]["P7"]["verdict"], "not testable")
        self.assertEqual(out["p7"]["unhand_coded"], ["d"])

    def test_p7_fails_below_80_percent(self):
        out = gr.grade(summary(), {"a": "restrict", "b": "tools", "c": "allow", "d": "allow"})
        self.assertEqual(out["predictions"]["P7"]["verdict"], "fails")
        self.assertEqual(out["p7"]["hand_restrict_of_auto"], 1)

    def test_hand_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "hand.csv")
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["slug", "hand_code", "note"])
                w.writerow(["a", "Restrict", "says should not join"])
            self.assertEqual(gr.read_hand(p), {"a": "restrict"})
            with open(p, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["b", "maybe", ""])
            with self.assertRaises(ValueError):
                gr.read_hand(p)


if __name__ == "__main__":
    unittest.main()
