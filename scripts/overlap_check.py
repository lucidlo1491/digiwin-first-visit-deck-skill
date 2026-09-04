#!/usr/bin/env python3
"""Geometric bbox-overlap invariant for the deck — measures, never eyeballs.
Catches content blocks (cards/panels/absolutely-positioned graphic nodes) that
bleed into each other (the slide-17 PDCA-ring-over-steps bug). Run BOTH languages.
Usage:  <miniconda python3> _qa/overlap_check.py [index.html]
Exit 1 if any overlap > tolerance; prints slide# + the two blocks + overlap px.
"""
import sys, pathlib, re
from playwright.sync_api import sync_playwright

deck = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()

JS = r"""
() => {
  // chrome + decorative layers are allowed to sit under/over content — exclude them
  const SKIP = ['nav','.nav-bar','.slide-num','.brand-mark','.tour-mark','.super-d',
                '.hero-glow','#particles','canvas','.wave-bg','.keyboard-hint',
                '#notes-panel','#dw-pres-btn','#lang-toggle','#present-view-btn','svg',
                '.contact-card','.cc-strip','.cover-bg','.cover-scrim'];
  const skip = el => SKIP.some(s => (el.matches && el.matches(s)) || (el.closest && el.closest(s)));
  const vis = el => { const st=getComputedStyle(el); const r=el.getBoundingClientRect();
    return st.visibility!=='hidden'&&st.display!=='none'&&+st.opacity!==0&&r.width>=8&&r.height>=8; };
  const ov = (A,B,T) => (Math.min(A.right,B.right)-Math.max(A.left,B.left))>T
                     && (Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top))>T;
  const rel = (a,b) => a.contains(b)||b.contains(a);   // ancestor/descendant — not a collision
  const TOL = 6;
  const out = [];
  document.querySelectorAll('section.slide').forEach((slide, i) => {
    // (1) COLUMN-BLEED: in any multi-column grid/flex, no descendant of column A may
    //     cross into column B's box (the slide-17 ring node bleeding into the steps column).
    const conts = [...slide.querySelectorAll('*')].filter(el => {
      const st=getComputedStyle(el);
      return (st.display==='grid'||st.display==='flex') && el.children.length>=2 && !skip(el) && vis(el);
    });
    conts.forEach(cont => {
      const cols = [...cont.children].filter(c => !skip(c) && vis(c));
      for (let a=0;a<cols.length;a++) for (let b=0;b<cols.length;b++) {
        if (a===b) continue;
        const Bbox = cols[b].getBoundingClientRect();
        const items = [cols[a], ...cols[a].querySelectorAll('*')].filter(d => !skip(d) && vis(d) && !cols[b].contains(d));
        for (const d of items) {
          if (ov(d.getBoundingClientRect(), Bbox, TOL)) {
            out.push({slide:i+1, a:'BLEED:'+String(d.className||d.tagName).slice(0,26),
                      b:'into['+String(cols[b].className||cols[b].tagName).slice(0,18)+']'});
            break;
          }
        }
      }
    });
    // (3) card-vs-card bleed (outermost cards overlapping)
    const CARD='.ex-card,.card,.stat,.cred,.ag-item,.ex-ag-item,.ex-row,.b-pain,.pc,.ex-pc,.ma-card,.ex-ma-card,.frame,.ex-lw,.lw,figure,.cap-cell,.ip';
    let cards=[...slide.querySelectorAll(CARD)].filter(el=>!skip(el)&&vis(el));
    cards=cards.filter(el=>!cards.some(o=>o!==el&&o.contains(el)));
    for(let a=0;a<cards.length;a++)for(let b=a+1;b<cards.length;b++)
      if(ov(cards[a].getBoundingClientRect(),cards[b].getBoundingClientRect(),TOL))
        out.push({slide:i+1, a:'CARD:'+String(cards[a].className).slice(0,24), b:'CARD:'+String(cards[b].className).slice(0,24)});
    // (4) FOOTER OVERFLOW — content must not reach the bottom chrome (brand-mark/tour-mark).
    //     Catches EN/TH running longer than ZH and spilling onto the footer (the S6 "Digiwin" overlap).
    const srect = slide.getBoundingClientRect();
    let chromeTop = srect.bottom - 50;
    slide.querySelectorAll('.brand-mark,.tour-mark').forEach(c=>{ if(vis(c)) chromeTop=Math.min(chromeTop, c.getBoundingClientRect().top); });
    const CSEL='p,h1,h2,h3,h4,li,.lead,.s6-card,.s6-logo,.s6-evo,.stat,.ch-card,.qcard,.fi,.cred,.dp-job,.dp-note,.s8b2-pay,.s8b2-floor,.s8-ribbon,.s5j-lbl,.cmmi-evidence';
    let spill=0, who='';
    slide.querySelectorAll(CSEL).forEach(el=>{ if(skip(el)||!vis(el)||!el.textContent.trim())return;
      const b=el.getBoundingClientRect().bottom; if(b>chromeTop+TOL && (b-chromeTop)>spill){ spill=b-chromeTop; who=String(el.className||el.tagName).slice(0,20);} });
    if(spill>2) out.push({slide:i+1, a:'OVERFLOW:'+who, b:'spills into footer (+'+Math.round(spill)+'px)'});
  });
  // de-dup
  const seen=new Set(); return out.filter(o=>{const k=o.slide+o.a+o.b; if(seen.has(k))return false; seen.add(k); return true;});
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

bad = False
# LANGS declaration (Peter 2026-07-13): check only the deck's declared languages; no comment = all four
_mL = re.search(r'<!--\s*LANGS:\s*([a-z,\s]+?)\s*-->', open(deck, encoding="utf-8").read())
LANGS = tuple(l.strip() for l in _mL.group(1).split(",") if l.strip()) if _mL else ("zh","en","th","ja")
for lang in LANGS:
    res = run(lang)
    if res:
        bad = True
        print(f"[{lang}] OVERLAPS:")
        for o in res:
            extra = f"  overlap {o['ox']}×{o['oy']}px" if 'ox' in o else ""
            print(f"   slide {o['slide']:>2}: [{o['a']}]  ×  [{o['b']}]{extra}")
    else:
        print(f"[{lang}] OK — no content-block overlaps")
sys.exit(1 if bad else 0)
