---
name: digiwin-first-visit-deck
description: >-
  Use when building the deck for the FIRST meeting with a fresh or early-stage manufacturing prospect
  (stage E / early-D), before any demo, quote or proposal — triggers: "build a first-visit deck", "初訪簡報",
  "discovery deck for <Company>", "deck for the first meeting with <Company>", or prepping a first visit to
  a new prospect. NOT for a near-decision deal with pricing / a V10 quote — that's /digiwin-erp-proposal-deck.
  No OSINT yet → run /digiwin-research-company first.
---

# /digiwin-first-visit-deck

Build the deck for the FIRST visit to a manufacturing prospect. This skill is the **process + QA + design
law**. The reference implementation is `docs/tatung-thailand-firstvisit/` (study it before building a new one).

## When to use
- First meeting with a fresh / early prospect (stage **E / early-D**); before discovery/demo; before any quote.
- Goal is to earn the next conversation and start filling the 六要素 — NOT to make the case or drop a price.

## When NOT to use
- Near-decision, EB engaged, you have a V10 quote → **`/digiwin-erp-proposal-deck`** (the 7-act proposal tier).
- A one-pager / LINE message → don't build a deck.
- No OSINT yet → run **`/digiwin-research-company`** first (its gold standard is this deck's raw material).

## The deck's THREE jobs (Peter, 2026-06-24 — the steering definition)
1. **Who we are** — specialized, professional manufacturing-ERP maker (NOT a generalist).
2. **We understand your industry** — surface the *typical* field bottleneck/pain scenarios we see, so the
   owner recognizes himself. These are **industry-general, hedged** ("產業普遍現象 · 非貴司特定數據") —
   never a claim about the client's own numbers.
3. **Earn the next conversation + fill the 項目六要素 + QUALIFY (摸底)** — provoke discovery so we know it's a
   **real, funded** project: is the scale / budget-signal / urgency real? (VP's qualification discipline —
   [[feedback_vp_qualification_discipline]]).

**★ DISCOVERY-QUESTION LAW — value-driven, not extractive (Peter 2026-07-22, [[feedback_value_driven_discovery_questions]]).** Every `Q · DISCOVERY` block must still work when the client **cannot quantify** (a no-system SME is the norm, not the exception). **NEVER ask 「一個月幾次 / 每天多少張 / 成本多少」** — they can't answer, it stalls (the Everydayhappy 7/15 silence), and it makes us an interrogator, not an advisor. Instead: **anchor → react** (「同業您這種規模通常是 X —— 您這邊比這多還少?」) + convert their not-knowing into the pain (「您有沒有一個可靠的數字?」 → the 「沒有」 IS the surfaced 隱性需求 = the C2 move; 連虧多少都看不見 = the risk, and the system is what ends the blindness). **We own the value case; the client only REACTS** (industry anchor + observed reality, never their DBD numbers quoted back). KEEP factual/feasibility Qs they CAN answer (who maintains the Express DB, can the vendor open tables); ask **urgency directly**, never budget. This is how the deck earns the 價值訴求 when the owner can't state it — the client-facing engine of the VP value-proposition test [[feedback_vp_value_proposition_test]]. **★ The concrete "anchor a number" script (VP 2026-07-23, [[feedback_vp_coaching_2026_07_23]] — 「價值論述的引導」):** on the inventory/waste pain, the presenter-notes run — read the warehouse with your eyes (條碼/label/顏色) → 3 probes (成品掉/斷料/呆滯庫存) → frequency test (常發生才要解決) → ask 盤點頻率 + 倉庫值多少 → **if they can't answer, YOU throw the number** (依規模 50–100萬 USD "sleeping money") → apply conservative **30% 呆滯** → **convert to THB for shock** (30萬 USD = 1000萬泰銖) → then the system price reads cheap ("一年多省 600 萬,這才是非做不可的理由"). This is the exact embodiment of anchor→react: the value case is ours to build, the client only reacts. **★ Boss-only sibling probe — 人機料法環 (Pass-2, [[feedback_vp_coaching_2026_07_23]]):** when the room is the owner, the same anchor→react runs on *true order cost* — "您這張訂單的成本 — 人工、機器攤提折舊保養、原料+半成品+呆滯、法規、環保消防 — 算得進去嗎?" → the 「沒有」 IS the wedge (**only an ERP totals it**; no system = 訂單在虧不自知). Feeds the boss 3-point value spine (算得出成本 → 降低浪費 → 戰略決策). Owner-only — don't run this on IT/procurement.

## ⭐ STEP -1 — VERIFY THE INPUTS EXIST (added 2026-08-31; never attest, RUN it)

```
python3 .claude/skills/digiwin-first-visit-deck/scripts/check_inputs.py <company-id> "<company name>"
```

Every other gate here is machine-enforced; "OSINT dossier promoted" was an attestation I wrote in
`design-shopping.md` — my word, in a skill built because my word was not good enough. This checks
that the dossier is promoted rather than a draft, that it is not staler than a recorded meeting
(→ run `--reconcile` first), and which Gate 0 path applies. **Company research is NOT done here —
the dossier is this deck's raw material; the only research this skill still owns is the industry
layer, and even that now lives in `/digiwin-research-company` and is reusable.**

## ⭐ PHASE 0 — Industry × Company Inquiry (MANDATORY; run BEFORE any slide)
The #1 failure mode is **templating** — reusing a prior deck's scenes and slapping on whatever's at hand
(generic sector grids, a carried-over pain triad, a default core question). The cure is a real
research → Nova → content protocol that makes **every slide from 5 onward provably specific to THIS industry
and THIS company**. Output a tangible **inquiry sheet** (`docs/<deck>/inquiry-<company>.md`) that PROMPTS
Peter with sharp questions and feeds Digiwin Nova.

1. **Industry research (Thai-specific).** For the client's *exact* sub-industry — electronics/EMS, auto-parts,
   food, etc., NOT "manufacturing" — research (WebSearch + domain knowledge): the macro shift hitting it in
   Thailand, the regulatory/compliance context (BOI + the relevant standard: IATF for auto, GMP/HACCP for
   food, RoHS/REACH for electronics export…), the operating model, and the **canonical operational
   bottlenecks of THAT industry**. → an **industry brief**.
   **OPTIONAL DEEP SWEEP (added 2026-08-25): NotebookLM Deep Research as the breadth arm** — for a
   sub-industry we haven't briefed before (or a moving regulation), launch a `notebooklm-mcp`
   `research_start` sweep using the NOVA-calibrated prompt template in
   `references/industry-sweep.md`, poll `research_status`, and fold the returned briefing into the
   industry brief **as one more SOURCE**: every claim keeps its citation, is tagged 【NotebookLM
   sweep <date>】, and passes the same rules — no client-specific claims from it ever land on a
   slide, hedge as 產業普遍現象, and anything steering strategy stays inside internal fences. The
   sweep NEVER replaces the entity layer (/digiwin-research-company: DBD/ImportYeti/NOVA are unreachable
   to it) — it only widens the industry layer.
2. **Company OSINT synthesis.** From `/digiwin-research-company` (`docs/gold-standard-<company>.md`): status &
   numbers, profile & strengths, ownership, financial trajectory, the specific signals. → a **company brief**.
   **SKIP every block under a `> INTERNAL ONLY — never into customer-facing artifacts` fence and any 【推論】-tagged
   claim** — that layer steers the PRESENTER's live questions only; it never lands on a slide or in notes verbatim.
3. **Intelligent questions → a FORWARDABLE Nova packet.** Don't improvise the questions — use the
   **Nova Inquiry Bank `references/nova-inquiry.md`** (the Tatung pattern, generalized). Fill its
   `{{placeholders}}` from the gold-standard fields (the doc has a field→question map) to produce a clean,
   copy-paste packet **`docs/<deck>/nova-questions-<company>.md`** — addressed TO Digiwin's Nova, with a short
   company context block + questions grouped by what they decide (pains / core question / close / EB /
   objection / 立案 / Thai-industry) + a Q→slide map. **Every question must state OUR hypothesis (from OSINT)
   and ask Nova to confirm/rank/improve — never blank.** This is the deliverable Peter hands to Nova; it is a
   REQUIRED output, not optional. (Worked example: `docs/tatung-thailand-firstvisit/nova-questions-tatung.md`.)
4. **Nova handoff (the real loop) — ASK NOVA LIVE YOURSELF (Peter, 2026-07-17).** The default is no longer
   "hand Peter a packet to forward" — **query the live Nova agent directly** via the procedure in
   `~/.claude/skills/digiwin-research-company/nova-live-consultation.md`: Playwright/Teams → `+ 新對話` in
   **南高-商機助手** → send the packet questions (self-contained, **ASCII hyphen only — em-dash triggers the
   WAF 403**) → capture answers verbatim via the job API to `docs/<deck>/nova-live-<date>.md`. **Ask whenever
   a deck decision is uncertain — not only up front:** the core question (S4), the industry-focus framing (S8),
   **which pains to show** (S12–14, owner-resonant, always framed through profit/cost, never a fixed triad),
   and the **resonant close** (S15) are all Nova-decided. Nova's real answers **DECIDE**; tag them 【Nova live
   <date>】 and keep strategy reasoning inside internal fences (never verbatim on a customer slide/notes).
   The forwardable packet `docs/<deck>/nova-questions-<company>.md` is still produced as the record, and
   becomes the **fallback** if the live agent is unreachable (then Peter forwards it and pastes answers back).
   The local `/nova-*` skills (`/nova-5-elements`, `/nova-intention-chain`, `/nova-pain-translation`,
   `/nova-role-questioning`, `/nova-objection-preempt`, `/nova-prep`) are a **PROXY** — use them to draft
   provisional answers + sharpen the questions, but the authoritative enrichment comes from the real (live) Nova.
   Record both in `inquiry-<company>.md` (provisional/proxy) vs the returned Nova answers (authoritative).
5. **Per-slide SPECIFICITY GATE.** Before building each slide 5→15, ask: *"Could this slide appear in any
   company's deck?"* If yes → it's templated; re-ground it in the industry brief + company brief. The
   industry-focus slide must show **depth in THEIR world** (e.g. electronics: PCBA · cabling · connectors ·
   display · smart devices), never a generic all-sector grid with their industry merely highlighted (the #1
   template tell). Pains must be that industry's real owner pains, not a reused 資金/產能/利潤.

## Where the 六要素 live (slides vs notes)
- **On slides** (visible): only 痛點 (the hedged field scenarios) + the two-layer 動機 (the close). Keep slides clean.
- **In the presenter notes** (the live discovery script): the full 六要素 probing — **EB-gate** (who decides:
  local vs HQ vs group IT), **時程/Critical-Date** (why now — **verify it skeptically**, don't take a claimed
  deadline at face value), **競爭** (current system incl. self-build — probe the *tier*, e.g. SAP P1/B1/HANA/cloud),
  **痛點→฿** quantification, and — per **VP's qualification discipline ([[feedback_vp_qualification_discipline]])** —
  **摸底 FIRST**: read the prospect's *scale · budget-signal · pain magnitude* from **signals** (what they run today,
  their size, behavior), never from their claims, before we invest in a demo/visit. Use the company-specific OSINT
  cues to *steer* questions, **never to recite the client's financials** — VP veto. The close ends with an
  **interest-check / next-meeting ask** that is **also a qualification gate** (is this real & funded? read the
  buyer's 面 vs 點 frame), not 收單.
- **Presenter-notes SURFACE — a SEPARATE WINDOW, NOT an inline panel on the deck (Peter 2026-07-01 — BURN).**
  The notes are the **rep's private notes "in another window"** — the `#present-view-btn` (🖥 講者視窗/Presenter,
  bottom-left) opens `openPresenter()` → a `window.open` presenter window (timer · slide-num · title · notes ·
  next · prev/next), which the rep drags to a second screen while the customer-facing deck stays **clean**. **Do
  NOT glue an inline `#notes-panel` onto the deck that follows the current slide** — Peter explicitly rejected
  that ("you put them right there on the slide deck… I do not want the version with the notes, the timer, and the
  slide deck that moves along"). The scaffold ships the separate-window presenter; keep it. (The `slide_gate`
  `presenter-notes` check accepts either surface, but the separate window is the mandated one.)
  **Since 2026-09-03 the window also carries (Peter reads Thai slowly): a LIVE MINIATURE of the current slide in
  the note language (the deck embeds itself with `?mirror=1`; `body.is-mirror` hides the chrome) and a resizable split (drag the divider or ◧ S/M/L, remembered in localStorage). All three follow
  the 中/EN toggle, so a Thai-language deck can be presented while reading it in Chinese or English. Slide tracking
  uses the deck's nearest-centre rule, not an IntersectionObserver (which reported the wrong slide at load).**
