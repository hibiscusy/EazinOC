import re, os

PAGES = [
    'story-jx.html', 'story-cb.html', 'story-dy.html', 'story-chen.html',
    'story-ll.html', 'story-swd.html', 'story-tl.html',
]

def new_hero(emoji, cn, en, img, intro, desc):
    return (
        '  <div class="story-hero">\n'
        '    <div class="st-row1">\n'
        f'      <span class="st-emoji">{emoji}</span>\n'
        '      <div class="st-name-wrap">\n'
        f'        <h1>{cn}</h1>\n'
        f'        <span class="en">{en}</span>\n'
        '      </div>\n'
        '    </div>\n'
        f'    <p class="st-intro">{intro}</p>\n'
        f'    <p class="st-desc">{desc}</p>\n'
        f'    <img class="st-img" src="{img}" alt="{cn}">\n'
        '  </div>\n'
    )

for fn in PAGES:
    t = open(fn, encoding='utf-8').read()
    # --- 从旧 hero 提取 emoji / 中文名 / 英文名 / 图片 ---
    m = re.search(r'  <div class="story-hero">\n(.*?)\n  </div>\n', t, re.S)
    if not m:
        print('!! 未找到 hero:', fn); continue
    inner = m.group(1)
    emoji = re.search(r'class="em">(.*?)</div>', inner).group(1)
    cn    = re.search(r'<h1>(.*?)</h1>', inner).group(1)
    en    = re.search(r'class="en">(.*?)</div>', inner).group(1)
    img   = re.search(r'<img src="(.*?)"', inner).group(1)
    # --- 从 line-head/sub2 取简介，从 line-desc 取说明 ---
    sub2 = re.search(r'<div class="sub2">(.*?)</div>', t, re.S)
    intro = re.sub(r'\s*<br>\s*', '·', sub2.group(1)) if sub2 else ''
    intro = intro.replace('×·', '× ')  # 兄弟线 sub2 含 " ×<br>"，避免丑陋的 "×·"
    dm = re.search(r'<p class="line-desc">(.*?)</p>', t, re.S)
    desc = dm.group(1) if dm else ''
    nh = new_hero(emoji, cn, en, img, intro, desc)
    # --- 替换 hero 块 ---
    t2 = t[:m.start()] + nh + t[m.end():]
    # --- 删除原 line-head + line-desc（内容已搬入卡片）---
    t2 = re.sub(r'    <div class="line-head">[^\n]*</div>\n    <p class="line-desc">[^\n]*</p>\n+', '', t2)
    open(fn, 'w', encoding='utf-8').write(t2)
    ok = t2.count('<div') == t2.count('</div>')
    print(f'{fn}: div {t2.count("<div")}/{t2.count("</div>")} {"OK" if ok else "BAD"} | '
          f'st-intro={"Y" if "st-intro" in t2 else "N"} | line-head-removed={"Y" if "line-head" not in t2 else "N"} | '
          f'img={img}')
