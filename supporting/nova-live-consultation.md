# Live NOVA Consultation — mandatory in-loop procedure

> Canonical procedure. Referenced by `/digiwin-research-company`, `/digiwin-first-visit-deck`, and
> `/digiwin-erp-proposal-deck`. Mandated by Peter 2026-07-17 ("ask NOVA whenever you have questions
> about your research, ask where you need to, so you are completely, undoubtedly confident").
> Standing authorization to query NOVA live yourself: Peter, 2026-07-15.

## What this is

NOVA is DigiWin's internal AI agent (45-yr institutional sales knowledge), reachable in Teams via a
Playwright MCP browser profile that already holds a valid Teams SSO session. Two layers already exist:
the **cached KB** (`nova-knowledge.md`, priors Q1–Q17, V1.0-signed) and the **gap queue**
(`docs/nova-queue.md`, batch-asked later). **This procedure is the third layer: query the LIVE NOVA
agent mid-run, in real time, whenever a judgment call cannot be grounded in run-evidence or the cached KB.**

The old model — generate a forwardable packet and wait for Peter to hand-carry it to NOVA and paste
answers back — is now the **fallback**, not the default. Default = ask NOVA directly, yourself, now.

## When to consult (bias toward asking)

Peter's rule: **ask whenever, ask where you need to.** Do NOT guess through a judgment call you could
resolve by asking. Consult NOVA when you hit any of these and the cached KB does not already answer it
*for this specific situation*:

- **Incumbent / product-fit play** — how to play a specific incumbent (e.g. eMES-on-SAP vs displacement),
  which module sequence, T100-vs-iGP framing for THIS company's structure.
- **Wedge & stage** — which pain to lead with; whether the evidence justifies C2-candidate vs E; deal
  structure for a multi-entity group.
- **Competitive** — how to beat/defend against a named competitor in this segment.
- **Objection handling** — the sharpest 話術 for an objection this owner is likely to raise.
- **Authority / family structure** — reading nominal-vs-real power; how to work a specific family layout.
- **Deck decisions (both deck skills)** — the narrative arc, which proof point lands for this audience,
  how to frame the complement-play or the pricing-tier reveal, 初訪七步驟 alignment, objection-preempt slides.
- **Any residual "I'm not sure"** after synthesis. If asking would raise your confidence, ask.

Batch related questions into ONE well-formed message when you can (fewer round-trips), but do not
withhold a question just to batch it — a mid-run blocker gets asked immediately.

## Access & driver (Playwright MCP)

The Playwright MCP persistent profile holds the Teams login. Navigation (re-derive each time; the iframe
periodically resets to the portal home):

1. App rail **鼎新數智** → **double-click** the **諾瓦Nova** tile → **業務大學姐** card → sub-assistant
   list → **南高-商機助手** (Peter's daily driver).
2. **`+ 新對話`** to open a fresh thread. **One NEW thread per company** — first line/context = the company
   name in English — to avoid cross-company contamination. (KB/methodology questions go in their own
   "SKILL KNOWLEDGE BASE" thread instead.)
3. **GOTCHA (proven):** a bare company-name-only first message creates a job that HANGS in PROCESSING and
   globally DISABLES the textbox. FIX: after `+ 新對話`, send the **FULL, SELF-CONTAINED question directly**
   (name the company inside the question) — skip the separate name-only anchor message.

## WAF gotcha — NO em-dash

A Cloud Armor WAF rule at `api.ai.digiwin.com` returns **403** when the POST body contains certain characters
adjacent to CJK phrasing. Confirmed triggers: the em-dash `—` (King Pac) **and the percent sign `%`** (Asia
Polysacks, 2026-07-24 — a question full of `3%`/`86%`/`76%` FAILED; spelling them out as `百分之三`/`三到五趴`
passed on the retry). The 403 page has no CORS headers, so the browser misreports it as "CORS blocked /
ERR_FAILED". **Write NOVA questions with ASCII hyphen `-` only (never `—`) and NO `%` sign (spell out
百分之N or use 趴).** Keep the prose plain; if a send returns ERR_FAILED, rephrase to remove `%`/`—` and retry. Health check: `/ext/v1/<agent>` POST failing while `history/v1` GETs succeed = WAF body
rejection (fix the text), NOT backend-down.

## Send & capture

- **Send:** fill the textbox (`請輸入...`), then element-level `press('Enter')` (or click the send arrow
  `.question-input svg.arrow-icon` in the frame whose URL contains **aiep-portal**). Verify the textbox
  cleared = sent. If the textbox is disabled, NOVA is still busy or the job hung (see gotcha) — reset with
  `+ 新對話`.
- **Never wait in place.** Answers generate server-side. Poll the job API instead of blocking:
  `browser_network_requests` filter `ext/v1/(SalesIPC|jobs)` → find the new job id from the POST 202 →
  read the latest `ext/v1/jobs/id/<job>` poll `response-body` → **`result.response.data.result` = the full
  verbatim markdown answer** (better than DOM scraping; jobs typically complete in 15-25 s). Never call
  `navigator.clipboard.readText()` (froze the renderer once).

## Record, tag, encode

- Save NOVA's answer **verbatim** to `docs/research-fragments/<company-id>/nova-live-<date>.md` (deck skills:
  `docs/<deck>/nova-live-<date>.md`), with the question that produced it.
- **Confidentiality: NOVA answers are INTERNAL strategy.** In any dossier or deck, NOVA-derived reasoning
  lives ONLY inside the internal fences, tagged **【NOVA live <date>】**. Never let NOVA's raw strategy
  language (competitive framing, authority reads, pain-in-฿) reach a customer-facing slide or a forwarded file.
- **Encode durable, generalizable priors back into `nova-knowledge.md`** (new §N, dated, tagged) so the KB
  compounds. Company-specific answers stay in the dossier/deck only. If NOVA reveals a methodology gap,
  also log it to `docs/nova-queue.md`.
- On promote, archive the live-capture file to `docs/_eval/archive/<company-id>/` alongside the fragments.

## Fallback (never fail the run)

If the Playwright profile's SSO has expired, the tile won't load, or the job never completes:
1. Retry once (`+ 新對話`, re-send). 2. If still down, fall back to the OLD model: write/append the question
to the forwardable packet `docs/<deck-or-co>/nova-questions-<company>.md` **and** to `docs/nova-queue.md`,
note in the run footer `NOVA live unreachable - N questions queued for Peter to forward`, and proceed on the
cached KB (tagged 【推論 calibrated by NOVA KB】). A live-NOVA outage never blocks shipping — it downgrades
to the queue.

## Footer line (both tiers / both deck skills)

Report what you actually asked: `NOVA live consulted: N questions (<one-line topics>) · KB updated: §N | none · queued: N`.
