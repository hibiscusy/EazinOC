import os
"""Rebuild relationship-map.html per user's reference grid layout.

Reference layout from screenshot:
  Top:    铃兰(L) —————— 谶(R)          [妈妈线]
  Upper:       度漪(center)             [师父线→谶]
  Mid-L:  铃兰 | 斯沃德 — 烬行 — 赛博恩 | 谶  [救治/教射箭/兄弟/爸爸]
  Bot:            塔拉(center)          [相遇L形绕右]

Node grid coords (viewBox 0 0 720 680):
  铃兰=(120,120) 谶=(600,120) 度漪=(360,220)
  斯沃德=(120,420) 烬行=(360,420,r40) 赛博恩=(600,420)
  塔拉=(360,600)
"""

import base64, math, pathlib, re

ROOT = pathlib.Path(r"os.path.dirname(os.path.abspath(__file__))")
CROPS = ROOT / "crops"

# ── Node definitions ──────────────────────────────────────────────
NODES = {
    "L": dict(name="铃兰",   en="LYNPHREDIL", cx=120, cy=120, r=32,
              img="anime_2", stroke="#5DA87A", name_fill="#98D4AD"),
    "C": dict(name="谶",     en="CHAIN",     cx=600, cy=120, r=32,
              img="anime_3", stroke="#B07568", name_fill="#D4ADA4"),
    "D": dict(name="度漪",   en="DU YI",     cx=360, cy=220, r=32,
              img="anime_5", stroke="#6B5640", name_fill="#A89A88"),
    "S": dict(name="斯沃德", en="SWORD MELON",cx=120, cy=420, r=32,
              img="anime_4", stroke="#C97D42", name_fill="#E8BC94"),
    "J": dict(name="烬行",   en="JINXING",   cx=360, cy=420, r=40,
              img="anime_1", stroke="#7BA3C0", name_fill="#B8D4E8"),
    "B": dict(name="赛博恩", en="CYBORN",    cx=600, cy=420, r=32,
              img="anime_7", stroke="#D8E0EC", name_fill="#EFF3F8"),
    "T": dict(name="塔拉撒里昂",en="THALASSARION",cx=360,cy=600,r=32,
              img="anime_6", stroke="#E8D47A", name_fill="#F5EBB8"),
}

# ── Edge definitions (from_id → to_id, color, label, bidirectional?) ─
EDGES = [
    ("L", "C", "#993556", "妈妈",   False),  # 铃兰→谶
    ("D", "C", "#534AB7", "师父",   False),  # 度漪→谶
    ("B", "C", "#993556", "爸爸",   False),  # 赛博恩→谶
    ("L", "S", "#3B6D11", "救治",   False),  # 铃兰→斯沃德
    ("J", "S", "#185FA5", "教射箭", False),  # 烬行→斯沃德
    ("J", "B", "#BA7517", "兄弟",   True),   # 烬行↔赛博恩 双向
    ("C", "T", "#0F6E56", "相遇",   False),  # 谶→塔拉 (L-shape)
]

# ── Helpers ───────────────────────────────────────────────────────
COLOR_MAP = {"#534AB7":"purple","#993556":"pink","#0F6E56":"green",
             "#BA7517":"gold","#3B6D11":"olive","#185FA5":"blue"}

def color_name(hex_c):
    return COLOR_MAP[hex_c]


def edge_point(cx, cy, r, tx, ty):
    """Point on circle (cx,cy,r) towards (tx,ty)."""
    dx, dy = tx - cx, ty - cy
    d = math.hypot(dx, dy) or 1
    return cx + r * dx / d, cy + r * dy / d


def embed_b64(filename):
    p = CROPS / f"{filename}.webp"
    return base64.b64encode(p.read_bytes()).decode()


def rect_bg(x, y, w=44, h=22):
    return f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="6" fill="#0b1020"/>'


def label_text(x, y, text, fill):
    return f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="{fill}">{text}</text>'


# ── Build SVG ────────────────────────────────────────────────────
lines_xml = []
labels_xml = []

