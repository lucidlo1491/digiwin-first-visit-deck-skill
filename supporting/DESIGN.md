# DESIGN — the design law for this repo (DigiWin)

This file is LAW, not guidance. It encodes decisions already paid for with failures.
When any rule here conflicts with a skill's default taste (Impeccable palettes, huashu templates,
ui-ux-pro-max styles), **this file wins**.

## 1 · Single source of style: the DigiWin Design System warehouse

**Three access paths to ONE system (use in this order):**
1. **`digiwin` MCP** (preferred for agents) — `search(intent)` → `get_component(id)` →
   `find_icon(intent)` → `list_tokens`/`get_token`, and `get_guideline('deck-layout')` for
   composition rules BEFORE composing any multi-element artifact (slide scaffolds are shoppable:
   `slide.cover`, `slide.content`, `slide.stats`, …). NOTE: the MCP caches the registry at boot —
   reconnect (`/mcp`) after warehouse changes.
2. **Local warehouse files** (source of truth): `/Users/peterlo/digiwindesignsystem/design-system/`
   (tokens.json + tokens.css, `components/index.json` + per-component `.md`, 2,673 icons +
   1,563 pictograms).
3. **Live site** (human browsing + remote fallback): **https://digiwindesignsystem.vercel.app/** —
   same registry served at `https://digiwindesignsystem.vercel.app/api/registry.json` (fetchable
   when the MCP isn't loaded, e.g. headless/cloud sessions).
- **Never invent styling. Never accept a skill's invented styling. Never mix two design systems.**
  Skills may CRITIQUE and EXPORT; only the warehouse styles. (huashu-design = critique + export
  ONLY; its 40 templates are off-limits. Impeccable's `palette.mjs` seed-color step: SKIP —
  committed brand colors exist.)
- Colors: semantic tokens only (`--smart-blue` #00AFF0, `--cyan-glow` #00E6FF, `--royal-blue`,
  `--dark-navy`, `--accent-coral/-purple/-mint`). No new hex. Fonts: **Noto Sans** (text),
  **JetBrains Mono for small labels/eyebrows ONLY** — never body copy. NOT Inter, NOT #1E3A8A.
- Before drawing anything new, shop the brand's real motifs first (Super-D mark, Data-Ocean
  dot-fields) — inventing abstract SVG when a brand motif exists is a known failure.
- A component that doesn't exist yet gets built INTO the warehouse (per its SCHEMA.md), not
  one-offed in the consuming project.

## 2 · The FacTech deck (docs/factech-2026-keynote/deck/) — architecture facts

- Single-file `<deck-stage>` deck: fixed **1920×1080 canvas**, uniformly scaled to any screen
  (0.57×–1.24× measured). Content MUST fit the canvas — overflow at 1080 = overflow everywhere.
- Each slide: `<section class="ds light|dark|navy" data-label>` with `.bar` (brandbug+pageno),
  `.body`, `.foot`. Never position/size the `<section>` itself.
- **12-col grid**: `.grid` + `.gcol-N` (128px margins, 16px gutters). Place by span, never ad-hoc %.
  Grid governs HORIZONTAL only; vertical fit is gated separately (see §5).
- **Bilingual**: every string has `.t-zh` + `.t-en` (toggle, only active shows). Dual-labels use
  `.dl-zh`/`.dl-en` — active language is the hero, other is muted decoration. EXCEPTION: system
  acronyms (ERP·MES·WMS) stay full-size heroes in BOTH languages.
- **Canonical spine = the cover's stepped PYRAMID** (`.zig`, widths 100/82/64/46%), Peter-locked
  2026-06-10 (reversed an earlier "uniform blocks" call — pyramid wins). Order **ERP·MES·WMS**,
  foundation at the BOTTOM (widest, dark-navy chip), acronyms big in BOTH languages (33px, never
  shrunk in EN), "systems you already run" small mono sub-text. On spine slides 7/16/30: `.zarr`
  up-arrows between tiers (blue `.on` along the lit path) + **progressive lighting** — unlit tiers
  `.dim` (grayscale, not just faded): p7 lights data+systems, p16 adds AI, p30 all lit like the
  cover. The cover itself has no arrows.

## 3 · Readability & content law (5–10 m viewing distance)

- Type must read from the back of a hall: titles ≥42px, body ≥22px, legends generous. When in
  doubt, bigger type + fewer words.
- **Words → visuals.** Don't make the audience read. One idea per slide, one HERO element per
  slide; everything else is supporting cast. Equal visual weight on everything = nothing read.
