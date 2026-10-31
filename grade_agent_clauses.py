"""Grade PREREGISTRATION-agent-clauses.md from the reader's summary.json and the hand-code table (Apache-2.0).
By MV2 of Munim, Inc., made with AI agents (Anthropic Claude). Written before any data was collected.

    python grade_agent_clauses.py --summary out/summary.json [--hand hand_codes.csv] [--out grades.json]

hand_codes.csv has one row per jam that mentions agents: slug,hand_code,note where hand_code is one of
restrict (restricts AI agents as participants), allow (allows them) or tools (about agentic tools only).
A prediction whose inputs are missing is "not testable", never "holds".
"""
import argparse
import csv
import json
import sys

HAND_CODES = {"restrict", "allow", "tools"}
CORE = {"P1", "P2", "P7"}


def verdict(ok):
    return "not testable" if ok is None else ("holds" if ok else "fails")


def read_hand(path):
    codes = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row["hand_code"].strip().lower()
            if code not in HAND_CODES:
                raise ValueError("bad hand_code %r for %s" % (code, row["slug"]))
            codes[row["slug"].strip()] = code
    return codes


def grade(s, hand=None):
    n = s["jams_read"]
    agent, restrict, rest = s["mentions_agent"], s["agent_restrict"], s["agent_not_restrict"]
    ma, mo = s["median_joined_agent"], s["median_joined_other"]
    share_ai = s["mentions_ai_share"]
    g = {
        "P1": (agent / n < 0.05) if n else None,
        "P2": restrict >= 3,
        "P3": (restrict >= rest) if agent else None,
        "P4": (ma > mo) if ma is not None and mo is not None else None,
        "P5": (0.40 <= share_ai <= 0.75) if share_ai is not None else None,
        "P6": s["mentions_ilands"] >= 2,
        "P7": None,
    }
    p7 = {}
    auto = [j["slug"] for j in s["agent_jams"] if j["agent_restrict"]]
    if hand is not None:
        missing = [j["slug"] for j in s["agent_jams"] if j["slug"] not in hand]
        agree = sum(1 for slug in auto if hand.get(slug) == "restrict")
        p7 = {"auto_restrict": len(auto), "hand_restrict_of_auto": agree, "unhand_coded": missing,
              "hand_counts": {c: sum(1 for j in s["agent_jams"] if hand.get(j["slug"]) == c) for c in sorted(HAND_CODES)}}
        if auto and not missing:
            g["P7"] = agree / len(auto) >= 0.8
            p7["share"] = round(agree / len(auto), 4)
    out = {"predictions": {k: {"verdict": verdict(v), "core": k in CORE} for k, v in g.items()},
           "inputs": {"jams_read": n, "listed": s.get("listed"), "parsed_ok": s.get("parsed_ok"),
                      "reader_version": s.get("reader_version"), "mentions_agent": agent, "agent_restrict": restrict,
                      "agent_not_restrict": rest, "median_joined_agent": ma, "median_joined_other": mo,
                      "mentions_ai_share": share_ai, "mentions_ilands": s["mentions_ilands"]},
           "p7": p7}
    core = [out["predictions"][k]["verdict"] for k in sorted(CORE)]
    out["core_held"] = "%d of %d" % (core.count("holds"), len(core))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True)
    ap.add_argument("--hand", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    with open(a.summary, encoding="utf-8") as f:
        s = json.load(f)
    out = grade(s, read_hand(a.hand) if a.hand else None)
    text = json.dumps(out, indent=2, ensure_ascii=True)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