for fid, tid, color, label, bi in EDGES:
    fn = NODES[fn_id := fid]
    tn = NODES[tid]

    if fn_id == "C" and tid == "T":
        # 相遇: L-shape around right edge
        sx, sy = edge_point(fn["cx"], fn["cy"], fn["r"], 700, tn["cy"])
        ex, ey = edge_point(tn["cx"], tn["cy"], tn["r"], fn["cx"], tn["cy"])
        path_d = f"M{sx:.1f},{sy:.1f} L680,{sy:.1f} L680,{ey:.1f} L{ex:.1f},{ey:.1f}"
        lines_xml.append(f'<path d="{path_d}" stroke="{color}" fill="none" stroke-width="2" marker-end="url(#arr-{color_name(color)})"/>')
        # Label on bottom segment
        lx, ly = (680 + ex) / 2, ey
        labels_xml.append(rect_bg(lx, ly))
        labels_xml.append(label_text(lx, ly, label, "#1D9E75"))
    else:
        sx, sy = edge_point(fn["cx"], fn["cy"], fn["r"], tn["cx"], tn["cy"])
        ex, ey = edge_point(tn["cx"], tn["cy"], tn["r"], fn["cx"], fn["cy"])
        marker = f' marker-end="url(#arr-{color_name(color)})"'
        if bi:
            marker += f' marker-start="url(#arr-{color_name(color)}-rev)"'
        lines_xml.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{color}" stroke-width="2"{marker}/>')
        lx, ly = (sx + ex) / 2, (sy + ey) / 2
        lw = len(label) * 12 + 12
        labels_xml.append(rect_bg(lx, ly, lw, 22))
        labels_xml.append(label_text(lx, y=ly, text=label, fill=color))

# ── Marker defs ──────────────────────────────────────────────────
MARKERS = ""
for cid, cname in [("purple","#534AB7"),("pink","#993556"),("green","#0F6E56"),
                    ("gold","#BA7517"),("olive","#3B6D11"),("blue","#185FA5")]:
    MARKERS += f'''    <marker id="arr-{cid}" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 L2.5,5 Z" fill="{cname}"/></marker>
    <marker id="arr-{cid}-rev" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="3" refY="5" orient="auto-start-reverse"><path d="M12,0 L3,5 L12,10 L9.5,5 Z" fill="{cname}"/></marker>
'''

# ── Nodes XML ────────────────────────────────────────────────────
clips = ""
nodes_xml = ""

for nid, n in NODES.items():
    sz = n["r"] * 2  # image size = diameter
    ix = n["cx"] - sz // 2
    iy = n["cy"] - sz // 2
    b64 = embed_b64(n["img"])
    clips += f'    <clipPath id="c{nid}"><circle cx="{n["cx"]}" cy="{n["cy"]}" r="{n["r"]}"/></clipPath>\n'
    nodes_xml += f'''    <!-- {n["name"]} · {"中心节点" if nid=="J" else ""} -->
    <image href="data:image/webp;base64,{b64}" x="{ix}" y="{iy}" width="{sz}" height="{sz}" preserveAspectRatio="xMidYMid slice" clip-path="url(#c{nid})"/>
    <circle cx="{n["cx"]}" cy="{n["cy"]}" r="{n["r"]}" fill="none" stroke="{n["stroke"]}" stroke-width="2"/>
    <rect x="{n["cx"]-30}" y="{n["cy"]+n["r"]+8}" width="60" height="20" rx="6" fill="#0b1020"/>
    <text x="{n["cx"]}" y="{n["cy"]+n["r"]+22}" text-anchor="middle" fill="{n["name_fill"]}" font-size="12">{n["name"]}</text>
'''

# ── Assemble full HTML ───────────────────────────────────────────
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>星际猎手关系图</title>
<style>
  body {{ margin:0; background:#0b1020; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
  svg {{ max-width:100vmin; max-height:100vmin; }}
</style>
</head>
<body>
<svg viewBox="0 0 720 680" xmlns="http://www.w3.org/2000/svg">
  <desc>星际猎手关系图：网格布局。烬行为中心节点，连接兄弟赛博恩、教射箭斯沃德；谶连接妈妈铃兰、爸爸赛博恩、师父度漪、相遇塔拉撒里昂（右侧L形绕行）。</desc>

  <!-- 据点虚线框 -->
  <rect x="24" y="24" width="672" height="632" rx="16" fill="none" stroke="#1e2a4a" stroke-width="2" stroke-dasharray="8 4"/>

  <!-- Arrow markers -->
  <defs>
{MARKERS}
{clips}  </defs>

  <!-- Relationship lines -->
  <g fill="none" stroke-width="2">
{''.join(lines_xml)}
  </g>

  <!-- Relationship labels -->
  <g font-size="12" font-weight="500">
{''.join(labels_xml)}
  </g>

  <!-- Avatar nodes -->
{nodes_xml}
</svg>
</body>
</html>'''

out = ROOT / "relationship-map.html"
out.write_text(html, encoding="utf-8")
print(f"Written: {out.stat().st_size} bytes")
print(f"Nodes: {len(NODES)}, Edges: {len(EDGES)}, Lines: {len(lines_xml)}, Labels: {len([e for e in EDGES])}")
