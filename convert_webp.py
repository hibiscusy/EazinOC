#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 crops/anime_1~7.png 转为同等透明度的 WebP，并批量改写所有 html 中的引用。

- 保留原 .png 作为未优化源（不删除）
- 仅转换角色图（7 张），pyx-photo.jpg 等不处理
- 引用替换：anime_N.png(?v=4)? -> anime_N.webp
"""
import os, re, glob
from PIL import Image

SRC = r"os.path.dirname(os.path.abspath(__file__))"
CROPS = os.path.join(SRC, "crops")

# 1) PNG -> WebP（保留 alpha 透明通道）
print("=== 转换图片 ===")
for i in range(1, 8):
    png = os.path.join(CROPS, f"anime_{i}.png")
    webp = os.path.join(CROPS, f"anime_{i}.webp")
    if not os.path.exists(png):
        print(f"  跳过（找不到）{png}")
        continue
    with Image.open(png) as im:
        im.save(webp, "WEBP", quality=92, method=6)
    op, nw = os.path.getsize(png), os.path.getsize(webp)
    print(f"  anime_{i}.png {op//1024}KB -> webp {nw//1024}KB  节省 {(1-nw/op)*100:.0f}%")

# 2) 批量改写 HTML 引用
print("=== 改写 HTML 引用 ===")
pat = re.compile(r"anime_([1-7])\.png(\?v=4)?")
total = 0
for html in sorted(glob.glob(os.path.join(SRC, "*.html"))):
    with open(html, encoding="utf-8") as f:
        s = f.read()
    ns, n = pat.subn(r"anime_\1.webp", s)
    if n:
        with open(html, "w", encoding="utf-8") as f:
            f.write(ns)
        total += n
        print(f"  {os.path.basename(html)}: {n} 处")
print(f"引用替换总计 {total} 处")
