#!/usr/bin/env python3
"""Impeccable design-quality gate — the STANDING step AFTER the DigiWin brand gate (slide_gate.py).

Peter 2026-07-01: the DigiWin brand gate proves a deck is ON-BRAND (tokens, icons, no-IoT, contact,
Tax-ID) — but "on-brand" and "well-designed" are different axes. The PLIC deck passed the brand gate
ALL-GREEN while carrying textbook AI-UI tells (side-tab accent stripes, a border-on-rounded card, and
content floating in dead space). So a second, design-quality gate is now standing.

This script is the MECHANICAL half. It runs Impeccable's deterministic detector (detect.mjs) and
partitions its findings:

  ADVISORY (known false-positives-BY-DESIGN on a DigiWin quad-lingual / navy deck — printed, never block):
    - numbered-section-markers  → the page numbers "NN / NN", not section scaffolding
    - dark-glow                 → the intentional brand-navy hero slides
    - em-dash-overuse           → legitimate CJK 破折號 in the zh/ja spans
                                  (⚠ still eyeball the EN/TH copy — that cadence IS a real tell there)
    - hero-eyebrow-chip /
      repeated-section-kickers  → the DigiWin brand eyebrow is a sanctioned design-system element;
                                  DESIGN.md wins over Impeccable's anti-eyebrow default.

  BLOCKING: EVERY other antipattern (side-tab, border-accent-on-rounded, nested-cards, gradient-text,
    gpt-thin-border-wide-shadow / glassmorphism, icon-tile-stack, low-contrast, tiny-text, text-overflow,
    cream-palette / ai-color-palette, marketing-buzzword, flat-type-hierarchy, ...). Unknown/new ids
    default to BLOCKING (fail-safe toward catching tells). Fix it — or, if it is genuinely a sanctioned
    brand choice, add its id to ADVISORY below WITH a one-line justification.

Exit 0 = no blocking hits (advisory may remain).  Exit 2 = blocking hits remain.

THIS IS ONLY THE MECHANICAL HALF. The sighted half — invoke the `impeccable` Skill's `critique`
(render every slide + READ the PNGs as a design director: hierarchy, dead-space, composition,
contrast at distance) — a detector CANNOT see composition or a slide floating in white. Both are
mandatory before deploy.
"""
import sys, os, subprocess, json, shutil

ADVISORY = {
    "numbered-section-markers",  # page numbers "NN / NN"
    "dark-glow",                 # brand-navy hero
    "em-dash-overuse",           # CJK 破折號 (still verify EN/TH manually)
    "hero-eyebrow-chip",         # DigiWin brand eyebrow — DESIGN.md-sanctioned
    "repeated-section-kickers",  # same brand eyebrow across slides
}


def _line(f):
    loc = f":{f['line']}" if f.get("line") else ""
    return f"  [{f.get('antipattern')}] {f.get('name', '')} — {str(f.get('snippet', ''))[:80]}{loc}"


def main():
    if len(sys.argv) < 2:
        print("usage: impeccable_gate.py <deck.html>")
        return 2
    deck = sys.argv[1]
    here = os.path.dirname(os.path.abspath(__file__))
    detect = os.path.normpath(os.path.join(here, "..", "..", "impeccable", "scripts", "detect.mjs"))
    node = shutil.which("node")
    if not node or not os.path.exists(detect):
        print(f"⚠ Impeccable detector unavailable (node={bool(node)}, detect exists={os.path.exists(detect)}) "
              f"— mechanical design-quality gate SKIPPED. Still run /impeccable critique manually.")
        return 0
    try:
        r = subprocess.run([node, detect, "--json", deck], capture_output=True, text=True, timeout=180)
    except Exception as e:  # noqa: BLE001
        print(f"⚠ detector run failed ({e}) — gate SKIPPED; run /impeccable critique manually.")
        return 0
    out = (r.stdout or "").strip()
    try:
        findings = json.loads(out) if out.startswith("[") else []
    except json.JSONDecodeError:
        findings = []
    blocking = [f for f in findings if f.get("antipattern") not in ADVISORY]
    advisory = [f for f in findings if f.get("antipattern") in ADVISORY]
    if advisory:
        print("ADVISORY (known DigiWin-deck false-positives — verify, do NOT block):")
        for f in advisory:
            print(_line(f))
        print()
    if blocking:
        print("✗ BLOCKING design-quality antipatterns (fix, or justify into ADVISORY):")
        for f in blocking:
            print(_line(f))
        print(f"\nGATE FAILED — {len(blocking)} blocking. Fix them and re-run. "
              f"THEN the sighted /impeccable critique (render + READ) before deploy.")
        return 2
    print("✓ Impeccable mechanical gate PASS — no blocking antipatterns.")
    print("  NEXT (mandatory): invoke the impeccable Skill → critique (render every slide + READ the PNGs "
          "as a design director) before deploy. The detector cannot see composition / dead-space / hierarchy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
