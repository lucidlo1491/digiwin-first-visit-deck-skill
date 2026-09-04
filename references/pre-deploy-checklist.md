# THE Pre-Deploy Checklist (deck) — one gate, everything checked, THEN deploy

> Mandated by Peter 2026-07-25 after the **Asia Polysacks "this looks hideous" burn**: every mechanical
> gate was green, so I called it done and deployed — but `VALIDATION.md` was only 3/15, no language was
> ever rendered, and the `digiwin` MCP was never shopped. Green mechanical ≠ good. This is the single
> ordered definition-of-done. **Deploy is physically blocked** (`build_portable.py` refuses) until the
> machine floor passes; the sighted ceiling is your commitment on top.

`scripts/preflight.py <deck/index.html>` runs and STAMPS the machine floor (Gates 1/3/4-evidence). It
writes `_qa/preflight.json`; `build_portable.py` refuses to build unless that stamp is `ok:true` and its
hash matches the exact `index.html` being shipped. Emergency bypass = `build_portable.py --force` (loud,
logged — never routine).

---

## Gate 0 — Inputs current *(before you build; not machine-checked — attest in `_qa/design-shopping.md`)*
- [ ] **VP methodology/coaching current** — check `~/Peter/Internal/VP Cheng - Sales Methodology.md` mtime; newest coaching folded in. *(This is why: on 2026-07-25 a 7/24 人機料法環 Pass-2 update existed that a 7/23-based build would have missed.)*
- [ ] **NOVA live consulted** for the deck's framing / pain / close decisions — verbatim captured in `docs/<deck>/nova-live-<date>.md`.
- [ ] **OSINT dossier promoted**; every argument-slide fact traced to a tagged source.

## Gate 1 — Design SOURCED, not improvised *(machine: `_qa/design-shopping.md` must exist + name the MCP calls)*
- [ ] `digiwin` MCP shopped: `search`/`get_component` for each organism · **`find_icon` for EVERY icon** · `get_token` for color/type · `get_guideline('deck-layout')` before composing.
- [ ] **Zero hand-drawn icons, zero invented hex.** Log the component / icon / token IDs used in `_qa/design-shopping.md` (this file IS the machine evidence).

## Gate 2 — Content-first spec approved *(not machine-checked — your record)*
- [ ] C1 content pack → C2 SPEC + `specs/NN-*.md` → **C3 Peter approved as TEXT.** No HTML before C3.

## Gate 3 — Mechanical, all green *(machine)*
- [ ] `slide_gate.py --report` ALL GREEN (`sdd-match`, `no-pricing`, `no-IoT`, `hedged`, `tax-id`, `contact+QR`, `reskin-suspect`/FRESH, `pain-argues`, `notes-thorough`).
- [ ] `lang_purity.py` · `overlap_check.py` · `svg_fit_check.py` · `impeccable_gate.py` all exit 0.
- [ ] **`VALIDATION.md` reads N/N** — every slide fully validated, *including its sighted-audit ledger row*. (3/15 is the tell that the READ never happened.)

## Gate 4 — Sighted craft READ *(machine forces the evidence to EXIST; YOU do the reading)*
- [ ] `render_trilingual.py` + `render_pdf.py` produced **fresh PNGs for EVERY declared language** (zh/en/th[/ja]) — preflight verifies each `renders*/slide-NN.png` exists, is newer than the deck, and isn't blank.
- [ ] **READ every one** — not just English. Per slide check: no sliver/clipped photo · no jagged giant-CJK/Thai · **no English legend inside a localized slide** · visual-serves-message passes · swap-test FAILS on S5–15.
- [ ] Log a one-line verdict per slide (keep/fix) — the machine can't see "sliver photo"; you must.

## Gate 5 — Show Peter, get the word *(not machine-blocked in this tier — still the norm)*
- [ ] ONE consolidated packet to Peter: all-language PNGs + `VALIDATION.md` + `design-shopping.md`. **Deploy only on Peter's "promote/deploy."**

## Gate 6 — Ship mechanics
- [ ] `build_portable.py` (gate passes → GUARD self-contained) → `vercel --prod` → **read the live URL** → `register_deck.py` → add the `presentations_map.json` bookmark line.

---

**The one rule that closes the hole:** *`build_portable.py` does not run until `preflight.py` has stamped
`ok:true` for this exact `index.html`.* The machine can't judge beauty — but it can refuse to ship a deck
whose all-language renders were never produced and whose validation ledger is half-empty. That is the floor
the Asia Polysacks deck failed, invisibly, before this existed.
