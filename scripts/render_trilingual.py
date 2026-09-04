"""Render a trilingual deck to PNGs in zh / en / th. Usage:
  <miniconda python3> render_trilingual.py <deck.html> [outdir_prefix=renders]
Outputs <prefix>/  <prefix>-en/  <prefix>-th/  (slide-NN.png each)."""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
deck = Path(sys.argv[1]).resolve()
prefix = sys.argv[2] if len(sys.argv) > 2 else "renders"
URL = deck.as_uri()
ids = re.findall(r'<section\s+class="slide[^"]*"\s+id="slide-(\d+)"', deck.read_text())
smax = max(int(i) for i in ids)
HIDE = ".nav-bar,.keyboard-hint,#lang-toggle,#notes-panel,#notes-btn,#present-view-btn{display:none !important;}"
def render(lang, outdir):
    out = deck.parent / outdir; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width":1920,"height":1080}, device_scale_factor=1).new_page()
        pg.goto(URL, wait_until="networkidle"); pg.wait_for_timeout(4500)
        pg.add_style_tag(content=HIDE)
        pg.evaluate("document.body.classList.remove('lang-zh','lang-en','lang-th','lang-ja')")
        pg.evaluate(f"document.body.classList.add('lang-{lang}')")
        pg.wait_for_timeout(500)
        for i in range(1, smax+1):
            loc = pg.locator(f"#slide-{i}")
            if loc.count()==0: continue
            loc.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
            loc.screenshot(path=str(out/f"slide-{i:02d}.png"))
        b.close()
    print(f"{lang}: {smax} slides -> {outdir}")
render("zh", prefix); render("en", f"{prefix}-en"); render("th", f"{prefix}-th"); render("ja", f"{prefix}-ja")
