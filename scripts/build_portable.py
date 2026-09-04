#!/usr/bin/env python3
"""Build a self-contained single-file (portable / Vercel-deploy) version of a deck's index.html.

Inlines the design-system slides.css (RESOLVING its relative `@import url('./tokens.css')`, which
can't resolve once the file is served standalone → CSS vars empty → dark-sec renders WHITE), inlines
blocks.css + the 3 JS files, and base64-embeds every assets/ image. Google-Fonts @import stays external.

★ GUARD (Peter 2026-06-30 — the king-pac deploy burn): after building, this ASSERTS the portable is
fully self-contained — no unresolved `@import url('./tokens.css')`, no leftover `assets/` refs, no
unresolved `../digiwin-2026-deck-design-system/` link/src. If ANY remain it prints the problem and
EXITS NON-ZERO, so a white-collapsed / asset-broken deck can never be copied to a deploy dir or shipped.
Always rebuild from index.html and let this guard pass BEFORE `vercel deploy` — never deploy a hand-aged
`_deploy/*-public` export (that's exactly what shipped the broken king-pac).

Usage:
  python3 build_portable.py [DECK_DIR] [--public PUBLIC_DIR]
    DECK_DIR    deck folder containing index.html (default: this script's parent)
    --public D  on GUARD OK, also copy the portable to D/index.html (the Vercel deploy dir)
"""
import base64, hashlib, json, re, mimetypes, sys
from pathlib import Path

argv = list(sys.argv[1:])
public = None
force = False
if "--public" in argv:
    i = argv.index("--public"); public = Path(argv[i + 1]); del argv[i:i + 2]
if "--force" in argv:
    force = True; argv.remove("--force")
DECK = Path(argv[0]) if argv else Path(__file__).parent
SYS  = DECK / ".." / "digiwin-2026-deck-design-system" / "system"
index = DECK / "index.html"
html = index.read_text()

# ★ PRE-DEPLOY GATE (Peter 2026-07-25 — the Asia Polysacks 'hideous' burn). Refuse to build/ship
# unless preflight.py wrote a FRESH ok=true stamp whose hash matches THIS exact index.html. The
# machine floor (green gates + all-language renders + shopping log) must be met before deploy.
if not force:
    stamp_p = DECK / "_qa" / "preflight.json"
    cur = hashlib.sha256(index.read_bytes()).hexdigest()
    stamp = {}
    if stamp_p.exists():
        try: stamp = json.loads(stamp_p.read_text())
        except Exception: stamp = {}
    if not stamp.get("ok"):
        print("✗ BLOCKED — no passing pre-deploy gate. Run:")
        print(f"    python3 {Path(__file__).parent/'preflight.py'} {index}")
        print("  (fix every ⛔, re-render all languages, until it prints ✅ DEPLOY-READY.)")
        sys.exit(2)
    if stamp.get("sha256") != cur:
        print("✗ BLOCKED — preflight stamp is STALE (index.html changed since it last passed).")
        print(f"    re-run: python3 {Path(__file__).parent/'preflight.py'} {index}")
        sys.exit(2)
    print(f"✓ pre-deploy gate OK (preflight.json matches index.html · langs={','.join(stamp.get('langs',[]))}).")
else:
    print("⚠️  --force: pre-deploy gate BYPASSED. You are shipping without the checklist. This is logged.")

# 1. inline slides.css — and RESOLVE its relative @import url('./tokens.css') (the white-render burn).
css = (SYS / "slides.css").read_text()
css = css.replace("@import url('./tokens.css');",
                  "/* tokens.css inlined for portable/deploy */\n" + (SYS / "tokens.css").read_text())
html = html.replace(
    '<link rel="stylesheet" href="../digiwin-2026-deck-design-system/system/slides.css" />',
    f"<style>\n{css}\n</style>",
)
# 1b. inline blocks.css (the block library; without it dark-sec/organism styles are missing).
_blocks_link = '<link rel="stylesheet" href="../digiwin-2026-deck-design-system/system/blocks.css" />'
if _blocks_link in html:
    html = html.replace(_blocks_link, f"<style>\n{(SYS / 'blocks.css').read_text()}\n</style>")
# 2. inline the 3 JS files
for js in ("particles.js", "nav.js", "fit.js"):
    code = (SYS / js).read_text()
    html = html.replace(
        f'<script src="../digiwin-2026-deck-design-system/system/{js}"></script>',
        f"<script>\n{code}\n</script>",
    )
# 3. base64-embed every assets/<file> reference
def data_uri(rel):
    p = DECK / rel
    mime = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
# match nested asset paths (assets/logos/x.png) — require a file extension so a bare dir never matches
ASSET_RE = r'assets/[A-Za-z0-9._/-]+\.[A-Za-z0-9]+'
for rel in sorted({m for m in re.findall(ASSET_RE, html)}):
    html = html.replace(rel, data_uri(rel))

out = DECK / (DECK.resolve().name.replace("-", "_") + "_可攜單檔.html")
out.write_text(html)
print(f"portable: {out.name}  {out.stat().st_size/1_048_576:.1f} MB")

# ★ GUARD — the portable MUST be fully self-contained, or we refuse to ship it.
problems = []
if "@import url('./tokens.css')" in html:
    problems.append("unresolved @import url('./tokens.css') → CSS vars empty → dark slides render WHITE (king-pac burn)")
rem_assets = re.findall(ASSET_RE, html)
if rem_assets:
    problems.append(f"{len(rem_assets)} unresolved assets/ ref(s) (missing file?): {sorted(set(rem_assets))[:3]}")
rem_ds = re.findall(r'(?:href|src)="\.\./digiwin-2026-deck-design-system/[^"]+"', html)
if rem_ds:
    problems.append(f"{len(rem_ds)} unresolved design-system link/src (tag mismatch?): {rem_ds[:2]}")
if problems:
    print("✗ GUARD FAILED — NOT deployable:")
    for p in problems: print("    ✗", p)
    sys.exit(1)
print("✓ GUARD OK — fully self-contained (tokens resolved, assets embedded, no external deps).")
if public:
    (public / "index.html").write_text(html)
    print(f"✓ copied → {public}/index.html  (ready for: cd {public} && vercel deploy --prod --yes)")
