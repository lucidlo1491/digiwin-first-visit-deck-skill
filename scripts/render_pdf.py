"""Export the deck to PDF per language — the ACTUAL deliverable Peter opens.

Why this exists (S8 burn, 2026-06-29): the live HTML (my Chromium screenshot) and the
exported PDF can DIVERGE on SVG effects — a blur filter on a thin/degenerate path renders
in Chromium but BLANK in the PDF. So the sighted self-review must READ the PDF, not only
the PNG. (`slide_gate.py svg-robust` now bans the known cause; this verifies the artifact.)

Usage:  <miniconda python3> render_pdf.py <deck.html> [outdir=_qa/pdf]
Outputs <outdir>/<deck>-zh.pdf, -en.pdf, -th.pdf, -ja.pdf  → READ them (one slide per page).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

deck = Path(sys.argv[1]).resolve()
outdir = deck.parent / (sys.argv[2] if len(sys.argv) > 2 else "_qa/pdf")
outdir.mkdir(parents=True, exist_ok=True)
URL = deck.as_uri()
HIDE = (".nav-bar,.keyboard-hint,#lang-toggle,#notes-panel,#notes-btn,#present-view-btn"
        "{display:none !important;}")
# one 1920x1080 landscape page per slide; defeat the fit-scale transform for print
PRINT = ("@page{size:1920px 1080px;margin:0;}"
         ".slide{page-break-after:always;transform:none !important;width:1920px;height:1080px;}"
         ".fit-wrapper{transform:none !important;}")

def export(lang):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width": 1920, "height": 1080}).new_page()
        pg.goto(URL, wait_until="networkidle"); pg.wait_for_timeout(4500)
        pg.add_style_tag(content=HIDE + PRINT)
        pg.evaluate("document.body.classList.remove('lang-zh','lang-en','lang-th','lang-ja')")
        pg.evaluate(f"document.body.classList.add('lang-{lang}')")
        pg.wait_for_timeout(500)
        out = outdir / f"{deck.stem}-{lang}.pdf"
        pg.pdf(path=str(out), width="1920px", height="1080px",
               print_background=True, prefer_css_page_size=True)
        b.close()
        print(f"{lang} -> {out}")

for L in ("zh", "en", "th", "ja"):
    export(L)
