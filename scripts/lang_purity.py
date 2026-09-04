#!/usr/bin/env python3
"""Language-purity gate — no unintentional script mixing per language mode.
Rule (Peter, 2026-06-17): each language version reads for its own audience.
  - EN mode: flag any CJK or Thai characters in visible content.
  - TH mode: flag any CJK characters (Thai + Latin technical terms OK).
  - ZH mode: flag any Thai characters (CJK + Latin technical terms OK).
Whitelist = genuine professional/proper tokens kept in original script
(e.g. Thai gov form ภพ.30 inside ZH/EN). Latin tech terms (SKU/ECN/OTD/BOI/
ISO/IATF/CMMI/VAT/PCBA/ERP/China+1/SMT/DIGIWIN/Tatung/Amata) are always allowed.
Usage: <miniconda python3> _qa/lang_purity.py [index.html]
Exit 1 if any contamination; prints slide# + lang + offending text.
"""
import sys, pathlib, re
from playwright.sync_api import sync_playwright

deck = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()

# Thai tokens that are allowed to appear inside ZH/EN content (proper/technical)
THAI_WHITELIST = ["ภพ.30", "ภพ", "฿"]   # Thai gov VAT form + Baht currency symbol

JS = r"""
() => {
  const SKIP = ['nav','.nav-bar','.slide-num','.brand-mark','.tour-mark','.super-d',
                '.hero-glow','#particles','canvas','.wave-bg','.keyboard-hint',
                '#notes-panel','#dw-pres-btn','#lang-toggle','#present-view-btn'];
  const skip = el => SKIP.some(s => (el.closest && el.closest(s)));
  const vis = el => { const st=getComputedStyle(el); const r=el.getBoundingClientRect();
    return st.visibility!=='hidden'&&st.display!=='none'&&+st.opacity!==0&&r.width>=2&&r.height>=2; };
  const out = [];
  document.querySelectorAll('section.slide').forEach((slide,i) => {
    const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
    let n; const seen=new Set();
    while ((n = walker.nextNode())) {
      const t = (n.textContent||'').trim();
      if (!t) continue;
      const p = n.parentElement;
      if (!p || skip(p) || !vis(p)) continue;
      if (seen.has(t)) continue; seen.add(t);
      out.push({slide:i+1, text:t});
    }
  });
  return out;
}
"""

def run(lang):
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width":1920,"height":1080})
        pg.goto(deck.as_uri())
        pg.evaluate("document.body.classList.remove('lang-zh','lang-en','lang-th','lang-ja')")
        pg.evaluate(f"document.body.classList.add('lang-{lang}')")
        pg.wait_for_timeout(700)
        res = pg.evaluate(JS)
        br.close()
    return res

CJK = re.compile(r"[㐀-鿿]")
THAI = re.compile(r"[฀-๿]")

def strip_wl(t):
    for w in THAI_WHITELIST:
        t = t.replace(w, "")
    return t

bad = False
# LANGS declaration (Peter 2026-07-13): check only the deck's declared languages; no comment = all four
_mL = re.search(r'<!--\s*LANGS:\s*([a-z,\s]+?)\s*-->', open(deck, encoding="utf-8").read())
LANGS = tuple(l.strip() for l in _mL.group(1).split(",") if l.strip()) if _mL else ("zh","en","th","ja")
for lang in LANGS:
    flags = []
    for r in run(lang):
        t = r["text"]
        if lang == "en":
            if CJK.search(t) or THAI.search(strip_wl(t)): flags.append(r)
        elif lang == "th":
            if CJK.search(t): flags.append(r)
        elif lang == "zh":
            if THAI.search(strip_wl(t)): flags.append(r)
        elif lang == "ja":
            if THAI.search(strip_wl(t)): flags.append(r)  # JP: flag Thai (kanji share CJK range)
    if flags:
        bad = True
        print(f"[{lang}] CONTAMINATION ({len(flags)}):")
        for f in flags:
            print(f"   slide {f['slide']:>2}: {f['text'][:70]}")
    else:
        print(f"[{lang}] OK — pure")
sys.exit(1 if bad else 0)
