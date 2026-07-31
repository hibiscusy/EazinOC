import zipfile, os

base = r"D:\WorkBuddy\1\2026-07-30-11-42-14"
out = os.path.join(base, "oc-universe-2026-07-31.zip")
top = "oc-universe"  # 解压后的顶层文件夹名

files = [
    "OC宇宙-人物时间线-蒲熠星.html",
    "theme.css",
    "build_stories.py",
    "story-jx.html", "story-dy.html", "story-cb.html", "story-chen.html",
    "story-ll.html", "story-swd.html", "story-tl.html",
    "crops/anime_1.png", "crops/anime_2.png", "crops/anime_3.png",
    "crops/anime_4.png", "crops/anime_5.png", "crops/anime_6.png",
    "crops/anime_7.png", "crops/pyx-photo.jpg",
    ".workbuddy/memory/MEMORY.md",
    ".workbuddy/memory/2026-07-30.md",
    ".workbuddy/memory/2026-07-31.md",
]

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    added, missing = 0, 0
    for f in files:
        src = os.path.join(base, f)
        if not os.path.exists(src):
            print("MISSING:", f)
            missing += 1
            continue
        z.write(src, os.path.join(top, f))
        added += 1
        print("added:", os.path.join(top, f))

print(f"\nDONE -> {out}\nadded={added} missing={missing}")
