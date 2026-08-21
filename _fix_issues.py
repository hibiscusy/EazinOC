# -*- coding: utf-8 -*-
import os, re

ROOT = r'os.path.dirname(os.path.abspath(__file__))'

# ---------- 1) Issue 1: fix cb/jx root source ----------
# cb: fix stale CSS version + wrong section id (line-jx -> line-cb)
p = os.path.join(ROOT, 'story-cb.html')
s = open(p, encoding='utf-8').read()
assert 'theme.css?v=20260804a' in s, 'cb css version not found'
s = s.replace('theme.css?v=20260804a', 'theme.css?v=20260805c')
assert '<section class="line" id="line-jx">' in s, 'cb line-jx not found'
s = s.replace('<section class="line" id="line-jx">', '<section class="line" id="line-cb">')
open(p, 'w', encoding='utf-8').write(s)
print('[1] story-cb.html: css->20260805c, id line-jx->line-cb')

# jx: fix stale CSS version
p = os.path.join(ROOT, 'story-jx.html')
s = open(p, encoding='utf-8').read()
assert 'theme.css?v=20260804a' in s, 'jx css version not found'
s = s.replace('theme.css?v=20260804a', 'theme.css?v=20260805c')
open(p, 'w', encoding='utf-8').write(s)
print('[1] story-jx.html: css->20260805c')

# ---------- 2) Issue 2: diary grid 5-col + lightbox ----------
# theme.css: replace diary-img-grid rules
p = os.path.join(ROOT, 'theme.css')
s = open(p, encoding='utf-8').read()
old = (
    '  .diary-img-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}\n'
    '  .diary-img-grid img{width:100%;border-radius:10px;object-fit:cover;aspect-ratio:3/4}'
)
new = (
    '  .diary-img-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:16px}\n'
    '  .diary-img-grid img{width:100%;height:auto;display:block;border-radius:10px;cursor:zoom-in;transition:filter .2s,transform .2s}\n'
    '  .diary-img-grid img:hover{filter:brightness(1.1)}\n'
    '  .img-lightbox{position:fixed;inset:0;background:rgba(4,5,18,.93);display:none;align-items:center;justify-content:center;z-index:9999;padding:4vw;cursor:zoom-out}\n'
    '  .img-lightbox.open{display:flex}\n'
    '  .img-lightbox img{max-width:92vw;max-height:90vh;width:auto;height:auto;border-radius:12px;box-shadow:0 12px 60px rgba(0,0,0,.6)}\n'
    '  @media(max-width:900px){.diary-img-grid{grid-template-columns:repeat(3,1fr)}}\n'
    '  @media(max-width:560px){.diary-img-grid{grid-template-columns:repeat(2,1fr)}}'
)
assert old in s, 'diary-img-grid old rule not found in theme.css'
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('[2] theme.css: diary-img-grid -> 5col responsive + lightbox css')

# story-tl.html: bump css version + inject lightbox script before </body>
p = os.path.join(ROOT, 'story-tl.html')
s = open(p, encoding='utf-8').read()
assert 'theme.css?v=20260805b' in s, 'tl css version not found'
s = s.replace('theme.css?v=20260805b', 'theme.css?v=20260805c')
marker = '  <script src="tabs.js"></script>\n</body>'
inject = (
    '  <script src="tabs.js"></script>\n'
    '  <script>\n'
    '  (function(){\n'
    '    var grid=document.querySelector(\'.diary-img-grid\');\n'
    '    if(!grid) return;\n'
    '    var lb=document.createElement(\'div\'); lb.className=\'img-lightbox\';\n'
    '    var im=document.createElement(\'img\'); lb.appendChild(im);\n'
    '    document.body.appendChild(lb);\n'
    '    grid.addEventListener(\'click\',function(e){\n'
    '      var t=e.target;\n'
    '      if(t&&t.tagName===\'IMG\'){ im.src=t.currentSrc||t.src; im.alt=t.alt; lb.classList.add(\'open\'); }\n'
    '    });\n'
    '    lb.addEventListener(\'click\',function(){ lb.classList.remove(\'open\'); });\n'
    '  })();\n'
    '  </script>\n'
    '</body>'
)
assert marker in s, 'tl tabs.js marker not found'
s = s.replace(marker, inject)
open(p, 'w', encoding='utf-8').write(s)
print('[2] story-tl.html: css->20260805c + lightbox script injected')

# ---------- 3) Issue 3: remove annotation sentence from all web pages ----------
anno_re = re.compile(r'(<br>\s*)?标注「粉丝整理 / 转发整理」的为同人向高质量补写或转载，非本人原博，仅供阅读参考。(\s*整理时间 2026\.07\.30。)?')
pages = [
    'OC宇宙-人物时间线-蒲熠星.html',
    'story-cb.html', 'story-jx.html', 'story-dy.html', 'story-ll.html',
    'story-swd.html', 'story-chen.html', 'story-tl.html',
]
for fn in pages:
    p = os.path.join(ROOT, fn)
    s = open(p, encoding='utf-8').read()
    n = len(anno_re.findall(s))
    s2 = anno_re.sub('', s)
    if n:
        open(p, 'w', encoding='utf-8').write(s2)
        print(f'[3] {fn}: removed {n} annotation block(s)')
    else:
        print(f'[3] {fn}: no annotation found (skip)')

print('\nALL ROOT FIXES DONE')
