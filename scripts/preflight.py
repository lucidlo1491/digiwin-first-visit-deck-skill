#!/usr/bin/env python3
"""THE pre-deploy gate (Peter 2026-07-25 — the Asia Polysacks 'hideous' burn).

ONE ordered checklist that MUST be N/N before a deck can be shipped. `build_portable.py`
refuses to build unless this has written a fresh `_qa/preflight.json` (ok=true) whose hash
matches the exact index.html being shipped — so a green-mechanical-but-ugly deck can never
reach `vercel deploy` again the way Asia Polysacks did.

What this ENFORCES (machine-checkable floor):
  Gate 3  mechanical  — slide_gate(--report) · lang_purity · overlap_check · svg_fit_check · impeccable_gate all exit 0
  Gate 3  measurable  — VALIDATION.md reads N/N (every slide fully validated)
  Gate 4  evidence    — render PNGs EXIST & are FRESH (mtime >= deck) for EVERY declared language (zh/en/th[/ja])
  Gate 1  evidence    — _qa/design-shopping.md exists & shows the digiwin MCP was shopped (get_component/find_icon/get_token/search)

  Gate 5  sighted     — sighted_stamp.py --check: EVERY slide attested against the CURRENT per-language
                        PNG hashes (Peter 2026-08-24, Dai-Ichi v5 burn — the sighted half was skipped
                        under deadline twice; now skipping it blocks deploy instead of shipping ugly)

What this CANNOT verify (the honesty floor): that the stamper actually READ the PNGs before
stamping. The stamp is an attributable attestation (--by is required and ledgered); reading the
slides — composition, dead space, hierarchy, legibility at distance, in EVERY language — is the
act the stamp asserts. Stamp only what you have looked at.

Usage:
  python3 preflight.py <deck.html> [--no-sdd|--proposal ...slide_gate passthrough]
Exit 0 + prints '✅ DEPLOY-READY' only when every box is green. Else exit 1.
"""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path

GRN, RED, YEL, RST = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
LANG_DIR = {"zh": "renders", "en": "renders-en", "th": "renders-th", "ja": "renders-ja"}

argv = sys.argv[1:]
if not argv:
    print("usage: preflight.py <deck.html> [--no-sdd|--proposal] [--deployed <url>]"); sys.exit(2)
DEPLOYED_URL = None
if "--deployed" in argv:
    _i = argv.index("--deployed"); DEPLOYED_URL = argv[_i + 1]; del argv[_i:_i + 2]
DECK = Path(argv[0]).resolve()
PASSTHRU = [a for a in argv[1:] if a.startswith("--")]   # forwarded to slide_gate only
if not DECK.exists():
    print(f"{RED}✗ no such deck: {DECK}{RST}"); sys.exit(2)

# ---- BURNS ritual (Peter 2026-07-25) — the recurring misses, printed EVERY run so the burn
# record is in the builder's face at build time, not in a memory that might not load.
BURNS = [
    "green mechanical gate ≠ good — the sighted all-language READ is the ceiling (Asia Polysacks 'hideous')",
    "READ every declared language, not just EN (jagged giant-Thai / EN legends shipped in Thai slides)",
    "never crop/shrink content to silence a gate — fix the layout (S6 sliver-photos burn)",
    "shop the digiwin MCP (find_icon/get_component/get_token) — hand-drawn icons are forbidden",
    "inputs current: VP playbook mtime + NOVA live + OSINT promoted (7/24 Pass-2 was missed once)",
    "every proper noun verified against a source ('Peera was never Peter!!!')",
    "design FRESH from THIS company's mechanism — swap-test must FAIL (SATS/King Pac reskin burn)",
    "after deploy: register_deck.py + presentations_map.json line (King Pac missing-bookmark burn)",
]
print(f"\n{YEL}  ── BURNS ritual (read before judging anything green) ──{RST}")
for b in BURNS: print(f"{YEL}  • {b}{RST}")
HERE = Path(__file__).resolve().parent
DDIR = DECK.parent
html = DECK.read_text(encoding="utf-8")
deck_mtime = DECK.stat().st_mtime

