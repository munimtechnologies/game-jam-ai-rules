# Results: do itch.io jam pages say anything about AI agents taking part?

Graded 2026-10-31 by AI agents working in the name of MV2 of Munim, Inc., against
`PREREGISTRATION-agent-clauses.md` (reader version 0.2, committed before any data was collected).

## Short answer

On 31 October 2026, 590 itch.io jam pages were open or upcoming, and all 590 were read. Only 5 of them (0.8%)
have host text about AI agents taking part. Just 1 of the 5 restricts agents: the 20 Second Game Jam 2026
(1,393 joined). 3 welcome them: Slapjam #2 and Playtest & Feedback Exchange Jams #9 and #10, the last two with
conditions. The 2026 Epic AI MegaJam treats agents as helpers on a human team. Most jams don't say anything about
agents at all, and more jams welcome them than turn them away.

Core predictions: 2 of 3 held (P1 and P7 held, P2 failed). All seven: 5 held, 2 failed.

## Grades

| # | Prediction | Result | Verdict |
|---|---|---|---|
| P1 (core) | `mentions_agent` on fewer than 5% of jams | 6 of 590 (1.0%) | holds |
| P2 (core) | At least 3 jams coded `agent_restrict` | 1 | fails |
| P3 | Restricting jams at least as many as the rest | 1 against 5 | fails |
| P4 | Median joined higher where agents are mentioned | 277.5 against 16.5 | holds |
| P5 | `mentions_ai` on 40% to 75% of jams | 384 of 590 (65.1%) | holds |
| P6 | iLands named on at least 2 pages | 3 pages | holds (see below) |
| P7 (core) | At least 80% of automated `agent_restrict` jams hand-coded as restricting agents | 1 of 1 (100%) | holds |

The reader read every listed jam (332 in progress and 258 upcoming), so no rate-limit caveat applies.

## The hand check (P7)

Every agent sentence was read by hand (`data/agent-clauses-2026-10-31-hand.csv`):

| Jam | Joined | Hand code | What the host's text says |
|---|---|---|---|
| 20 Second Game Jam 2026 | 1,393 | restrict | "AI agents (including but not limited to iLands) should not join this jam and will have their entries removed" |
| Slapjam #2 | 314 | allow | "Solo creators, teams and autonomous AI entrants are welcome." |
| Playtest & Feedback Exchange Jam #9 | 238 | allow | Agents may join with four conditions: they must say plainly that an entry is by an AI agent, must not open community threads asking for playtests, must not playtest human-made games unless those makers playtest theirs first, and must not rank human-made games |
| Playtest & Feedback Exchange Jam #10 | 31 | allow | The same four conditions |
| 2026 Epic AI MegaJam | 2,654 | tools | "Up to five humans. As many AI agents as you want." The page counts coding agents among the AI tools allowed |
| 1-BIT JAM 15 + Prizes | 241 | none | No rule. The only match was an entrant's account address in the list of entries |

The one jam the reader coded as restricting agents really does restrict them, so P7 holds. With a single jam,
though, this is a weak test of the restrict code.

## What the reader got wrong

These are reported as the pre-registration requires. No threshold was changed.

- **Entry lists count as page text.** A jam's main page also lists entries, and reader 0.2 read those too.
  Because of that, 1-BIT JAM 15 was counted as mentioning agents only because an entrant's account name contains
  "iLands". Five more matches on Playtest & Feedback Exchange Jam #10 also came from its entry list. Read by hand,
  **5 of 590 pages (0.8%)** have host text about agents, not 6. The median joined count of those 5 is 314.
  P1 and P4 hold either way.
- **P6 rests on that bug.** iLands appears on 3 pages, but only one of them, the 20 Second Game Jam, names it in
  the host's own text. The other two matches are entrants' account names. P6 holds on the reader's count as
  pre-registered, but read by hand it would fail (1 page).
- **Missed restrictions inside "allow" pages.** On the Playtest & Feedback Exchange pages, the sentences that
  restrict agents ("Do not playtest human made games...") don't use the word "agent", so the keyword reader didn't
  connect them to agents. The hand code is still "allow", because those rules let agents join under conditions.
- **No missed rules.** A hand search of all 590 saved pages for "agent", "agents", "bot", "bots" and "iLands"
  found no other rule about agents as participants. The other hits are game titles, themes, tabletop "agents",
  anti-vote-bot rules, and two jams (Jamference AI Game Jam Hack 3 and Vibecoded Game Jam) that list coding agents
  among the AI tools allowed. That is tool use, which this count leaves out on purpose.

`mentions_ai` (P5) may also include some words from entry lists. A next version of the reader will skip the
entry list.

## Why this is new

Earlier counts of jam AI rules, including this repository's 2,165-jam census, code AI as a tool. Web searches on
30 and 31 October 2026 found no count of jam pages that address AI agents as participants. This is a first
snapshot of a rule type that only appeared in autumn 2026.

## Limits

This is one snapshot taken on one day. Only main jam pages were read, so rules on Discord, in FAQs or on
separate rules pages are missed (Epic's rule that an entrant, not an AI agent, must submit is on a separate
page). Only English terms were searched. The six jams that mention agents are too few for anything beyond
counts. Account names of agent entrants are never listed here.

## Files

- `data/agent-clauses-2026-10-31-summary.json`: the reader's counts. In it, host sentences are quoted and
  entry-list matches are only counted.
- `data/agent-clauses-2026-10-31-hand.csv`: the hand codes.
- `grade_agent_clauses.py` 0.2.1: adds the hand code `none` after the data was seen. It can't change P7, which
  counts only the reader's restrict jams. `test_agent_results.py` re-runs the grading from these files.

Made with AI agents (Anthropic Claude) working in the name of MV2 of Munim, Inc. Text and data CC BY 4.0, code
Apache-2.0; quoted rules belong to their hosts. MV2 of Munim, Inc., mv2@munimtech.com.
