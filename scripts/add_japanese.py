#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_japanese.py — upgrade a trilingual (中/EN/ไทย) Digiwin deck to quad-lingual by
inserting a `t-ja` sibling next to every `t-th` node, the 4th toggle pill, and the
lang-ja CSS/JS. STRUCTURAL: it never drops a node (the gate fails on a missing t-ja),
the translations come from an authored JSON map keyed by the t-zh inner HTML.

  Extract the keys to translate:
    python3 add_japanese.py extract <deck.html> <map.json>
      → writes/merges {zh_inner: ""}  (fill the empty values with Japanese, keep markup)
  Apply (fails loudly if any key is unmapped / empty):
    python3 add_japanese.py apply <deck.html> <map.json>
      → inserts t-ja spans/texts + 4-pill toggle + lang-ja CSS/JS, in place

Groups = a maximal run of adjacent t-zh/t-en/t-th elements of the same tag (span OR
SVG text), whitespace-separated. Within a group: key = the t-zh inner; insert point =
right after the t-th element (clone its open tag, swap class → t-ja). Order-agnostic
(handles th-before-zh groups). Idempotent guard: refuses to apply twice.
"""
import sys, re, json, io

def elements_of(html, tag):
    """All <tag ... class="t-zh|t-en|t-th"> elements with nesting-correct inner spans."""
    classpat = re.compile(r'<%s\b[^>]*\bclass="(t-(?:zh|en|th))"[^>]*>' % tag)
    openpat  = re.compile(r'<%s\b' % tag)
    closepat = re.compile(r'</%s>' % tag)
    out = []
    for m in classpat.finditer(html):
        cls = m.group(1); inner_start = m.end(); depth = 1; i = inner_start
        inner_end = after = None
        while depth > 0:
            no = openpat.search(html, i); nc = closepat.search(html, i)
            if not nc:
                raise SystemExit("unbalanced <%s> near offset %d" % (tag, m.start()))
            if no and no.start() < nc.start():
                depth += 1; i = no.end()
            else:
                depth -= 1
                if depth == 0:
                    inner_end = nc.start(); after = nc.end()
                else:
                    i = nc.end()
        out.append({"tag": tag, "cls": cls, "start": m.start(), "inner_start": inner_start,
                    "inner_end": inner_end, "after": after,
                    "open": html[m.start():inner_start], "inner": html[inner_start:inner_end]})
    return out

def groups(html):
    """Yield groups (lists of element-records) of adjacent same-tag t-XX elements.
    A group breaks on a non-whitespace gap, a tag change, OR a class repeating
    (so zh,en,th,zh,en,th in one SVG = TWO groups, not one)."""
    allg = []
    for tag in ("span", "text"):
        els = sorted(elements_of(html, tag), key=lambda e: e["start"])
        cur = []
        for e in els:
            adj = bool(cur) and html[cur[-1]["after"]:e["start"]].strip() == "" and cur[-1]["tag"] == e["tag"]
            repeat = any(x["cls"] == e["cls"] for x in cur)
            if adj and not repeat:
                cur.append(e)
            else:
                if cur: allg.append(cur)
                cur = [e]
        if cur: allg.append(cur)
    return allg

def do_strip(deck, _mapfile=None):
    """Revert a quad-lingual deck back to trilingual (remove t-ja nodes + toggle/CSS/JS)."""
    html = io.open(deck, encoding="utf-8").read()
    # remove t-ja nodes (nesting-correct), rightmost first
    spans, classpat = [], re.compile(r'<(span|text)\b[^>]*\bclass="t-ja"[^>]*>')
    cuts = []
    for m in classpat.finditer(html):
        tag = m.group(1); depth = 1; i = m.end()
        op = re.compile(r'<%s\b' % tag); cl = re.compile(r'</%s>' % tag)
        while depth > 0:
            no = op.search(html, i); nc = cl.search(html, i)
            if not nc: break
            if no and no.start() < nc.start(): depth += 1; i = no.end()
            else:
                depth -= 1
                if depth == 0: cuts.append((m.start(), nc.end()))
                else: i = nc.end()
    for a, b in sorted(cuts, key=lambda x: -x[0]):
        html = html[:a] + html[b:]
    html = html.replace("\n  " + TOGGLE_PILL, "").replace(TOGGLE_PILL, "")
    html = html.replace(CSS_BASE_NEW, CSS_BASE_OLD, 1).replace(CSS_RULE_ADD, CSS_RULE_ANCHOR, 1)
    html = html.replace(JS_NEW, JS_OLD, 1)
    io.open(deck, "w", encoding="utf-8").write(html)
    print("strip: removed %d t-ja nodes; reverted toggle/CSS/JS. t-zh=%d t-ja=%d" %
          (len(cuts), html.count('class="t-zh"'), html.count('class="t-ja"')))

def keys(html):
    out = []
    for g in groups(html):
        zh = next((e for e in g if e["cls"] == "t-zh"), None)
        if zh: out.append(zh["inner"])
    # unique, keep order
    seen = set(); uniq = []
    for k in out:
        if k not in seen:
            seen.add(k); uniq.append(k)
    return uniq

def do_extract(deck, mapfile):
    html = io.open(deck, encoding="utf-8").read()
    try:
        existing = json.load(io.open(mapfile, encoding="utf-8"))
    except Exception:
        existing = {}
    n_new = 0
    for k in keys(html):
        if k not in existing:
            existing[k] = ""; n_new += 1
    json.dump(existing, io.open(mapfile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    todo = sum(1 for v in existing.values() if not v.strip())
    print("extract: %d unique zh keys, %d new, %d still need Japanese → %s" %
          (len(keys(html)), n_new, todo, mapfile))

TOGGLE_PILL = '<button type="button" data-lang="ja">日本</button>'
CSS_BASE_OLD = ".t-th{display:none;} .t-en{display:none;}"
CSS_BASE_NEW = ".t-th{display:none;} .t-en{display:none;} .t-ja{display:none;}"
CSS_RULE_ANCHOR = "body.lang-en .t-zh{display:none;} body.lang-en .t-en{display:revert;}"
CSS_RULE_ADD = ("body.lang-en .t-zh{display:none;} body.lang-en .t-en{display:revert;}\n"
                "body.lang-ja .t-zh{display:none;} body.lang-ja .t-ja{display:revert;}\n"
                "body.lang-ja{font-family:'Hiragino Sans','Noto Sans JP','Noto Sans',system-ui,sans-serif;}")
JS_OLD = ("      document.body.classList.toggle('lang-zh', lang==='zh');\n"
          "      document.documentElement.lang = lang==='en' ? 'en' : (lang==='th' ? 'th' : 'zh-Hant');")
JS_NEW = ("      document.body.classList.toggle('lang-zh', lang==='zh');\n"
          "      document.body.classList.toggle('lang-ja', lang==='ja');\n"
          "      document.documentElement.lang = lang==='en' ? 'en' : (lang==='th' ? 'th' : (lang==='ja' ? 'ja' : 'zh-Hant'));")

def do_apply(deck, mapfile):
    html = io.open(deck, encoding="utf-8").read()
    if 'class="t-ja"' in html:
        raise SystemExit("ABORT: deck already has t-ja nodes (apply is not idempotent). Re-run from the trilingual source.")
    TR = json.load(io.open(mapfile, encoding="utf-8"))
    missing = []
    inserts = []   # (position, text)
    for g in groups(html):
        zh = next((e for e in g if e["cls"] == "t-zh"), None)
        th = next((e for e in g if e["cls"] == "t-th"), None)
        host = th or zh or g[-1]
        key = zh["inner"] if zh else None
        if key is None:
            continue   # intentional single-language node (e.g. a th-only legal name) — leave as-is
        ja = TR.get(key, "")
        if not ja.strip():
            missing.append(key); continue
        new_open = host["open"].replace(host["cls"], "t-ja", 1)
        node = new_open + ja + ("</%s>" % host["tag"])
        inserts.append((host["after"], node))
    if missing:
        print("APPLY ABORTED — %d unmapped/empty Japanese keys:" % len(missing))
        for k in missing[:60]:
            print("   • " + k.replace("\n", " ")[:90])
        sys.exit(1)
    for pos, node in sorted(inserts, key=lambda x: -x[0]):
        html = html[:pos] + node + html[pos:]
    # toggle pill (after the 中 button)
    if TOGGLE_PILL not in html:
        html = re.sub(r'(<button[^>]*data-lang="zh"[^>]*>中</button>)',
                      r'\1\n  ' + TOGGLE_PILL, html, count=1)
    # CSS
    html = html.replace(CSS_BASE_OLD, CSS_BASE_NEW, 1)
    html = html.replace(CSS_RULE_ANCHOR, CSS_RULE_ADD, 1)
    # JS
    html = html.replace(JS_OLD, JS_NEW, 1)
    io.open(deck, "w", encoding="utf-8").write(html)
    # sanity report
    nzh = html.count('class="t-zh"'); nja = html.count('class="t-ja"')
    print("apply: inserted %d t-ja nodes (t-zh=%d, t-ja=%d). toggle/CSS/JS patched." %
          (len(inserts), nzh, nja))
    for label, needle in [("toggle-pill", TOGGLE_PILL), ("css-base", CSS_BASE_NEW),
                          ("css-rule", "body.lang-ja .t-ja"), ("js", "toggle('lang-ja'")]:
        print("   %s %s" % ("OK " if needle in html else "MISS", label))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "strip" and len(sys.argv) >= 3:
        do_strip(sys.argv[2]); raise SystemExit(0)
    if len(sys.argv) != 4 or mode not in ("extract", "apply"):
        raise SystemExit(__doc__)
    (do_extract if mode == "extract" else do_apply)(sys.argv[2], sys.argv[3])
