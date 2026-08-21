import os
"""Embed relationship-map SVG into index.html, above the 日常 section, with 'OC关系网' title."""

import pathlib

ROOT = pathlib.Path(r"os.path.dirname(os.path.abspath(__file__))")

# Read the relationship map SVG
rm = ROOT / "relationship-map.html"
rm_text = rm.read_text(encoding="utf-8")
# Extract just the <svg>...</svg> block
import re
svg_match = re.search(r"(<svg.*?</svg>)", rm_text, re.S)
svg_block = svg_match.group(1)

# Build the section to insert (title + responsive container + svg)
section = f'''    <!-- OC关系网 -->
    <div class="sec-title">OC关系网</div>
    <div style="display:flex;justify-content:center;margin-bottom:32px;">
{svg_block}
    </div>

'''

# Insert into each index file
for idx_file in [ROOT / "OC宇宙-人物时间线-蒲熠星.html", ROOT / "dist" / "index.html"]:
    s = idx_file.read_text(encoding="utf-8")
    anchor = '<div class="sec-title" id="daily">日常</div>'
    if anchor not in s:
        print(f"WARNING: {idx_file.name} missing daily anchor!")
        continue
    if "OC关系网" in s:
        print(f"{idx_file.name}: already has OC关系网, skipping")
        continue
    new_s = s.replace(anchor, section + anchor)
    idx_file.write_text(new_s, encoding="utf-8")
    print(f"OK: {idx_file.name} ({len(new_s)} bytes)")

print("\nDone! Verify:")
for idx_file in ["dist/index.html", "OC宇宙-人物时间线-蒲熠星.html"]:
    p = ROOT / idx_file
    s = p.read_text(encoding="utf-8")
    has_title = "OC关系网" in s
    has_svg = "<svg" in s and "烬行" in s
    has_daily = 'id="daily"' in s
    order = s.find("OC关系网") < s.find('id="daily"')
    print(f"  {idx_file}: title={has_title} svg={has_svg} daily={has_daily} order_ok={order}")
