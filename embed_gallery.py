"""在所有story-*.html的角色模块(.story-hero)下方插入.photo-gallery相册展示区"""
import os, re

BASE = 'D:/WorkBuddy/1/2026-07-30-11-42-14'

# 角色相册配置：key=story文件前缀, value=(gallery页面名, 图片目录, 显示数量)
GALLERIES = {
    'dy': ('gallery-dy.html', 'dy-gallery', 7),   # 度漪有7张
    # 其他角色暂无图片，保留空结构
    'jx': (None, None, 0),
    'cb': (None, None, 0),
    'chen': (None, None, 0),
    'll': (None, None, 0),
    'swd': (None, None, 0),
    'tl': (None, None, 0),
}

def make_gallery_html(prefix, gallery_page, img_dir, count):
    """生成相册HTML片段"""
    if count == 0 or not gallery_page:
        # 无图片时：空容器（隐藏），后续加图时直接填入
        return '<div class="photo-gallery" style="display:none"></div>\n'
    
    thumbs = min(count, 5)  # 默认展示5张
    extra = count - thumbs
    
    lines = [f'<div class="photo-gallery">']
    for i in range(1, thumbs + 1):
        img_path = f'crops/{img_dir}/{prefix}_{i:02d}.webp'
        lines.append(
            f'  <a href="{gallery_page}" class="photo-thumb">'
            f'<img src="{img_path}" alt="{prefix} {i}" loading="lazy" decoding="async"/></a>'
        )
    if extra > 0 or count > 0:
        # “查看全部”入口（始终展示，点击进入相册内页）
        lines.append(
            f'  <a href="{gallery_page}" class="photo-more">查看全部 →</a>'
        )
    lines.append('</div>')
    return '\n'.join(lines) + '\n'

# 插入标记：在 </div>（story-hero结束）和 <section class="line"> 之间
INSERT_AFTER = re.compile(r'(</div>\s*)(<section class="line"[^>]*>)', re.DOTALL)

for prefix, (gpage, gdir, cnt) in GALLERIES.items():
    fname = f'story-{prefix}.html'
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        print(f'SKIP {fname} (not found)')
        continue
    
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    
    # 避免重复插入
    if 'photo-gallery' in html:
        print(f'SKIP {fname} (already has gallery)')
        continue
    
    gal_html = make_gallery_html(prefix, gpage, gdir, cnt)
    new_html = INSERT_AFTER.sub(r'\1' + gal_html + r'\2', html, count=1)
    
    if new_html == html:
        print(f'WARN {fname}: insertion point not found')
        continue
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    # 同步到dist
    dist_path = os.path.join(BASE, 'dist', 'index.html' if prefix == 'dy' else f'story-{prefix}.html')
    # dist里的文件名：索引页是index.html，其他是story-*.html
    if prefix == 'dy':
        dist_path = os.path.join(BASE, 'dist', 'story-dy.html')
    else:
        dist_path = os.path.join(BASE, 'dist', f'story-{prefix}.html')
    
    # 对于dist，也做同样插入（dist是副本）
    if os.path.exists(dist_path):
        with open(dist_path, encoding='utf-8') as f:
            dhtml = f.read()
        if 'photo-gallery' not in dhtml:
            dnew = INSERT_AFTER.sub(r'\1' + gal_html + r'\2', dhtml, count=1)
            with open(dist_path, 'w', encoding='utf-8') as f:
                f.write(dnew)
            print(f'  + {fname} (root+dist) [{cnt} photos]')
        else:
            print(f'  + {fname} (root only, dist already had)')
    else:
        print(f'  + {fname} (root only, dist missing)')

# 也把gallery-dy.html同步到dist
import shutil
gsrc = os.path.join(BASE, 'gallery-dy.html')
gdst = os.path.join(BASE, 'dist', 'gallery-dy.html')
if os.path.exists(gsrc):
    shutil.copy2(gsrc, gdst)
    print(f'  + gallery-dy.html -> dist/')

print('Done.')
