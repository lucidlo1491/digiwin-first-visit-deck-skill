#!/usr/bin/env python3
"""Sighted-read attestation — makes "I looked at the PNGs" a checkable artifact.

WHY (Peter 2026-08-24, the Dai-Ichi v5 burn): the two-half design gate (mechanical
detectors + sighted critique, mandated 2026-07-01 after PLIC) failed the same way
twice in one morning — every machine gate was green while under-filled, white-on-white
and dead-space slides shipped, because the sighted half is the one step that is not a
script, so deadline pressure eats it first. "Just because I'm in a hurry doesn't mean
we should let the quality drop."

WHAT: stamping a slide records the SHA-256 of its rendered PNG in EVERY declared
language into `_qa/sighted_stamps.json`. `--check` (called by preflight as a BLOCKING
gate) fails if any slide is unstamped or any current PNG's hash differs from its
stamp — so any re-render that changes pixels silently invalidates the attestation and
deploy is blocked until someone looks again.

THE CONTRACT: stamping IS the attestation. Run `--stamp` ONLY for slides whose
current PNGs you (human or agent) have actually READ in every language listed —
composition, hierarchy, dead space, legibility at distance. Stamping unread slides
defeats the gate's purpose and recreates the burn this exists to prevent; the `--by`
note is recorded so the ledger shows who attested what, on what basis.

Usage:
  sighted_stamp.py <deck.html> --check
  sighted_stamp.py <deck.html> --stamp all|2,3,15 --by "who/what read them"
  sighted_stamp.py <deck.html> --status
"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

LANG_DIR = {"zh": "renders", "en": "renders-en", "th": "renders-th", "ja": "renders-ja"}

argv = sys.argv[1:]
if not argv or argv[0].startswith("--"):
    print(__doc__.strip().splitlines()[-4].strip())
    sys.exit(2)
DECK = Path(argv[0]).resolve()
if not DECK.exists():
    print(f"no such deck: {DECK}")
    sys.exit(2)
DDIR = DECK.parent
STAMPS = DDIR / "_qa" / "sighted_stamps.json"

html = DECK.read_text(encoding="utf-8")
m = re.search(r"<!--\s*LANGS:\s*([a-z,\s]+?)\s*-->", html)
langs = [x.strip() for x in m.group(1).split(",")] if m else ["zh", "en", "th"]
slide_ids = sorted(int(i) for i in re.findall(r'id="slide-(\d+)"', html))


def png(slide, lang):
    return DDIR / LANG_DIR.get(lang, f"renders-{lang}") / f"slide-{slide:02d}.png"


def current_hashes(slide):
    out = {}
    for lang in langs:
        p = png(slide, lang)
        if not p.exists():
            return None, f"S{slide} missing {p.parent.name}/{p.name} — render first"
        out[lang] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out, ""


def load():
    if STAMPS.exists():
        return json.loads(STAMPS.read_text(encoding="utf-8"))
    return {"slides": {}}


if "--stamp" in argv:
    which = argv[argv.index("--stamp") + 1]
    by = argv[argv.index("--by") + 1] if "--by" in argv else ""
    if not by.strip():
        print("REFUSED: --by is required — the stamp is an attestation; say who read the PNGs and on what basis.")
        sys.exit(2)
    targets = slide_ids if which == "all" else [int(x) for x in which.split(",")]
    data = load()
    for s in targets:
        if s not in slide_ids:
            print(f"REFUSED: slide {s} is not in this deck ({len(slide_ids)} slides)")
            sys.exit(2)
        hashes, err = current_hashes(s)
        if err:
            print(f"REFUSED: {err}")
            sys.exit(2)
        data["slides"][str(s)] = {"ts": int(time.time()), "by": by, "langs": langs, "hashes": hashes}
    STAMPS.parent.mkdir(exist_ok=True)
    STAMPS.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"stamped {len(targets)} slide(s) by: {by}")
    sys.exit(0)

if "--status" in argv or "--check" in argv:
    data = load()
    unstamped, stale, missing = [], [], []
    for s in slide_ids:
        rec = data["slides"].get(str(s))
        hashes, err = current_hashes(s)
        if err:
            missing.append(s)
            continue
        if not rec:
            unstamped.append(s)
            continue
        # a stamp must cover every currently-declared language and match every hash
        if any(rec.get("hashes", {}).get(l) != hashes[l] for l in langs):
            stale.append(s)
    ok = not (unstamped or stale or missing)
    if "--status" in argv:
        for s in slide_ids:
            rec = data["slides"].get(str(s), {})
            state = ("MISSING-PNG" if s in missing else "UNSTAMPED" if s in unstamped
                     else "STALE" if s in stale else "ok")
            print(f"  S{s:02d}  {state:<12} {rec.get('by','')[:70]}")
    if ok:
        print(f"sighted-stamp OK — {len(slide_ids)} slides attested against current renders ({','.join(langs)})")
        sys.exit(0)
    bits = []
    if missing:
        bits.append(f"missing PNGs {missing}")
    if unstamped:
        bits.append(f"UNSTAMPED {unstamped}")
    if stale:
        bits.append(f"STALE (renders changed since last read) {stale}")
    print("sighted-stamp BLOCK — " + "; ".join(bits) +
          " → READ those PNGs in every language, then sighted_stamp.py --stamp <ids> --by '...'")
    sys.exit(1)

print("one of --check / --stamp / --status required")
sys.exit(2)
