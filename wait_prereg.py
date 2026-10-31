"""Wait until the pre-registration is public on GitHub with the expected reader version (Apache-2.0).

    python wait_prereg.py --url URL --marker TEXT [--minutes 120]

Exits 0 once the file at URL contains TEXT, 1 if it never does. The data job runs only after this succeeds,
so no jam page is read before the predictions are public.
"""
import argparse
import sys
import time
import urllib.request

UA = "MV2-Munim-agent-clauses/0.2 (MV2 of Munim, Inc.; mv2@munimtech.com)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--marker", required=True)
    ap.add_argument("--minutes", type=float, default=120)
    a = ap.parse_args()
    end = time.time() + a.minutes * 60
    while True:
        try:
            req = urllib.request.Request(a.url + "?t=%d" % time.time(), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", "replace")
            if a.marker in body:
                print("prereg public with %r" % a.marker, flush=True)
                return 0
            print("prereg found without marker; waiting", flush=True)
        except Exception as e:
            print("not yet: %r" % e, flush=True)
        if time.time() > end:
            print("gave up: prereg never appeared", flush=True)
            return 1
        time.sleep(120)


if __name__ == "__main__":
    sys.exit(main())
