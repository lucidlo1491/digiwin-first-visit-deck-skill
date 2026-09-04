# Content Pack — `docs/<deck>/content-<company>.md`  (C1 · the kitchen prep)

> **What this is.** The FULL content of the deck, prepared BEFORE any layout exists — like
> prepping a dish: every piece of text, every number, every asset named and ready. NO layout
> talk in this file (that's the SDD's job, C2). Peter reviews THIS file (plus SPEC.md) at
> the C3 checkpoint — his corrections land here, as text edits, before a single slide is built.
>
> **Why it exists (Peter, 2026-07-13).** Content and layout were decided simultaneously, so
> every content problem surfaced as a render-time layout problem (overflow, spills, reskins) —
> the iteration burn. Content-first + budgets kills that class of iteration by construction.

## File header (required, before the first slide section)

```markdown
# Content Pack — <Company> first-visit deck
> Sources: docs/gold-standard-<id>.md · inquiry-<company>.md §D/E (Nova answers, dated)
> Audience: <the people in the room + the 核決者 read from OSINT — who must feel what>
> Languages: zh, en, th[, ja]   ← ja ONLY when the main contact or a shareholder is
>   Japanese (per the OSINT decision map / group structure). This line drives the deck's
>   `<!-- LANGS: ... -->` declaration and the gate's language checks.
> Arc in one line: <the story spine, e.g. "rules changed → we're the specialist → your 3
>   floor pains → your call">

## Gate 0 — deck-level arc answers (REQUIRED — references/arc-questions.md, Peter 2026-07-25)
- Q0.1 核決者/room → <verified names + roles> → 【source】
- Q0.2 customer verbatim → <his priority order, his words, timestamps> → 【逐字稿/電話】
- Q0.3 摸底 state → <scale/budget-signal/pain from SIGNALS + what this meeting must learn> → 【…】
- Q0.4 inputs current → <VP playbook mtime · NOVA consults run · OSINT promoted> → 【…】
- Q0.5 vertical + languages → <anchor pack · LANGS> → 【…】
- Q0.6 the ONE next step → <bookable ask, sized to the venue> → 【…】
```

## Per-slide section (repeat for every slide; slide count/order is THIS deck's, not the scaffold's)

```markdown
## S<NN> — <working name>

- **Message** (the ONE thing, one line — if you can't say it in one line, it's two slides)
- **Audience note** — what the owner/EB should FEEL or recognize on this slide
  (from the OSINT profile: e.g. "MNC 職業經理人 — risk defense outranks profit")
- **Source fact** — the OSINT/Nova line this slide is grounded in, with its tag
  (【DBD】/【公開】/inquiry §E …). A slide with no source fact is templated BY DEFINITION —
  it will fail the specificity gate. Industry-general pains cite the industry brief +
  the hedge line (產業普遍現象 · 非貴司特定數據).
- **Copy** — ALL on-slide text, verbatim, in every shipping language (zh + en + th, + ja
  when triggered). Structure: eyebrow · headline · lead · body/cards · captions · CTA.
  ⚠ Write TO the length budgets below — copy that doesn't fit the pan is NOT prepped.
- **Length budgets** — per text zone, from the target block's geometry (see the SDD
  template's multiplier table): e.g. `headline zh ≤14ch · lead zh ≤40ch · en ≤1.4× zh ·
  th ≤1.5× zh`. The budgets are copied into the SDD and enforced at the sighted gate.
- **Data** — the exact numbers any chart will consume (the future gen_chart JSON, inline):
  series, values, units, the illustrative-% disclaimer if hedged. NO invented numbers —
  every figure traces to the source fact or is labeled 示意/illustrative.
- **Assets needed** — real logo / plant photo / cert to source, WITH provenance
  (URL / Drive path); or "generate: <illustration intent>"; or "none — typographic slide".
- **Presenter-note seeds** — the 六要素 probes, EB-gate question, objection script this
  slide must carry in its notes (bullet form; full notes are authored at build).
```

## Rules

1. **No layout words in this file.** "Chart on the left" / block names / grid spans belong
   in the SDD. If you catch yourself writing layout here, stop — you're cooking before
   the prep is done (the exact failure this stage exists to prevent).
2. **Every slide has a Source fact.** This is the NotebookLM grounding discipline made
   mechanical — `slide_gate.py sdd-match` fails a spec whose source-fact field is empty.
3. **INTERNAL-fence hygiene** — nothing from the gold standard's fenced blocks or 【推論】
   lines lands in Copy (they may inform Presenter-note seeds only, per the OSINT law).
   Never the client's own financials, on slides OR spoken.
4. **Copy discipline carries the sales law**: pains hedged, no pricing, no IoT/即時 framing,
   eMES not SFT/SFC, cross-strait rules — the content pack is where these are enforced
   CHEAPLY, before layout exists.
5. **C3 checkpoint** — Peter reads this file + SPEC.md's arc table. His edits here are the
   cheap ones. Build starts only on his explicit approval (escape hatch: "just do it").