- **Presenter-notes LANGUAGE — EN ⇄ 中文(繁) toggle, ONE at a time (Peter 2026-06-30), INSIDE the presenter window.**
  The presenter window has its **own** 中/EN toggle showing **English OR 繁體中文, never both at once**, **independent
  of the slide language** (the rep + reviewer Eddie/VP read the notes; the slides serve the customer). Author EVERY
  note in **both** `en` and `zh` and key the `NOTES` object so the window switches (`NOTES[n] = {zh, en}`); a note
  left single-language is a gate FAIL. Notes are **not** translated into ไทย/日本語 — only EN + 繁中 (that's who reads
  them). They stay internal (stripped on public builds).
- **★ Presenter-notes THOROUGHNESS — the notes must let a presenter who does NOT read the on-screen language
  UNDERSTAND the slide (Peter 2026-07-01 — BURN: "I don't read Thai/日本語 natively; the presenter notes must help
  me understand").** The slides are in ไทย/日本語 for the customer, but the rep may not read those fluently — so each
  note is his lifeline. Every note MUST, in BOTH languages: **(1) FIRST say in plain language what the slide SHOWS /
  MEANS** — the headline, the point, what the customer is looking at (so he can present a Thai/JP slide he can't
  read); **(2) THEN the talk-track** — what to say, which 六要素 to probe, the EB-gate, the pain→฿ framing, what to
  listen for. **A terse one-liner / talk-track-only shorthand is NOT enough — it FAILS.** The `slide_gate`
  `notes-thorough` check enforces this mechanically: every slide's `NOTES` entry must have **non-empty `zh` AND
  `en`, each above a length floor**, and the window must carry the `nlang` toggle. (True depth is still a sighted
  judgment — the floor is the floor, your read is the ceiling.)

## The first-visit arc — v2, 12 slots / 5 acts (VP Cheng revamp, 2026-07-25; supersedes the 15-slide v1)

### ★ IN THAILAND, NOBODY KNOWS WHO DIGIWIN IS — the intro is load-bearing (2026-08-31)

**This is not a trade against VP's arc. It is a market correction.** VP's 12-slot design assumes a
prospect who already has some idea who DigiWin is — true in Taiwan, where 80%+ of listed
manufacturers run our software. **In Thailand it is false.** Peter is the one standing in front of
these clients; the VP is in Vietnam. What the room actually produced:

- On two joint first visits with Chewie, **neither company had heard of DigiWin.**
- Their VP/CEO asked directly: **「I don't know you guys. Can you please let me know you better
  inside the slide?」**
- And our pain read was so precise that, from an unknown vendor, **it almost felt like a scam.**

So the company introduction is not overhead competing with the pain act — **it is what buys the right
to be precise about his pain at all.** Accuracy without identity is not credibility; from a stranger
it reads as surveillance. In a market where the brand is unknown, slides 2-3 are doing work, not
taking up room.

**We are iterating because the clients told us what they want to hear.** That is the highest evidence
class this skill has. When field evidence from the room conflicts with a designed arc, **the room
wins**, and the arc gets updated — not hedged against.

**The two changes that came out of it:**

- **Slides 2–5, `digiwin.who` / `heritage` / `stack` / `thailand`** — a real introduction. Who we are,
  how 44 years got us here, that the stack is one product family rather than several vendors stitched
  together, and that there is a Thai team on the ground. **Four pages, not a token one** — in a market
  with no brand recognition this is the part that earns the rest of the deck a hearing.
- **Slides 13–17, the CASE BLOCK** — five beats: 背景 → before → 方案 → 導入過程 → 成果, placed AFTER
  the pain. A case study is proof against a pain already felt; shown first it is another vendor claim.
  `case.before` must echo the pains at 10–12 or the block argues for someone else's problem, and
  `case.results` must carry measured before→after indicators — which is exactly why the TONO
  訂單達交 page worked in the room.
  ⚠ TONO's reference-publication rights with Taiwan were still PENDING as of 2026-08-20 — sanctioned
  for controlled 1:1 prospect sharing only.

**What VP's revamp still gets right, and stays:** pain before deep trust, no price on any slide, the
人機料法環 question as the peak, and 摸底 in the presenter notes. His fix was for a deck that sold the
company for five pages and reached the pain too late. Two intro pages in an unknown-brand market is
not that deck.

**VP's diagnosis of v1:** 「先賣公司、後講痛——這是反的。」 Five trust pages before any pain, to an owner
who opens with "I don't need your ERP", means he stops listening by slide 9. **先讓他痛，再讓他信。**
**The spine (every deck serves it):** 把老闆從「我不需要你們的系統」搬到「我連自己這張訂單賺多少都算不出來
——這件事越早做越省」，然後只跟你約下一步。**賣「算得清楚」的價值，不賣一套系統。**

**★ THE QUESTION PROTOCOL (Peter 2026-07-25): a slide may NOT be generated until its question set in
`references/arc-questions.md` is answered WITH SOURCES** — Gate 0 (deck-level) in the content-pack
header, per-slot answers in each spec's `## Arc answers` section (gate-enforced by `slide_gate.py
sdd-match`). Slot library: `docs/digiwin-2026-deck-design-system/SLOTS-FIRSTVISIT.md`.

| # | Act | Slot | ONE job | Block |
|---|-----|------|---------|-------|
| 1 | A1 定調 | `cover.disarm` | disarm: "today = your next step, not a sale" — echo his words | cover-meta + presenter/QR |
| 2 | A1 我們是誰 | `digiwin.who` ★ | 只做製造業軟體，不做通用軟體 · 1982 · 55,000+ 工廠客戶 | `.dark-sec` stat-row |
| 3 | A1 | `digiwin.heritage` ★ | 沿革與底蘊：44 年怎麼走過來、股東結構、在台灣製造業的位置 | `.ch-grid` / timeline |
| 4 | A1 | `digiwin.stack` ★ | ERP／MES／WMS／APS 同一套底層，不是多家拼裝 | `.split-2` |
| 5 | A1 | `digiwin.thailand` ★ | 2017 進駐 · 在地泰籍團隊 · 在地客戶 | `.cred-row` |
| 6 | A1 他的世界 | `industry.mirror` | his EXACT sub-industry squeeze; ends on a question he can't answer | `.ch-grid` / `.s3press` |
| 7 | A1 | `company.snapshot` | homework=trust: public facts + **Tax ID** + REAL logo/plant photos; NO financials | `.s6-grid` |
| 8 | A2 痛 | `owner.question` ★peak | **人機料法環**: 「這張訂單真實賺多少，算得出來嗎?」 — anchor→react | `.bigq` on `.dark-sec` |
| 9 | A2 | `owner.threepoints` | ①算得出成本 ②降低浪費 ③ERP=戰略決策依據 — each mapped to a FACT of his | `.ch-grid` 3-up |
| 10–12 | A2 | `pain.1/.2/.3` | felt-first field pains, hedged 產業普遍現象, anchor→react Q, FRESH viz per mechanism | `.pq` |
| 13 | A3 案例 | `case.who` ★ | the case company's **background** — size, products, market, so he recognises himself in it | `.s6-grid` |
| 14 | A3 | `case.before` ★ | **the BEFORE state** — must ECHO the pains at 10–12, or the case argues for someone else's problem | `.pq` |
| 15 | A3 | `case.solution` ★ | what we actually put in — scope, and what we deliberately did NOT do | `.split-2` |
| 16 | A3 | `case.rollout` ★ | **how the implementation actually went** — phases, elapsed time, who from their side, what was hard. Answers the question he won't ask: "will this happen to us too?" | `.s5j` / timeline |
| 17 | A3 | `case.results` ★ | **the INDICATORS — before → after, measured.** The payload; 13–16 exist to make these believable | `.ch-grid` stat-row |
| 18 | A3 信 | `whyus.vertical` | 45yr + the 10-sec pitch narrowed to his vertical — the deeper why-us, not a logo wall | `.dark-sec` stat-row + `.cred-row` |
| 19 | A3 | `proof.strip` | team · CMMI · compliance — ONE LINE each | `.ch-grid` / `.split-2` |
| 20 | A4 路 | `firststep.board` | 依成熟度先上車: lightest first block, riding on his incumbent, NEVER replace | `.s5j` / `.s8b2` |
| 21 | A5 收 | `close.nextstep` | ONE concrete bookable next step + 兩層動機 + interest-check; NO price | `.closeq` + `.fk` + `.cc-strip` |

**★ LENGTH IS NOT THE CONSTRAINT — the content is (Peter, 2026-08-31).** The deck runs 21 slides
because 21 slides of content is what the room asked for: four pages of company introduction in a
market that has never heard of DigiWin, and a five-beat case study that a single page cannot carry.
**Do not compress this arc to hit a page count.** If a specific meeting is short, drop slides for
THAT deck and say which — never thin the standing arc.

Slides that a per-deck cut may drop first, in order, if a particular room genuinely has no time:
`proof.strip` (19) → `whyus.vertical` (18, folds into 17) → `digiwin.thailand` (5, only when the
prospect already knows we are in Thailand). Everything else is load-bearing.

**Hard-wired invariants (VP, gate-backed — full text in arc-questions.md):**
- **R1 · zero ฿ on any slide, ever** — value numbers are verbal, conservative (labour base, never revenue base), anchor-only. **Exception: the optional `money.mirror` slot below, and ONLY under its preconditions.**
- **R2 · 人機料法環 is boss-only; anchor, don't force** — his 「不知道」 IS the wedge (C2), never demand self-quantification.
- **R3 · 摸底 lives in presenter notes; every slide must sell 值得** — before shipping any slide ask 「這頁在賣『值得』，還是在賣 feature/賣公司？」; company-selling pages get cut/merged.

### ★ OPTIONAL SLOT `money.mirror` — MJ 超級數字力 on public DBD data (added 2026-08-11, Peter-authorized; worked example = Asia Polysacks S9, 13-slide arc)
An extra slide inserted AFTER the pain act (between `pain.3` and `whyus.vertical`), telling the
prospect's OWN public-DBD financial story in MJ Lin's plain language — 「賺到的錢在倉庫睡覺」, never
accounting jargon. **This is the sanctioned R1 exception**, legal only when ALL preconditions hold:
1. **Peter explicitly authorizes it per deck** (it overrides the MJ×VP red line 「禁用客戶 DBD 數字」 —
   his call, per-deal). Rationale on the slide itself: every figure is **labeled as public DBD filings
   anyone can read** («DBD 公開申報資料，任何人皆可查閱» disclaimer line is MANDATORY).
2. **先讚後刀 (MJ iron rule, notes-enforced):** `company.snapshot` must carry a GENUINE praise line
   from the same DBD read (e.g. receivable-days improvement), and the presenter notes on both slides
   script the order: the praise lands and the owner tells HOW before this slide may be turned.
3. **Plain-language translation only:** inventory days = 「料睡幾天才變回現金／錢比貨睡得久」; the
   profit-vs-inventory reconciliation = 「賺到的錢睡進了倉庫」→「不是虧損，是被凍結的現金」; the
   improvement bridge quantifies cash freed at HIS scale and names what it funds. Arithmetic only —
   never invent figures the filings don't support; compute ratios and STATE assumptions.
4. **Ends on an answerable floor question** (which stage do the extra days sleep in) — anchor→react,
   never 盤點/audit language (heavy-ERP tell), never demand self-quantification.
5. **Charts via `gen_chart` (BE years, LANG-NEUTRAL numbers); leave-behind carries NO client numbers**
   (present-only; the portable/public build is for presenting, print/PDF handouts use the hedged version).
6. **★ GENERIC-FIRST, ACTUAL-ON-TOGGLE (added 2026-08-20 — Dai-Ichi field lesson).** Client's own
   people (IT lead Tananant + Khun Nok, 8/20 online meeting) reacted to the client-numbers version with
   「你有我們的資料，我們沒有你的」/「像來查戶口」 — even with the DBD-public disclaimer, LEADING with
   the prospect's own filings reads as surveillance to a Thai room. The slot now ships DUAL-MODE:
   - **Default = generic industry mirror**: same visual, but typical TW/TH peer RANGES only (存貨 70–90
     天 · 應收 75–90 天 · 循環 ≈ 5 個月 · 凍結 ≈ 營收⅓), eyebrow 「台灣＆泰國同業常態」, disclaimer
     「非任何特定公司之數據」. DBD click-cards LOCKED in this mode (they carry the actual figures).
   - **Actual mode on demand**: presenter-window 🔒/🔓 button (or key N on the deck) flips
     `body.nums-actual` — the DBD version with the mandatory disclaimer, cards unlocked. Markup:
     wrap number-bearing nodes in sibling `.n-gen`/`.n-act` containers (SVG `<g>`, HTML block), CSS
     `.n-act{display:none!important}` + `body.nums-actual` inversions; never mix with `t-*` on one node.
   - **What-if slider (the convincer):** `<input type=range>` under the chart — 「存貨天數改善 −X% →
     釋放現金」, range/zones from NOVA §3 citable benchmarks (conservative −5% / typical −15–25% /
     best −40%, "DigiWin customers typically see"), default −15%. Generic mode outputs % of annual
     revenue; actual mode outputs ฿M + % of a year's net profit. `stopPropagation` on keydown; a
     colored "woken" slice on the inventory bar tracks the slider. Worked example: Dai-Ichi S9.
Build mechanics for the extra slot: shift scaffold ids N..21 → N+1..22 descending, clone the
`pain.3` light shell as the new section, renumber `slide-num` chrome to `NN / 22` post-splice,
renumber `specs/` + `visual_audit.tsv` rows, add the slot spec with `## Arc answers` covering the
authorization + 先讚後刀 + never-do lines. The `sections()` gate sorts by id, so ids MUST be renumbered
to presentation order (CLOSE = max id). See `docs/asia-polysacks-firstvisit/_qa/build2.py` for the
worked transform.

**★ NO-COPY LAW (gate-enforced `scaffold-v2` check): a new deck starts ONLY from
`docs/digiwin-2026-deck-design-system/_scaffold-firstvisit-v2.html`** (marker `<!-- SCAFFOLD:
firstvisit-v2 -->`) — never by copying a prior deck's index.html (that's how the SATS look bled into
every deck; Tatung/King Pac carry 278–368-line style forks). Corrections compound into blocks.css /
the scaffold — never fork per deck. Legacy pre-v2 decks: gate with `--no-sdd`; don't retrofit.

