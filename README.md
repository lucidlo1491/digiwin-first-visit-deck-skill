# digiwin-first-visit-deck

A "skill" that teaches an AI assistant (Claude Code) how to build the slide deck for the very first
meeting with a factory, in three languages at once. Written so anyone can follow, even with no sales or
AI background.

---

## 1. What is a skill?

Imagine hiring a very smart assistant who has read every book in the world but has never worked at your
company. A **skill** is a folder of instructions you hand them: *"When I ask for this job, here is exactly
how we do it, step by step, and here are the traps."* The assistant reads it and does the job that way.
If the skill has a checker script, the job is not finished until the checker passes.

## 2. The job this skill does

You type:

```
/digiwin-first-visit-deck <company>
```

after the research on that company exists (see the sister skill `digiwin-research-company`), and the
assistant builds the deck for the first meeting. The deck is in Thai, English and Chinese at the same
time, because that is who sits in the room: the Thai factory team, the salesperson, and sometimes a
Chinese-speaking owner or head-office colleague.

## 3. The idea behind the deck

On a first visit the customer does not know us and does not yet trust us. So the deck is built in this
order, and the order is the point:

1. **We understand you.** Their industry, their kind of factory, the headaches factories like theirs have.
2. **Here is what those headaches cost**, in their own numbers where we have them.
3. **Here is what we do about it**, with cases from similar factories, each case carrying a measurable result.
4. **What happens next.** One clear next step.

Product features come last. Cases come after the pain, never before. That rule came from a real meeting
that went wrong when the deck opened with the product.

## 4. What makes it careful

- **Content before slides.** A content pack is written and approved first; then one page of design per
  slide; only then does anyone draw. No slide without a spec.
- **Language law.** Every slide is written in the language it will be spoken in, by a native-language rule
  set (`references/language-law.md`). Internal team jargon is banned from customer slides, and a script
  hunts for leaks.
- **Looked at, not assumed.** Slides are rendered to pictures and read before the deck is called done.
  Scripts check for overlapping text, text off the edge, wrong-language leaks, and missing inputs.
- **One visual system.** Colours, type, spacing and icons come only from the company's design system,
  never from the assistant's imagination. `supporting/DESIGN.md` is the law the deck obeys.
- **Asks the experts.** When the deck needs a judgement call (which pain to lead with, which case to show),
  the skill asks the company's in-house AI of senior sales experts (NOVA) and records the advice.

## 5. Files

| File | What it is |
|---|---|
| `SKILL.md` | The procedure, start to finish |
| `references/arc-questions.md` | The questions the deck must answer, in order |
| `references/content-pack-template.md` | What to gather before any slide is drawn |
| `references/slide-sdd-template.md` | The one-page design written per slide |
| `references/language-law.md` | Which language goes where; banned words |
| `references/blocks.md` | The reusable slide building blocks |
| `references/acceptance-criteria.md`, `references/pre-deploy-checklist.md` | What "finished" means |
| `references/nova-inquiry.md` | The questions to put to the senior experts while building |
| `scripts/preflight.py`, `scripts/check_inputs.py` | Refuse to start without research and a content pack |
| `scripts/slide_gate.py`, `overlap_check.py`, `svg_fit_check.py`, `lang_purity.py`, `lang_native_lint.py` | Layout and language checkers |
| `scripts/render_pdf.py`, `render_trilingual.py`, `build_portable.py`, `gen_chart.py`, `add_japanese.py`, `sighted_stamp.py`, `impeccable_gate.py` | Rendering and packaging helpers |
| `supporting/DESIGN.md`, `supporting/PRODUCT.md` | The design law and product context the skill loads before styling anything |
| `supporting/deck-design-system/BLOCKS.md`, `SLOTS-FIRSTVISIT.md` | The deck design system's blocks and the slot map for a first-visit deck |
| `supporting/nova-live-consultation.md` | How to consult the live expert AI (shared with the research skill) |

## 6. Install and use

1. Install Claude Code.
2. Copy this folder to `<your-project>/.claude/skills/digiwin-first-visit-deck/`.
3. Have the research report for the company ready (from `digiwin-research-company`).
4. Type `/digiwin-first-visit-deck <company>`. It expects the company design system on disk and a browser
   for rendering; it tells you what is missing when you run it.

## 7. House rules

- Content pack, then per-slide spec, then slides. Never the other way round.
- Speak the customer's language, literally, in plain words.
- Render and look before saying "done". Pixel math is not proof.
- Cases after pain, and every case carries a number.
- Style from the design system only.

## 8. Glossary

| Word | Plain meaning |
|---|---|
| **ERP / MES** | Software for a company's paperwork / for the factory floor |
| **Deck** | A slide presentation |
| **Content pack** | The words and facts gathered before any slide is drawn |
| **SDD** | "Slide design document": one page of design per slide, written first |
| **Trilingual** | Thai, English and Chinese on the same slides |
| **NOVA** | The company's in-house AI trained on senior sales experts |

*Private repository. DigiWin Thailand, 2026.*
