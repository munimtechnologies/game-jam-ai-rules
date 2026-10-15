# game-jam-ai-rules

An open, quote-backed dataset of what itch.io game jams say about AI-made work, by MV2 of Munim, Inc.

itch.io lets every jam host write their own rules, and many now say something about generative AI.
We could not find any published dataset of those rules: the closest prior art is
[a browser extension](https://mrgabas.itch.io/itchio-jam-ai-policy-filter) that classifies a jam's
page automatically when you open it, and forum threads that quote a few jams. This repository records
the rule for each jam with the sentence it comes from, so anyone can check it and count.

## History: 11 recurring jams, 2021 to 2027 (read 14 October 2026)

`data/recurring-jams-history-2026-10-14.csv` follows **11 recurring jam series** through **55
editions**: SCREAM JAM, GMTK Game Jam, Brackeys, Godot Wild Jam, Kenney Jam, GitHub's Game Off,
Gamedev.js, Boss Rush Jam, Bigmode, Pirate Software and GDevelop BIG Game Jam. itch.io keeps old jam
pages online, so each past edition's rule can be read and dated. We found no earlier record of when
jams adopted AI rules; searches of the web and arXiv turned up only single-jam rule pages and forum posts.

51 editions have ended and list their entries; 4 are upcoming. Share of editions, and of submitted
games, made under a rule that bans AI-made work in some form, by the year the edition started:

| year | editions | with a ban | entries | entries under a ban | share of entries |
|------|-----:|-----:|-----:|-----:|-----:|
| 2021 | 1 | 0 | 217 | 0 | 0% |
| 2022 | 4 | 0 | 6688 | 0 | 0% |
| 2023 | 14 | 4 | 11169 | 699 | 6% |
| 2024 | 12 | 4 | 16083 | 4465 | 28% |
| 2025 | 12 | 8 | 20687 | 18452 | 89% |
| 2026 | 8 | 5 | 15814 | 14814 | 94% |

What it shows:

- **In four years, AI bans went from none of these jams to almost all of their games.** No edition
  read from 2021 or 2022 has an AI rule. In 2026, 94% of the games submitted to these series' ended
  editions were made under a ban. GMTK, the largest jam on itch.io, weighs heavily (10,531 entries in
  2026). Without it, the share is 16% (2023), 52% (2024), 80% (2025) and 81% (2026).
- **Six series adopted a restriction, and the date can be pinned down.** Godot Wild Jam between #53
  (January 2023) and #54 (February 2023), the earliest found; GMTK in August 2024 (a request, "We ask
  that you do not use generative AI ... to create any assets or code"), turned into a ban on AI art and
  audio in 2025; SCREAM JAM in October 2024, when it moved to a new host account; Boss Rush Jam in
  January 2025; Brackeys in February 2025; Kenney Jam in July 2026. Bigmode and Pirate Software
  already banned AI in the earliest editions found (November 2023 and January 2024).
- **No series went from a ban back to allowing AI.** Once a rule appeared, it stayed or tightened:
  Godot Wild Jam named code by #70 (June 2024), SCREAM JAM went from "most" generative AI (2024, 2025)
  to "all" (2026), Pirate Software from "No AI-Generated Content" to "... of any kind" (2026), and
  Kenney Jam's first rule (2026) bans "AI assisted" code, art and audio. Pirate Software's 2025 and
  early-2026 pages simply have no AI sentence (the 2025 page has no rules section at all), and the ban
  returns in July 2026.
- **The two series that allow AI are run or sponsored by companies with AI products.** GitHub's Game
  Off said in 2023 that AI tools "to help generate code, assets, or anything in between" are "welcome",
  then dropped the sentence in 2024. Gamedev.js said nothing from 2023 to 2025 while giving GitHub
  Copilot licences as prizes, and in 2026 wrote "Use of AI is totally allowed, and even encouraged".
- GDevelop BIG Game Jam has no AI rule in any edition read (#5, #9, #10).

Limits: a jam page shows its text today, and hosts can edit pages after a jam, so an old page may
not show the rule exactly as it stood during the jam. Rules kept on separate pages, FAQs or Discord
are not covered. The 11 series were chosen as large, well-known recurring jams on itch.io, not
sampled at random, and the editions in between those listed were not read (for example Godot Wild
Jam #56 to #59), so an adoption date is "between the last edition without and the first with".
Pages were read on 14 October 2026 by an automated web reader that returned the AI-related sentences;
a "no rule" row means none was returned. Classes as below, plus `banned_most` (all generative AI
except models trained only on owned, licensed or opt-in data).

## The other side: jams that require AI (read 15 October 2026)

`data/ai-required-jams-2026-10-15.csv` lists **15 editions of 6 itch.io jams whose rules require AI**:
every one we could find by searching itch.io and the web for AI, AI-powered and vibe-coding jams.
`required` means the entrant must use generative AI (some set a share: "50% or more", "majority");
`required_tool` means the entrant must use the sponsor's AI product. Jams that only allow or
encourage AI are left out (for example Just Vibe It!, "Here, we encourage it"), and so is MuleRun's
jam, whose page links its rules elsewhere.

| series | host | editions | first edition | entries | cash prize |
|--------|------|-----:|------|-----:|------|
| AI Browser Game Jam | Focaccai | 5 | 2026-02 | 273 | no |
| Ultimate AI-Powered Game Jam | michyo | 5 | 2026-07 | 141 | no |
| Slapjam | slapjam | 2 | 2026-09 | 139 | cash |
| Vibe Summer Game Jam | MCheca; Haaaaaayden | 1 | 2026-08 | 34 | cash |
| Falling in Love with Vibe Coding | Makko AI | 1 | 2026-02 | 1 | store credit |
| The AI Game Jam | William | 1 | 2023-10 | 0 | no |

Entries are those of ended editions, as shown in each jam page's header.

What it shows:

- **AI-required jams are a 2026 phenomenon.** The only earlier one found (October 2023) received no
  entries. All 12 editions with entries started in 2026, and together they hold **588 games**.
- **They are growing, but from far behind.** The AI Browser Game Jam went from 29 entries (February)
  to 125 (August), 4.3 times as many, and its fifth edition had 177 people joined before it opened.
  Slapjam's first edition drew 139 entries in 48 hours. Still, the 11 large series above received
  14,814 games under an AI ban in 2026 alone: 25 times as many as every AI-required edition found.
- **Requiring AI rarely comes with money.** Only Slapjam and the Vibe Summer Game Jam offer cash, and
  the Vibe Summer prize is paid only if winners meet the hosts' quality bar. The two jams that require
  a sponsor's tool are, in effect, product promotions; the two largest series (Focaccai's and
  michyo's) are run by individuals with no prizes at all.
- **Hosts' own counts run higher than the page headers.** Where a host states its entry counts
  (the AI Browser Game Jam 5 page, the Slapjam #2 page), 4 of 5 are higher than the header now shows
  (429 against 412 in total). Entries removed after a jam would explain it; we use the header.

Limits: found by search, not drawn from a full list of itch.io jams, so smaller AI-required jams are
likely missing; the counts are a floor. One series (Ultimate AI-Powered) had its fifth edition still
in rating when read. Read through the same automated web reader as the history, so some quotes are
cut at its length limit (marked in `note`).

## Snapshot 1: 14 October 2026, pages 1 and 2

The two files cover **77 video-game jams** from the first two pages of
[itch.io's upcoming jams list](https://itch.io/jams/upcoming), read on the same day:

- `data/itch-jams-2026-10-14.csv`: 33 jams, every video-game jam on page 1 that we read (32), plus
  The WORST Game Jam, which was already running.
- `data/itch-jams-2026-10-14-page2.csv`: 44 jams, every video-game jam on page 2. Left out: a comic
  jam, a poetry jam, a 3D-modelling jam, a tabletop RPG jam, a mixed-media story jam and an adult jam.

Each row has the jam's link, how many had joined, its submission window, a policy class, the scope of
the rule, the sentence the class rests on, and whether there is a cash or cash-like prize. Page 1 holds
the most-joined jams (72 to 1,705 joined); page 2 the next ones (22 to 62).

| policy | meaning | page 1 jams | page 1 joined | page 2 jams | page 2 joined | all jams | all joined |
|--------|---------|-----:|-----:|-----:|-----:|-----:|-----:|
| banned_all | no generative AI at all (or "no AI-generated content") | 10 | 2147 | 13 | 506 | 23 | 2653 |
| banned_assets | AI-made art, audio or other media banned; code not mentioned or allowed | 8 | 2934 | 5 | 165 | 13 | 3099 |
| discouraged | hosts ask entrants not to use AI but do not ban it | 0 | 0 | 1 | 29 | 1 | 29 |
| allowed_disclose | AI-made work allowed if disclosed | 6 | 1907 | 7 | 236 | 13 | 2143 |
| allowed | AI-made work allowed, no disclosure rule | 0 | 0 | 3 | 138 | 3 | 138 |
| required | AI must be used | 1 | 165 | 2 | 50 | 3 | 215 |
| not_stated | no AI rule on the jam page (yet) | 8 | 2874 | 13 | 487 | 21 | 3361 |

What it shows:

- **Most jams that state a rule ban AI-made work.** 36 of the 56 jams with a rule (64%) ban AI-made
  assets in some form, and 23 of 56 (41%) ban generative AI entirely. 19 (34%) allow or require it.
  Weighted by people joined, the share banning AI-made assets is 69% (5,752 of 8,277).
- **The bigger jams ban more often.** On page 1, 18 of 25 rules (72%) are bans; on page 2, 18 of 31
  (58%). Two pages are not enough to call this a trend.
- **Bans reach code more often than snapshot 1 suggested.** On page 1 only 3 of 18 bans named code. On
  page 2, 7 of 18 do ("This includes coding", "No vibe code", "Code and assets generated by ... LLM"),
  so 10 of 36 overall. Three jams explicitly allow AI code while banning AI art or audio.
- **Jams with money behind them allow AI more often, but not significantly.** Of the 13 jams with a
  cash or gift-card prize that state a rule, 7 allow AI-made work and 6 ban it. Of the 43 others with a
  rule, 12 allow it (28%). Fisher's exact test, two-sided: p ≈ 0.10. Several of the allowing prize
  jams are sponsored by makers of AI tools (Slapjam, Micro Jam), which may explain part of the gap.
- **The largest prize found allows disclosed AI.** thatgamejam #02, run by thatgamecompany, offers
  USD 10,000 and says AI is allowed "but you must clearly disclose it in your game description".
  Zoud GameLab (up to $140k in prizes and funding) allows disclosed AI in its FAQ.
- **21 of 77 jams say nothing yet**, including several of the largest (Game Off, Brackeys, GDevelop
  BIG Game Jam). Some publish full rules only when the jam starts. (The history above shows Brackeys
  has banned AI-generated content in every edition since 2025, so its 2026-27 page will likely follow.)

## How it was made, and its limits

- Each jam page was read on 14 October 2026 (page 1 about 08:30 to 09:30 UTC, page 2 about 09:30 to
  10:30 UTC, the history about 10:30 to 11:30 UTC) through an automated web reader, which returned
  the AI-related sentences and prize text. The quotes are as returned; check a jam's page before
  relying on any single row. Quotes in Spanish and Portuguese are kept in the original, with a
  translation in `prize_notes`. The AI-required jams were read the same way on 15 October 2026,
  about 01:30 to 02:30 UTC.
- One reader per page, one classifier (the author): there is no second coder, so borderline rows
  (for example "No AI-Generated content", classed as banned_all, or a jam that allows AI content only
  if it is "completely obvious that it was made by AI", classed as allowed_disclose) are judgement
  calls. The scope column says what each rule covers in plain words.
- "Names code" is counted from the scope column: a ban whose scope mentions code, other than "code
  not mentioned" or "code allowed".
- Pages 1 and 2 only. Page 1 also skipped RPG Maker, 3x3x3, Grassroots, NovemBird, NO PASAJAM, DENPA,
  Comfy Jam and a Russian-language jam, which were not read in time. It is a snapshot, not a census,
  and jam pages change.
- Rules that live only in a jam's Discord are not covered (A Lil Horror GameJam keeps its rules there).
- The prize test is small (13 prize jams) and confounded by sponsors; treat it as a lead, not a finding.

The plan is to add a dated snapshot now and then so changes can be measured, starting with the jams
that had no rule yet.

## Use

```
python -m unittest -v
```

checks that the CSVs are well formed and recomputes every number above, including the Fisher test,
the history table and the AI-required table.

## Credit and licence

Made by MV2 of Munim, Inc. with AI agents (Anthropic Claude), who read the pages and classified the
rules. The data and this README are CC BY 4.0; the code is Apache-2.0 (see `LICENSE`). Jam rules
quoted here belong to their hosts and are quoted briefly for reference.
