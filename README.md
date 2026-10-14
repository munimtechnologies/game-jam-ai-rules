# game-jam-ai-rules

An open, quote-backed dataset of what itch.io game jams say about AI-made work, by MV2 of Munim, Inc.

itch.io lets every jam host write their own rules, and many now say something about generative AI.
We could not find any published dataset of those rules: the closest prior art is
[a browser extension](https://mrgabas.itch.io/itchio-jam-ai-policy-filter) that classifies a jam's
page automatically when you open it, and forum threads that quote a few jams. This repository records
the rule for each jam with the sentence it comes from, so anyone can check it and count.

## Snapshot 1: 14 October 2026

`data/itch-jams-2026-10-14.csv` covers **33 video-game jams**: every video-game jam on page 1 of
[itch.io's upcoming jams list](https://itch.io/jams/upcoming) that we read that day (32), plus The
WORST Game Jam, which was already running. Each row has the jam's link, how many had
joined, its submission window, a policy class, the scope of the rule, the sentence the class rests
on, and whether there is a cash or cash-like prize.

| policy | meaning | jams | joined |
|--------|---------|-----:|-------:|
| banned_all | no generative AI at all (or "no AI-generated content") | 10 | 2147 |
| banned_assets | AI-made art, audio or other media banned; code not mentioned or allowed | 8 | 2934 |
| allowed_disclose | AI-made work allowed if disclosed | 6 | 1907 |
| required | most of the game must be AI-made | 1 | 165 |
| not_stated | no AI rule on the jam page (yet) | 8 | 2874 |

What the snapshot shows:

- **Most jams that state a rule ban AI-made work.** 18 of the 25 jams with a rule (72%) ban AI-made
  assets in some form, and 10 of 25 (40%) ban generative AI entirely. Weighted by people joined, the
  share banning AI-made assets is 71% (5,081 of 7,153).
- **Art and audio are where most hosts draw the line, not code.** 8 of the 18 bans cover only art,
  audio or other media. Only three rules mention code at all in a ban (Godot Wild Jam: "no vibe
  code"; Historically Accurate Game Jam: "generating assets and code"; SMALL SCOPE JAM: "no full
  AI-generated code"), and one host (Synty) explicitly allows AI code tools while banning AI assets.
- **Openly welcoming jams are few.** 6 allow AI-made work with disclosure (one of them, the 20 Second
  Game Jam, adds that it would rather see human-made games) and 1 requires it.
- **Jams with money behind them are split.** Of the 5 jams with a cash or gift-card prize, 2 ban
  generative AI entirely (Pixel Forge MEGA JAM, Bad Plan Horror Jam), 2 allow it with disclosure (The
  WORST Game Jam, Spooky 2D Jam '26) and 1 states no rule for its game track (Bezi Jam 14, run by an
  AI tools company, whose fan-art track bans AI art). Zoud GameLab (up to $140k in prizes and funding)
  allows disclosed AI in its FAQ.
- **8 of 33 jams say nothing yet**, including several of the largest (Game Off, Brackeys, GDevelop
  BIG Game Jam). Some publish full rules only when the jam starts.

## How it was made, and its limits

- Each jam page was read on 14 October 2026 (about 08:30 to 09:30 UTC) through an automated web
  reader, which returned the AI-related sentences and prize text. The quotes are as returned; check a
  jam's page before relying on any single row.
- One reader per page, one classifier (the author): there is no second coder, so borderline rows
  (for example "No AI-Generated content", classed as banned_all) are judgement calls. The scope
  column says what each rule covers in plain words.
- Page 1 of the upcoming list only; comic, music and tabletop jams were left out, and so were
  RPG Maker, 3x3x3, Grassroots, NovemBird, NO PASAJAM, DENPA, Comfy Jam and a Russian-language jam
  on the same page, which were not read in time. It is a snapshot, not a census, and jam pages change.
- Rules that live only in a jam's Discord are not covered (A Lil Horror GameJam keeps its rules there).

The plan is to add a dated snapshot now and then so the trend can be measured.

## Use

```
python -m unittest -v
```

checks that the CSV is well formed and that the counts above match it.

## Credit and licence

Made by MV2 of Munim, Inc. with AI agents (Anthropic Claude), who read the pages and classified the
rules. The data and this README are CC BY 4.0; the code is Apache-2.0 (see `LICENSE`). Jam rules
quoted here belong to their hosts and are quoted briefly for reference.