# declared languages
m = re.search(r"<!--\s*LANGS:\s*([a-z,\s]+?)\s*-->", html)
langs = [x.strip() for x in m.group(1).split(",")] if m else ["zh", "en", "th"]
slide_ids = sorted(int(i) for i in re.findall(r'id="slide-(\d+)"', html))

rows = []   # (gate, name, ok, detail)
def check(gate, name, ok, detail=""):
    rows.append((gate, name, bool(ok), detail))
    return bool(ok)

def run(script, extra=()):
    p = subprocess.run([sys.executable, str(HERE / script), str(DECK), *extra],
                       capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr).strip().splitlines()[-1:] and \
        (p.stdout + p.stderr).strip().splitlines()[-1] or ""

# ---- Gate 3 · mechanical ----
ok, tail = run("slide_gate.py", ["--report", *PASSTHRU]); check("3", "slide_gate (--report)", ok, tail)
for s in ("lang_purity.py", "overlap_check.py", "svg_fit_check.py", "impeccable_gate.py"):
    ok, tail = run(s); check("3", s.replace(".py", ""), ok, tail)

# ---- Gate 3 · scripts-parse (added 2026-08-12): every <script> block must PARSE under node.
# The presenter/NOTES died silently for weeks (re.sub escape-eating + a </style> inside the
# presenter's JS string) while every source-READING gate stayed green — only execution-level
# checking catches a dead script. node missing → INCONCLUSIVE fail (never skip silently).
import tempfile
_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
_bad, _n = [], 0
for _i, _sc in enumerate(_blocks):
    if not _sc.strip() or 'src=' in _sc[:0]:
        continue
    _n += 1
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as _tf:
        _tf.write(_sc); _tp = _tf.name
    try:
        _r = subprocess.run(["node", "--check", _tp], capture_output=True, text=True, timeout=20)
        if _r.returncode != 0:
            _line = (_r.stderr or "parse error").strip().splitlines()
            _bad.append("script#%d: %s" % (_i, next((l for l in _line if "Error" in l), _line[-1])[:90]))
    except FileNotFoundError:
        _bad.append("node not found — cannot verify scripts parse (install node or fix PATH)")
        break
check("3", "scripts-parse (node)", not _bad, "; ".join(_bad[:2]) if _bad else "%d script blocks parse OK" % _n)

# ---- Gate 3 · measurable: VALIDATION.md N/N ----
val = DDIR / "VALIDATION.md"
if val.exists():
    mm = re.search(r"(\d+)\s*/\s*(\d+)\s+slides?\s+fully\s+validated", val.read_text())
    if mm:
        full, tot = int(mm.group(1)), int(mm.group(2))
        check("3", "VALIDATION.md N/N", full == tot and tot > 0, f"{full}/{tot} validated")
    else:
        check("3", "VALIDATION.md N/N", False, "could not parse validated count")
else:
    check("3", "VALIDATION.md N/N", False, "VALIDATION.md missing (run slide_gate --report)")

# ---- Gate 4 · render evidence: fresh PNGs for EVERY declared language ----
for lang in langs:
    d = DDIR / LANG_DIR.get(lang, f"renders-{lang}")
    if not d.is_dir():
        check("4", f"render:{lang}", False, f"missing dir {d.name}/ (run render_trilingual.py)"); continue
    missing, stale, tiny = [], [], []
    for s in slide_ids:
        png = d / f"slide-{s:02d}.png"
        if not png.exists(): missing.append(s)
        elif png.stat().st_mtime < deck_mtime: stale.append(s)
        elif png.stat().st_size < 3000: tiny.append(s)
    if missing or stale or tiny:
        bits = []
        if missing: bits.append(f"missing {missing}")
        if stale:   bits.append(f"STALE (older than deck) {stale}")
        if tiny:    bits.append(f"blank<3KB {tiny}")
        check("4", f"render:{lang}", False, "; ".join(bits))
    else:
        check("4", f"render:{lang}", True, f"{len(slide_ids)} fresh PNGs")

