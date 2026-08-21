import os
# -*- coding: utf-8 -*-
import re, os

ROOT = r"os.path.dirname(os.path.abspath(__file__))"
INDEX = "OC宇宙-人物时间线-蒲熠星.html"
idx_path = os.path.join(ROOT, INDEX)

with open(idx_path, encoding="utf-8") as f:
    html = f.read()

# ---------- 1) 提取 <style> 内容 -> theme.css ----------
m = re.search(r"<style>(.*?)</style>", html, re.S)
css = m.group(1)
theme_path = os.path.join(ROOT, "theme.css")
with open(theme_path, "w", encoding="utf-8") as f:
    f.write(css)
    f.write("\n\n/* ===== 角色卡可点击 + 故事页样式（追加） ===== */\n")
    f.write("""  .role-link{text-decoration:none;color:inherit;display:block;cursor:pointer}
  .role-link:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:0 10px 28px rgba(94,163,255,.18)}
  .role-link .top{transition:.2s}
  .role-link:hover .top{color:#fff}

  /* 故事页 */
  .story-page{padding-bottom:40px}
  .back{display:inline-flex;align-items:center;gap:6px;margin:18px 0 8px;color:var(--accent);text-decoration:none;font-size:14px;letter-spacing:.05em}
  .back:hover{text-decoration:underline}
  .story-hero{display:flex;align-items:center;gap:18px;margin:6px 0 24px;padding:14px 18px;background:var(--panel);border:1px solid var(--line);border-radius:16px;backdrop-filter:blur(8px)}
  .story-hero img{width:auto;height:auto;max-height:130px;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,.3)}
  .story-hero .em{font-size:32px;line-height:1}
  .story-hero h1{font-size:23px;color:#fff;margin:2px 0 0}
  .story-hero .en{font-size:12.5px;color:var(--muted);letter-spacing:.06em;margin-top:3px}
  .story-hero .st-emoji{display:flex;flex-direction:column;gap:4px}
""")
# 索引页用 link 替换 style
html = html.replace("<style>" + css + "</style>",
                    '<link rel="stylesheet" href="theme.css">', 1)

# ---------- 2) 提取各条故事线 section ----------
def extract_section(s, sec_id):
    start_marker = f'<section class="line" id="{sec_id}">'
    si = s.index(start_marker)
    depth = 0
    i = si
    # 找到匹配 </section>
    while i < len(s):
        o = s.find("<section", i)
        c = s.find("</section>", i)
        if c == -1:
            break
        if o != -1 and o < c:
            depth += 1
            i = o + len("<section")
        else:
            depth -= 1
            if depth == 0:
                return s[si:c + len("</section>")]
            i = c + len("</section>")
    raise SystemExit(f"未找到 {sec_id} 的结束标签")

line_jx   = extract_section(html, "line-jx")
line_dy   = extract_section(html, "line-dy")
line_chen = extract_section(html, "line-chen")
line_ll   = extract_section(html, "line-ll")
line_swd  = extract_section(html, "line-swd")
line_tl   = extract_section(html, "line-tl")

# ---------- 3) 角色卡 -> 故事页映射 ----------
# card_id -> (story_file, emoji, name, en, img)
cards = {
    "r-jx":   ("story-jx.html",   "🏹", "烬行",       "JINXING",      "crops/anime_1.png"),
    "r-dy":   ("story-dy.html",   "🎤", "度漪",       "DU YI",        "crops/anime_5.png"),
    "r-cb":   ("story-cb.html",   "⚙️", "赛博恩",     "CYBORN",       "crops/anime_7.png"),
    "r-ch":   ("story-chen.html", "🗡️", "谶",         "CHAIN",        "crops/anime_3.png"),
    "r-ll":   ("story-ll.html",   "💚", "铃兰",       "LYNPHREDIL",   "crops/anime_2.png"),
    "r-swd":  ("story-swd.html",  "🐱", "斯沃德·麦伦","SWORD MELON",  "crops/anime_4.png"),
    "r-tl":   ("story-tl.html",   "🧜", "塔拉撒里昂", "THALASSARION", "crops/anime_6.png"),
}

# line section 归属
line_for = {
    "story-jx.html":   line_jx,
    "story-cb.html":   line_jx,   # 兄弟线共享
    "story-dy.html":   line_dy,
    "story-chen.html": line_chen,
    "story-ll.html":   line_ll,
    "story-swd.html":  line_swd,
    "story-tl.html":   line_tl,
}

