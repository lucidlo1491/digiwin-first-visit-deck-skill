"""svg_fit_check.py — catch SVG <text> overflowing the <rect> it visually sits inside,
in EVERY declared language. This is the blind spot overlap_check.py has by design:
overlap_check skips `svg` entirely (it only measures HTML DOM blocks), and SVG text never
wraps or triggers container overflow — it just paints past any shape. So a label that fits
in English can spill out of its box in Thai/中文 (30–40% wider for the same content) and no
mechanical gate sees it; only a per-language sighted READ would — and only for the language
you actually looked at. This closes that hole.

Method: for each <svg>, for each <rect>, find <text> whose rendered bbox CENTER falls inside
the rect (i.e. text meant to live in that box). If the text bbox extends past the rect's
left/right edge beyond TOL, flag it. Runs once per declared language (<!-- LANGS: … -->).

Usage:  <miniconda python3> svg_fit_check.py <deck.html>
Exit 0 = all fit; exit 1 = overflow(s) found (printed slide/lang/text/px).
"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

TOL = 6  # px of allowed spill (text-anchor rounding)
deck = Path(sys.argv[1]).resolve()
src = deck.read_text()
m = re.search(r"<!--\s*LANGS:\s*([a-z,\s]+)-->", src)
langs = [x.strip() for x in (m.group(1) if m else "zh,en,th").split(",") if x.strip()]

JS = r"""
(TOL) => {
  const out = [];
  document.querySelectorAll('section.slide').forEach((slide, si) => {
    slide.querySelectorAll('svg').forEach(svg => {
      const rects = [...svg.querySelectorAll('rect')];
      const texts = [...svg.querySelectorAll('text')];
      for (const t of texts) {
        let tb; try { tb = t.getBBox(); } catch(e) { continue; }
        if (!tb || tb.width === 0) continue;
        const cx = tb.x + tb.width/2, cy = tb.y + tb.height/2;
        // find the rect this text sits inside (center within rect bounds)
        let host = null;
        for (const r of rects) {
          const rx = +r.getAttribute('x'), ry = +r.getAttribute('y');
          const rw = +r.getAttribute('width'), rh = +r.getAttribute('height');
          if (cx >= rx && cx <= rx+rw && cy >= ry && cy <= ry+rh) { host = {rx,ry,rw,rh}; break; }
        }
        if (!host) continue;  // label not inside a box → not our concern
        const spillL = host.rx - tb.x;                 // >0 = text pokes out left
        const spillR = (tb.x + tb.width) - (host.rx + host.rw); // >0 = pokes out right
        const spill = Math.max(spillL, spillR);
        if (spill > TOL) {
          out.push({slide: si+1, text: (t.textContent||'').trim().slice(0,40),
                    spill: Math.round(spill), boxW: Math.round(host.rw), textW: Math.round(tb.width)});
        }
      }
    });
  });
  return out;
}
"""

def check(lang, pg):
    pg.evaluate("l => { document.body.classList.remove('lang-zh','lang-en','lang-th','lang-ja'); document.body.classList.add('lang-'+l); }", lang)
    pg.wait_for_timeout(250)
    return pg.evaluate(JS, TOL)

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width":1920,"height":1080}, device_scale_factor=1).new_page()
    pg.goto(deck.as_uri(), wait_until="networkidle"); pg.wait_for_timeout(1500)
    for lang in langs:
        for hit in check(lang, pg):
            fails.append((lang, hit))
    b.close()

if fails:
    print(f"✗ svg-fit: {len(fails)} SVG text(s) overflow their box")
    for lang, h in fails:
        print(f"   S{h['slide']} [{lang}]  spill {h['spill']}px  (text {h['textW']}px > box {h['boxW']}px)  “{h['text']}”")
    sys.exit(1)
print(f"✓ svg-fit: all SVG box-labels fit in {'/'.join(langs)}")
