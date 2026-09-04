# Deck Block Library — catalog

The reusable slide-body **blocks** for Digiwin first-visit / proposal decks. CSS lives in
`system/blocks.css`; a blank arc that already uses them is `_scaffold-firstvisit.html`.

**How to build a deck now:** copy `_scaffold-firstvisit.html` → `docs/<deck>/index-draft.html`, fill each block's
`{{PLACEHOLDER}}` from OSINT + Nova's reply, run `_qa/slide_gate.py`. **Do NOT hand-roll slide bodies from raw
primitives** — pick a block. If a block needs a tweak, fix it in `blocks.css` so every future deck inherits it
(that's the whole point — corrections compound into the system, not per deck).

Each block below states **the rule it bakes in** = the correction Peter once made by hand, now permanent.

| Block (class) | Use for | Rule it bakes in (the correction) | Gate guard |
|---|---|---|---|
| `.em` / `.dark-sec .em` | any load-bearing phrase | emphasis renders **everywhere**, not just `.lead`; mark 1–3 phrases/slide | `emphasis`, `emphasis-styled` |
| `.agenda-grid` **or** `.s5j` | the agenda slide | re-thought to preview THIS deck's message, glanceable; never a reused rail | `visual` |
| `.ch-grid`/`.ch-card` | 3-up industry/rule cards | cards **fill the band** — flex column, icon chip top, consequence anchored bottom w/ divider; **no dead top/bottom space** | `visual`, `informative` |
| stat-row (`slides.css`) + `.cred-row` | the "who we are" trust slide | quantitative stat row + qualitative chip row on ONE slide (no bottom void, no 2nd about-us slide) | `visual`, `emphasis` |
| `.s6-grid` | company snapshot | real logo + real plant photos + **13-digit Tax ID** + one-line read; no financials, no "we did homework" | `visual`, `tax-id` |
| `.photo-strip` / `.split-2` / `.cmmi-scene` | local-team photos / cert evidence | trust = what they can **SEE** (real photos/cert, clean crop); icons under-sell | `visual` |
| `.s8b2` + `.compliance-rail-wrap` | solution/method relationship scene | show the **relationship as one connected structure**, not parallel lists; **connectors must touch** (measure); **no filter on thin paths** | `svg-robust`, overlap |
| `.team-panel` | local team / any role list | **one enclosed designed panel** (hub + chips on a spine + payoff), not floating primitive boxes | `visual` |
| `.pq` + `.pq-chart`/`.qcard`/`.triad-key` | a pain + discovery question | pain = a **chart that ARGUES** (right type via `gen_chart.py`) beside a **hedged** discovery Q; encoding agrees w/ claim | `hedged`, `informative` |
| `.askcard` | the `money.mirror` floor question | the `.qcard` sibling for the **money.mirror** slot only. `.qcard` means "hedged INDUSTRY-GENERAL question" and the gate binds it to 「產業普遍現象 · 非貴司特定數據」; money.mirror shows the client's OWN public DBD filings, so hedging them would be false. Same recipe, opposite contract — an **on-the-record** floor question under the mandatory 「DBD 公開申報資料，任何人皆可查閱」 disclaimer. **Never on a pain slide.** (Dai-Ichi 2026-08-19) | — |
| `.s3press` (+`.pq`) | a concept illustration (squeeze etc.) | generated scene (nano-banana) + overlay labels; **semantic encoding** (arrows converge inward = squeeze) | `informative` |
| `.bigq` (on `.dark-sec`) | the core-question peak | ONE peak; the question **dominates** (90px); `.hl` the sharpest phrase | `emphasis` |
| `.closeq`+`.fk` + `.contact-card.cc-strip` | the close | the ASK, most legible, **no quote** (first-visit); **vertically centered** (fit.js override); contact + LINE QR | `no-pricing`, `contact+QR` |
| `.draft-ph` | a Nova-dependent slide, pre-answers | declare the slide's JOB as a placeholder; **never ship it** | `no-draft` |

## Mix & match — the blocks are a PALETTE, not a fixed template

The scaffold's 15-slide arc is a **default**, not a mandate. Compose what THIS company needs:

- **Repeat a block** — 4 pains → four `.pq` slides; two factories/entities → two `.s6-grid` snapshots; two
  industry angles → two `.s8b2` scenes. A block can appear 0, 1, or N times.
- **Drop a block** — no margin squeeze story → delete the `.s3press`/`.pq` squeeze slide; buyer not skeptical →
  fold team + compliance into fewer slides.
- **Add / reorder** — insert an extra industry-focus, a group-structure slide, a competitive slide (proposal).
  The gate is **count-agnostic** (derives cover/close/content) — a 12- or 18-slide deck passes the same way;
  just renumber the cosmetic `slide-num` / nav denominators.
- **Vary a block's internals** — card/role/stat grids default to 3 or 6 columns; for 2 or 4, add a one-line
  deck-local override (e.g. `#slide-2 .ch-grid{grid-template-columns:repeat(4,1fr)}`) — that's layout arithmetic,
  not a craft change, so it's fine deck-local. (A *craft* fix still goes back to `blocks.css`.)
- **What stays fixed:** the block's **look/layout/craft** (the brand) and the **invariants** the gate enforces
  (visual per slide · emphasis · hedged pains · contact+QR on cover/close · Tax ID · no pricing first-visit).
  Everything else — arc, count, order, copy — is yours to shape per company. **Phase-0 (OSINT→Nova) decides the
  actual arc + content**, so reusing blocks keeps decks coordinated without making them templated.

## Minimal snippets

**Rule cards (`.ch-grid`)** — 3 cards that fill the band:
```html
<div class="ch-grid v-center">
  <div class="ch-card">
    <div class="ic"><!-- find_icon SVG --></div>
    <div class="kicker">{{TAG · MONO}}</div>
    <h4><span class="t-zh">{{標題}}</span><span class="t-en">{{Headline}}</span><span class="t-th">{{หัวข้อ}}</span></h4>
    <p><span class="t-zh">{{一句後果,含 <span class="em">重點</span>}}</span> …</p>
  </div> … ×3
</div>
```

**Local-team panel (`.team-panel`)** — enclosed unit:
```html
<div class="team-panel v-center">
  <div class="team-hub"><span class="pin"><!-- pin SVG --></span>
    <div class="ht"><div class="h1l">{{HUB · 城市 22F}}</div><div class="h2l">{{副標 + <span class="em">重點</span>}}</div></div>
    <span class="chip6">{{N FUNCTIONS}}</span></div>
  <div class="team-roles"><div class="team-role"><span class="ic"><!--SVG--></span><span class="rl">{{角色}}</span></div> … ×6</div>
  <div class="team-payoff"><span class="pi"><!--SVG--></span><span class="pt">{{收束句 + <span class="em">重點</span>}}</span></div>
</div>
```

**Pain + discovery (`.pq`)** — chart that argues + hedged Q:
```html
<div class="pq v-center">
  <div class="pq-viz"><img class="pq-chart c-all" src="assets/pain1.png" alt="…"></div>
  <div class="pq-body">
    <h3>{{論點標題}}</h3>
    <p>{{一句解讀,含 <span class="em">重點</span>}}</p>
    <div class="qcard"><div class="qlabel">Q · DISCOVERY</div>
      <div class="qtext">{{開放式探詢問題}}</div></div>
    <div class="pq-tag">產業普遍現象 · 非貴司特定數據</div>
  </div>
</div>
```

See `system/blocks.css` for the full set + the rule headers, and `_scaffold-firstvisit.html` for the whole arc
wired together. Charts: `/digiwin-deck-visual/scripts/gen_chart.py`. Images: `gen_image.py`. Icons: `find_icon`.