def build_story_page(story_file, emoji, name, en, img, section_html):
    # 修复跨页锚点
    section_html = section_html.replace('href="#line-chen"', 'href="story-chen.html#line-chen"')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} 的故事 · 蒲熠星 OC 宇宙</title>
<link rel="stylesheet" href="theme.css">
</head>
<body>
<div class="stars"></div>
<div class="stars2"></div>
<div class="wrap story-page">
  <a class="back" href="{INDEX}">&larr; 返回星际宇宙</a>
  <div class="story-hero">
    <img src="{img}" alt="{name}" fetchpriority="high" decoding="async">
    <div class="st-emoji">
      <div class="em">{emoji}</div>
      <h1>{name}</h1>
      <div class="en">{en}</div>
    </div>
  </div>
{section_html}
  <footer>
    <div class="tip">✦ 故事仍在连载 ✦</div>
    <p>以上为蒲熠星本人微博（@蒲熠星 UID 2882733894）发布的 OC 文章整理。<br>标注「粉丝整理 / 转发整理」的为同人向高质量补写或转载，非本人原博，仅供阅读参考。</p>
    <p style="margin-top:10px;color:var(--muted);font-size:11.5px">返回：<a href="{INDEX}">角色宇宙主页</a></p>
  </footer>
</div>
</body>
</html>
"""

for card_id, (story_file, emoji, name, en, img) in cards.items():
    page = build_story_page(story_file, emoji, name, en, img, line_for[story_file])
    with open(os.path.join(ROOT, story_file), "w", encoding="utf-8") as f:
        f.write(page)
    print("生成故事页:", story_file, "->", name)

# ---------- 4) 索引页：角色卡改可点击 ----------
def make_clickable(s, card_id, href):
    open_tag = f'<div class="rc" id="{card_id}">'
    oi = s.index(open_tag)
    open_len = len(open_tag)
    # 深度计数找匹配 </div>
    depth = 1
    i = oi + open_len
    close_pos = None
    while i < len(s):
        o = s.find("<div", i)
        c = s.find("</div>", i)
        if c == -1:
            break
        if o != -1 and o < c:
            depth += 1
            i = o + 4
        else:
            depth -= 1
            if depth == 0:
                close_pos = c
                break
            i = c + 6
    if close_pos is None:
        raise SystemExit(f"找不到 {card_id} 的闭合 div")
    s = s[:oi] + f'<a class="rc role-link" id="{card_id}" href="{href}">' + s[oi+open_len:close_pos] + "</a>" + s[close_pos+6:]
    return s

for card_id, (href, *_rest) in cards.items():
    ot = f'<div class="rc" id="{card_id}">'
    if ot not in html:
        raise SystemExit(f"[{card_id}] 未找到角色卡: {ot!r}；当前 html 长度 {len(html)}")
    html = make_clickable(html, card_id, href)
print("角色卡已改为可点击链接")

# ---------- 5) 索引页：移除 6 条故事线 section ----------
start_marker = "<!-- ============ 线一：烬行 & 赛博恩 ============ -->"
si = html.index(start_marker)
fi = html.index("<footer>")
# 截断到 footer 之前
before = html[:si].rstrip("\n")
html = before + "\n\n" + html[fi:]
print("已移除原故事线 section")

# ---------- 6) 索引页：更新顶部导航 ----------
old_nav = """    <a href="#line-jx">烬行·赛博恩</a>
    <a href="#line-dy">度漪</a>
    <a href="#line-chen">谶</a>
    <a href="#line-ll">铃兰</a>
    <a href="#line-swd">斯沃德</a>
    <a href="#line-tl">塔拉撒里昂</a>"""
new_nav = """    <a href="story-jx.html">烬行</a>
    <a href="story-dy.html">度漪</a>
    <a href="story-cb.html">赛博恩</a>
    <a href="story-chen.html">谶</a>
    <a href="story-ll.html">铃兰</a>
    <a href="story-swd.html">斯沃德</a>
    <a href="story-tl.html">塔拉撒里昂</a>"""
html = html.replace(old_nav, new_nav, 1)
print("已更新顶部导航")

# ---------- 7) 写回索引页 ----------
with open(idx_path, "w", encoding="utf-8") as f:
    f.write(html)
print("索引页已写回")
