# Block library — pointer (lives in the shared design system)

The reusable slide-body **blocks** + the turnkey scaffold do NOT live in this skill — they live in the shared
deck design system so both deck skills and every deck consume ONE copy:

- **`docs/digiwin-2026-deck-design-system/system/blocks.css`** — the pre-corrected slide-body organisms (cards,
  team panel, squeeze, journey, snapshot, relationship scene, pain, peak, close, draft placeholder). Each block's
  header names the **rule/correction it bakes in**. Loaded after `slides.css`.
- **`docs/digiwin-2026-deck-design-system/BLOCKS.md`** — the catalog: block · use-when · the rule it bakes in ·
  gate guard · snippets · the **Mix & match** recipes (vary count/order/arc per company).
- **`docs/digiwin-2026-deck-design-system/_scaffold-firstvisit.html`** — a blank 15-slide arc wired to the blocks
  with `{{TOKEN}}`s + per-slide JOB comments. The build starting point.

## How to use (see SKILL.md build step C)
1. Copy `_scaffold-firstvisit.html` → `docs/<deck>/index-draft.html`.
2. **Reuse the blocks (look/craft); ADAPT the arc + content per company** — a block may appear 0/1/N times;
   add/remove/reorder slides (the gate is count-agnostic). The 15-slide arc is a DEFAULT, not a cage.
3. Fill every `{{TOKEN}}` from OSINT + Nova; copy real `assets/` in.
4. Run `scripts/slide_gate.py` (FAILS on any unfilled `{{token}}`) → render → READ → the sighted pass.

## The compounding rule
A new correction goes back into **`blocks.css`** (craft) or **`scripts/slide_gate.py`** (mechanical) — **never
forked into one deck**. A one-line deck-local *layout-arithmetic* tweak (e.g. a 4-column card grid) is fine; a
*craft* fix is not. This is what stops the per-company re-correction.

Related: [[acceptance-criteria.md]] (the measurable per-section bar) · [[nova-inquiry.md]] (the Nova packet).
