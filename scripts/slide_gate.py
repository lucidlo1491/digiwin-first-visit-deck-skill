#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slide_gate.py — the HARDWIRED per-slide checklist for a Digiwin first-visit deck.

Why this exists (Peter, 2026-06-29): the build is routine, but steps get skipped
(no visual, templated agenda, real-time/IoT language, missing contact/Tax-ID, stale
template names). This script turns the checklist into a GATE: it scores every slide
on every rule and EXITS NON-ZERO until all are green. "If a slide does not have the
correct outcome, go back and redo it until it is done."

Usage:  python3 _qa/slide_gate.py index-draft.html
Run it BEFORE declaring any slide / the deck done, and after every edit. Every ✗ is
a redo, not a note. Pair with the SIGHTED gate (render_trilingual.py + READ the PNGs).

It composes the mechanical gates (lang_purity, overlap_check) and adds per-slide
outcome rules. It does NOT replace reading the PNGs — a visual can PASS structurally
and still be ugly; the human/sighted gate stays in the loop.
"""
import re, sys, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PROPOSAL = "--proposal" in sys.argv          # proposal deck: pricing + later-stage framing allowed
REPORT   = "--report" in sys.argv            # also write VALIDATION.md (measurable per-slide output)
NO_SDD   = "--no-sdd" in sys.argv            # legacy decks built before the content-first/SDD tier (2026-07-13)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
DECK = args[0] if args else os.path.join(os.path.dirname(HERE), "index-draft.html")
html = open(DECK, encoding="utf-8").read()

# ---- LANGS declaration (Peter 2026-07-13: 中/EN/ไทย always; 日本語 only when the main contact or a
# shareholder is Japanese). The deck declares its shipping set: <!-- LANGS: zh,en,th --> or zh,en,th,ja.
# No declaration = legacy deck = all four (backward compatible with every deck shipped before 2026-07-13).
_mL = re.search(r'<!--\s*LANGS:\s*([a-z,\s]+?)\s*-->', html)
LANGS  = [l.strip() for l in _mL.group(1).split(",") if l.strip()] if _mL else ["zh", "en", "th", "ja"]
HAS_JA = "ja" in LANGS

# ---- config -------------------------------------------------------------------
STALE_NAMES      = ["Tatung", "大同", "監視器", "Amata", "電子製造", "IATF"]   # template bleed
BANNED_TERMS     = ["IoT", "物聯網", "即時數據", "real-time data", "realtime data"]  # no IoT/real-time framing (first-visit)
PRICING_TERMS    = ["報價單", "報價表", "quotation", "NT$", "USD ", "報價:", "unit price"]  # first-visit = no price

def sections():
    out = []
    for m in re.finditer(r'<section class="slide([^"]*)" id="slide-(\d+)">(.*?)</section>', html, re.S):
        out.append((int(m.group(2)), m.group(1), m.group(3)))
    return sorted(out)

SECS = sections()
# DERIVE structure from the deck (works for any arc/length — first-visit 15 OR proposal 20+):
_ALL = [sid for sid, _, _ in SECS]
COVER = min(_ALL) if _ALL else 1
CLOSE = max(_ALL) if _ALL else 1
CONTENT_SLIDES = set(s for s in _ALL if s != COVER)   # every non-cover slide owes a real visual
CONTACT_SLIDES = {COVER, CLOSE}                        # cover + close need the LINE-QR contact block
def _is_pain(body):                                    # hedged-pain slide = has the discovery-question card (S12–14 only)
    return 'class="qcard"' in body.lower()
results = {}   # sid -> list[(rule, ok, detail)]
lite_slides = []   # slides passing 'informative' only via a VIS-LITE declaration = the upgrade worklist

# --- sighted-audit ledger (per-deck) — LOAD-BEARING for pain slides (see per-slide check 13) -----
# The ledger lives NEXT TO THE DECK (<deck>/_qa/visual_audit.tsv), not next to this script. The old
# code read it from HERE (the script dir) → it was ALWAYS empty, so the per-visual "does it argue?"
# verdict never bound to anything. Resolve it relative to the deck and parse it BEFORE the per-slide loop.
AUDIT = {}   # sid -> (message, serves, layout, verdict, note, stranger_says)
_deckdir = os.path.dirname(os.path.abspath(DECK))
for _cand in (os.path.join(_deckdir, "_qa", "visual_audit.tsv"), os.path.join(_deckdir, "visual_audit.tsv")):
    if os.path.exists(_cand):
        for ln in open(_cand, encoding="utf-8"):
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"): continue
            p = ln.split("\t")
            sid_s = p[0].lstrip("Ss") if p else ""
            if len(p) >= 4 and sid_s.isdigit():
                AUDIT[int(sid_s)] = (p[1], p[2].strip().upper(), p[3].strip().upper(),
                                     (p[4].strip().lower() if len(p) > 4 else ""),
                                     (p[5].strip() if len(p) > 5 else ""),
                                     (p[6].strip() if len(p) > 6 else ""))
        break

def add(sid, rule, ok, detail=""):
    results.setdefault(sid, []).append((rule, ok, detail))

for sid, cls, body in SECS:
    low = body.lower()
    # 1) chrome present (cover uses cover-meta instead of a tour-mark)
    need = ("slide-num", "brand-mark", "cover-meta") if sid == 1 else ("slide-num", "brand-mark", "tour-mark")
    add(sid, "chrome", all(t in body for t in need))
    # 2) no stale template name
    # A deck may declare an EVIDENCED exception: <!-- STALE-OK: IATF (reason) -->. Some STALE_NAMES
    # (notably IATF) are real facts for some customers — ALUMET genuinely holds IATF 16949 — so a
    # blanket ban produced a false positive. The allowlist requires a stated reason, so the check
    # still catches silent template bleed. (Peter 2026-08-10, ALUMET.)
    _ok = {t.strip().split("(")[0].strip().lower()
           for m in re.findall(r"<!--\s*STALE-OK:(.*?)-->", html, re.S) for t in m.split(",")}
    hit = [n for n in STALE_NAMES if n.lower() in low and n.lower() not in _ok]
    add(sid, "no-stale", not hit, ",".join(hit))
    # 3) a REAL visual (svg or img) on every content slide — catches "all text" slides
    if sid in CONTENT_SLIDES:
        has_vis = ("<svg" in low) or ("<img" in low)
        add(sid, "visual", has_vis, "" if has_vis else "TEXT-ONLY — add a graphic/pictograph/photo")
    # 4) banned framing (IoT / real-time) — first-visit only (proposal may discuss it)
    if not PROPOSAL:
        bhit = [t for t in BANNED_TERMS if t.lower() in low]
        add(sid, "no-IoT/realtime", not bhit, ",".join(bhit))
    # 5) no pricing on a first-visit deck (proposal deck DOES carry a quote)
    if not PROPOSAL:
        phit = [t for t in PRICING_TERMS if t.lower() in low]
        add(sid, "no-pricing", not phit, ",".join(phit))
    # 6) pains hedged — FIRST-VISIT only (proposal pains use the client's verbatim quotes, not hedged scenarios)
    if not PROPOSAL and _is_pain(body):
        add(sid, "hedged", "產業普遍現象" in body, "" if "產業普遍現象" in body else "add 產業普遍現象 · 非貴司特定數據")
    # 7) contact invariant (cover + close, derived)
    if sid in CONTACT_SLIDES:
        ok = ("line-qr" in low) or ("contact-card" in low)   # any *-line-qr asset (distributor decks carry the SMK rep's QR, not Peter's — 2026-07-13)
        add(sid, "contact+QR", ok, "" if ok else "cover/close need the LINE-QR contact block")
    # 9) no leftover DRAFT placeholders OR unfilled scaffold tokens ({{...}})
    add(sid, "no-draft", ("pending nova" not in low) and ('class="draft-ph"' not in low) and ("{{" not in body),
        "unfilled scaffold {{token}} or draft placeholder — fill from OSINT/Nova before shipping" if ("{{" in body or 'class="draft-ph"' in low or "pending nova" in low) else "")
    # 10) EMPHASIS — every content slide marks its essence (a .em/.hl highlight)
    if sid in CONTENT_SLIDES:
        add(sid, "emphasis", ('class="em"' in body) or ('class="hl"' in body),
            "" if (('class="em"' in body) or ('class="hl"' in body)) else "no highlight — mark the essence phrase in `.em`")
    # 11) INFORMATIVE graphic OR a declared <!-- VIS-LITE: reason --> (no silent decorative-only slides)
    if sid in CONTENT_SLIDES:
        # SUPERSET of every deck's informative-organism classes (so syncing this canonical never strips a deck's)
        ORG = ['s3sq','s8b2','s5j','compliance-rail-wrap','cmmi-ladder','stat-row','s6-grid',
               'ch-grid','focus-grid','s8-ribbon','s8b-roles','team-panel','pq ','class="triad"',
               'class="loop','class="stack','class="ploop','class="board','sol-grid']
        draw = len(re.findall(r'<(?:path|rect|circle|line|polyline|ellipse)\b', body))
        photo = bool(re.search(r'<img[^>]+src="assets/(?!peter-line-qr)[^"]+\.(?:jpe?g|png|webp)"', body))
        informative = photo or draw >= 8 or any(o in body for o in ORG)
        lite = '<!-- VIS-LITE' in body
        add(sid, "informative", informative or lite,
            "" if (informative or lite) else "icon/number only — add an informative graphic OR declare <!-- VIS-LITE: reason -->")
        if lite and not informative:
            m = re.search(r'<!-- VIS-LITE:(.*?)-->', body)   # only PENDING upgrades land on the worklist
            if m and ('UPGRADE' in m.group(1).upper() or 'PENDING' in m.group(1).upper()):
                lite_slides.append(sid)
    # 11b) CHART SELF-LABELED (Peter 2026-07-19 — the AMK S11/S12 double-correction burn):
    #     a data-chart image must be SELF-LABELED in the chart layer, per language — an HTML legend/
    #     step-label row beside a chart <img> lives in a different layer and can never center under
    #     the marks (pq-cap/wf-steps pattern = AUTO-FAIL). And a single language-neutral chart
    #     (c-all) is only legal when its baked text is purely numeric — declare <!-- LANG-NEUTRAL: reason -->.
    if 'pq-chart' in body:
        bad_legend = ('class="pq-cap"' in body) or ('class="wf-steps"' in body)
        add(sid, "chart-self-labeled", not bad_legend,
            "" if not bad_legend else "HTML legend row beside a chart img — bake labels INTO the chart per language (c-zh/c-en/c-th), delete the pq-cap/wf-steps row")
        if 'pq-chart c-all' in body and '<!-- LANG-NEUTRAL' not in body:
            add(sid, "chart-per-language", False,
                "c-all chart carries text? render per-language PNGs (c-zh/c-en/c-th) with baked labels, or declare <!-- LANG-NEUTRAL: numbers-only -->")
    # 12) SVG ROBUSTNESS — no filter on a stroke-only/line connector (zero-area bbox → renders BLANK
    #     in the PDF and in non-Chromium browsers; my Chromium screenshot paints it, so I "verify" a
    #     line the customer can't see — the S8 centre-line burn 2026-06-29). Drop the filter or give it area.
    frag = re.findall(r'<(?:line|path|polyline)\b[^>]*\bfilter=[^>]*>', body)
    frag = [t for t in frag if t.startswith('<line') or 'fill="none"' in t or "fill='none'" in t]
    add(sid, "svg-robust", not frag,
        "" if not frag else "SVG filter on a stroke/line (zero-area bbox → blank in PDF). Drop the filter or give the element area. (S8 burn)")
    # 13) PAIN VISUAL ARGUES — the sighted audit is LOAD-BEARING here, NOT decoration.
    #     A templated dial passes EVERY mechanical check above (it has an <svg>, an .em, an org class) yet
    #     argues nothing — the #1 regression (Everydayhappy/P.Inter/Win Chance S12–14 reskinned King Pac,
    #     2026-06-30). The mechanical gate gives FALSE COMFORT. So a hedged-pain slide is GREEN only when its
    #     visual_audit.tsv row PROVES the shape depicts THIS pain: serves=Y, verdict ∈ keep/simplify (NOT
    #     re-tool/remove/blank), and a non-empty note = the CONTRACT (which mechanism the shape encodes, fresh,
    #     not a swapped number on the reference organism). Missing row / serves=N / re-tool / empty note = FAIL.
    if not PROPOSAL and _is_pain(body):
        a = AUDIT.get(sid)
        if not a:
            add(sid, "pain-argues", False,
                "no visual_audit.tsv row — write the per-pain CONTRACT (serves=Y  verdict=keep/simplify  note=the mechanism the SHAPE depicts, designed fresh from THIS pain, distinct from any reference deck). Pain visuals gate on the sighted audit, not just the mechanical checks.")
        else:
            served = a[1] == "Y"; verdict_ok = a[3] in ("keep", "simplify", "polish"); has_note = bool(a[4])
            add(sid, "pain-argues", served and verdict_ok and has_note,
                "" if (served and verdict_ok and has_note) else
                "audit row: serves=%s verdict=%s note=%s — ship a pain visual only at serves=Y, verdict=keep/simplify, mechanism note FILLED. (re-tool/remove/blank/serves=N = the templated-dial regression — redesign the SHAPE to DEPICT the pain via /digiwin-deck-visual, then update the row.)"
                % (a[1] or "?", a[3] or "?", "set" if has_note else "EMPTY"))
    # 13b) SPEAK-TEST ENFORCED (Peter 2026-08-11 — "shrink the gap"): the most judgment-heavy sighted
    #     step becomes a FORCED ARTIFACT so it survives a weaker builder. Every hedged-pain slide and
    #     every data-chart slide must carry audit column 7 `stranger-says` — ONE sentence: what a
    #     stranger says the visual MEANS with all copy covered. Floor (mechanical): non-empty, >=15
    #     chars, not a copy of the message column. Ceiling (sighted): is the sentence TRUE of the
    #     render — read the PNG, and Peter spot-checks the claim in seconds. If you cannot write the
    #     sentence, the visual does not argue — redesign via /digiwin-deck-visual, then fill the row.
    if (not PROPOSAL and _is_pain(body)) or 'pq-chart' in body:
        a = AUDIT.get(sid)
        say = (a[5] if a and len(a) > 5 else "").strip()
        ok_say = bool(a) and len(say) >= 15 and say.lower() != (a[0].strip().lower() if a else "")
        add(sid, "speak-test", ok_say,
            "" if ok_say else
            "audit col 7 `stranger-says` %s — cover the copy and write the ONE sentence a stranger reads off the visual alone (>=15 chars, not the headline restated). Can't write it => the visual doesn't argue: redesign via /digiwin-deck-visual."
            % ("MISSING (no row)" if not a else ("EMPTY" if not say else "TOO THIN/RESTATED")))
    # 14) NO UN-RELABELED SCAFFOLD PLACEHOLDER VISUALS (Peter 2026-07-01 — the recurring deck-visual SKIP).
    #     S11 (empty 3-shape rail) + S2 (empty-circle icons) shipped ALL-GREEN because 'visual'/'informative'
    #     only check an <svg> EXISTS, not that it's REAL — both were scaffold defaults left un-relabeled, i.e.
    #     the /digiwin-deck-visual pass was skipped. Catch them OBJECTIVELY (no audit/honesty needed):
    if sid in CONTENT_SLIDES:
        ic_bad = False   # (a) placeholder ICON — an .ic slot whose svg is ONLY a bare circle/rect
        for ic in re.findall(r'<div class="ic"[^>]*>(.*?)</div>', body, re.S):
            if '<svg' in ic and '<img' not in ic and not re.search(r'<(?:path|polyline|line|image|text|use)\b', ic) and re.search(r'<(?:circle|rect)\b', ic):
                ic_bad = True
        rail_bad = False  # (b) unlabeled DIAGRAM — a rail-wrap whose svg is PRIMITIVE SHAPES (rect/circle/polygon,
        #     NOT <path> icons) AND carries NO label anywhere (neither an SVG <text> NOR an HTML `t-` label span) =
        #     the empty scaffold rail. A real labeled flow (path-icons + HTML .t-zh labels, e.g. the .cflow block)
        #     is NOT a placeholder — so require primitive shapes + zero labels, else we false-positive on real flows.
        m_rw = re.search(r'class="[^"]*rail-wrap[^"]*"(.*?)(?:brand-mark|</section>)', body, re.S)
        if m_rw:
            rw = m_rw.group(1)
            if '<svg' in rw and re.search(r'<(?:rect|circle|polygon)\b', rw) \
               and not re.search(r'<(?:text|tspan)\b', rw) and 'class="t-' not in rw:
                rail_bad = True
        _ph = ("empty-circle/rect icon; " if ic_bad else "") + ("unlabeled shape diagram (no <text>)" if rail_bad else "")
        add(sid, "no-placeholder", not (ic_bad or rail_bad),
            "" if not (ic_bad or rail_bad) else
            "UN-RELABELED SCAFFOLD PLACEHOLDER — " + _ph + ". A bare circle/rect icon or an unlabeled shape diagram is FILLER, not a visual (the /digiwin-deck-visual pass was skipped). Rebuild via /digiwin-deck-visual: a communicative find_icon pictograph, or a LABELED diagram that argues.")

    # 15) RESKIN-SUSPECT — a scaffold-default / prior-deck ARGUMENT organism left intact = the "scent"
    #     (Peter 2026-07-17, the S8 automation-factory burn: the Unilever "ERP-brain -> floor-stations -> eMES"
    #     diagram was reused for a greenfield no-ERP company + text-swapped — it FABRICATED a factory-automation
    #     need the client never stated AND its shape argued the WRONG company's logic). Reusing LAYOUT blocks
    #     (stat-row / card / .pq / cover / chrome) is FINE — that's the brand; reusing an ARGUMENT diagram's
    #     STRUCTURE is the scent. Registry = known scaffold/prior-deck argument-organism class skeletons; GROW it
    #     as new scents are caught. Pass only if absent OR justified with <!-- FRESH: why this shape is THIS
    #     company's argument, not the scaffold's -->. Acceptance-criteria §0 (SWAP TEST + PROVENANCE) is the judgment.
    if sid in CONTENT_SLIDES:
        RESKIN_ORGANISMS = {
            's8b2-brain': 'ERP-brain -> floor-stations (eMES) diagram — a greenfield/no-ERP firm has NO brain to bolt floor-eyes onto; redesign the argument-shape from THIS company\'s real situation',
            's8b2-nerves': 'ERP-brain nerve-fan (eMES) diagram — same reskin family',
        }
        hit = next((msg for cls, msg in RESKIN_ORGANISMS.items() if cls in body), None)
        fresh = '<!-- FRESH' in body
        add(sid, "reskin-suspect", (hit is None) or fresh,
            "" if (hit is None or fresh) else
            "SCAFFOLD/PRIOR-DECK ARGUMENT ORGANISM INTACT — " + hit + ". SWAP TEST: would this visual + framing work UNCHANGED for a different company? If yes, it's borrowed structure — redesign the SHAPE from THIS slide's claim via /digiwin-deck-visual, or justify with <!-- FRESH: reason -->. (acceptance-criteria §0)")

# ---- SDD-MATCH — the content-first tier (Peter 2026-07-13) ---------------------
# Tatung had per-slide specs and the practice DECAYED because nothing enforced it. This check makes the
# C1/C2 artifacts load-bearing: every slide must have a spec, and the build must MATCH what the spec declared.
# Mechanical floor only — spec QUALITY (does the scene argue? is the metaphor fresh?) stays a sighted judgment.
# Legacy decks built before 2026-07-13: run with --no-sdd (explicit, visible in the command — not a default).
if not NO_SDD:
    _specdir = os.path.join(_deckdir, "specs")
    SDD = {}
    if os.path.isdir(_specdir):
        for _fn in sorted(os.listdir(_specdir)):
            _m = re.match(r"(\d{1,2})-.*\.md$", _fn)
            if _m:
                SDD[int(_m.group(1))] = open(os.path.join(_specdir, _fn), encoding="utf-8").read()
    _has_pack = any(f.startswith("content-") and f.endswith(".md") for f in os.listdir(_deckdir))
    _has_arc  = os.path.exists(os.path.join(_deckdir, "SPEC.md"))
    for sid, _cls, _body in SECS:
        sp = SDD.get(sid)
        if sp is None:
            add(sid, "sdd-match", False,
                "no specs/%02d-*.md — the C2 spec tier is REQUIRED (content-first, Peter 2026-07-13). Back-fill the spec or, for a pre-2026-07-13 deck, run with --no-sdd." % sid)
            continue
        probs = []
        # 1) source fact non-empty (the mechanical specificity gate)
        _sf = re.search(r"\*\*Source fact\*\*\s*(.+?)(?:\n\s*\n|\n- \*\*)", sp, re.S)
        if not (_sf and _sf.group(1).strip().strip("-–— ").strip()):
            probs.append("Source fact empty/missing (a slide with no source fact is templated by definition)")
        # 1b) Arc answers present + filled (Peter 2026-07-25: a slide may not be GENERATED until its
        #     arc-questions are answered with sources — references/arc-questions.md. An honest
        #     "unknown - must learn in the meeting" is a valid answer; a blank or {{placeholder}} is not.)
        _aa = re.search(r"##\s*Arc answers\s*\n(.*?)(?:\n##\s|\Z)", sp, re.S)
        if not _aa:
            probs.append("## Arc answers missing — answer references/arc-questions.md for this slot BEFORE spec'ing (Peter 2026-07-25)")
        else:
            _lines = [l.strip() for l in _aa.group(1).splitlines() if l.strip().startswith(("-", "Q"))]
            _bad = [l[:48] for l in _lines if re.search(r"(→|->)\s*$", l) or "{{" in l]
            if len(_lines) < 2:
                probs.append("## Arc answers has <2 answered lines — the interrogation was skipped")
            elif _bad:
                probs.append("## Arc answers has empty/placeholder answers: %s" % _bad[:2])
        # 2) declared block classes appear in this slide's HTML (layout = a block choice)
        _cl = set(re.findall(r"`\.([a-z][a-z0-9-]{1,24})`", sp))
        if _cl and not any(c in _body for c in _cl):
            probs.append("none of the spec's declared block classes %s found in the slide" % sorted(_cl)[:4])
        # 3) declared engine outputs exist on disk
        for _af in set(re.findall(r"assets/[A-Za-z0-9._-]+\.(?:png|jpg|jpeg|svg|webp)", sp)):
            if not os.path.exists(os.path.join(_deckdir, _af)):
                probs.append("declared %s missing on disk" % _af)
        add(sid, "sdd-match", not probs, "; ".join(probs))
    # deck-level artifacts (reported on the cover slide's row)
    if not _has_pack:
        add(COVER, "sdd-pack", False, "content-<company>.md missing (C1 kitchen prep) — see references/content-pack-template.md")
    if not _has_arc:
        add(COVER, "sdd-arc", False, "SPEC.md missing (C2 arc table) — see references/slide-sdd-template.md")

# ---- global / composed gates --------------------------------------------------
glob = []
# v2 scaffold marker (Peter 2026-07-25 — the NO-COPY law): a NEW first-visit deck must be composed from
# _scaffold-firstvisit-v2.html, never copied from a prior deck's index.html (that's how the SATS look
# bled into every deck). Legacy pre-v2 decks run with --no-sdd (same escape as the SDD tier).
if not NO_SDD and not PROPOSAL:
    glob.append(("scaffold-v2", "SCAFFOLD: firstvisit-v2" in html,
                 "missing <!-- SCAFFOLD: firstvisit-v2 --> — deck was not composed from the v2 scaffold. Start from _scaffold-firstvisit-v2.html (12 slots / 5 acts, SLOTS-FIRSTVISIT.md); copying a prior deck is a gate FAIL. Pre-v2 decks: run with --no-sdd."))
glob.append(("fit=clientWidth", "window.innerWidth/1920" not in html,
             "fitDeck must scale by clientWidth (else white columns on dark slides)"))
glob.append(("lang-toggle", 'id="lang-toggle"' in html and all(("lang-%s"%l) in html for l in LANGS)
             and (('data-lang="ja"' in html) if HAS_JA else True),
             "need one pill per DECLARED language %s (<!-- LANGS: ... -->; ja only when a Japanese contact/shareholder — Peter 2026-07-13)" % LANGS))
# CHROME ZONING: the 4-pill toggle (~298px from right edge) overflows a top-right-anchored #present-view-btn
# (the old right:236px pattern was sized for 3 pills) → proven 62×39px overlap, 日本語 pill unclickable.
# Top-right = #lang-toggle ONLY; notes/present control belongs in the bottom zone. (Peter 2026-06-30)
_pvb_topright = bool(re.search(r'#present-view-btn\s*\{[^}]*\btop:\s*\d', html)) and bool(re.search(r'#present-view-btn\s*\{[^}]*\bright:\s*\d', html))
glob.append(("chrome-zoning", not _pvb_topright,
             "a top-right-anchored #present-view-btn (top:+right: offsets) collides with the 4-pill 日本語 toggle (62px overlap → unclickable). Move the notes/present control to the BOTTOM zone; top-right holds only #lang-toggle."))
# LANGUAGE balance across the DECLARED set: every text node carries one span per declared language
_qcnt = {l: html.count('class="t-%s"'%l) for l in LANGS}
_bal  = _qcnt["zh"] == _qcnt["en"] and (_qcnt.get("ja", _qcnt["zh"]) == _qcnt["zh"]) and _qcnt["th"] >= _qcnt["zh"]
glob.append(("lang-balance", _bal,
             "span counts off %s — every t-zh needs a sibling per declared language; t-th may carry intentional single-lang extras (ja decks: run add_japanese)"%_qcnt))
# no UNTRANSLATED Japanese (only when ja is declared): a t-ja that is a verbatim CJK copy of its t-zh (>=8 chars)
if HAS_JA:
    _zhset = set(re.findall(r'<span class="t-zh">([^<]{8,})</span>', html))
    _jadup = sorted(set(t for t in re.findall(r'<span class="t-ja">([^<]{8,})</span>', html) if t in _zhset and re.search(r"[\u3400-\u9fff]", t)))
    glob.append(("ja-translated", not _jadup, ("t-ja left as Chinese: " + " | ".join(_jadup[:4])) if _jadup else ""))
glob.append(("tax-id present", bool(re.search(r'\b\d{13}\b', html)), "a 13-digit juristic ID must appear (the company snapshot)"))
# emphasis must actually RENDER: `.em` used in markup but only descendant-scoped in CSS (e.g. `.lead .em`)
# paints as plain text — emphasis present but DEAD (the King Pac 2026-06-29 burn). Require a global `.em{` rule.
_uses_em = 'class="em"' in html
_em_styled = bool(re.search(r'(?:^|[}\n,])\s*\.em\s*[,{]', html)) or ('blocks.css' in html)
glob.append(("emphasis-styled", (not _uses_em) or _em_styled,
             "`.em` is used in markup but only descendant-scoped in CSS (e.g. `.lead .em`) → highlights render as PLAIN TEXT. Add a global `.em{...}` rule."))
# COMPLETENESS: a sales/visit/co-sell deck MUST carry the presenter-notes system (the live talk-track /
# 六要素 discovery script). The scaffold dropped it 2026-06-30 → every deck since lost it and it reached Peter.
# Require a NOTES object with an entry per slide PLUS a presenter SURFACE. Two surfaces are valid (Peter 2026-07-01):
#   (a) SEPARATE WINDOW — `openPresenter()` + a `#present-view-btn` (his private notes in another window; PREFERRED —
#       keeps the customer-facing deck clean), OR (b) inline `#notes-panel`. An inline panel that sits ON the deck and
#       follows the slide is NOT wrong per se, but the separate window is what Peter asked to keep "like before".
_n_obj = bool(re.search(r'\bNOTES\s*=\s*\{', html))
_n_count = len(re.findall(r'^\s*\d+\s*:', html, re.M)) if _n_obj else 0
_n_window = ('openPresenter' in html) and ('present-view-btn' in html)   # separate-window presenter (king-pac style)
_n_panel  = 'id="notes-panel"' in html                                    # inline drawer
_n_surface = _n_window or _n_panel
glob.append(("presenter-notes", _n_surface and _n_obj and _n_count >= len(_ALL)-0,
             "presenter-notes system missing/incomplete (need a NOTES object with an entry per slide + a presenter surface: "
             "EITHER a separate-window `openPresenter()`/#present-view-btn OR an inline #notes-panel — the live talk-track). Restore from the scaffold."
             if not (_n_surface and _n_obj) else
             ("NOTES has %d entries for %d slides — author one per slide" % (_n_count, len(_ALL)))))
# THOROUGHNESS + BILINGUAL (Peter 2026-07-01 — "I don't read Thai/日本語 natively; the presenter notes must HELP me
# UNDERSTAND the slide, so make them thorough"). A note is only useful to a presenter who can't read the slide's
# on-screen language if it (a) exists in a language he DOES read — BOTH 繁中 AND EN, toggled in the window — and
# (b) is THOROUGH: it first says what the slide SHOWS/MEANS in plain language, then the talk-track. Enforce:
#   · every slide's NOTES entry has NON-EMPTY zh AND en   · each above a length floor (no terse shorthand)
#   · the presenter WINDOW carries the 中/EN toggle (nlang).   Flat Chinese-only / one-liner notes now FAIL.
_ZH_FLOOR, _EN_FLOOR = 40, 55
_win_toggle = ('nlang' in html)                       # the in-window 中/EN note-language toggle (APC-style window)
_notes_problems = []
if _n_obj:
    _mb = re.search(r'\bNOTES\s*=\s*\{(.*?)\n\}\s*;', html, re.S) or re.search(r'\bNOTES\s*=\s*\{(.*)\}\s*;', html, re.S)
    _bn = _mb.group(1) if _mb else ''
    for _em in re.finditer(r'(\d+)\s*:\s*\{([^{}]*)\}', _bn, re.S):
        _n = _em.group(1); _inner = _em.group(2)
        _zh = re.search(r'zh\s*:\s*"((?:[^"\\]|\\.)*)"', _inner)
        _en = re.search(r'en\s*:\s*"((?:[^"\\]|\\.)*)"', _inner)
        _zt = (_zh.group(1) if _zh else '').strip(); _et = (_en.group(1) if _en else '').strip()
        if not _zt or not _et:
            _notes_problems.append("S%s missing %s" % (_n, "en (Chinese-only)" if _zt else ("zh" if _et else "zh+en")))
        elif len(_zt) < _ZH_FLOOR or len(_et) < _EN_FLOOR:
            _notes_problems.append("S%s too terse (zh %d/%d, en %d/%d — explain the slide, not just the talk-track)" % (_n, len(_zt), _ZH_FLOOR, len(_et), _EN_FLOOR))
glob.append(("notes-thorough", _n_obj and _win_toggle and not _notes_problems,
             ("presenter notes must be BILINGUAL {zh,en} + THOROUGH + toggled in-window (Peter: 'I don't read Thai/JP — the notes must help me understand the slide'). "
              + ("presenter WINDOW is missing the 中/EN toggle (nlang) — upgrade openPresenter to the bilingual window. " if not _win_toggle else "")
              + ("Notes: " + "; ".join(_notes_problems[:8]) if _notes_problems else ""))
             if (not _win_toggle or _notes_problems) else ""))
# CREDIBILITY: Digiwin's trust proof should appear somewhere (client scale / TSMC supply-chain depth).
glob.append(("credibility", ('55,000' in html) or ('TSMC' in html) or ('44' in html and '製造業' in html),
             "no Digiwin credibility proof (55,000+ clients / 92% of TSMC suppliers / 44-yr maker) — add it to the trust slide"))

def run(script):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), DECK], capture_output=True, text=True)
    out = p.stdout + p.stderr
    ok = ("CONTAMINATION" not in out and "OVERLAPS" not in out and "BLEED" not in out
          and "✗ svg-fit" not in out)
    return ok, out.strip().splitlines()[-3:]
for s, label in [("lang_purity.py", "lang-purity"), ("overlap_check.py", "overlap"), ("svg_fit_check.py", "svg-fit")]:
    if os.path.exists(os.path.join(HERE, s)):
        ok, tail = run(s)
        glob.append((label, ok, "" if ok else " | ".join(tail)))

# ---- report -------------------------------------------------------------------
RST="\033[0m"; RED="\033[31m"; GRN="\033[32m"
def mark(ok): return GRN+"✓"+RST if ok else RED+"✗"+RST
fails = 0
print("\n=== SLIDE GATE — %s ===" % os.path.basename(DECK))
print("--- GLOBAL ---")
for name, ok, det in glob:
    fails += not ok
    print("  %s %-20s %s" % (mark(ok), name, "" if ok else RED+det+RST))
print("--- PER SLIDE ---")
for sid, cls, body in SECS:
    title = re.search(r'slide-title">.*?<span class="t-zh">([^<]{0,18})', body)
    nm = title.group(1) if title else (cls.strip() or "")
    row = results[sid]
    nf = sum(1 for _,ok,_ in row if not ok)
    fails += nf
    flags = "  ".join("%s%s"%(mark(ok), "" ) + r for r,ok,_ in row if not ok)
    badge = (GRN+"PASS"+RST) if nf==0 else (RED+"%d✗"%nf+RST)
    print("  S%-2d %-5s %-14s %s" % (sid, badge, nm[:14], ""))
    for r, ok, det in row:
        if not ok:
            print("        %s %-16s %s" % (mark(ok), r, RED+det+RST))
if lite_slides:
    print("\n--- ⚑ VIS-LITE worklist (declared text/icon-only — upgrade to an informative graphic) ---")
    print("  slides: " + ", ".join("S%d"%s for s in sorted(set(lite_slides))))
# ---- MEASURABLE OUTPUT: VALIDATION.md (mechanical gate + sighted-audit ledger; AUDIT parsed above) ----
if REPORT:
    import datetime
    L = ["# Validation Report — %s" % os.path.basename(DECK),
         "_Generated %s · regenerate with `slide_gate.py <deck> --report`. A slide is **validated** only when it is"
         " mechanical-green AND its sighted visual-serves-message audit passes._\n" % datetime.date.today().isoformat(),
         "**Global:** " + " · ".join("%s %s" % ("✅" if ok else "❌", n) for n, ok, _ in glob) + "\n",
         "Acceptance per slide = **Mechanical** (gate) · **Serves message** (glanceable, right visual) · **Layout** "
         "(vertically balanced, no dead void / off-centre, on-grid, chrome clear). All three ✅ → validated.\n",
         "| Slide | Title | Mechanical | Serves msg | Layout | Status |",
         "|---|---|---|---|---|---|"]
    full = 0
    for sid, cls, body in SECS:
        t = re.search(r'slide-title">.*?<span class="t-zh">([^<]{0,20})', body)
        nm = (t.group(1) if t else cls.strip()) or "—"
        nf = sum(1 for _, ok, _ in results[sid] if not ok)
        mech = "✅ all" if nf == 0 else "❌ " + ",".join(r for r, ok, _ in results[sid] if not ok)
        a = AUDIT.get(sid)
        served = bool(a) and a[1] == "Y"
        laidout = bool(a) and a[2] == "Y"
        smsg = ("✅ " + a[0]) if served else (("❌ " + a[0]) if a else "⏳ not audited")
        slay = ("✅ " + (a[4] if a[4] else "balanced")) if laidout else (("❌ " + (a[4] or "fix layout")) if a else "⏳")
        done = nf == 0 and served and laidout
        full += done
        L.append("| S%d | %s | %s | %s | %s | %s |" % (sid, nm, mech, smsg, slay, "✅ validated" if done else "⏳ pending"))
    tot = len(SECS)
    L.append("\n**%d / %d slides fully validated** (mechanical-green AND sighted-audit-pass)." % (full, tot))
    if lite_slides:
        L.append("\n⚑ VIS-LITE upgrade worklist: " + ", ".join("S%d" % s for s in sorted(set(lite_slides))))
    open(os.path.join(os.path.dirname(os.path.abspath(DECK)), "VALIDATION.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n📋 wrote VALIDATION.md — %d/%d slides fully validated" % (full, tot))

print("\n%s  total ✗ = %d  %s" % ((GRN+"ALL GREEN"+RST) if fails==0 else (RED+"GATE FAILED"+RST), fails,
                                  "→ deck may proceed to the SIGHTED gate (render + READ PNGs)" if fails==0 else "→ redo the ✗ items, re-run"))
sys.exit(1 if fails else 0)