- A single concept is ONE container, not N bordered cards (cards fragment one idea — the slide-6
  legend lesson). Vary background decoration per slide; remove it where meaningless (the repeated
  "curly ocean line" reads as boring by the second slide).
- Translate MEANING, not words (e.g. "Look north" → 仰望/標竿, never 往北看).
- Case/proof slides must each look DISTINCT — one template with swapped numbers is a known
  Peter-rejection.

## 4 · Craft bar (what "done" looks like)

- Quality benchmark = the deck's own best slides: the car-dashboard metaphor (p6), DIKW fertile-soil
  (p12), the cover, the Taiwan logo-wall (p11). Match that, or it's not done.
- Bespoke inline SVG in the deck's own viz style — bold strokes, few elements, legible at distance.
  **No raster/stock/emoji/clip-art.** Human figures are HARD: if a figure looks like a blob or
  snowman, redo or redesign without the figure (the "hideous wave-1" lesson).
- Tells of not-done: gradient-button genericness, invisible concept elements (a "broken bridge"
  nobody can see), clutter (>1 hero), mono-font body text, decoration competing with content.

## 4b · Peter's accumulated taste rules (each one was a real correction — never re-learn these)

- **Icons must literally SAY the thing.** ERP=finance/ledger columns · MES=factory building ·
  Machine=gear (a radial dial reads as a SUN — rejected) · WMS=storage box. Always `find_icon`
  by intent; if Peter wouldn't name the concept from the glyph alone, it's wrong. (2026-06-10, p5)
- **No floating tags with dead space.** A corner tag + content below it leaves a hole; put icon ·
  name · tag on ONE header row. (2026-06-10, p5)
- **Sentence = line.** In closing/punch paragraphs, never let a sentence wrap mid-thought; break
  so each sentence owns its line, the bold punch sentence standing alone. (2026-06-10, p8)
- **One concept = one container** — a 4-item legend is a strip with dividers, not 4 cards. (p6)
- **Metaphors must be VISIBLE at distance** — a "broken bridge" the eye can't find = failed.
  Concept elements get size, contrast, glow; verify on the zoom crop, not the thumbnail. (p5)
- **Build-up states must read as OFF vs ON** — dim = grayscale, not faded color; arrows mark the
  lit path; the final slide shows everything lit. (spine, p7/16/30)
- **Logo = headline** when brand proof matters; align all stat-row elements on ONE baseline. (p8)
- Repetition kills: booth CTAs max 2×; identical case templates rejected; same bg motif on
  consecutive slides rejected.
- **Scenes tell stories, icons don't.** "Icons slapped here and there" = rejected. An illustration
  must act out the slide's argument — series grammar: pain(gray+coral) → [AI core] → win(accent),
  BEFORE/AFTER markers. Same clock with a different sweep > two different icons. (2026-06-10, cases)
- **Arrange text for SCANNING, not reading.** Full-width prose sentences = unread. Break into
  ✕/✓ punch-lines — one thought, ONE line (≤~30ch, verify no wrap), markers carry the arc. Kill
  dead gaps between related blocks (no justify-space-between scatter). (2026-06-10, cases)
- **EN deck = English everywhere content-bearing.** Eyebrows/kickers with real content (案例 01 ·
  射頻元件製造商) must be t-zh/t-en toggled, not Chinese-only. Dual-label tags (痛點 · PAIN) are ok.
  Case-slide minimums: punch-lines 24px, tags 15px, who-pill 21px. (2026-06-10)
- **THE SPACING LAW (Peter has had to repeat this 3× — never again).** EVERY margin, gap, and
  padding in the deck is a multiple of 8 (4 allowed for hairline-fine adjustments). `34px`,
  `26px`, `18px` freehand values are DEFECTS — audit your own CSS numbers before rendering.
  Defaults: **48px** of air between major blocks (content ↔ punchline bar), **24–32px** between
  related blocks, 16px inside components. Applies INSIDE bespoke SVG scenes too (flow zones and
  edges breathe in 8-pt steps). The 12-col grid is horizontal law; the 8-pt scale is spacing law.
  When a slide "feels crammed," the fix is almost always snapping gaps UP to the next 8-pt step,
  not shrinking content. (p24 + p28, 2026-06-10)
  **Corollary (p30): SPEND THE SLACK.** Passing the ÷4 lint with 12/24px gaps between MAJOR blocks
  is still a defect when the gate shows unused vertical room. Before shipping, check the slide's
  slack (no overflow = there IS room) and widen major gaps toward 48px FIRST. Compression is only
  justified when the canvas is actually full. The DigiWin system never asks for tight — that
  instinct is mine and it's wrong.