## Design & language law (enforced by the QA gates)
- **Warehouse-only** styling — digiwin MCP (`search`/`get_component`/`find_icon`/`get_token`), 12-col grid,
  8-pt spacing, semantic tokens (coral=pain, blue=reference/solution, navy=hero). No invented colors/icons.
- **Languages: 中 / EN / ไทย always; 日本語 ONLY when the main contact or a shareholder is Japanese (Peter
  2026-07-13 — supersedes the 2026-06-30 "日本語 always" rule).** The JA trigger is read from the OSINT decision
  map / group structure (JP JV, JP parent, JP strategic shareholder — e.g. Mitsui at SATS) and recorded in the
  content pack header. The deck DECLARES its languages in a comment near the top: `<!-- LANGS: zh,en,th -->` or
  `<!-- LANGS: zh,en,th,ja -->` — `slide_gate.py` reads it and enforces exactly the declared set (3-pill toggle
  default; 4-pill when ja declared). Within the declared set the old strictness holds: every text node carries
  a span per declared language via `t-zh`/`t-en`/`t-th`(/`t-ja`) (HTML **and** paired SVG `<text>`),
  active-language hero; a node missing a declared language is a gate FAIL.
  - **HOW (the generator — don't hand-add 150+ `t-ja` spans):** build the deck **trilingual first** (中/EN/ไทย),
    then run **`scripts/add_japanese.py extract <deck> map.json`** (dumps every unique `t-zh` inner as a JSON
    skeleton), author the 日本語 values in the map, then **`scripts/add_japanese.py apply <deck> map.json`** —
    it inserts a `t-ja` sibling after every `t-zh/en/th` group (HTML **and** SVG `<text>`), adds the 4th pill,
    and patches the lang CSS/JS. It refuses to apply with any empty/unmapped key (no silent drops) and is not
    idempotent (`strip` mode reverts). Intentional single-language nodes (e.g. a Thai-only legal name) are left
    alone — the gate's `quad-balance` requires span-count parity across the DECLARED languages (`t-th>=t-zh` for Thai). The gate also fails
    `ja-translated` if a `t-ja` is a verbatim CJK copy of its `t-zh` (Chinese left in the JP span).
- **Chrome ZONING — the language toggle owns the TOP-RIGHT alone; the notes / present-view control goes to the
  BOTTOM, never beside the toggle (Peter 2026-06-30).** With 4 pills (中/EN/ไทย/日本語) `#lang-toggle` is ~244px
  wide (≈298px in from the right edge). The old pattern of pinning `#present-view-btn` at `top:20px;right:236px`
  (sized for a 3-pill toggle) makes the **日本語 pill OVERFLOW into it — proven 62×39px overlap → the pill is
  unclickable** in click-presentation. So: top-right holds ONLY `#lang-toggle`, free to grow to N pills; put the
  presenter control in the bottom zone (`#present-view-btn` bottom-left → separate presenter window). **Never hard-code a
  top-right offset that assumes pill count.** The scaffold already zones this way; the `slide_gate` `chrome-zoning`
  check fails any deck that has `lang-ja` AND a top-right-anchored `#present-view-btn`.
- **Language PURITY** — each mode reads for its own audience; only verified technical/proper tokens stay in
  original (SKU, ECN, OTD, BOI, ISO, IATF, CMMI, VAT, PCBA, ERP, SMT, China+1, ภพ.30, ฿, Tatung, DIGIWIN,
  Amata). **日本語 = natural business Japanese for a JP reader (kanji+kana); do NOT leave Chinese-only phrasing
  in the `t-ja` span — 繁中 that isn't valid Japanese is a purity FAIL; keep only verified loan/tech katakana.**
  NO cross-language gloss lines. `_qa/lang_purity.py` must pass for **all FOUR** languages.
- **CJK line-break discipline** — wrap label segments in `<span class="nw">` so wrapping is only at semantic
  boundaries, never mid-phrase (e.g. 您現場可能正面對 / 的挑戰, not …挑 / 戰).
- **Visual slides → REQUIRED SUB-SKILL: INVOKE `digiwin-deck-visual` (Skill tool) — do NOT reconstruct it.**
  Before building OR fixing ANY slide's visual, **invoke the `digiwin-deck-visual` Skill and follow it** — do
  not approximate its method from this page. This deck owns arc/copy and names the visual router only so you
  recognize WHEN a visual is due; the canonical law (Step-0 judgment · the `gen_chart.py`/`gen_image.py`/
  `find_icon` router · `graphics-law.md` · `image-ops.md` · `acceptance-criteria.md` · the ship-gate) lives in
  that skill and must be **loaded, not remembered**. ▸ **Red flag — "I already know the chart engine / the
  law, I'll just inline it" → STOP and invoke.** Knowing the concept ≠ loading the skill; reconstruction
  drifts (it invents guidelines, hand-draws SVG charts = the shapes-combined trap, skips the image-ops
  recipes). One invocation per build covers every slide. Then, per slide, it DECIDES *"would a visual
  genuinely help here?"* — the **lightest type that does the job** (icon/pictograph → graphic → image) at
  **minimal scope**. **Add nothing when text alone is clearer** — many slides need no visual; never a
  full-bleed decorative image.
- **★ PAIN slides (S12–14) — DESIGN each visual FRESH from THIS pain's mechanism; batch-copying the reference
  (King Pac) organism + a swapped number is the #1 regression (AUTO-FAIL).** Run the per-slide Step-0 +
  visual-serves-message audit on EVERY pain slide individually — never reskin the prior deck. Per
  `digiwin-deck-visual`, the viz STRUCTURE must DEPICT the pain (its shape argues it): yield-loss → part-whole
  donut (97/3 — King Pac), traceability → genealogy tree, flow loss → sankey, **working-capital squeeze →
  diverging bars (revenue ↓ vs inventory+AR ↑, indexed 100/91/151), NOT a lone "65% · 示意" dial that argues
  nothing**. A gauge with a bare illustrative round % = AUTO-FAIL (removal-test fail; worse than text).
  (Burn 2026-06-30: Everydayhappy / P.Inter / Win Chance S12–14 degraded into reskinned King Pac copies —
  "slapping on numbers" Peter rejected.)
  When the answer is yes, it produces + verifies the asset to its law (`GRAPHICS-STANDARDS.md` /
  `graphics-law.md`). **Before slotting ANY visual in, the deck challenges it — *"are you sure you're doing
  your real job?"* — and rejects placeholders (a shape/box behind-or-beside text, a dumped image, generic
  filler, a restatement) via the real-job test (convey / convince / attract + removal test).** Deck owns
  arc/copy; the visual skill owns the *whether/which/craft*. Runs in this same main loop (sighted gate holds). **Architecture (LOCKED): visual accept/reject NEVER leaves the sighted main loop — do NOT delegate visual judgment to a sightless sub-agent; a sub-agent may only do MECHANICAL sourcing (download the customer’s real logo/plant photos/cert, draft SVG markup) and hand back files for the in-loop render-and-READ. The visual skill SOURCES real assets (mode B), not just graphics.**
