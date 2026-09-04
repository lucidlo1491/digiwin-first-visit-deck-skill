#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lang_native_lint.py <deck.html> [more.html ...] — mechanical floor for translationese.

Flags known calque/register tells in CUSTOMER-FACING copy (t-zh / t-th spans + SVG text).
Born 2026-08-20 from Peter's feedback that zh-TW and ไทย deck copy read like literal English.
The ban-lists mirror references/language-law.md + docs/digiwin-2026-deck-design-system/deck-glossary.tsv.
A hit = REWRITE the line (law: author-native). Exit 1 on any hit. The sighted
"would a native salesperson say this aloud?" pass remains the ceiling.
"""
import io, re, sys

ZH_BANS = [
    ("容錯率",        "owner-language: 不給你犯錯的空間"),
    ("先上車",        "internal shorthand — slide says 第一步/先從最有感的一塊開始"),
    ("騎在",          "internal ride-on metaphor — say 現有系統不動,我們接上去"),
    ("賦能",          "buzzword calque"),
    ("異質系統",      "say 兩套系統各記各的"),
    ("可視性",        "say 看得見"),
    ("數據驅動",      "say 用數字說話/用數字下注"),
    ("場景",          "陸味 — rephrase (現場/情況)"),
]
TH_BANS = [
    ("ความสูญเปล่า",   "ภาษาเขียน — say ของเสีย/รูรั่ว"),
    ("ภาษีของเสีย",    "reads as garbage tax — say ของเสียกินกำไร"),
    ("ความจริงสต๊อก",  "calque — say เลขสต๊อกชุดเดียว"),
    ("ให้อภัย",        "personified market — say พลาดไม่ได้แล้ว"),
    ("ถูกแช่แข็ง",     "passive legalese — say จมอยู่ใน…"),
    ("สมควร",         "stiff — say ก็ต้อง…"),
    ("พึงระลึก",       "ภาษาเขียน"),
    ("วินิจฉัยได้ว่า",  "ภาษาเขียน — say ตัดสินใจ/ดูออก"),
    ("อันเนื่องมาจาก",  "ภาษาเขียน — say เพราะ"),
    ("ความจริงของสต๊อก", "calque variant — say เลขสต๊อกจริง"),
    ("ตามสอบ",          "wrong term — traceability = สอบกลับ/ตรวจสอบย้อนกลับ"),
    ("วุฒิภาวะ",        "person-maturity word — CMMI = มาตรฐานกระบวนการพัฒนา"),
    ("หลักประกันความเสี่ยง", "風險保證 calque — say หลักประกัน 3 ข้อ"),
    ("การวินิจฉัย",      "medical register — say การตรวจสุขภาพ (NOVA 體檢)"),
]

SPAN = re.compile(r'class="(t-zh|t-th)"[^>]*>(.*?)</(?:span|text|tspan)>', re.S)
JSTR = re.compile(r'"(zh|th)"\s*:\s*"((?:[^"\\]|\\.)*)"')  # lang strings in JS data objects

def lint(path):
    s = io.open(path, encoding="utf-8").read()
    hits = []
    for m in SPAN.finditer(s):
        lang, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        bans = ZH_BANS if lang == "t-zh" else TH_BANS
        for term, why in bans:
            if term in txt:
                hits.append((lang, term, why, txt.strip()[:70]))
    for m in JSTR.finditer(s):
        lang, txt = "t-" + m.group(1), m.group(2)
        bans = ZH_BANS if lang == "t-zh" else TH_BANS
        for term, why in bans:
            if term in txt:
                hits.append((lang + "/js", term, why, txt.strip()[:70]))
    return hits

def main():
    bad = 0
    for path in sys.argv[1:]:
        hits = lint(path)
        if hits:
            bad += len(hits)
            print(f"✗ {path} — {len(hits)} native-register hit(s):")
            for lang, term, why, ctx in hits:
                print(f"   [{lang}] «{term}» — {why}\n        …{ctx}…")
        else:
            print(f"✓ {path} — native-register lint clean")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
