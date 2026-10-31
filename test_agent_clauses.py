"""Tests for agent_clauses.py on made-up pages (no network). Apache-2.0, MV2 of Munim, Inc."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_clauses as ac  # noqa: E402

CHROME = "<nav><a href=\"/jams\">Game Jams</a></nav><footer><p>Sell your games on our marketplace.</p></footer>"


def jam_page(title, body, joined="1,234"):
    return ("<html><head><title>%s - itch.io</title><script>var AI_agent = 1;</script></head><body>%s"
            "<div class=\"stat_value\">%s</div><div class=\"stat_label\">Joined</div>"
            "<div class=\"jam_body\">%s</div></body></html>" % (title, CHROME, joined, body))


class Parse(unittest.TestCase):
    def test_slugs(self):
        h = ('<a href="/jam/alpha-jam">A</a><a href="https://itch.io/jam/beta">B</a><a href="/jam/alpha-jam">A</a>'
             '<a href="/jam/alpha-jam/entries">E</a><a href="/jams/upcoming">U</a><a href="/jam/new">N</a>')
        self.assertEqual(ac.jam_slugs(h), ["alpha-jam", "beta"])

    def test_page_total(self):
        self.assertEqual(ac.page_total("<div>Page 1 of 7</div>"), 7)
        self.assertEqual(ac.page_total('<a href="?page=2">2</a><a href="?page=6">6</a>'), 6)
        self.assertEqual(ac.page_total("<p>nothing</p>"), 1)

    def test_title_and_menus_end_lines(self):
        h = "<title>X - itch.io</title><header><nav><a>Jams</a></nav></header><p>Rule one.</p><footer>Shop</footer>"
        self.assertEqual(ac.to_text(h), "X - itch.io\nJams\nRule one.\nShop")

    def test_parse_jam(self):
        r = ac.parse_jam(jam_page("Cool Jam", "<p>Make a game. AI agents should not join.</p>"))
        self.assertEqual(r["title"], "Cool Jam")
        self.assertEqual(r["joined"], 1234)
        self.assertIn("AI agents should not join.", r["sentences"])
        self.assertIn("Game Jams", r["sentences"])
        self.assertFalse(any("AI_agent" in s for s in r["sentences"]))  # scripts are not text


class Code(unittest.TestCase):
    def code(self, body):
        return ac.code_jam(ac.parse_jam(jam_page("J", body))["sentences"], set())

    def test_ban(self):
        c = self.code("<p>AI agents (including but not limited to iLands) should not join this jam.</p>")
        self.assertTrue(c["mentions_ai"] and c["mentions_agent"] and c["agent_restrict"])
        self.assertEqual(c["agent_terms"], ["ai agents", "ilands"])

    def test_allow(self):
        c = self.code("<p>Teams may include AI agents alongside humans.</p>")
        self.assertTrue(c["mentions_agent"])
        self.assertFalse(c["agent_restrict"])

    def test_tool_rule_is_not_agent(self):
        c = self.code("<p>Generative AI is banned for art.</p><p>Use any engine.</p>")
        self.assertTrue(c["mentions_ai"])
        self.assertFalse(c["mentions_agent"])

    def test_lowercase_ai_in_words_is_not_ai(self):
        c = self.code("<p>Explain the main rules. Wait for the train. Said hello.</p>")
        self.assertFalse(c["mentions_ai"])

    def test_other_agent_forms(self):
        for s in ["Autonomous bots will be removed.", "No AI-powered agents.", "Agentic tools are fine.",
                  "A.I. agents may not enter.", "Bot accounts are banned."]:
            self.assertTrue(self.code("<p>%s</p>" % s)["mentions_agent"], s)

    def test_secret_agent_is_not_ai(self):
        self.assertFalse(self.code("<p>Play as a secret agent. Agents of chaos welcome.</p>")["mentions_agent"])

    def test_chrome_is_ignored(self):
        pages = [ac.parse_jam(jam_page("J%d" % i, "<p>Theme %d. Have fun!</p>" % i))["sentences"] for i in range(10)]
        chrome = ac.chrome_sentences(pages, 0.2)
        self.assertIn("Sell your games on our marketplace.", chrome)
        self.assertIn("Game Jams", chrome)
        self.assertNotIn("Theme 3.", chrome)


class Summary(unittest.TestCase):
    def test_counts(self):
        rows = [
            {"slug": "a", "title": "A", "listing": "in-progress", "joined": 300, "entries": None,
             **ac.code_jam(["AI agents should not join this jam."], set())},
            {"slug": "b", "title": "B", "listing": "upcoming", "joined": 10, "entries": None,
             **ac.code_jam(["AI is allowed."], set())},
            {"slug": "c", "title": "C", "listing": "upcoming", "joined": 20, "entries": None,
             **ac.code_jam(["Have fun."], set())},
        ]
        s = ac.summarize(rows)
        self.assertEqual((s["jams_read"], s["mentions_ai"], s["mentions_agent"], s["agent_restrict"]), (3, 2, 1, 1))
        self.assertEqual(s["by_listing"], {"in-progress": 1, "upcoming": 2})
        self.assertEqual((s["median_joined_agent"], s["median_joined_other"]), (300, 15))


class Offline(unittest.TestCase):
    def test_end_to_end_from_raw(self):
        with tempfile.TemporaryDirectory() as d:
            raw, out = os.path.join(d, "raw"), os.path.join(d, "out")
            os.makedirs(raw)
            pages = {
                "list-in-progress-1.html": '<a href="/jam/one">1</a><a href="/jam/two">2</a>',
                "list-upcoming-1.html": '<a href="/jam/two">2</a><a href="/jam/three">3</a>',
                "jam-one.html": jam_page("One", "<p>AI agents will have their entries removed.</p>", "50"),
                "jam-two.html": jam_page("Two", "<p>Generative AI must be disclosed.</p>", "900"),
                "jam-three.html": jam_page("Three", "<p>Make something small.</p>", "7"),
            }
            for name, h in pages.items():
                with open(os.path.join(raw, name), "w", encoding="utf-8") as f:
                    f.write(h)
            script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_clauses.py")
            p = subprocess.run([sys.executable, "-I", script, "--out", out, "--raw-dir", raw],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            with open(os.path.join(out, "summary.json"), encoding="utf-8") as f:
                s = json.load(f)
            self.assertEqual((s["listed"], s["jams_read"], s["mentions_ai"], s["mentions_agent"]), (3, 3, 2, 1))
            self.assertEqual(s["by_listing"], {"in-progress": 2, "upcoming": 1})
            self.assertEqual(s["agent_jams"][0]["slug"], "one")
            self.assertEqual(s["reader_version"], "0.2")
            self.assertIn("Game Jams", s["chrome_sentences"])
            self.assertTrue(os.path.exists(os.path.join(out, "jams.csv")))


if __name__ == "__main__":
    unittest.main()
