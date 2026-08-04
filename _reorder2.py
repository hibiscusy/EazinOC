# -*- coding: utf-8 -*-
# Reverse-chronological reorder for OC story pages.
# Strategy: extract each <div class="node"> block ONCE (balanced-div scan),
# sort by parsed date DESC (stable), reassemble preserving exact whitespace.
# DRY RUN by default; pass --write to actually rewrite files.

import re, sys

FILES = [
    "story-tl.html",
    "story-chen.html",
    "story-cb.html",
    "story-jx.html",
    "OC宇宙-人物时间线-蒲熠星.html",
]

WRITE = "--write" in sys.argv

def parse_date(text):
    # 巡演期间 -> newest within year
    if "巡演" in text:
        m = re.search(r"(\d{4})", text)
        if m:
            return (int(m.group(1)), 13, 0)
    m = re.search(r"(\d{4})\.(\d{1,2})\.(\d{1,2})", text)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"(\d{4})\.(\d{1,2})", text)
    if m:
        return (int(m.group(1)), int(m.group(2)), 0)
    m = re.search(r"(\d{4})\s*年", text)
    if m:
        return (int(m.group(1)), 0, 0)
    m = re.search(r"(\d{4})", text)
    if m:
        return (int(m.group(1)), 0, 0)
    return (0, 0, 0)

def find_close(html, div_pos):
    # div_pos: index of '<' of the opening <div ...>; returns index of matching '</div>'
    assert html.startswith("<div", div_pos), html[div_pos:div_pos+20]
    open_end = html.find(">", div_pos) + 1
    depth = 1
    j = open_end
    while j < len(html):
        lt = html.find("<", j)
        if lt == -1:
            break
        if html.startswith("<div", lt):
            depth += 1
            j = html.find(">", lt) + 1
        elif html.startswith("</div>", lt):
            depth -= 1
            if depth == 0:
                return lt
            j = lt + 6
        else:
            j = lt + 1
    return len(html)

def find_node_end(inner, start):
    assert inner.startswith('<div class="node">', start), inner[start:start+20]
    open_end = inner.find(">", start) + 1
    depth = 1
    j = open_end
    while j < len(inner):
        lt = inner.find("<", j)
        if lt == -1:
            break
        if inner.startswith("<div", lt):
            depth += 1
            j = inner.find(">", lt) + 1
        elif inner.startswith("</div>", lt):
            depth -= 1
            if depth == 0:
                return lt + 6
            j = lt + 6
        else:
            j = lt + 1
    return -1

def split_nodes(inner):
    positions = []
    i = 0
    while True:
        idx = inner.find('<div class="node">', i)
        if idx == -1:
            break
        end = find_node_end(inner, idx)
        if end == -1:
            break
        positions.append((idx, end))
        i = end
    if not positions:
        return inner, [], ""
    leading = inner[:positions[0][0]]
    blocks = []
    for k, (s, e) in enumerate(positions):
        block = inner[s:e]
        nxt = positions[k+1][0] if k+1 < len(positions) else len(inner)
        sep = inner[e:nxt]
        blocks.append((block, sep))
    return leading, blocks, ""

def get_title(node):
    m = re.search(r'c-title">([^<]*)<', node)
    return m.group(1) if m else "?"

def get_date(node):
    m = re.search(r'c-date">([^<]*)<', node)
    return m.group(1) if m else ""

def reorder_inner(inner):
    leading, blocks, _ = split_nodes(inner)
    def keyf(b):
        return parse_date(get_date(b[0]))
    old_order = [(get_title(b), get_date(b)) for b, _ in blocks]
    blocks_sorted = sorted(blocks, key=keyf, reverse=True)
    new_inner = leading + "".join(b + s for b, s in blocks_sorted)
    new_order = [(get_title(b), get_date(b)) for b, _ in blocks_sorted]
    return new_inner, old_order, new_order

def reorder_tl_region(region):
    # region is substring starting at '<div class="tl">'
    tl_open_end = region.find(">", region.find('<div class="tl">')) + 1
    close = find_close(region, region.find('<div class="tl">'))
    inner = region[tl_open_end:close]
    new_inner, old_o, new_o = reorder_inner(inner)
    new_region = region[:tl_open_end] + new_inner + region[close:]
    return new_region, old_o, new_o

def process(html):
    new_html = html
    reports = []
    # tab-panels
    for m in list(re.finditer(r'<div class="tab-panel"', html)):
        div_pos = m.start()
        close = find_close(html, div_pos)
        panel = html[div_pos:close+6]
        new_panel, old_o, new_o = reorder_tl_region(panel)
        pid = re.search(r'id="([^"]+)"', panel)
        pid = pid.group(1) if pid else "?"
        reports.append(("tab:" + pid, old_o, new_o))
        new_html = new_html.replace(panel, new_panel, 1)
    # single .tl (files without tab-panels)
    if not re.search(r'<div class="tab-panel"', html):
        m = re.search(r'<div class="tl">', html)
        if m:
            div_pos = m.start()
            close = find_close(html, div_pos)
            region = html[div_pos:close+6]
            new_region, old_o, new_o = reorder_tl_region(region)
            reports.append(("single .tl", old_o, new_o))
            new_html = new_html.replace(region, new_region, 1)
    return new_html, reports

def main():
    for fn in FILES:
        try:
            html = open(fn, encoding="utf-8").read()
        except FileNotFoundError:
            print("MISSING:", fn)
            continue
        new_html, reports = process(html)
        changed = new_html != html
        print("=" * 70)
        print(fn, "  [CHANGED]" if changed else "  [unchanged]")
        for label, old_o, new_o in reports:
            if old_o == new_o:
                print("  - %s : order already correct (no change)" % label)
                continue
            print("  - %s : REORDER" % label)
            print("      OLD:")
            for t, d in old_o:
                print("        %s | %s" % (d, t))
            print("      NEW:")
            for t, d in new_o:
                print("        %s | %s" % (d, t))
        if changed and WRITE:
            # bump theme.css version to force refresh
            new_html = re.sub(r'theme\.css\?v=\w+', 'theme.css?v=20260805a', new_html)
            open(fn, "w", encoding="utf-8").write(new_html)
            print("    >> written (css version bumped to 20260805a)")
    print("=" * 70)
    print("DRY RUN (no files written)" if not WRITE else "WRITE COMPLETE")

if __name__ == "__main__":
    main()
