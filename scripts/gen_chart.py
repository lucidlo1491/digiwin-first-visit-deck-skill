#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_chart.py — render an ECharts option to a crisp, DigiWin-themed PNG.

The data-viz engine for /digiwin-deck-visual. Hand-coded primitive SVG has a low
ceiling ("shapes combined"); a real chart engine (ECharts) gives gauges · sankey ·
trees · radar · bars — informative AND on-brand. Output is a transparent-bg PNG you
drop in assets/ and embed.  (Verified 2026-06-29.)

Usage:
  <miniconda python3> gen_chart.py <option.json> <out.png> [WxH]   # default 900x560, rendered @2x

The option is a normal ECharts option (JSON). The 'digiwin' theme is pre-registered
(Smart-Blue/Royal-Blue/Navy/Coral palette, Noto + JetBrains) so series inherit brand
colors automatically; override per-series when you need to (e.g. coral for a loss).
KEEP BAKED TEXT MINIMAL + language-neutral (numbers, %, OEE, BRCGS) — trilingual
descriptive copy goes in the DECK layer for language purity; for label-heavy charts
render one PNG per language by swapping the label strings in the option.
"""
import sys, json, pathlib, tempfile, subprocess
from playwright.sync_api import sync_playwright

opt_path, out = sys.argv[1], pathlib.Path(sys.argv[2])
W, H = (sys.argv[3].split("x") if len(sys.argv) > 3 else ("900", "560"))
option = open(opt_path, encoding="utf-8").read()

THEME = json.dumps({
    "color": ["#00AFF0", "#003CC8", "#000864", "#FF6E82", "#5EC8EF", "#8D9199", "#22C55E"],
    "backgroundColor": "transparent",
    "textStyle": {"fontFamily": "Noto Sans TC, Noto Sans, Noto Sans Thai, sans-serif"},
    "title": {"textStyle": {"color": "#000864", "fontWeight": 800}},
    "legend": {"textStyle": {"color": "#3a4a63"}},
    "categoryAxis": {"axisLine": {"lineStyle": {"color": "#B7C2D0"}},
                     "axisLabel": {"color": "#5b6b80"}, "splitLine": {"show": False}},
    "valueAxis": {"axisLine": {"show": False}, "axisTick": {"show": False},
                  "axisLabel": {"color": "#8D9199"},
                  "splitLine": {"lineStyle": {"color": "#E6EDF5"}}},
})

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;800;900&family=Noto+Sans:wght@400;600;700;800&family=Noto+Sans+Thai:wght@400;600;700&family=JetBrains+Mono:wght@600;800&display=swap');
html,body{margin:0;background:transparent}#c{width:__W__px;height:__H__px}</style></head>
<body><div id="c"></div><script>
echarts.registerTheme('digiwin', __THEME__);
var ch=echarts.init(document.getElementById('c'),'digiwin',{renderer:'svg'});
ch.setOption(__OPT__);
</script></body></html>"""

html = (TEMPLATE.replace("__W__", W).replace("__H__", H)
        .replace("__THEME__", THEME).replace("__OPT__", option))

with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html); tmp = f.name

out.parent.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": int(W), "height": int(H)}, device_scale_factor=2).new_page()
    pg.goto(pathlib.Path(tmp).resolve().as_uri(), wait_until="networkidle")
    pg.wait_for_timeout(1600)            # fonts + echarts
    pg.locator("#c").screenshot(path=str(out), omit_background=True)
    b.close()
# trim transparent margins so it sits tight in the slide
subprocess.run(["magick", str(out), "-trim", "+repage", str(out)], check=False)
print("rendered", out)
