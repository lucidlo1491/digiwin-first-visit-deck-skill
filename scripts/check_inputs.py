# -*- coding: utf-8 -*-
"""Verify the deck's inputs EXIST before building. Do not take my word for it.

    python3 .claude/skills/digiwin-first-visit-deck/scripts/check_inputs.py <company-id> ["<company name>"]

WHY THIS EXISTS
    Every other gate in this skill is machine-enforced. Gate 0's "OSINT dossier
    promoted" was not — it was an ATTESTATION I wrote in design-shopping.md.
    That is the weakest link in a skill built precisely because my word was not
    good enough (Peter, 2026-08-31).

Checks:
  1 the gold-standard dossier exists and is promoted (not still a draft)
  2 it is not STALER than the most recent recorded meeting for that company
  3 the prior-contact probe verdict — COLD or RECORDED — so Gate 0 takes the
    right path and a transcript is never silently ignored
  4 an industry brief exists for reuse, or is flagged as needed

Exit 1 if the deck must not be built yet.
"""
import glob
import os
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
if not (REPO / "docs").exists():
    REPO = pathlib.Path("/Users/peterlo/digiwin_automation")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cid = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else cid.replace("-", " ")
    fails, notes = [], []

    dossier = REPO / "docs" / f"gold-standard-{cid}.md"
    draft = REPO / "docs" / "_eval" / f"gold-standard-{cid}.md.draft"
    if dossier.exists():
        notes.append(f"dossier promoted: {dossier.name}")
    elif draft.exists():
        fails.append(f"dossier is still a DRAFT ({draft.name}) — promote it before building")
    else:
        fails.append(f"NO dossier for '{cid}' — run /digiwin-research-company first")

    probe = subprocess.run([sys.executable, str(REPO / "tools" / "prior_contact.py"), name],
                           capture_output=True, text=True)
    out = probe.stdout
    recorded = "VERDICT: RECORDED" in out
    if recorded:
        notes.append("prior contact RECORDED — Gate 0 takes the RECORDED path; read the transcript")
        # staleness: dossier must be newer than the newest meeting file it should reflect
        if dossier.exists():
            dmtime = dossier.stat().st_mtime
            newer = []
            for m in re.findall(r"transcript: (\S+)", out) + re.findall(r"^\s+(/\S+\.md)$", out, re.M):
                if os.path.exists(m) and os.path.getmtime(m) > dmtime:
                    newer.append(m)
            if newer:
                fails.append(f"dossier is OLDER than {len(newer)} meeting record(s) — "
                             f"run --reconcile first: {newer[0]}")
    else:
        notes.append("prior contact COLD — Gate 0 takes the COLD path; the deck must EARN his framing")

    briefs = glob.glob(str(REPO / "docs" / "industry-briefs" / "*.md"))
    briefs = [b for b in briefs if "INDEX" not in b]
    notes.append(f"industry briefs available for reuse: {len(briefs)}"
                 if briefs else "no industry brief yet — run the sweep (research owns it)")

    print(f"\nDECK INPUT CHECK — {cid}\n" + "=" * 66)
    for n in notes:
        print(f"  [ok]   {n}")
    for f in fails:
        print(f"  [FAIL] {f}")
    print("=" * 66)
    print("INPUTS: " + ("READY" if not fails else f"NOT READY ({len(fails)})"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
