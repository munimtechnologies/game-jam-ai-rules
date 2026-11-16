# Snapshot 2: itch.io upcoming jams, page 1, read 16 November 2026

MV2 of Munim, Inc. Made with AI agents. Data and text CC BY 4.0; code Apache-2.0.
Data: [`itch-jams-2026-11-16.csv`](itch-jams-2026-11-16.csv). Pre-registration (written before the
jam pages were read): [`PREREGISTRATION.md`](PREREGISTRATION.md). Checks: `python -m unittest -v test_snapshot2`
recomputes every number below from the CSV.

## What was read
Page 1 of https://itch.io/jams/upcoming (default sort "Most Joined"), about 00:30 UTC on 16 November 2026.
That page lists 50 jams; 6 are not game jams or are 10-year placeholder listings (two music, two comic,
one poetry, one placeholder), which leaves **44 jams with 9,577 joined in total**. Each jam's main itch.io
page was read once by a web reader asked for every sentence about AI, prizes and eligibility. The classes are
the same as in snapshot 1 (14 October 2026). Two jams set different rules for different tracks (`mixed`).
For those, `main_track_policy` gives the rule for the track with the main game prize.

## Counts (44 jams)
| policy | jams |
|---|---|
| banned_all | 22 |
| banned_assets | 6 |
| discouraged (LLM use lowers the score) | 1 |
| mixed (Bezi Jam 15, MEAT on MARS) | 2 |
| allowed | 2 |
| allowed_disclose | 2 |
| required | 1 |
| not_stated | 8 |

- **36 of 44 jams state a rule.** In their main track, **29 of those 36 (81%) ban AI-made assets**,
  either all generative AI (22) or assets such as art and audio (7, counting MEAT on MARS's 100-hour track).
- **6 jams permit AI in their main track**, with 340 of 9,577 joined (3.6%). Jams that ban it in their
  main track hold 7,573 joined (79.1%).
- The three biggest jams (GMTK 2027, MFG Gambler's Jam, Metroidvania Month Finale; 1,000+ joined each) all
  ban AI art or audio. MFG also bans AI code.

## Where the cash is (not pre-registered; exploratory)
9 of the 44 jams state cash prizes. **4 of those 9 permit AI in their game track**: Slapjam #3, Micro Jam 070,
Bezi Jam 15 and PIXEL-DECK JAM #1. Only **2 of the 35 jams without cash** permit it (Gamedev.js 2027 and the
Z4597 jam). Fisher's exact test gives two-sided **p = 0.011**. The test was chosen after we saw the data,
and the numbers are small, so treat this as a lead, not a finding. Snapshot 1 found no significant link
(p about 0.10) on a different, larger sample.

A likely reason: three of those four cash pots are tied to AI products. Bezi, which sponsors Bezi Jam 15,
makes an AI development assistant. Micro Jam's cash this round is mostly a $100 category for games made with
Ziva, an AI agent for Godot. Slapjam is built around AI tools ("Use AI tools as part of making your game").
The other cash jams ban AI (Pixel Forge, b3agz for assets), score LLM use lower (GMT Jam #1), split by track
(MEAT on MARS) or say nothing (Uplifting).

## Same jams, one month apart
12 jams appear in both snapshot 1 (pages 1 and 2, 14 October) and this one. 11 have the same class. One
tightened: Metroidvania Month went from not_stated to banned_assets, which was already reported in
RECHECK-2026-11-14.md. **None relaxed.**

## Predictions (written before reading the pages)
| | prediction | result | verdict |
|---|---|---|---|
| P1 | >= 55% of stated jams ban AI-made assets in their main track | 29 / 36 = 81% | held |
| P2 | <= 8 allowed / allowed_disclose / required / required_tool | 5 (6 if Bezi's game track counts) | held |
| P3 | not_stated is 20% to 45% of the 44 | 8 / 44 = 18% | **failed** (fewer silent pages than expected) |
| P4 | 0 relaxations among jams in both snapshots | 0 of 12 | held |
| P5 | no jam with >= 1,000 joined is `allowed` | 0 of 3 | held |
| P6 | <= 3 jams with cash prizes AND allow AI-made assets | 3 by the literal classes; 4 counting Bezi's game track; 5 with MEAT on MARS's 48-hour track | held literally, **failed** on the game-track reading |

## Limits
- The pre-registration was written in the same session, before the jam pages were read, but it is published
  together with the results. No outside timestamp backs up the order.
- One reading of each page, through a summarising web reader, by a single coder with no second coder. Four
  pages (Pixel Forge, Micro Jam 070, GMT Jam #1, MEAT on MARS) were read minutes before the pre-registration
  was written while scouting prizes. They are flagged `read_before_prereg=yes`.
- Only main jam pages were read. Rules kept in Discord, FAQs elsewhere or announcement posts are not counted.
  Game Off 2026 is one example: its page says nothing about AI, but GitHub's blog does.
- "Cash" means the page names a money amount, gift cards excluded. Prize claims in titles ("$30k Prizes",
  "+ Prizes") were checked against the page body.
- The list is ordered by sign-ups, so this sample over-represents the largest upcoming jams, not jams in general.
- RPG LATAM JAM 2026 turned out to be a tabletop jam. It stays in the sample because the pre-registered
  title rule did not exclude it. Dropping it changes no verdict.
