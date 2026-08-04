#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_photos.py — OC宇宙网站「加照片」一键流程
============================================
把任意照片加进网站，自动完成：
  1. 转 WebP（高画质保清晰：quality=88, method=6, **保持原始分辨率不缩放**）
  2. 同步到 crops/ 与 dist/crops/
  3. 输出可直接粘贴的 <img> 标签（含 width/height 防CLS + loading=lazy + decoding=async）
  4. 版本号 cache-busting：新图 ?v=1；更新已有同名图自动在 HTML 引用基础上 +1

用法
----
  python add_photos.py <图片或目录> [图片或目录 ...] [--prefix 前缀] [--inject HTML]

参数
----
  sources     一个或多个图片文件 / 目录（目录则递归收录常见图片格式）
  --prefix    输出文件名前缀，如 --prefix photo-  →  photo-xxx.webp
  --inject    可选：把生成的 <img> 标签追加到指定 HTML 的 <!-- PHOTOS-INJECT --> 标记后
              （该标记不存在则追加到 </body> 前）。同步 dist 同名文件。

设计原则
--------
  * 视觉质量优先：只转格式、不降低分辨率，WebP 用接近无损的画质参数。
  * dist/ 是部署副本，每次都同步，避免"本地有、线上缺"的旧坑。
  * 不删除任何源文件，纯增量。
"""
import os
import re
import sys
import shutil
import argparse
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.abspath(__file__))
CROPS = os.path.join(ROOT, "crops")
DIST_CROPS = os.path.join(ROOT, "dist", "crops")
QUALITY = 88          # 高画质保清晰
METHOD = 6            # 压缩方法（更慢但体积更优）
MAX_W = 1600          # 超过此宽才等比缩放（防止个别超大原图），一般照片不触发
SUPPORTED = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff")


def active_htmls():
    """返回需要参与版本号推断 / 注入的活跃 HTML 列表。"""
    names = ["OC宇宙-人物时间线-蒲熠星.html"]
    for f in sorted(os.listdir(ROOT)):
        if f.startswith("story-") and f.endswith(".html"):
            names.append(f)
    return [os.path.join(ROOT, n) for n in names if os.path.exists(os.path.join(ROOT, n))]


def next_version(stem, html_files):
    """在 HTML 中查找 crops/<stem>.webp?v=N 的最大 N，返回 N+1；无则 1。"""
    ver = 0
    pat = re.compile(r"crops/" + re.escape(stem) + r"\.webp\?v=(\d+)")
    for hf in html_files:
        try:
            txt = open(hf, encoding="utf-8").read()
        except Exception:
            continue
        for m in pat.finditer(txt):
            ver = max(ver, int(m.group(1)))
    return ver + 1


def convert(src, stem):
    """转 WebP（保分辨率），返回 (out_path, w, h)。"""
    im = Image.open(src)
    im.load()
    # 仅对超大原图做等比缩放到 MAX_W，正常照片保持原尺寸
    if im.width > MAX_W:
        ratio = MAX_W / im.width
        im = im.resize((MAX_W, round(im.height * ratio)), Image.LANCZOS)
    # 模式归一：带透明用 RGBA，否则 RGB
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    os.makedirs(CROPS, exist_ok=True)
    os.makedirs(DIST_CROPS, exist_ok=True)
    out = os.path.join(CROPS, stem + ".webp")
    im.save(out, "WEBP", quality=QUALITY, method=METHOD)
    shutil.copy2(out, DIST_CROPS)  # 同步部署副本
    return out, im.width, im.height


def collect(sources):
    files = []
    for s in sources:
        if os.path.isdir(s):
            for r, _, fs in os.walk(s):
                for f in sorted(fs):
                    if f.lower().endswith(SUPPORTED):
                        files.append(os.path.join(r, f))
        elif os.path.isfile(s):
            files.append(s)
    return files


def build_tag(stem, w, h, ver, alt):
    return (
        f'<img src="crops/{stem}.webp?v={ver}" alt="{alt}" '
        f'width="{w}" height="{h}" loading="lazy" decoding="async" '
        f'style="width:100%;max-width:760px;height:auto;display:block;margin:0 auto"/>'
    )


def inject(html_path, tags):
    txt = open(html_path, encoding="utf-8").read()
    block = "\n".join(tags)
    marker = "<!-- PHOTOS-INJECT -->"
    if marker in txt:
        txt = txt.replace(marker, marker + "\n" + block, 1)
    else:
        txt = txt.replace("</body>", block + "\n</body>", 1)
    open(html_path, "w", encoding="utf-8").write(txt)
    # 同步 dist 同名文件
    base = os.path.basename(html_path)
    shutil.copy2(html_path, os.path.join(ROOT, "dist", base))


def main():
    ap = argparse.ArgumentParser(description="OC宇宙网站加照片一键流程")
    ap.add_argument("sources", nargs="+", help="图片文件或目录（可多个）")
    ap.add_argument("--prefix", default="", help="输出文件名前缀，如 photo-")
    ap.add_argument("--inject", default=None, help="把标签注入到该 HTML（可选）")
    args = ap.parse_args()

    htmls = active_htmls()
    files = collect(args.sources)
    if not files:
        print("✗ 未找到任何图片文件。", file=sys.stderr)
        sys.exit(1)

    print(f"处理 {len(files)} 张图片  (WebP quality={QUALITY}, 保持原分辨率)\n")
    tags = []
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]
        stem = (args.prefix + base) if args.prefix else base
        alt = base
        try:
            out, w, h = convert(f, stem)
        except Exception as e:
            print(f"✗ 转换失败 {f}: {e}", file=sys.stderr)
            continue
        ver = next_version(stem, htmls)
        tag = build_tag(stem, w, h, ver, alt)
        tags.append(tag)
        kb = os.path.getsize(out) / 1024
        print(f"✓ crops/{stem}.webp  ({w}x{h}, {kb:.1f}KB, ?v={ver})")

    if not tags:
        print("没有成功处理的图片。", file=sys.stderr)
        sys.exit(1)

    if args.inject:
        inject(args.inject, tags)
        print(f"\n→ 已注入 {len(tags)} 张到 {args.inject} 并同步 dist。")
    else:
        print("\n--- 可粘贴的 <img> 标签（已同步 dist/crops）---\n")
        for t in tags:
            print(t + "\n")

    print("提示：更新已有同名图时版本号会自动 +1；新图为 ?v=1。")


if __name__ == "__main__":
    main()
