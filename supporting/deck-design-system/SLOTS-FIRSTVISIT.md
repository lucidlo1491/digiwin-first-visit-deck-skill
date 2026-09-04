# SLOTS — First-Visit Deck v2 (12 canonical page-level slots)

> One level above BLOCKS.md: a **slot** = an arc position with one job, its allowed page-organisms
> (from `system/blocks.css`), its required content fields, and its question gate. A new deck is
> `_scaffold-firstvisit-v2.html` (marker `<!-- SCAFFOLD: firstvisit-v2 -->`) + 12 filled slots —
> **never a copy of a prior deck's index.html** (gate-enforced). Corrections compound into
> blocks.css / this file — never fork per deck.
>
> Arc per VP Cheng 2026-07-25 (痛 before 信). Question gate per
> `.claude/skills/digiwin-first-visit-deck/references/arc-questions.md` — a slot may not be spec'd
> until its questions are answered with sources.
>
> **Spine:** 把老闆從「我不需要你們的系統」搬到「我連自己這張訂單賺多少都算不出來」，然後只跟你約下一步。
> 賣「算得清楚」，不賣系統。

Legend: **V** = variable (company-specific, swap every deck) · **C** = constant (institutional
default copy ships in the scaffold; adapt only the emphasis) · **V/C** = constant skeleton,
variable emphasis.

| # | Act | Slot | ONE job | Allowed blocks (blocks.css) | Var | Required content-pack fields |
|---|-----|------|---------|------------------------------|-----|------------------------------|
| 1 | A1 定調 | `cover.disarm` | Disarm: "today = your next step, not a sale" — echo his words | cover-meta + `.meta-block.presenter` + `.pqr` QR (contact invariant) | V | disarm line (his words) · meeting meta · presenter+QR |
| 2 | A1 | `industry.mirror` | His exact sub-industry squeeze; ends on a question he can't answer | `.ch-grid` (3 rule-cards) or `.s3press` (pressure scene) | V | 2–3 sourced squeeze facts · closing can't-answer Q |
| 3 | A1 | `company.snapshot` | Homework = trust: public facts + Tax ID + real logo/photos; NO financials | `.s6-grid` (id/logo/legal + evo chips + `.s6-photos`) | V | Tax ID · facts list · situational read · photo assets w/ provenance |
| 4 | A2 痛 | `owner.question` ★peak | 人機料法環 can't-compute anxiety: 「這張訂單真實賺多少，算得出來嗎?」 | `.bigq` on `.dark-sec` (+ `.triad` facets = 人機料法環 picks) | V | the ONE question (NOVA-decided) · which 人機料法環 elements lit |
| 5 | A2 | `owner.threepoints` | ①算得出成本 ②降低浪費 ③ERP=戰略決策依據(不是給員工用的) | `.ch-grid` 3-up (owner-value skin; icon per point via find_icon) | V/C | the 3 points each mapped to a FACT of his · which is primary |
| 6 | A2 | `pain.1` | His FELT #1 pain (his verbatim), hedged 產業普遍現象, anchor→react Q | `.pq` (fresh viz depicting THIS mechanism + `.qcard` + `.pq-tag` hedge) | V | pain mechanism · anchor · react-Q · viz contract (swap-test) |
| 7 | A2 | `pain.2` | Second pain (climbing toward value) — same law | `.pq` | V | 〃 |
| 8 | A2 | `pain.3` | Value-anchor pain (the money) — ฿ stays in notes | `.pq` | V | 〃 + notes-only ฿ anchor |
| 9 | A3 信 | `whyus.vertical` | 45yr + in-country logos NARROWED to his vertical; 10-sec pitch | `.dark-sec` stat-row + `.cred-row` | C | vertical pick · relevant local proof · 10-sec line |
| 10 | A3 | `proof.strip` | Risk-killers: team · CMMI · compliance — ONE LINE each | `.split-2` or stacked `.cred-row` rows (compressed old S9/10/11 constants) | C | which 3 lines for THIS buyer · what's cut |
| 11 | A4 路 | `firststep.board` | 依成熟度先上車: lightest first block, riding on his incumbent, never replace | `.s5j` journey (maturity path; destination lit) or `.s8b2` (ride-on relationship scene) | V | incumbent named · the first block (his ask) · ride-on sentence · phase-2 deferred |
| 12 | A5 收 | `close.nextstep` | ONE concrete next step + 兩層動機 + interest-check; NO price | `.closeq` + `.fk` fork + `.contact-card.cc-strip` (contact invariant) | V | the bookable step · org×personal motive · notes: 摸底 trio + 喊數字 script + 分款包 price-deferral |

## What changed vs the 15-slot v1 scaffold
- **CUT**: standalone Agenda (old S5; one line on the cover if needed).
- **MERGED**: old S2–S4 (shift/squeeze/core-question) → slots 2 + 4. Old S7/S9/S10/S11 (about/team/
  CMMI/compliance constants) → slots 9 + 10 (their 4-language constant copy survives as slot
  defaults — compressed, not deleted).
- **MOVED**: pains from after-trust (old 12–14) to before-trust (slots 6–8). Snapshot up into Act 1.
- **NEW**: slot 4 owner.question (人機料法環 peak), slot 5 owner.threepoints, slot 11
  firststep.board (product-by-maturity — `.s5j` repurposed from agenda to the maturity path).
- Old organisms all survive in blocks.css; `.agenda-grid` simply has no slot in v2.

## Slot rules (bind at build)
1. Every slot's spec (`specs/NN-<slot>.md`) opens with `## Arc answers` — gate-enforced.
2. Icons/pictograms per slot via `digiwin` MCP `find_icon`; tokens via `get_token`; log to
   `_qa/design-shopping.md` (preflight Gate 1).
3. Pain-slot visuals (6–8) are designed FRESH from the pain's mechanism — swap-test must FAIL;
   reskinning a prior deck's organism = AUTO-FAIL (`reskin-suspect` + `pain-argues` gates).
4. VP invariants R1–R3 (see arc-questions.md): zero ฿ on slides · 人機料法環 = boss-only,
  anchor-don't-force · 摸底 in notes; every slide sells 值得, not features/company.
5. Constant slots (9–10) may be lightly re-emphasized per audience but their institutional copy is
   maintained HERE (scaffold), not per deck.
