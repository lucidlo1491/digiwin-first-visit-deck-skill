# Nova Inquiry Bank — FIRST-VISIT (discovery) deck

The reusable engine behind Phase 0. It turns a company's **OSINT gold standard** into a sharp,
forwardable **Nova question packet** (the Tatung pattern, generalized). Output is
`docs/<deck>/nova-questions-<company>.md` — Peter forwards it to Digiwin's real **Nova** agent; Nova's
answers DECIDE the pains, the core-question line, the close/motive, the EB play, and the objection preempt.

## ⛔ This is a THINKING SCAFFOLD, not a fill-in-the-blanks template (Peter 2026-06-25)
Do **NOT** mechanically substitute `{{placeholders}}` and hand the result to Nova — that produces generic,
template-smelling questions and defeats the purpose. The sections below are the **dimensions to cover**; the
actual questions must be **freshly reasoned from THIS company's OSINT + a real understanding of its industry**.
The bar is the Tatung packet: each question there came from *reading* Tatung's dossier and *understanding*
electronics/EMS high-mix economics — the "complexity tax" pain hypothesis, the "每一條產品線到底還賺不賺?"
core line, the TSTI-group-IT objection. That depth is the product. If a question could be pasted onto another
company unchanged, it has failed — rewrite it from this company's facts.

## How to use (builder)
1. **READ** `docs/gold-standard-<company>.md` end-to-end (+ the live `digiwin_osint` row). Understand their
   **industry** (sub-industry economics, where margin leaks, what compliance/customers demand) and their
   **specific situation** (the financial story, the transformation, the decision structure).
2. **REASON, don't fill.** Use the placeholders only as a coverage map; write each question in *their* terms —
   form a real pain hypothesis from their numbers, draft a core-question line that fits their owner, name the
   objection their structure actually invites. (The Tatung & BFC packets show the depth: `nova-questions-tatung.md`,
   `docs/bfc-proposal/nova-questions-bfc.md`.)
3. **Every question states OUR reasoned hypothesis** and asks Nova to *confirm / rank / improve* — never a blank
   "what do you think?". Arriving with a researched POV is what makes us look like a consultant, not a vendor.
4. Draft provisional answers with the local `/nova-*` proxy skills (`/nova-pain-translation`,
   `/nova-intention-chain`, `/nova-role-questioning`, `/nova-objection-preempt`, `/nova-5-elements`) and
   record them in `inquiry-<company>.md` — but the **authoritative** answers come from the real Nova.
5. **Burn rule:** financial signals (margin / SG&A / revenue volatility / inventory / debt) are used ONLY to
   *steer* the pain hypothesis. They go in the Nova context block, **never recited to the customer on a slide**
   (VP veto — "we dug through your accounts"). On slides, pains stay "產業普遍現象".

## Field → question map (where each placeholder comes from)
| Gold-standard field | Feeds |
|---|---|
| business_group · TSIC · products_description · sub-industry | 背景, Q1 pain set, Q7 industry angle |
| ownership_origin (台商/日商/泰商/陸商/MNC) | 背景, Q1 framing, Q4 EB structure, Q5 positioning |
| financial trajectory (margin / SG&A / revenue YoY / inventory / D-E) | Q1 pain hypothesis + ranking (steer only) |
| transformation signal (大量→高混 / greenfield ramp / export shift / M&A) | 背景, Q1, Q2 core question |
| customers + certifications (IATF/ISO/GMP/export) | 背景, Q1 (traceability pain), Q7 |
| directors + parent_companies + group IT entity | Q4 EB / role, Q5 objection |
| technology_systems (incumbent ERP / Excel / Odoo / group system) | Q5 objection preempt |
| BOI status + province/estate | Q7 Thailand-specific angle |

---

## ▼ FORWARDABLE TEMPLATE (paste into `nova-questions-<company>.md`, fill `{{…}}`, send to Nova)

# 給 Nova 的提問 — {{公司中/英名}} 初訪 deck
> 可直接轉發給 Digiwin Nova。Nova 回覆後,把答案貼回給我,我用來精修這份初訪簡報。

## 背景(給 Nova 的 context)
我們要為 **{{公司中/英名}}** 做一份**初訪簡報(discovery deck)**。
- {{年數}} 年 {{ownership：台商/日商/泰商/陸商/MNC}} {{產業/次產業}} 廠{{,母公司 {{parent}}}};{{廠區/工業區}}、約 {{員工數}} 人、{{廠數/面積}};統編 {{tax_id}}。
- 成長/轉型訊號:{{transformation — 例:大量代工→高混低量 / 新廠 ramp / 出口轉內銷 / 併購擴張}}。
- 財報訊號(僅供研判痛點,不對客戶引述):{{毛利趨勢 · SG&A 趨勢 · 營收波動 · 庫存佔比 · 負債}}。
- 客戶/認證:{{主要客戶/品牌 ODM}} + {{IATF/ISO/GMP/出口}}(→ {{追溯/合規驅動}})。
- 決策結構:{{董事名單/簽字權}} + {{母公司}} + {{集團 IT 公司,若有}}。
- 現有系統:{{incumbent — SAP/Oracle/Excel/Odoo/集團系統/無}}。
- 初訪目標:① 展現我們的專業 ② 讓老闆認出自己的痛 ③ 觸發六要素、確認是不是真商機。請就以下給建議。

## 一、痛點選擇與框架
1. 我們研判這位老闆真正的痛是 **{{痛點假設 a / b / c — 由 OSINT 訊號推得}}** —— 而**不是** {{看似明顯但其實不對的痛,例:呆滯料卡現金(若庫存已精實)}}。**Nova 同意嗎?對這位 {{ownership}} 老闆,哪一個最能打中?排序?**
2. 這幾個痛,要怎麼用「**獲利 / 降本**」的語言去框,老闆才最有感?

## 二、核心問題(情緒高潮頁)
3. 對一個 {{產業/轉型情境}} 的老闆,最尖銳的那句「看不清 / 守不住」核心問題該怎麼問?我們想用 **「{{我方候選核心問句}}」** —— Nova 有更打中的版本嗎?

## 三、收尾與動機
4. 收尾我們想用 **「{{我方候選收尾切角}}」** 來引出動機。**這個切角會打中老闆嗎?** 初訪要怎麼把「**個人動機 + boss intention(兩層動機 / 企圖邏輯鏈)**」挖出來?

## 四、角色 / EB(可贏性)
5. {{決策結構 — 例:台商子公司,決策可能在 泰國/台北母公司/集團 IT}}。初訪要怎麼**不尷尬地問出系統決策權**在誰手上?怎麼找/養一個能接觸 EB 的 Coach?

## 五、異議預判
6. 老闆可能說「{{最可能的異議 — 由現有系統/母公司IT/ownership 推得,例:我們集團有自己的 IT,為什麼找你?}}」初訪該怎麼**預先化解**(不打對方痛處,而凸顯製造業原廠深度)?

## 六、立案 / 推進
7. 這次初訪,**最少要拿到哪些資訊**才算真商機(立案三要項:量化理由 / 專案小組 / 明確時程)?下一步該約什麼?

## 七、泰國 / 產業特定
8. {{產業}} + {{BOI/合規,例:2025 BOI 60 天稽核 / GMP / IATF}} 在泰國,有沒有 Nova 認為**初訪一定要點到**的角度?

---
*回覆對應到 deck:Q1–Q2 → 痛點 slides · Q3 → 核心問題(情緒高潮)· Q4 → 收尾 · Q5/Q6 → 講者備註(EB/異議)· Q7 → 下一步 · Q8 → 產業/合規 slide。*
