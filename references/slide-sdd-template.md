# Slide SDD — `docs/<deck>/SPEC.md` + `docs/<deck>/specs/NN-<name>.md`  (C2 · how each slide is built)

> **What this is.** The specification-driven documentation tier (Peter, 2026-07-13):
> AFTER the content pack (C1) is prepped, each slide gets a FULL build spec — Tatung-style
> (`docs/tatung-thailand-firstvisit/specs/` is the worked precedent; `docs/sats-firstvisit/specs/`
> is the current reference implementation). The build (D) may ONLY follow these specs;
> `slide_gate.py`'s `sdd-match` check refuses a deck whose slides lack one or drift from one.
>
> **Why gate-enforced.** Tatung had this tier and it decayed — King Pac/Everydayhappy shipped
> with no specs because nothing forced them and composing from blocks felt faster. The specs
> are only real if the gate makes them load-bearing.

## Tier 1 — `SPEC.md` (the whole-deck arc; what Peter reads at C3 alongside the content pack)

```markdown
# SPEC — <Company> first-visit deck
> Locked decisions (from Nova, dated): core question · pain order · close ask · template A/B/C/D
> Languages: zh, en, th[, ja + the trigger fact]

## Arc (the story thread — every slide's exit feeds the next slide's entry)
| # | slide | the ONE thing it does | act | exit → next entry | source fact |
|---|-------|----------------------|-----|-------------------|-------------|
(one row per slide; the story-thread column is the cohesion check — a slide whose exit
doesn't set up the next slide's entry is a broken thread, fix the arc not the slide)

## Must-NOT list (deck-level)
(no pricing · pains hedged · no IoT/即時 framing · no client financials · cross-strait · …)
```

## Tier 2 — `specs/NN-<name>.md` (FULL per-slide spec, ~100 lines; Peter's depth decision 2026-07-13)

Field sections, in order (all required; write "NONE, and why" rather than omitting):

```markdown
# Slide NN — <name>   [NEW | DOCUMENT-EXISTING]

## Arc answers
(REQUIRED FIRST, gate-enforced — Peter 2026-07-25. Answer this slot's question set from
references/arc-questions.md, one line per question: `Qx.y → <answer> → 【source-tag】`.
An honest "unknown - must learn in the meeting" is valid and routes to presenter notes;
a blank or {{placeholder}} fails `slide_gate.py sdd-match`. No answers = this slide may
not be generated.)
- Q<slot>.1 → <answer> → 【source】
- Q<slot>.2 → <answer> → 【source】
- ...

- **Act / role**
  Narrative position, emotional job, what this slide must NOT contain. How it picks up
  the previous slide's exit and hands off to the next (the SPEC.md thread, elaborated).

- **The ONE message (frozen, verbatim)**
  The exact copy from content-<company>.md §S<NN> in every shipping language — quoted,
  not paraphrased. Plus the per-zone LENGTH BUDGETS (see multiplier table below).

- **Source fact**
  The OSINT/Nova line (tagged) this slide is grounded in — copied from the content pack.
  ⚠ gate-checked non-empty. This replaces the vibes version of the specificity gate.

- **Illustrative SCENE**
  The visual that ACTS OUT the message: hero element, build states, semantic encoding
  (coral=pain, blue=reference/solution, navy=hero; dim=grayscale not faded), background
  motifs. THE METAPHOR CONTRACT: which mechanism of THIS company's pain the SHAPE encodes
  — designed fresh, never a reskin of the prior deck's organism (the King Pac burn).
  A typographic slide states so explicitly (a peak question slide is deliberately icon-free).

- **Warehouse parts**
  Block + variant (e.g. `.pq` chart-left — layout is a BLOCK CHOICE, never freeform;
  wanting a new arrangement = add a block/variant to blocks.css so every deck inherits it),
  find_icon ids (or "NONE, and why"), semantic tokens (no raw hex), grid spans
  (12-col / 128px margin / 16px gutter math).

- **Visual routing**
  TYPE (data | illustration | diagram | photo | logo | icon | typographic) →
  ENGINE (gen_chart <spec.json> | gen_image "<prompt>" | find_icon <id> | source <URL/Drive>
  | inline-svg | n/a) → OUTPUT file in assets/. ⚠ gate-checked: declared files must exist.
  DATA visuals name the exact JSON from the content pack's Data field.

- **Layout**
  ONE primary block; which copy lands in which zone; the 1–3 `.em`/`.hl` emphasis phrases;
  8-pt vertical rhythm values; 888px height budget; chrome zones clear; `.nw` no-break
  segments for CJK phrases that must not split.

- **Gate criteria**
  What THIS slide's render-READ must verify beyond the global gates (e.g. "hedge line
  visible in all languages", "fan-out shape readable at glance", "stat-row clear of footer
  in th/ja"). These become the slide's row in the sighted audit ledger.
```

## Length-budget multipliers (from the block geometry; measured on shipped decks)

| zone | zh budget | en | th | ja |
|---|---|---|---|---|
| headline (`.slide-title`) | set per block, typ. ≤16ch | ≤1.4× zh | ≤1.5× zh | ≤1.1× zh |
| lead (`p.lead`, 32px) | ≤40ch/line, ≤2 lines | ≤1.4× | ≤1.5× | ≤1.1× |
| card title / chip | ≤10ch | ≤1.5× | ≤1.6× | ≤1.2× |
| bigq question (`.bigq .q`) | ≤3 deliberate line-breaks | fills ≤8 lines | ≤6 lines | ≤7 lines |

(EN/TH routinely run 1.3–1.5× zh — the S6 footer-overflow class. Copy is written TO these
budgets at C1; a budget violation found at build time is a CONTENT bug, fix the copy not
the layout.)

## Process notes

- Specs are AUTHORED BY THE MODEL (full depth is cheap for me, expensive for Peter);
  Peter's C3 reading = content pack + SPEC.md arc; spec files are for spot-checks.
- `sdd-match` (mechanical): per slide — `specs/NN-*.md` exists · its declared block class
  appears in that slide's HTML · declared engine outputs exist in assets/ · Source fact
  non-empty. Spec QUALITY (does the scene argue? is the metaphor fresh?) stays a sighted
  judgment — the gate is the floor, the eyes are the ceiling.
- A mid-build discovery that forces a layout change goes BACK INTO THE SPEC first (edit
  spec → rebuild slide), so the spec never lies about the artifact.