- **Annotation ladder (p24's 4 iterations — start at the top rung):** floating pills + dashed
  leaders ✗ → clamped tag ✗ (asserts, doesn't explain) → clamped CARD: number-dot grips the
  element + glyph + title + ONE-line explainer ✓. Cards must NEVER cover the element's face —
  when edges are crowded, flank as WINGS gripping the side edges. Check SVG label collisions at
  zoom (ASK/ANSWER had to stack vertically). (2026-06-10)
- **Bilingual-abuse tell:** any `.t-en{display:block;font-size:<small>}` override = the EN deck
  renders titles tiny (p24's original "squint" bug). t-zh/t-en must stay symmetric toggles.
- **Don't invert the source framework's hierarchy.** p28: the FOUR HIGHS are the characterization
  (original deck's emphasis); departments are nested evidence. Reorganizing by department was
  rejected — when redesigning, the original conceptual spine stays the primary axis. (2026-06-10)
- **Connectors must carry meaning, not decoration.** A plain line between blocks = rejected.
  Show source → flow → destination (glowing port, gradient direction, arrowhead into the consumer).
  And never label a concept twice (kicker repeating the title) — spend that space on a plain-words
  definition instead. (p28)

## 5 · Verification gates (ALL mandatory, in order)

0. **RE-READ §4b BEFORE designing, and audit your draft against it BEFORE rendering.** Rules loaded
   at session start are forgotten by mid-session — recording without re-reading is how the same
   defects (34px margins, repeated kickers) kept shipping. Treat §4b as a pre-flight checklist.
0b. **CONSULT PETER'S MACHINE-READABLE GUIDELINES before composing any slide** — they are the
   canonical composition law: `/Users/peterlo/digiwindesignsystem/design-system/guidelines/`
   (`deck-layout.json` — 12-col grid, space scale "never invent intermediate values", **888px
   content-height budget**, ONE primary block per slide, chrome zones, per-archetype recipes;
   plus `deck-typography.json`, `deck-collision.json`, `deck-contrast.json`, `deck-checklist.json`).
   Via MCP: `get_guideline('deck-layout')` (reconnect /mcp if the tool is missing — boot cache).
   The design lint reads the space scale FROM tokens.json, so the scale is enforced mechanically:
   only 4·8·12·16·24·32·48·64·96·128 pass.
1. **Design lint**: `python3 docs/factech-2026-keynote/deck/_qa/design_lint.py <deck.html>` —
   MECHANICAL enforcement of the spacing law (÷4/8), type minimums (<15px content), and the
   EN-shrink bilingual bug. Ratcheted: 222 legacy (Claude-Design-era) violations are frozen in
   `design_lint_baseline.txt`; any NEW violation fails. When touching a slide, also clean its
   legacy values and re-baseline (`--baseline`).
1b. **Layout gate**: `python3 docs/factech-2026-keynote/deck/_qa/layout_invariants.py <deck.html>` —
   checks BOTH languages; OVERFLOW (scrollHeight>clientHeight) is the authoritative vertical-fit
   check. Gate-clean is the FLOOR, not the bar.
2. **Render & judge as a designer**: screenshot via Playwright, READ the PNG, score it with the
   5-dimension critique (philosophy / hierarchy / detail / functionality / innovation — huashu
   `references/critique-guide.md`) and/or Impeccable `/audit`. Geometry/bbox assertions for
   layout claims — `is_visible()` ≠ no-overlap.
3. **Show Peter the PNG and get approval BEFORE deploying.** One slide at a time. No batch deploys.
   Subagents may draft, but they are SIGHTLESS — never ship their visual output unjudged.
4. Deploy: `cp deck/index-v2-loops.html factech-loops-public/index.html && cd factech-loops-public
   && vercel deploy --prod --yes`. Rollback = `vercel promote <previous-deployment-url>`.
- PDF/PPTX export (stage backup): `node ~/digiwin_automation/.agents/skills/huashu-design/scripts/
  export_deck_stage_pdf.mjs --html index-v2-loops.html --out out.pdf --width 1920 --height 1080`
  (hide fixed chrome + pick language first for the final handout).

## 6 · Other artifacts in this repo

- VP monthly report: `_render_pdf.py` → `_qa.py` → visually verify all 8 slide PNGs (17-item
  checklist) before "done". Customer quotation PDFs: ALWAYS one page, portrait.
- Same warehouse law applies to dashboards, brochures, proposal decks — 100% DigiWin, no mixing.