# ---- Gate 5 · SIGHTED-STAMP (Peter 2026-08-24 — the Dai-Ichi v5 burn) ----
# The sighted half of the design gate used to be advisory prose under the verdict; under
# deadline pressure it was skipped twice in one morning and under-filled/white-on-white
# slides shipped on green mechanical gates. Now it BLOCKS: every slide must carry a
# sighted attestation (sighted_stamp.py) whose per-language PNG hashes match the CURRENT
# renders — any re-render that changes pixels invalidates the stamp until someone reads
# the slide again. Stamping unread slides is the only bypass, and the --by ledger makes
# that a deliberate, attributable act instead of a silent omission.
ok, tail = run("sighted_stamp.py", ["--check"]); check("5", "sighted-stamp", ok, tail)

# ---- Gate 6 · post-deploy registration (only when --deployed <url> passed) ----
if DEPLOYED_URL:
    _map = Path(__file__).resolve()
    # repo root = walk up until automation/presentations exists (deck lives under docs/<deck>/)
    _root = DDIR
    while _root != _root.parent and not (_root / "automation" / "presentations" / "presentations_map.json").exists():
        _root = _root.parent
    _mapf = _root / "automation" / "presentations" / "presentations_map.json"
    if _mapf.exists():
        # presentations_map.json is keyed by Vercel SLUG, not by full URL (it carries zero
        # "vercel.app" strings), so the old full-URL substring match could never pass — it
        # failed identically for every deck ever shipped. Match the slug the URL resolves to.
        # (Dai-Ichi, 2026-08-19: caught the check itself, not the deck.)
        _slug = DEPLOYED_URL.rstrip("/").split("//")[-1].split(".")[0]
        _txt = _mapf.read_text()
        _in_map = (f'"{_slug}"' in _txt) or (DEPLOYED_URL.rstrip("/") in _txt)
        check("6", "bookmark map", _in_map,
              "" if _in_map else f"slug '{_slug}' not in presentations_map.json — add the entry + run build_list.py (King Pac missing-bookmark burn)")
    else:
        check("6", "bookmark map", False, "presentations_map.json not found from deck dir — check repo layout")
    check("6", "register_deck reminder", True, "run database/register_deck.py --taxid ... --commit (attest in design-shopping.md)")

# ---- Gate 1 · design-system shopping evidence ----
shop = DDIR / "_qa" / "design-shopping.md"
if shop.exists() and len(shop.read_text().strip()) > 200 and \
   re.search(r"get_component|find_icon|get_token|search\(", shop.read_text()):
    check("1", "design-shopping.md (digiwin MCP)", True, "shopping log present")
else:
    check("1", "design-shopping.md (digiwin MCP)", False,
          "_qa/design-shopping.md missing/thin — log the component/icon/token IDs you shopped")

# ---- verdict ----
fails = [r for r in rows if not r[2]]
print(f"\n  PRE-DEPLOY GATE · {DECK.name} · langs={','.join(langs)} · {len(slide_ids)} slides\n")
for gate, name, ok, detail in rows:
    mark = f"{GRN}✅{RST}" if ok else f"{RED}⛔{RST}"
    print(f"  {mark}  [G{gate}] {name:<28} {('' if ok else RED)}{detail}{RST}")

stamp = {"ok": not fails, "deck": DECK.name,
         "sha256": hashlib.sha256(DECK.read_bytes()).hexdigest(),
         "langs": langs, "slides": len(slide_ids), "ts": int(time.time())}
(DDIR / "_qa").mkdir(exist_ok=True)
(DDIR / "_qa" / "preflight.json").write_text(json.dumps(stamp, indent=2))

if fails:
    print(f"\n{RED}⛔ NOT DEPLOY-READY — {len(fails)} blocker(s). Fix, re-render, re-run.{RST}")
    print(f"{YEL}   build_portable.py will REFUSE to ship until this passes.{RST}\n")
    sys.exit(1)
print(f"\n{GRN}✅ DEPLOY-READY — machine gates green + renders fresh + every slide sighted-stamped.{RST}")
print(f"{YEL}   The stamps assert the PNGs were READ — if you stamped without reading, that lie is in the ledger.{RST}\n")
sys.exit(0)
