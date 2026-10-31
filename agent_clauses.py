"""Agent-entrant clauses on itch.io jam pages: which open and upcoming jams say anything about AI agents taking
part, and what (Apache-2.0). By MV2 of Munim, Inc., made with AI agents (Anthropic Claude).

    python agent_clauses.py --out /out [--delay 2.0] [--max-pages 20] [--raw-dir DIR]

Reads only public pages that itch.io's robots.txt allows (/jams/in-progress, /jams/upcoming and each /jam/<slug>
main page), one request every --delay seconds, with a User-Agent that names MV2 and his email. Saves every page it
read under out/raw/ so the parse can be redone offline (--raw-dir reuses them without any network).

Writes jams.csv (one row per jam: listing, joined, whether the page mentions AI at all, whether it mentions AI
agents, the automated restrict code, and the matching sentences) and summary.json (the counts that
PREREGISTRATION-agent-clauses.md grades). Only jam pages are read; no entry, author or user data is collected.
Sentences that appear on more than --chrome-share of all jam pages are treated as site chrome and ignored.

Reader version 0.2 (2026-10-31): page title, navigation, header and footer text now end a line, so the title no
longer runs into the site's menu text and site chrome is recognised. Fixed before any data was collected.
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

VERSION = "0.2"
BASE = "https://itch.io"
UA = "MV2-Munim-agent-clauses/%s (MV2 of Munim, Inc.; mv2@munimtech.com)" % VERSION
LISTINGS = ["in-progress", "upcoming"]
NOT_JAMS = {"new", "created", "joined", "ending", "starting", "upcoming", "in-progress", "past", "featured"}

# AI agents as actors (entrants, accounts, bots), not AI as a tool. Case-insensitive except bare "AI".
AGENT = re.compile(r"\b(?:AI|A\.I\.|LLM)[- ]?(?:powered |driven |based )?[Aa]gents?\b"
                   r"|(?i:\bautonomous (?:AI )?(?:agents?|bots?)\b|\bilands\b|\bagentic\b"
                   r"|\bbot accounts?\b|\bAI (?:accounts?|bots?|entrants?|participants?)\b)")
AI_ANY = re.compile(r"\b(?:AI|GenAI|Gen-AI|LLMs?|ChatGPT|Midjourney|Copilot|Claude|Stable Diffusion)\b|\bA\.I\."
                    r"|(?i:\bgenerative\b|\bartificial intelligence\b|\bmachine[- ]generated\b)")
RESTRICT = re.compile(r"(?i)\b(?:not|no|ban|bans|banned|prohibit\w*|forbid\w*|disallow\w*|disqualif\w*|"
                      r"remove|removed|won't|isn't|aren't|cannot|can't|never|only humans?|human[- ]made only)\b")
# Closing tags that end a line of visible text.
BLOCK_END = re.compile(r"(?i)<br\s*/?>|</(?:p|div|tr|li|h\d|table|section|dt|dd|td|th|title|nav|header|footer"
                       r"|aside|article|main|ul|ol|form|blockquote|pre)>")


def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                break
            time.sleep(20 * (i + 1) if e.code == 429 else 5 * (i + 1))
        except Exception as e:  # retry, then give up loudly
            last = e
            time.sleep(5 * (i + 1))
    raise last


def to_text(h):
    """Visible text with one line per block."""
    h = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", h)
    h = re.sub(r"\s+", " ", h)
    h = BLOCK_END.sub("\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h)
    lines = [re.sub(r"[ \t\u00a0]+", " ", ln).strip() for ln in h.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def sentences(text):
    """Lines split further at sentence ends; short fragments kept (rules are often bullet points)."""
    out = []
    for ln in text.split("\n"):
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", ln) if s.strip()]
    return out


def jam_slugs(page_html):
    """Jam slugs linked from a listing page, in page order, without repeats."""
    slugs = re.findall(r'href="(?:https://itch\.io)?/jam/([A-Za-z0-9_-]+)"', page_html)
    return [s for s in dict.fromkeys(slugs) if s not in NOT_JAMS]


def page_total(page_html):
    m = re.search(r"Page\s+\d+\s+of\s+(\d+)", to_text(page_html))
    if m:
        return int(m.group(1))
    nums = [int(n) for n in re.findall(r"[?&]page=(\d+)", page_html)]
    return max(nums) if nums else 1


def count_before(text, label):
    m = re.search(r"([\d,]+)\s+%s\b" % label, " ".join(text.split()))
    return int(m.group(1).replace(",", "")) if m else None


def parse_jam(page_html):
    text = to_text(page_html)
    m = re.search(r"(?is)<title>(.*?)</title>", page_html)
    title = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""
    title = re.sub(r"\s*-\s*itch\.io$", "", title)
    return {"title": title, "joined": count_before(text, "Joined"),
            "entries": count_before(text, "(?:Entries|Submissions)"), "sentences": sentences(text)}


def code_jam(sents, chrome):
    """Automated codes for one jam from its non-chrome sentences."""
    own = [s for s in sents if s not in chrome]
    ai = [s for s in own if AI_ANY.search(s)]
    agent = [s for s in own if AGENT.search(s)]
    restrict = [s for s in agent if RESTRICT.search(s)]
    return {"mentions_ai": bool(ai), "mentions_agent": bool(agent), "agent_restrict": bool(restrict),
            "agent_terms": sorted({m.group(0).lower() for s in agent for m in AGENT.finditer(s)}),
            "agent_sentences": [s[:400] for s in agent]}


def chrome_sentences(all_sents, share):
    """Sentences on more than `share` of pages (and on at least 3) are site chrome, not jam rules."""
    n = len(all_sents)
    seen = {}
    for sents in all_sents:
        for s in set(sents):
            seen[s] = seen.get(s, 0) + 1
    return {s for s, c in seen.items() if c >= 3 and c > share * n}


def median(xs):
    s = sorted(xs)
    if not s:
        return None
    k = len(s) // 2
    return s[k] if len(s) % 2 else (s[k - 1] + s[k]) / 2


def summarize(rows):
    n = len(rows)
    agent = [r for r in rows if r["mentions_agent"]]
    restrict = [r for r in agent if r["agent_restrict"]]
    j_agent = [r["joined"] for r in agent if r["joined"] is not None]
    j_rest = [r["joined"] for r in rows if not r["mentions_agent"] and r["joined"] is not None]
    return {"jams_read": n,
            "by_listing": {l: sum(1 for r in rows if r["listing"] == l) for l in LISTINGS},
            "mentions_ai": sum(r["mentions_ai"] for r in rows),
            "mentions_ai_share": round(sum(r["mentions_ai"] for r in rows) / n, 4) if n else None,
            "mentions_agent": len(agent),
            "mentions_agent_share": round(len(agent) / n, 4) if n else None,
            "agent_restrict": len(restrict),
            "agent_not_restrict": len(agent) - len(restrict),
            "median_joined_agent": median(j_agent),
            "median_joined_other": median(j_rest),
            "mentions_ilands": sum(1 for r in agent if "ilands" in r["agent_terms"]),
            "agent_jams": [{"slug": r["slug"], "title": r["title"], "listing": r["listing"], "joined": r["joined"],
                            "agent_restrict": r["agent_restrict"], "agent_terms": r["agent_terms"],
                            "agent_sentences": r["agent_sentences"]} for r in agent]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--delay", type=float, default=2.0)
    ap.add_argument("--max-pages", type=int, default=20)
    ap.add_argument("--chrome-share", type=float, default=0.2)
    ap.add_argument("--raw-dir", default="", help="reuse pages saved by an earlier run (no network)")
    a = ap.parse_args()
    raw = os.path.join(a.out, "raw")
    os.makedirs(raw, exist_ok=True)
    problems = []

    def page(name, url):
        if a.raw_dir:
            p = os.path.join(a.raw_dir, name)
            if not os.path.exists(p):
                return ""
            with open(p, encoding="utf-8") as f:
                return f.read()
        h = fetch(url)
        with open(os.path.join(raw, name), "w", encoding="utf-8") as f:
            f.write(h)
        time.sleep(a.delay)
        return h

    listed = {}
    for listing in LISTINGS:
        first = page("list-%s-1.html" % listing, "%s/jams/%s" % (BASE, listing))
        total = min(page_total(first), a.max_pages)
        found = jam_slugs(first)
        for k in range(2, total + 1):
            try:
                found += jam_slugs(page("list-%s-%d.html" % (listing, k), "%s/jams/%s?page=%d" % (BASE, listing, k)))
            except Exception as e:
                problems.append("list %s %d: %r" % (listing, k, e))
        for s in found:
            listed.setdefault(s, listing)
        print("%s: %d pages, %d jams" % (listing, total, len(found)), flush=True)

    parsed = []
    for k, (slug, listing) in enumerate(listed.items()):
        try:
            h = page("jam-%s.html" % slug, "%s/jam/%s" % (BASE, slug))
        except Exception as e:
            problems.append("jam %s: %r" % (slug, e))
            continue
        if not h:
            problems.append("jam %s: empty" % slug)
            continue
        row = parse_jam(h)
        row.update({"slug": slug, "listing": listing})
        parsed.append(row)
        if k % 50 == 0:
            print("read %d/%d" % (k + 1, len(listed)), flush=True)

    chrome = chrome_sentences([r["sentences"] for r in parsed], a.chrome_share)
    rows = []
    for r in parsed:
        rows.append({**{k: r[k] for k in ("slug", "title", "listing", "joined", "entries")},
                     **code_jam(r["sentences"], chrome)})

    cols = ["slug", "title", "listing", "joined", "entries", "mentions_ai", "mentions_agent", "agent_restrict",
            "agent_terms", "agent_sentences"]
    with open(os.path.join(a.out, "jams.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([json.dumps(r[c], ensure_ascii=False) if c in ("agent_terms", "agent_sentences")
                        else r[c] for c in cols])
    summary = summarize(rows)
    summary.update({"reader_version": VERSION, "listed": len(listed), "chrome_sentences": sorted(chrome)[:200],
                    "problems": problems, "parsed_ok": len(rows) >= 0.95 * len(listed) > 0})
    with open(os.path.join(a.out, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("agent_jams", "chrome_sentences")},
                     indent=2, ensure_ascii=True))
    sys.exit(0 if summary["parsed_ok"] else 1)


if __name__ == "__main__":
    main()