- **Chrome**: fit-to-window on load (no white gutters, no F needed) + top & bottom chrome auto-hide ~1.5s.
- **CONTACT INVARIANT (from now on — Peter 2026-06-25) — contact + LINE QR on the FIRST and LAST page,
  CO-LOCATED with 簡報人, NOT a separate top-right card.**
  - **Cover:** put it INSIDE the existing `簡報人 (Peter Lo · Digiwin Thailand)` meta-block — `.meta-block.presenter`
    = a `.pv` column (label · `Peter Lo · Digiwin Thailand` value · then **email and phone on SEPARATE `.value-sub`
    lines**, ~18px, segmented `0XX-XXX-XXXX`) + a `.pqr` holding the QR `<img>` beside it. **No duplicate "Peter Lo"
    and no second card** — there is already one Peter on the slide (the burn: a top-right `.cc-tr` repeated the name).
  - **Close:** ONE centered group `.contact-card.cc-strip` (bigger QR `<img>` + a stacked `.cc-t`: `<b>Peter Lo</b>`,
    email, phone) — a single group, never a duplicate card.
  - **The QR is self-evident — do NOT add an "加 Peter 的 LINE / Add on LINE" label** (the green LINE badge already
    says it; Peter cut the label as redundant). Make the **QR big** (cover ~124px, close ~120px), email/phone bigger
    on their own lines (so it's distinctive, not cramped on one small line).
  - **Asset:** branded LINE QR `assets/peter-line-qr.png` (copy from a sibling deck) — navy `#000864` modules on white
    (smart-blue is too light to scan), green LINE badge kept. Add `.contact-card` to the `overlap_check.py` SKIP list.

## QA gates (MANDATORY — run before declaring done / promoting)
Use miniconda python for Playwright: `/opt/homebrew/Caskroom/miniconda/base/bin/python3`.

**★★ THE PRE-DEPLOY GATE — one checklist, machine-ENFORCED, then deploy (Peter 2026-07-25, the Asia Polysacks "hideous" burn).** Every mechanical gate below can be GREEN while the deck is ugly — that's exactly what shipped Asia Polysacks (all green, yet `VALIDATION.md` 3/15, zero languages rendered, `digiwin` MCP never shopped). So the individual gates are now wrapped by **`scripts/preflight.py <deck/index.html>`** — the single ordered definition-of-done in **`references/pre-deploy-checklist.md`** (READ IT). preflight runs Gates 1/3/4-evidence and STAMPS `_qa/preflight.json`; **`build_portable.py` physically refuses to build/ship unless that stamp is `ok:true` and its hash matches the exact `index.html`.** It enforces: all mechanical gates exit 0 · `VALIDATION.md` N/N · **fresh render PNGs exist for EVERY declared language** (the all-language READ I skipped) · `_qa/design-shopping.md` proves the MCP was shopped (`find_icon`/`get_component`/`get_token`). The machine floor can't see "sliver photo / wrong-language legend / jagged giant-Thai" — so after `✅ DEPLOY-READY` you STILL READ every PNG it lists (the sighted ceiling) and show Peter the packet. Emergency bypass = `build_portable.py --force` (loud, logged — never routine). **Gate 0 (inputs current): before building, check the VP playbook mtime for newer coaching + consult NOVA live — attest both in `_qa/design-shopping.md`.**

**0. ⭐ `scripts/slide_gate.py <deck.html>` — the HARDWIRED per-slide checklist. Run FIRST and after EVERY edit; it exits non-zero until ALL GREEN. Redo each ✗ until green.** Anti-skip gate (Peter 2026-06-29: *"a checklist for you to complete so that if a slide does not have the correct outcome, you go back and redo it until it is done"*). It composes lang_purity + overlap + **svg-fit** (`svg_fit_check.py` — fails when an SVG `<text>` overflows the `<rect>` it sits in, in any declared language; the blind spot overlap_check skips since it treats an `<svg>` as one block — the Unilever S15 Thai burn 2026-07-14) and enforces, per slide:
   - **VISUAL on every content slide (2–15)** — must contain a real `<svg>`/`<img>` (graphic · pictograph · photo). **TEXT-ONLY FAILS** — a wall of text, text-cards, or a big *styled number* is NOT a visual. Add a communicative DigiWin pictograph (`/digiwin-deck-visual` → MCP `find_icon`) or a graphic that ARGUES. (Audiences fatigue after 2–3 text-only slides — Peter.)
   - **no `IoT` / `物聯網` / `即時數據` / "real-time data"** framing on a first visit — don't trigger IoT/sensor thinking; frame eMES as *visibility & management* (「看得見、管得到」), not real-time data feedback.
   - **no pricing/quote · pains hedged (`產業普遍現象`) · contact+LINE-QR on cover & close · Tax ID on the snapshot · no stale template names (Tatung/大同/…) · no leftover DRAFT/PENDING-NOVA · fit=clientWidth** (else white columns show beside dark slides).
   - **content must NOT OVERFLOW into the footer** — `overlap_check.py` now flags content spilling onto the brand-mark/tour-mark. **ALWAYS run every DECLARED language (`<!-- LANGS: ... -->`)**: EN/TH leads run longer than ZH and spill into "DIGIWIN…" where ZH fits (the S6 burn 2026-06-29). Fix by shortening the lead / tightening spacing, not by letting it ride.
   - **EMPHASIS — every content slide marks its essence** in a `.em`/`.hl` highlight (so the audience catches the page's point at a glance; the gate fails a slide with none). Keep the lead short, then emphasize 1–3 load-bearing phrases — not over-marked.
   - **INFORMATIVE graphic — every content slide either IS an informative graphic** (a real photo · a rich multi-element SVG · a recognized informative-organism class) **OR declares `<!-- VIS-LITE: reason -->`** when a number/icon/text is deliberately the argument. A bare decorative slide with no justification FAILS; the gate prints the **VIS-LITE upgrade worklist** every run so icon/number-only slides can't hide. (Then the sighted READ gate judges whether it's *truly* informative.)
   - **`svg-robust` — no `filter=` (blur/glow) on a `<line>` or stroke-only (`fill="none"`) `<path>`/`<polyline>`.** A thin/straight connector has a ~zero-area bounding box, so a filter region is empty → it paints **BLANK in the PDF and in non-Chromium browsers** while my Chromium screenshot leniently shows it (the S8 centre-line burn 2026-06-29: I kept "verifying" a connector the customer couldn't see). Use a solid stroke; glows belong only on shapes with real area.
   - **`no-placeholder` — un-relabeled scaffold placeholder visuals = FAIL (Peter 2026-07-01, the recurring deck-visual SKIP).** The gate now objectively fails a bare `<circle>`/`<rect>` icon (the scaffold's empty `.ic`) or an **unlabeled shape diagram/rail** (inline SVG with shapes but **no `<text>`** — the S11 empty-rail + S2 empty-circles burn). These passed `visual`/`informative` before because "an `<svg>` exists" ≠ "a visual argues." No honesty needed — it's a signature match. Fix = rebuild via **`/digiwin-deck-visual`** (a communicative `find_icon` pictograph, or a LABELED diagram). ▸ **`/digiwin-deck-visual` is NOT optional final polish — it is a MANDATORY GATE STAGE; the deck is not done until EVERY visual clears it.** (See that skill's top block + the size/staged≠done/answer-the-request criteria.)
   - **`pain-argues` — the sighted audit is now LOAD-BEARING for pain slides (S12–14), not decoration (Peter 2026-06-30).** A templated dial passes *every other* mechanical check (it has an `<svg>`, an `.em`, an org-class) yet argues nothing — so the gate now binds a pain slide's green light to its **`_qa/visual_audit.tsv` row**: green ONLY at `serves=Y`, `verdict ∈ keep|simplify`, and a **filled `note` = the per-pain CONTRACT** (which mechanism the SHAPE encodes, designed fresh — NOT a swapped number on the reference organism). Missing row / `serves=N` / `re-tool` / `remove` / blank note = **FAIL**. **`verdict` = REMAINING action** (keep/simplify = shippable; re-tool/remove = work remains) — log *history* in the `note`, never in `verdict` (the King Pac ledger ambiguity). Ledger header: `# slide⇥message⇥serves(Y/N)⇥layout(Y/N)⇥verdict⇥note⇥stranger-says`.
   - **`speak-test` — ENFORCED col 7 `stranger-says` (Peter 2026-08-11 "shrink the gap").** For every hedged-pain slide AND every `pq-chart` data slide, the row must carry **ONE sentence: what a stranger says the visual MEANS with all copy covered** (≥15 chars, not the headline restated) — else the gate FAILS. This converts the most judgment-heavy sighted step into a forced artifact any builder (any model) must produce, and Peter can spot-check the claim against the PNG in seconds. Can't write the sentence → the visual doesn't argue → redesign via `/digiwin-deck-visual`, then fill the row. The floor forces the artifact to exist; whether the sentence is TRUE of the render stays a sighted judgment. (Two bugs fixed 2026-06-30: the gate had been reading the ledger from the *script* dir → always empty; and the verdict never touched the exit code → a `re-tool` dial shipped green. Both closed.) ⚠️ **LIMIT — the gate cannot detect a DISHONEST `keep`** (P.Inter shipped `keep` rows while degraded). It forces the contract to exist and blocks explicit needs-work verdicts; it can't verify a truthful keep. **The sighted READ (gate 3) + show-Peter stay mandatory — the audit row is the floor, the eyes are the ceiling.**
   **At build start, TodoWrite one item per slide; a slide is "done" only when the gate is green AND you've READ its PNG.** Mechanical pass ≠ good: the gate gates *structure*, the sighted READ gate (3) gates *craft*. Both mandatory.
   **▸ Build-level TodoWrite tripwire: `[ ] digiwin-deck-visual Skill invoked before authoring any visual` — if any slide's chart/photo/diagram was hand-made WITHOUT first loading deck-visual's law, that slide is NOT done; redo it through the skill.** (A `slide_gate.py` check can confirm a visual EXISTS but cannot see whether the skill was loaded — this human tripwire is the backstop.)

1. `scripts/lang_purity.py <deck.html>` → pure in zh / en / th.
2. `scripts/overlap_check.py <deck.html>` → 0 content-block bleeds in every declared language.
3. `scripts/render_trilingual.py <deck.html>` → **READ every PNG in every declared language, and run the per-slide
   VISUAL-SERVES-MESSAGE AUDIT** (Peter 2026-06-29 — the gate proves a graphic *exists*; this proves it *works*).
   **For EVERY slide, with `/digiwin-deck-visual`, ask & log a verdict:**
   1. **What is this slide's ONE message?**
   2. **Does the visual SERVE it — comprehensible at a GLANCE?** Or does it force the audience to read / confuse them? (A "real" chart that confuses still FAILS — the S12 sankey burn; replaced with a yield donut.)
   3. **Do we even NEED a graphic here** — or would icons / a glanceable headline be clearer? (S2 was a wall of words → trimmed to icon + headline + one line.)
   4. **Right TYPE / tool?** (the router — S3 was a concept mis-tooled as flat SVG → rebuilt as a nano-banana illustration.)
   5. **Professional LAYOUT?** vertically **balanced** (no dead void / top-loaded — the S15 burn), nothing off-centre that should be centred, on the 12-col grid + 128px margins, ONE primary block, chrome zones clear, fills the 888px budget.
   6. **Does the ENCODING agree with the message?** Read ONLY the shapes — arrows, sizes, positions, colours — and check you reach the same conclusion as the headline. Arrows point the way the force/flow truly goes (the S3 burn: 售價↓ + 成本↑ must converge *inward* on 利潤 to read "squeeze"); bigger = the thing that's actually bigger; coral = pain, never inverted. A visual whose encoding contradicts the words teaches the opposite — rebuild it.
   Verdict each: **keep / simplify / re-tool / remove**; rebuild the fails. Subagents are sightless — this audit stays in the sighted loop, then **show Peter the PNGs**.
6. **MEASURABLE OUTPUT — `scripts/slide_gate.py <deck> --report` → `VALIDATION.md`** (Peter 2026-06-29: "an output that can be measured to verify the work is actually done, per section"). A per-slide scorecard: **Mechanical · Serves-message · Layout**, each ✅/❌ → `N/N slides fully validated`. Maintain `_qa/visual_audit.tsv` (the sighted ledger: `slide ⇥ message ⇥ serves ⇥ layout ⇥ verdict ⇥ note ⇥ stranger-says` — col 7 gate-enforced on pain/chart slides). **Promote ONLY at N/N fully validated** — not "15 slides exist," but every section validated on all three dimensions.
4. Open the deck fresh in a browser → fills the window on load (fit check).
5. **Specificity gate** — for every slide 5→15: "could this appear in any company's deck?" If yes, it failed —
   re-ground it in the Phase-0 industry + company briefs. Industry-focus must show depth in THEIR sub-industry,
   pains must be that industry's owner pains. (This is the anti-templating check; it is NOT optional.)

## ⭐ AUTONOMOUS SELF-REVIEW — the hands-off contract (Peter 2026-06-29)
**Goal: given (1) the OSINT gold-standard and (2) Nova's reply, build a ship-quality deck end-to-end with ZERO Peter intervention until ONE final review.** Peter spent a full day hand-correcting King Pac (S2 wall-of-words, S3 mis-tooled *then* arrows-backwards, S8 connector gap *then* blank-in-PDF, S12 confusing chart, S15 off-centre, ugly logo crop). Every one was a place I declared "done" on a green gate and the deck still failed in his hands. The fix is not more hand-holding — it is a disciplined loop where **I PLAY PETER** before he ever looks.

**The loop (repeat until it converges, then show Peter once):**
1. **Build / fix** the slide(s) per Phase-0 specificity + the tool-router.
2. **Mechanical gate** — `slide_gate.py` to ALL GREEN (structure floor; redo each ✗).
2b. **Design-quality gate (Impeccable) — the STANDING step right after the DigiWin brand gate (Peter 2026-07-01).** `scripts/impeccable_gate.py <deck.html>` runs Impeccable's `detect.mjs` and **BLOCKS** the AI-UI tells the brand gate CANNOT see — side-tab / border-on-rounded / nested-cards / gradient-text / glassmorphism / low-contrast / tiny-text / text-overflow / cream-palette / marketing-buzzword; **advisory-only** (never blocks) for the DigiWin false-positives-by-design: page-numbers (NN/NN), brand-navy hero, CJK 破折號, brand eyebrow. Redo each BLOCKING ✗. *On-brand ≠ well-designed: the PLIC deck passed the brand gate ALL-GREEN while carrying side-tab stripes + a dead-space float — this gate is why it's standing.*
3. **Sighted adversarial review — be the harshest version of Peter.** Render trilingual AND **export the actual deliverable** (see below); READ every page in 中/EN/ไทย/日本語 and run the 6-question visual-serves-message audit *against `references/acceptance-criteria.md`* per slide. Assume each slide is wrong until proven right: is the message glanceable? right visual type? **does the encoding AGREE with the claim** (arrows/sizes/colours)? balanced layout? real assets, cleanly cropped? Log a verdict in `_qa/visual_audit.tsv`. **Then invoke the `impeccable` Skill → `critique` for an independent design-director READ** (AI-slop verdict, hierarchy, dead-space, composition, contrast-at-distance) — the mechanical gates can't see composition; the PLIC S11 dead-space float passed every mechanical check and only the sighted critique caught it.
4. **Fix every fail and GOTO 2.** A slide is done only when mechanical-green AND the adversarial review finds nothing. `--report` → `VALIDATION.md` must read **N/N fully validated**.
5. **Only then, ONE consolidated show to Peter** (the PNGs + VALIDATION.md), not a stream of half-checked slides.

**VERIFY THE ARTIFACT PETER OPENS, not just my render.** My Chromium screenshot and the exported PDF/other browsers **diverge** (the S8 blank-line burn). So the sighted pass renders the live HTML *and* exports the PDF per language and READs those pages — the deliverable is the source of truth. Fragile constructs that cause divergence (SVG filters on thin/degenerate paths) are now banned by the `svg-robust` gate; if a NEW divergence appears, fix the instance **and add a mechanism** (a gate check or an acceptance criterion) so it can't recur — that is how the day's-worth of corrections compounds into autonomy instead of repeating.

**Turn every NEW defect into a mechanism, not just a fix.** When the adversarial pass (or Peter) finds a class of error not yet covered: (a) fix it, (b) add the rule to `slide_gate.py` if mechanically checkable or to `acceptance-criteria.md` if it's a judgment, (c) note it in memory `[[feedback_deck_build_gate]]` / `[[feedback_deck_visual_sourcing]]`, (d) re-sync the gate to both deck skills. The bar: the next deck never needs Peter for a defect a prior deck already taught.

## Hard rules
- **Every content slide earns a VISUAL — no all-text slides** (gate-enforced; a styled number is not a visual). Choosing/finishing the visual is **`digiwin-deck-visual`'s job** — invoke it (see the REQUIRED SUB-SKILL gate above) and hand it a **brief** (data · message · canvas · tier); it owns the TYPE router (chart-engine vs illustration vs SVG vs photo) and the "never hand-draw a chart" rule. Don't re-derive that here. (King Pac S12–14: number+icon → ECharts sankey/gauge/lot-genealogy tree.)
- **The agenda (S5) is RE-THOUGHT per deck to preview THIS deck's core message — never a reused template rail/wave.** Ask: does this agenda fit King Pac's "SAP runs the office, the floor is dark, we light it" story, or is it a carried-over scene? If carried-over, rebuild it to the message. (Peter 2026-06-29.)
- **Solution / method slides show the RELATIONSHIP, not parallel lists.** e.g. eMES = the SAP-brain's *eyes & nerves ON the floor* — one connected top-down structure (brain → nerves → machine stations), not a "process row" sitting beside a "capability row" talking past each other. (Peter 2026-06-29: "they're two parallel lines.")
- **No IoT / real-time-data framing on a first visit** — eMES = visibility & management of the floor for SAP, not sensor/IoT data-streaming (don't make the owner think IoT from the start). (Peter 2026-06-29.)
- **Highlight the load-bearing phrases in any long body sentence/lead** — wrap them in `.em` (bold royal-blue `#003CC8` on light slides, cyan-glow on dark) so the reader tracks the point through a long line; a wall of uniform text loses them. Keep the lead short first, *then* emphasize 2–3 key phrases. (Peter 2026-06-29.) `.em{font-weight:700;color:var(--royal-blue)}` + `.dark-sec .lead .em{color:var(--cyan-glow)}`.
- **No pricing, no quote, no product feature-dump.** The close is a 動機 question + interest-check, NOT 收單.
- **No courtesy visits (VP, 2026-07-01 — [[feedback_vp_qualification_discipline]]).** The presenter notes drive
  **摸底 before we invest** (scale/budget-signal/magnitude, read from signals not claims); before a physical visit,
  broker a **consultant ↔ their key window pre-call** to focus scope. A blind walk-through wastes both sides' time
  and reads as unprofessional; lead the customer's rhythm, distrust a claimed deadline until verified.
- **Pains are hedged industry scenarios** — never claim the client's numbers; **never recite their financials**
  to them (VP veto). Use OSINT only to steer the presenter's live questions.
- **Cross-strait**: Taiwanese-owned customer → Taiwan positioning, no China market/listing references.
- **eMES not SFT/SFC**; iGP has no APS; respect the product portfolio rules.
- Work in a `*-draft.html`; promote to the live file only on Peter's "promote". `index.html` stays untouched until then.

## Build process (gated) — CONTENT-FIRST + SDD (Peter, 2026-07-13; supersedes the compose-directly flow)
**The change and its why:** content and layout used to be decided simultaneously in "compose", so every
content problem surfaced as a render-time layout problem (overflow across languages, footer spills, reskinned
visuals) — months of post-build iteration, with Peter's corrections landing at the MOST expensive point (after
15 slides × N languages were rendered). The fix is kitchen-prep: ALL content is prepared and specified as TEXT,
Peter approves it as text, and only then does HTML get built. Tatung had this tier (`SPEC.md` + `specs/01–14`)
and it decayed because nothing enforced it — so now `slide_gate.py`'s **`sdd-match`** check refuses a deck
whose slides lack a spec or drift from one. Reference implementation: `docs/sats-firstvisit/` (content pack +
SPEC.md + specs/), alongside Tatung.

A. `/digiwin-research-company` (if no gold standard) → read OSINT. **Know the audience:** the 核決者/owner profile from
   the OSINT decision map is the header of the content pack — every slide's copy is written AT that reader.
B. **PHASE 0 — Industry × Company Inquiry** (above): industry research + company brief → **inquiry sheet**
   (`inquiry-<company>.md`) that prompts Peter → Nova handoff → lock the core question, industry-focus framing,
   the owner-resonant pains, and the resonant close. Nothing slide-5+ is designed until Phase 0 decides it.
C1. **CONTENT PACK — `content-<company>.md` (kitchen prep; template: `references/content-pack-template.md`).**
   Every slide's message, audience note, **source fact** (the OSINT/Nova line it's grounded in — a slide with
   none is templated by definition), full copy in every shipping language written TO length budgets, exact
   chart data, and named assets with provenance. **NO layout talk in this file.** Copy that doesn't fit its
   budget is not prepped — a budget violation discovered later is a CONTENT bug (fix the copy, not the layout).
C2. **SDD — `SPEC.md` (arc table + locked decisions + story-thread check) + `specs/NN-<name>.md` per slide,
   FULL Tatung depth (template: `references/slide-sdd-template.md`).** Each spec: Act/role · frozen message ·
   source fact · illustrative SCENE with the metaphor contract (designed for THIS company, never a reskin) ·
   warehouse parts (**block + variant — layout is a block choice, never freeform**; a new arrangement = a new
   block/variant in `blocks.css` so every deck inherits it) · visual routing (engine + output file) · layout
   zones/emphasis/rhythm · per-slide gate criteria. Specs are authored by the model — full depth costs the
   model, not Peter.
C3. ⭐ **PETER CHECKPOINT — approve C1 + C2 as TEXT, before ANY HTML.** Present the content pack + SPEC.md arc
   table (spec files on request). Peter's corrections land here, cheaply. Build starts only on explicit
   approval. Escape hatch: "just do it" skips the checkpoint (executor mode) — C1/C2 are still produced.
D. **Build strictly from the SDD — compose from the BLOCK LIBRARY. Reuse the LOOK, adapt the ARC:**
   - **REUSE always — the blocks** (`system/blocks.css`): look/layout/craft. This is the consistent part (the
     brand) and where every past correction lives. Do NOT hand-roll slide bodies from primitives.
   - **ADAPT every time — the arc, content, and which-blocks-and-how-many.** The scaffold
     (`docs/digiwin-2026-deck-design-system/_scaffold-firstvisit.html`) is a **DEFAULT arrangement, not a cage.**
     Copy it → `docs/<deck>/index-draft.html`, then shape it to THIS company: a block can appear **0, 1, or N
     times** (4 pains → four `.pq`; no squeeze → drop S3; group → two `.s6-grid`); add/remove/reorder slides. The
     gate is **count-agnostic** (12 or 18 slides pass) — renumber the cosmetic `slide-num`/nav denominators.
     **Phase-0 (OSINT→Nova) decides the actual arc + content** — never robotically fill the 15 default slots; the
     specificity gate ("could this slide be any company's deck?") still applies to every slide.
   **Fill every `{{TOKEN}}`** from the content pack + SDD (never improvise copy at build time); copy `assets/`
   (peter-line-qr, cert, real customer logo/plant photos, generated charts) in; author the presenter notes from
   the content pack's note-seeds (the live 六要素 script). **If a block's craft needs a change, fix it in
   `blocks.css`** (every future deck inherits it) — never fork an organism into one deck. A one-line deck-local
   *layout-arithmetic* tweak (e.g. a 4-col card grid) is fine; a *craft* fix is not. See `BLOCKS.md` (catalog +
   the Mix & match recipes). **A mid-build discovery that forces a content/layout change goes BACK INTO the
   content pack / spec FIRST, then the slide is rebuilt** — the spec never lies about the artifact.
E. Run all QA gates (incl. **`sdd-match`** + the specificity gate) + render-and-READ every shipping language
   (per the deck's `<!-- LANGS: ... -->` declaration) → show Peter PNGs. With C3 done, this show should be
   near-zero surprises — corrections here mean C1/C2 missed something; feed the lesson back into the templates.
F. On "promote": copy draft → live, rebuild PDFs ×3 (magick) + portable single file (`scripts/build_portable.py`).
G. **Vercel deploy — ALWAYS rebuild the portable from the CURRENT `index.html`; NEVER deploy a hand-aged
   `_deploy/*-public` export (king-pac burn 2026-06-30).** The `*-public/index.html` deploy copies drift from
   the working deck — deploying them ships an OLD or broken deck. The deck references the design-system
   `slides.css` (which `@import`s `tokens.css`); served standalone that `@import` does NOT resolve → **CSS
   vars empty → every dark slide renders WHITE** (king-pac shipped white this way). So:
   `python3 scripts/build_portable.py docs/<deck> --public docs/_deploy/<deck>-public` → the build inlines +
   resolves tokens and **GUARD-asserts the portable is fully self-contained (no unresolved tokens `@import`,
   no leftover `assets/`, no external design-system ref); it exits non-zero rather than emit a deployable
   broken file.** Only on GUARD OK → `cd docs/_deploy/<deck>-public && vercel deploy --prod --yes`. Then
   **load the live URL and READ it** (dark, current content) — the `?cb=` cache-buster forces fresh.
H. **REGISTER the deck in the pipeline — a deck built for a lead MUST appear in Deals + Deck Tracker automatically, not by hand (Peter 2026-07-01).** After deploy, run
   `.venv/bin/python3.13 database/register_deck.py --taxid <13-digit> --company "<name>" --type first-visit --link <vercel-url> --version v1 --status "✅ Done" --commit`.
   It **upserts the Deck Tracker row** (keyed on Tax ID; Company/Stage/Industry/OSINT auto-pull via formula) and **ensures a Deals stub exists** (never overwrites an existing deal's Stage/Next-Action — a new stub leaves Stage BLANK for Peter to set). Idempotent; dry-run without `--commit` first. Also true for a **local-only** build (deck done, no deploy yet): register it with the local status so it shows in the tracker.

## Reference
- **BLOCK LIBRARY (compose, don't hand-roll): `docs/digiwin-2026-deck-design-system/`** — `system/blocks.css`
  (the pre-corrected slide-body organisms, each header naming the rule it bakes in) · `BLOCKS.md` (the catalog:
  block · use-when · rule · gate guard) · `_scaffold-firstvisit.html` (blank 15-slide arc wired to the blocks —
  the build starting point). **Every correction Peter makes goes back into `blocks.css`/`slide_gate.py`, not into
  one deck** — that's how the per-deck re-correction stops (Peter 2026-06-29).
- **CONTENT-FIRST templates: `references/content-pack-template.md` (C1) + `references/slide-sdd-template.md`
  (C2, incl. the per-language length-budget multipliers)** — the kitchen-prep + SDD tier (Peter 2026-07-13).
  Reference implementation: `docs/sats-firstvisit/` (content-sats.md + SPEC.md + specs/), alongside Tatung's specs/.
- **Per-section ACCEPTANCE CRITERIA: `references/acceptance-criteria.md`** — the measurable bar each slide must
  clear (GLOBAL + per-section, on Mechanical · Serves-message · Layout). The validation source of truth; `slide_gate.py --report` scores against it → `VALIDATION.md`.
- Reference implementation: `docs/tatung-thailand-firstvisit/` (deck + `specs/01–14` per-slide specs +
  `SPEC.md` / `REDO-SPEC*.md` build history + `GRAPHICS-STANDARDS.md`).
- **VP qualification discipline: [[feedback_vp_qualification_discipline]]** — the rep's discovery/qualification
  standard baked into the presenter notes + close (摸底 before invest · no courtesy visits · lead-not-follow ·
  read the buyer's 面 vs 點). Full playbook = Obsidian `Internal/VP Cheng - Sales Methodology.md` Part 18.
- Related: `/digiwin-erp-proposal-deck` (next-stage tier) · `/digiwin-research-company` (OSINT) · `/nova-*` (discovery lenses)
  · `/digiwin-deck-visual` (graphics + image specialist, per GRAPHICS-STANDARDS.md).
- STATUS: scaffolded 2026-06-24 (build-now / harden-after-approval). Harden = extract clean template assets
  (system CSS + a blank cover/arc), add an eval set, after the Tatung deck is approved.
