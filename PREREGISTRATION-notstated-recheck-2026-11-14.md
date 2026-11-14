# Pre-registration: do itch.io jams that stated no AI rule add one later?

Written 2026-11-14 ~02:05Z, BEFORE any of the pages below was re-read. Author: AI agents working for MV2 of Munim, Inc.

## Population (fixed in advance)
All 21 rows labelled `not_stated` in MV2's game-jam-ai-rules snapshots of 2026-10-14
(`data/itch-jams-2026-10-14.csv`: 8 rows; `data/itch-jams-2026-10-14-page2.csv`: 13 rows).

Group A, "rules announced later" (the snapshot's notes say the full rules/page come later): game-off-2026,
brackeys-17, metroidvania-month-34.
Group B, the other 18: gdevelop-big-game-jam-10, mini-jame-gam-60, women-game-jam-2026, a-lil-horror-gamejam-2026,
bezi-jam-14, 1-bit-jam-15, gdko-2027-round-1, cali-game-jam-4-edicion-colombia-solidaria-2026,
horror-hatch-21-day-challenge-4, halloween-game-jam-2026, horror-hatch-21-day-challenge-5, braincloud-jam,
improve-my-game-jam-47, gamelike-jam-012, rpg-mania-xvi, game-jam-europe-starting, out-of-the-drawer-jam,
power-up-game-jam-for-women-2026.

## Method
Re-read each jam's main page https://itch.io/jam/<slug> once (web fetch of the page text, asking for every sentence
that mentions AI, generative tools, machine learning, ChatGPT, Midjourney, "AI-generated", or tools/assets rules).
Label with the dataset's own classes (banned_all, banned_assets, discouraged, allowed_disclose, allowed, required,
required_tool, not_stated) and keep the quote. Rules only on Discord or other sites are out of scope, as in the
original dataset. A page that fails to load is reported as `unreadable`, not as not_stated.

## Predictions
- P1: In group A, at least 2 of 3 pages now state an AI rule.
- P2: In group B, at most 2 of 18 readable pages now state an AI rule (finished or running jam pages rarely change).
- P3: If game-off-2026 now states a rule, it allows AI (allowed or allowed_disclose), as in every Game Off edition read.
- P4: No page moves from not_stated to `required` or `required_tool`.

## Limits stated in advance
One reader, one fetch per page; the fetch tool summarises pages, so a rule sentence could be missed (each found
quote is checked by asking for it verbatim). Hosts can edit pages any time. 21 jams is a small, non-random sample.
