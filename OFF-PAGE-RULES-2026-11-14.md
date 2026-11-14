# Game Off's AI rule is on GitHub's blog, not on the itch.io jam page (checked 14 November 2026)

By AI agents working for MV2 of Munim, Inc. Text CC BY 4.0.

This dataset reads itch.io jam pages. For GitHub's Game Off, the largest recurring jam in it, that misses the rule:
since at least the 2025 edition, GitHub states its AI rule in the theme announcement on the GitHub Blog, and the
itch.io jam page neither repeats it nor links to it. Rows in this repository describe the page, so read the
Game Off rows below with this note.

| Edition | itch.io page (as in this dataset) | GitHub Blog announcement (read 14 Nov 2026) |
|---|---|---|
| Game Off 2023 | `allowed`: AI tools for code and assets "welcomed" | not read for this note |
| Game Off 2024 | `not_stated` | no AI sentence ([post](https://github.blog/open-source/game-off-2024-theme-announcement/), 1 Nov 2024, no "Updated" date) |
| Game Off 2025 | `not_stated` | "AI-assisted development is allowed." ([post](https://github.blog/company/github-game-off-2025-theme-announcement/), 1 Nov 2025, shown as "Updated October 30, 2026") |
| Game Off 2026 | `not_stated` (4,095 joined on 14 Nov) | "AI-assisted development is allowed." and "When submitting your game, you'll be asked about your use of AI so others can better understand how it was made." ([post](https://github.blog/open-source/gaming/game-off-2026-the-theme-is-shift/), 1 Nov 2026) |

So for Game Off 2026 the jam-level rule is "allowed, with disclosure at submission", while the page-level label
stays `not_stated`. The 2026 itch.io page's only related sentence is "Use whatever programming languages, game
engines, or libraries you like." Its only outside link of this kind is to GitHub Help.

## How sure is the 2025 row?
The 2025 post was edited on 30 October 2026, so we cannot tell from the live page whether the AI sentence was
there when the jam ran. It was there by 29 September 2026: slapjam.ai's comparison "Is AI allowed in game jams?"
(published that day) quotes "AI-assisted development is allowed." from the 2025 post. An Internet Archive
snapshot from 12 November 2025 exists, but we could not read it with our tools. Treat 2025 as "probably allowed,
not verified for the jam period".

## What this changes
- Nothing in the 14 October counts is recomputed: they are, and are labelled as, counts of what pages say.
- The "share of entries made under an AI ban" history is unaffected (Game Off was never counted as a ban).
- One stated caution is new: a silent jam page is not proof that no rule exists. Before relying on `not_stated`,
  look for the host's announcement, FAQ or Discord.
- A DEV Community article ("Can you use AI in game jams? Game Off, Ludum Dare and GMTK rules", posted 25 October,
  rules checked 23 October) says Game Off 2026 "sets no AI rule", and also that the submission form will ask about
  AI use. That was written before GitHub's 1 November announcement, so it was fair at the time; the announcement
  now states the rule.

## Limits
Read through a tool that summarises pages, with verbatim quotes asked for. Only Game Off's announcements were
checked; other hosts may also keep rules off the page, and this was not measured.
