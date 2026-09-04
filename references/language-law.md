# language-law.md — AUTHOR-NATIVE copy law (Peter 2026-08-20, the translationese burn)

> Origin: feedback on the Manston + Dai-Ichi decks — zh-TW and ไทย read "like a literal translation
> of English… does not convey the meaning." Root causes found: (1) copy conceived in zh/EN then
> rendered per-line into TH; (2) INTERNAL strategy shorthand leaking verbatim onto slides
> (Peter's example: 「依成熟度先上車，騎在你們現有的系統上」 — weird to a native zh-TW reader).

## Rule 0 — copy is AUTHORED in each language, never translated
For every slide zone, each language is written FRESH by asking: *how would a native salesperson
SAY this point aloud to this audience?* If you catch yourself mapping the zh sentence
word-by-word, stop and re-express. The three versions must agree on the MESSAGE, not the syntax.

## Rule 1 — internal register never reaches a slide
The skill's strategy vocabulary — 先上車 · 騎乘句 · 摸底 · 痛點 · 楔子 · 三本帳變一本(ok spoken) ·
anchor→react · slot names — is for specs and presenter notes ONLY. On slides, say what a
salesperson would say: 先上車 → 「第一步」/「先從最有感的一塊開始」; 騎在你們的系統上 →
「你們現有的系統不動，我們接上去」.

## Rule 2 — zh-TW register: NOVA/VP spoken sales language
The native corpus is in-house: NOVA live replies + VP Cheng coaching + MJ 數字力 phrasing.
Sound like them, not like translated research prose.
- BAN tech-compound calques as owner-language: 容錯率(→ 不給你犯錯的空間) · 異質系統(→ 兩套系統各記各的) ·
  可視性/能見度(→ 看得見) · 賦能 · 場景 (陸味) · 數據驅動(→ 用數字說話).
- Taiwanese sales idiom over engineered nouns: 算得清楚 · 看得見管得到 · 錢睡在倉庫 · 帳跟得上.

## Rule 3 — ไทย register: Thai-to-Thai, spoken-business, 15-year-old readable
Binding references (READ them, they already exist):
- `localization-core/DOCTRINE-BRIEF.md` — "the Thai version is a Thai-native rendering, not a
  translation"; swap Chinese/abstract metaphors for Thai-native ones.
- memory `feedback_thai_register_plain` — everyday words over ภาษาเขียน; natural loanwords are
  GOOD (ออเดอร์ สต๊อก ล็อต ออดิต ยีลด์); short clauses; active voice.
- memory `reference_thai_erp_formal_vocabulary` (ERPNext/Frappe .po, formal) +
  `feedback_thai_factory_vocabulary` (floor speech) for terminology.
Mechanical tells of translationese (the linter flags these):
- ความ-…-nominalizations where a verb phrase speaks (ความสูญเปล่า → ของเสีย/รูรั่ว)
- ถูก-passives in value lines (ถูกแช่แข็ง → จมอยู่ใน…)
- personified abstractions (ตลาดให้อภัย… → ตลาดเดี๋ยวนี้พลาดไม่ได้แล้ว)
- stiff modals: สมควร/พึง/ย่อม → ก็ต้อง…/…กันหน่อย
- word-for-word compound calques: ความจริงสต๊อก → เลขสต๊อกชุดเดียว(ตรงกันทั้งบริษัท) ·
  ภาษีของเสีย → ของเสียกินกำไร

## Rule 4 — EN register: plain business, spoken
Short, verbal, no consulting-brochure abstractions. If it wouldn't be said across a table, rewrite.

## Rule 5 — the corpus is the referee
When unsure how to say it in TH, SEARCH `article-replication/` (891 gate-passed native packages)
for the concept before inventing phrasing. For zh, search NOVA replies / VP transcripts.
Shared terminology lives in `docs/digiwin-2026-deck-design-system/deck-glossary.tsv` — check it
FIRST; add to it whenever a new concept gets a settled tri-lingual expression.

## Gate wiring
`scripts/lang_native_lint.py <deck.html>` — mechanical floor for the tells above (TH + zh ban-lists).
Run it with the other gates; a hit = rewrite the line, never whitelist casually. The sighted
read-aloud test per language stays the ceiling: **would a native salesperson say this sentence?**
