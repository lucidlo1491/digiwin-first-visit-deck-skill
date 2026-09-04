# Arc Questions — the interrogation every slide must pass BEFORE it may be generated

> Mandated by Peter 2026-07-25 ("what questions will each slide/arc be asking before the slides are
> generated?" — the cure for "you copied this from the SATS deck; evaluate what is needed to fit what
> I want"). Arc + rules per VP Cheng's 2026-07-25 revamp (12 slots / 5 acts, 痛 before 信).
>
> **THE RULE: a slide may not be spec'd (`specs/NN-*.md`) until its questions below are answered WITH
> SOURCES.** Each spec opens with a required `## Arc answers` section — one line per question:
> `Qn.n → <answer> → 【source-tag】`. `slide_gate.py sdd-match` FAILS a spec whose `## Arc answers`
> is missing or has an empty answer. An honest "unknown — must learn in the meeting" IS a valid
> answer (it routes the item to presenter notes); a blank or a guess is not.

**The spine every deck serves (VP verbatim):** 把老闆從「我不需要你們的系統」搬到「我連自己這張訂單賺多少
都算不出來——這件事越早做越省」，然後只跟你約下一步。**賣「算得清楚」的價值，不賣一套系統。**

---

## GATE 0 — deck-level (answer before ANY slide; record in the content-pack header)

**FIRST, establish which path this deck is on (added 2026-08-31). Do not attest it — RUN it:**

```
python3 .claude/skills/digiwin-first-visit-deck/scripts/check_inputs.py <company-id> "<company name>"
```

It verifies the dossier is promoted (not a draft), that the dossier is not STALER than a recorded
meeting, and returns the path. Peter records every phone call, so "no verbatim" is rarer than this
gate assumed — the transcript usually exists and simply was never looked for.

**PATH A — RECORDED** (a call or meeting happened and was recorded):

- **Q0.1 Who is in the room, and who is the 核決者?** Every person's name/title verified against a
  source (card, DBD, transcript) — never inferred. (Burn: "Peera was never Peter!!!")
- **Q0.2 What did the customer SAY, verbatim?** His priority order, his words, his objections —
  traced to the recording/notes with timestamps. The deck honors his framing before ours.

**PATH B — COLD** (genuinely no prior contact):

Q0.1 and Q0.2 above are unanswerable, and answering both "unknown" every time makes the gate stop
discriminating. On a cold visit the deck's job is to **EARN his framing, not reflect it** — which is
what this skill's own discovery law already says (anchor → react; his 「不知道」 IS the surfaced pain).

- **Q0.1c Who do we EXPECT in the room, and which of them is unverified?** From the DBD signatory
  and the dossier's decision map. **Nobody may be named as 核決者 without a source** — that guardrail
  is what the Peera burn bought, and it holds harder when we have no card at all. A name heard on a
  phone call is NOT a verified source for authority; it establishes pain and process, not identity.
- **Q0.2c We have no verbatim, so: what industry framing will he NOD at, and what is the ONE question
  that produces his verbatim in the room?** Sourced from the reusable industry brief
  (`docs/industry-briefs/`) plus the dossier's hedged field pains. The answer to Q0.2c is the deck's
  actual instrument — everything downstream exists to get him talking.
- **Q0.3 摸底 state:** what do we already know of **scale / budget-signal / pain magnitude** from
  SIGNALS (what they run, size, behavior — never their claims)? What must THIS meeting learn?
- **Q0.4 Inputs current?** VP playbook mtime checked for newer coaching · NOVA live consulted on
  framing / pains / close · OSINT dossier promoted. Attest in `_qa/design-shopping.md`.
- **Q0.5 Which vertical anchor pack and which languages?** (`<!-- LANGS: ... -->`; ja only on a JP
  contact/shareholder.)
- **Q0.6 What is the ONE next step we want booked — sized to the meeting format?** (lobby ≠ factory;
  a heavy ask in a light venue kills the close. VP: 沒約到=白跑.)

## ACT 1 — 定調 + 他的世界 (disarm, mirror, homework)

**S1 `cover.disarm`**
- What ONE sentence disarms THIS owner — ideally echoing his own words back? ("today = your next
  step, not a sale")
- What is the meeting frame (venue, who invited whom, warm/cold)?
- What must the cover NOT promise? (no product name as the headline, no price, no "solution")

**S2 `industry.mirror`**
- What is his EXACT sub-industry — never "manufacturing"? (woven-PP/FIBC, not "plastics")
- Which 2–3 squeeze facts are TRUE and SOURCED for that industry (cost structure, buyer pressure,
  compliance)? Would he nod at each?
- What closing question does the slide end on that he CANNOT answer? (the mirror's job is the nod
  + the first "…I don't actually know")

**S3 `company.snapshot`**
- Which PUBLIC facts prove homework WITHOUT financials? (Tax ID, founding, certs, capacity,
  milestones — DBD/site sourced; client financials NEVER on a slide)
- What one-line situational read shows we understood his position, not just scraped it?
- Which REAL logo / plant photos, with provenance? (photo-free when real assets exist = miss)

## ACT 2 — 痛 · 老闆的高度 (the heart of the deck)

**S4 `owner.question` ★peak**
- Walk **人機料法環** against HIS cost structure: 人 (labour/piece) · 機 (amortization, maintenance)
  · 料 (material + WIP + dead stock) · 法 (regulatory) · 環 (environmental/fire) — where exactly is
  THIS owner cost-blind?
- What is the sharpest can't-answer question — NOVA-consulted, one sentence, 一句入魂?
- Confirm anchor→react: the question invites a reaction to OUR anchor; it never demands he
  self-quantify. His 「不知道」 IS the wedge (C2), not a failure.

**S5 `owner.threepoints`**
- How does each point map to a FACT of his? ①算得出成本 (which cost is invisible to him today)
  ②降低浪費 (which waste is visibly growing) ③戰略決策依據 (what decision is he making blind)?
- Which of the three is PRIMARY for this owner — and does the slide's emphasis follow that?
- Is every claim owner-language (money, decisions), zero feature-language?

**S6–S8 `pain.1/.2/.3` — answer per pain**
- WHY this pain, in this order? (felt-first: his verbatim #1 leads; value pains climb after)
- What INDUSTRY-GENERAL anchor hedges it (產業普遍現象 · 非貴司特定數據)?
- What is the react-question? (never 「一個月幾次 / 每天多少張 / 成本多少」 — the Everydayhappy
  silence burn)
- What MECHANISM must the visual DEPICT — would the finished slide FAIL the swap test (unusable for
  any other company)? A reskinned prior organism with swapped numbers = AUTO-FAIL.
- What ฿ figures stay in presenter notes ONLY (VP R1)?

## ACT 3 — 信 (minimum credibility, after the pain)

**S9 `whyus.vertical`**
- Which ONE vertical do we narrow to for him? (塑膠/金屬/汽機車… — VP: 收斂, never all-sector)
- Which in-country proof is relevant to HIM (Thai logos, 泰金寶-class anchor; reference-approved
  only, live deals never named)?
- What is the 10-second version? (45yr · 55k clients · your vertical · local — one breath)

**S10 `proof.strip`**
- Which 3 risk-killers does THIS buyer actually need (local team? CMMI? Revenue-Dept compliance?
  e-Tax hook?) — one LINE each?
- What gets CUT? (default: everything else. One page of proof, never five — VP: 賣公司的頁一律砍)

## ACT 4 — 路 (product-by-maturity)

**S11 `firststep.board`**
- What is his system maturity TODAY — incumbent NAMED (AX/Express/Excel…), and what stays?
- What is the lightest first block HE already asked for (先上車)? One block, not a suite.
- What rides on what? ("on top of X, feeding X, never replacing X" — the exact sentence)
- What is explicitly DEFERRED to phase 2 (and framed as "already there when you're ready")?

## ACT 5 — 收

**S12 `close.nextstep`**
- What CONCRETE next step — what, where, who attends, how long? (bookable in the room)
- What two-layer motive: org (survival/value math) × personal (what does succeeding mean to HIM —
  2nd-gen proof, control, legacy)?
- Which 摸底 probes go to presenter NOTES (champion name · incumbent maintainer · budget-signal
  read via 分款包 magnitude anchor)? Which 喊數字 script (conservative base, verbal-only)?
- What is the interest-check that doubles as qualification (real & funded, 面 vs 點)?

---

## Hard-wired invariants (VP 2026-07-25 — apply to EVERY slide, every deck)

- **R1 · Zero ฿ on any slide, ever.** Value numbers are VERBAL, CONSERVATIVE (labour/throughput
  base, never revenue-base), anchor-only. On-slide numbers become acceptance-time commitments.
  Pain anchors are industry-general; the client's own DBD numbers never appear.
- **R2 · 人機料法環 is boss-only; anchor, don't force.** The full-cost narrative targets the 核決者,
  not managers. On-slide it anchors + invites reaction; it never forces self-quantification.
  "I don't know" is the surfaced 隱性需求 — the C2 move.
- **R3 · 摸底 lives in notes; every slide sells 值得.** Qualification (scale/budget/champion/
  authority-chain) is presenter-note craft, never slide copy. Before any slide ships, ask:
  **「這頁在賣『值得』，還是在賣 feature / 賣公司？」** — feature/company pages get cut or merged.
  The close is always ONE concrete next step; price is deferred with the 分款包/固定工時 line.

*(Debrief discipline, never on a slide: 自我檢討≠怪客戶 — after the visit, the first question is
"did I ask the right questions to move the case?", logged in the deal record.)*
