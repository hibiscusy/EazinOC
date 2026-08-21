#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构造一个干净的发布目录 dist/，供 CloudStudio 部署分享。

- 入口 index.html = 首页副本（供根域名直接访问）
- 保留原中文名首页 OC宇宙-人物时间线-蒲熠星.html（story 页"返回"链接指向它）
- 复制 theme.css、7 个 story-*.html、crops 全部图片
"""
import os, shutil

SRC = r"os.path.dirname(os.path.abspath(__file__))"
DST = os.path.join(SRC, "dist")
HOMEPAGE = "OC宇宙-人物时间线-蒲熠星.html"

CORE_FILES = [
    HOMEPAGE, "theme.css", "tabs.js",
    "story-jx.html", "story-dy.html", "story-cb.html", "story-chen.html",
    "story-ll.html", "story-swd.html", "story-tl.html",
]

os.makedirs(DST, exist_ok=True)
for f in CORE_FILES:
    shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))

# 入口：首页副本
shutil.copy2(os.path.join(SRC, HOMEPAGE), os.path.join(DST, "index.html"))

# 图片目录：清理白名单外的旧文件后，仅复制被引用的资源（角色 webp + 蒲熠星照片）
crops_dst = os.path.join(DST, "crops")
os.makedirs(crops_dst, exist_ok=True)
need = set([f"anime_{i}.webp" for i in range(1, 8)] + ["pyx-photo.jpg"])
for f in os.listdir(crops_dst):
    if f not in need:
        try:
            os.remove(os.path.join(crops_dst, f))
        except OSError:
            pass
for img in sorted(need):
    sp = os.path.join(SRC, "crops", img)
    if os.path.exists(sp):
        shutil.copy2(sp, os.path.join(DST, "crops", img))

print("发布目录已生成:", DST)
for name in sorted(os.listdir(DST)):
    p = os.path.join(DST, name)
    if os.path.isfile(p):
        print(f"  {name}  ({os.path.getsize(p)} bytes)")
    else:
        print(f"  {name}/  ({len(os.listdir(p))} files)")
