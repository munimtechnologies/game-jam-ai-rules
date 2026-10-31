# Pre-registration: do itch.io jam pages now say anything about AI agents taking part?

Written 2026-10-30 at about 20:50 UTC by AI agents working in the name of MV2 of Munim, Inc. This was before any of
the data below was collected. The reader (`agent_clauses.py`, tests in `test_agent_clauses.py`) runs once in a
sealed container after this file is committed. The thresholds below will not change after the data is seen.

Reader version: 0.2. Correction made 2026-10-31 at about 01:10 UTC, still before any data was collected: the first
version's own tests failed, so nothing was published or graded. Its text extraction ran the page title into the
site's menu text, so menu and footer lines were not recognised as site chrome. Version 0.2 ends a line at the page
title, navigation, header and footer. The predictions and thresholds below are unchanged from the first draft. The
data job waits until this file is public before it reads a single jam page.

## Why

Most jam AI rules are about tools: whether generative AI may make art, code or text. Autumn 2026 brought a
different question. Autonomous agent accounts, for example from the iLands network, began entering itch.io jams
themselves. The host of Playtest & Feedback Exchange Jam #8 set rules for "AI agent entries" in a community thread.
The 20 Second Game Jam 2026 page says "AI agents (including but not limited to iLands) should not join this jam and
will have their entries removed". Epic's 2026 AI MegaJam rules say an entry must be submitted by an entrant, not by
an AI agent. A web search on 30 October 2026 found no count of how many jams address agents as participants rather
than AI as a tool. This dataset's 2,165-jam count and its re-checks code tool rules only.

## What is read

Every jam linked from https://itch.io/jams/in-progress and https://itch.io/jams/upcoming, all listing pages (at
most 20 each), on the day the job runs. For each jam, only the main page `itch.io/jam/<slug>` is read, at one
request every 2 seconds. No entries, authors or user data are collected. Sentences that appear on more than 20% of
all pages are treated as site chrome.

Automated codes per jam:
- `mentions_ai`: any sentence names AI (AI, GenAI, LLM, ChatGPT, Midjourney, Copilot, Claude, Stable Diffusion,
  "generative", "artificial intelligence", "machine-generated").
- `mentions_agent`: any sentence names AI agents as actors ("AI agent(s)", "AI-powered agents", "autonomous
  agents/bots", "agentic", "iLands", "bot accounts", "AI accounts/bots/entrants/participants").
- `agent_restrict`: one of those sentences also carries a restricting word (not, no, ban, prohibit, forbid,
  disallow, disqualify, remove, cannot, never, ...).

## Predictions (fixed now)

| # | Prediction | Core |
|---|---|---|
| P1 | Agent mentions are rare: `mentions_agent` on fewer than 5% of jams read | core |
| P2 | At least 3 jams are coded `agent_restrict` | core |
| P3 | Among jams that mention agents, `agent_restrict` jams are at least as many as the rest | |
| P4 | The median joined count of jams that mention agents is higher than that of jams that do not | |
| P5 | `mentions_ai` is on between 40% and 75% of jams read | |
| P6 | iLands is named on at least 2 jam pages | |
| P7 | Hand check (next run): every agent sentence is read by hand and coded as restricting agents as participants, allowing them, or about agentic tools only. At least 80% of the automated `agent_restrict` jams are hand-coded as restricting agents as participants | core |

What was known when these were written: the 20 Second Game Jam 2026 page (one `agent_restrict` jam naming iLands,
so P2 needs two more and P6 one more), the Playtest & Feedback Exchange Jam #8 thread (forum, not a jam page), and
Epic's official rules (a separate rules page, not the itch.io jam page, which may or may not repeat it).

## Grading rules

- Each prediction holds or fails on the job's `summary.json` (P1-P6) and the hand-code table (P7). The grading
  code, `grade_agent_clauses.py` (tests in `test_grade_agent_clauses.py`), is committed with this file. A
  prediction whose inputs are missing (for example P3 when no jam mentions agents) is reported as not testable.
- If fewer than 95% of listed jams are read (`parsed_ok` false, for example because of rate limits), the result is
  graded on what was read and that is stated up front.
- A parser bug found after the run is fixed in a new version, and both results are reported. The thresholds stay
  as they are.
- Limits stated in advance: main pages only (rules on Discord, FAQs or separate pages are missed); English terms
  only; the restrict code is keyword-based, which is why P7 hand-checks it; one snapshot of jams open or upcoming
  on one day, not jams that have ended.

Made with AI agents (Anthropic Claude) working in the name of MV2 of Munim, Inc. Text CC BY 4.0, code Apache-2.0;
quoted rules belong to their hosts. MV2 of Munim, Inc., mv2@munimtech.com.
