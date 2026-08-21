# -*- coding: utf-8 -*-
"""OC 宇宙站点图片优化:
1) 为 crops 中宽度>1000px 的 webp 生成 800px 宽缩略图 (_800.webp)
2) 重写所有站点 HTML 的 <img>: 懒加载 + 解码异步 + 响应式 srcset/sizes
   - 首图(fetchpriority=high, 不懒)以保 LCP
   - 灯箱大图(alt 含"大图")只用原图, 不加 srcset (放大仍清晰, 且同源走缓存)
3) 同步 crops 与编辑后的 HTML 到 dist/ 供 gh-pages 部署
"""
import os, re, shutil, glob
from PIL import Image

ROOT = r"os.path.dirname(os.path.abspath(__file__))"
CROPS = os.path.join(ROOT, "crops")
DIST = os.path.join(ROOT, "dist")

# ---------- 1. 生成响应式缩略图 ----------
print("== 生成 800w 缩略图 ==")
thumb_count = 0
for dp, _, fns in os.walk(CROPS):
    for fn in fns:
        if not fn.lower().endswith(".webp"):
            continue
        full = os.path.join(dp, fn)
        base, _ = os.path.splitext(full)
        thumb = base + "_800.webp"
        if os.path.exists(thumb):
            continue
        try:
            with Image.open(full) as im:
                im = im.convert("RGB")
                w, h = im.size
                if w <= 1000:
                    continue
                nw, nh = 800, max(1, round(h * 800 / w))
                im = im.resize((nw, nh), Image.LANCZOS)
                im.save(thumb, "WEBP", quality=82, method=4)
                thumb_count += 1
        except Exception as e:
            print("  ERR thumb:", full, e)
print("  新增缩略图:", thumb_count)

# ---------- 2. 重写 <img> 标签 ----------
IMG_RE = re.compile(r'<img\b[^>]*?>', re.IGNORECASE)
ATTR_RE = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*"([^"]*)"')

def rewrite_file(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    seen_first = {"v": False}
    def repl(m):
        tag = m.group(0)
        attrs = dict(ATTR_RE.findall(tag))
        src = attrs.get("src", "")
        base = src.split("?")[0]
        q = ("?" + src.split("?", 1)[1]) if "?" in src else ""
        is_first = not seen_first["v"]
        seen_first["v"] = True
        for k in ("loading", "decoding", "srcset", "sizes", "fetchpriority"):
            attrs.pop(k, None)
        is_lightbox = "大图" in attrs.get("alt", "")
        if is_first:
            attrs["fetchpriority"] = "high"
            attrs["decoding"] = "async"
        else:
            attrs["loading"] = "lazy"
            attrs["decoding"] = "async"
        # 响应式: 仅 crops 下的 webp 且有缩略图; 灯箱大图保持原图
        if base.lower().endswith(".webp") and base.startswith("crops/") and not is_lightbox:
            thumb = base[:-5] + "_800.webp"
            if os.path.exists(os.path.join(ROOT, thumb)):
                attrs["srcset"] = f"{src} 1600w, {thumb}{q} 800w"
                attrs["sizes"] = "(max-width: 768px) 100vw, 800px"
        order = ["src", "srcset", "sizes", "alt", "class", "width", "height",
                 "loading", "decoding", "fetchpriority"]
        parts = []
        for k in order:
            if k in attrs:
                parts.append(f'{k}="{attrs.pop(k)}"')
        for k, v in attrs.items():
            parts.append(f'{k}="{v}"')
        return "<img " + " ".join(parts) + ">"
    new_html, n = IMG_RE.subn(repl, html)
    if n:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
    return n

# 根目录站点 HTML (排除旧残留 _old_rm.html)
root_html = [f for f in glob.glob(os.path.join(ROOT, "*.html"))
             if os.path.basename(f) != "_old_rm.html"]
# dist 下独有的关系图
dist_only = [os.path.join(DIST, "relationship-map.html")]

total = 0
for p in root_html + dist_only:
    if os.path.exists(p):
        n = rewrite_file(p)
        if n:
            total += n
            print(f"  改写 {os.path.relpath(p, ROOT)}: {n} 个 img")
print("  改写 img 总数:", total)

# ---------- 3. 同步到 dist/ ----------
print("== 同步到 dist/ ==")
shutil.copytree(CROPS, os.path.join(DIST, "crops"), dirs_exist_ok=True)
for f in root_html:
    name = os.path.basename(f)
    dst = os.path.join(DIST, name)
    if os.path.exists(dst):
        shutil.copy2(f, dst)
print("  同步完成")
print("DONE")
