# 项目记忆 · 蒲熠星 OC 宇宙人物时间线页面

## 项目概况
- 主文件（索引/角色卡页）：`OC宇宙-人物时间线-蒲熠星.html`。
- **本地预览正确方式（重要，2026-08-17 修正）**：站点直接以**项目根目录**发布（`story-*.html` + `theme.css` + `crops/` 都在根目录，没有 `dist/`）。⚠️ 项目根 `serve.py` 内部把根写死成 `dist/`，而 `dist/` 并不存在 → `python serve.py` 会直接崩溃（FileNotFoundError）。**正确起法**：在根目录起一个 ThreadingHTTPServer（用 `SimpleHTTPRequestHandler` 并设 `h.directory='E:/Eazin/EazinOC'`），端口 8090。访问 `http://127.0.0.1:8090/story-chen.html` 等英文入口。**坑**：用 `present_files` 传本地 html 文件路径会走 WorkBuddy 静态预览面板（`127.0.0.1:53081/static-html/...`），该面板**不加载 `crops/` 等相对子目录资源 → 图片全部不显示**，务必用 HTTP 服务 URL 预览。⚠️ **不要用 `python -m http.server`**（单线程会间歇性假死导致裂图）；重启前先 `netstat -ano | grep :8090` 查旧进程并 `taskkill /PID <pid> /F` 掉，再起新服务。若预览看到旧内容，多半是旧进程在 serve 旧快照（8090 上的老进程可能来自别的目录），关掉重启即可。
- **多页结构（2026-07-31 重构）**：每个 OC 角色拥有独立故事页，索引页角色卡点击进入。
  - 故事页：`story-jx.html`(烬行) `story-dy.html`(度漪) `story-cb.html`(赛博恩) `story-chen.html`(谶) `story-ll.html`(铃兰) `story-swd.html`(斯沃德·麦伦) `story-tl.html`(塔拉撒里昂)
  - 兄弟线（烬行&赛博恩）内容同时存在于 `story-jx.html` 与 `story-cb.html`
  - 故事页含：返回链接 + 角色头图(hero) + 该角色 `<section class="line">` 时间线 + footer
  - 塔拉撒里昂页中"见谶线"链接已改为 `story-chen.html#line-chen` 跨页锚点
- 共享样式：`theme.css`（从原 `<style>` 抽出，索引页与所有故事页均 `<link>` 引用；含 `.role-link`/`.story-hero`/`.back` 等追加样式）
- 角色图：`crops/anime_1~7.webp`（页面实际引用，png 为源图）；本人照 `crops/pyx-photo.jpg`。
- 云端分享：CloudStudio 沙箱（旧版），需重新部署（把整个工作区含 theme.css/story-*.html/crops 一起打包到 deploy/oc-share）才同步最新。
- 生成脚本：`build_stories.py`（可重跑重建故事页；注意角色卡 id 是 `r-ch` 不是 `r-chen`）

## 默认样式约定
- **小标题默认样式 = `.sec-title`**：14px、字距 .2em、`var(--accent)` 蓝字、左侧 5×18px 渐变色条（`::before`）。所有分区小标题统一用它（如"故事总时间线 · 概览""宇宙 · 角色"）。
- 大标题（角色线）用 `.line-head`（emoji + h2 + 右侧 sub2）。
- 页面深色星空主题，配色变量 `--accent`(蓝) `--accent2`(粉) `--bg` `--panel` `--line` `--muted` `--soft` `--glow`。
- 全局非斜体：`em,i,q,blockquote,cite,.poem{font-style:normal}`。

## 角色英文名（用户指定）
烬行=JINXING · 铃兰=LYNPHREDIL · 谶=CHAIN · 度漪=DU YI · 赛博恩=CYBORN · 斯沃德麦伦=SWORD MELON · 塔拉撒里昂=THALASSARION

## Git 协作约定
- 远程 `origin` = `git@github.com:hibiscusy/EazinOC.git`（SSH 免密，本机 `~/.ssh/id_ed25519`）。
- **推送节奏**：用户要求「改完前不推送，累积本地 commit，等用户说『改完了/推送』再一次性 `git push`」。即平时只 `git commit`，不要自动 push；记忆/笔记改动也一并本地提交、暂存不推。
- 旧部署(CloudStudio 沙箱)为旧版，定稿后需重新 deploy 才同步。
- **⚠️ 永久站点 `hibiscusy.github.io/EazinOC/` 由 GitHub Pages 构建，源 = `gh-pages` 分支（不是 `main`）**。所以「推 main」不会自动更新永久站点——这就是 2026-08-13 用户发现永久站点没更新的根因。要上线永久站点，必须把站点文件同步到 `gh-pages` 分支（工作流见下）。**推荐一步到位**：在仓库 Settings→Pages 把 Source 改成 `main` 分支 / root，之后每次 `git push` 自动上线永久站点（改源后给 main 加 `.nojekyll` 以禁用 Jekyll 处理中文文件名/下划线文件）。
- **同步 gh-pages 的安全工作流（不动主工作树）**：`git worktree add -b gh-pages-build <临时目录> main` → 临时目录内 `git rm -rf .` → `git checkout main -- <站点文件：index.html / OC宇宙-人物时间线-蒲熠星.html / author-pyx.html / theme.css / tabs.js / story-*.html / gallery-*.html / crops>` → 建 `.nojekyll` → `git commit` → `git push origin gh-pages-build:refs/heads/gh-pages --force` → 回主目录 `git worktree remove <临时目录> --force` + `git branch -D gh-pages-build`。已验证：`8bc3c69` 上线成功（2026-08-13）。
- **本地 `origin/main` 跟踪引用会过期**（fetch 被 sandbox kill 无法刷新），表现为 `git status` 误报「ahead 1」。修正：`git update-ref refs/remotes/origin/main <真实SHA>`（用 `git ls-remote origin` 取真实 SHA；实测 origin/main 已=本地 HEAD，push 并未丢失）。
- ⚠️ **本环境 git fetch/pull 被 sandbox 静默 kill**：`git ls-remote` 能成功（仅取 ref，数据小），但 `git fetch`/`git pull` 传输 pack 数据时整个进程被 killed（连后续 `echo` 都不执行、无报错）。修复：对含网络传输的 git 命令加 `dangerouslyDisableSandbox: true`（工具会请求授权）。纯本地 git 操作（`reset`/`commit`/`add`）不受影响，无需关 sandbox。
- **`.git` 丢失恢复法**：若 `.git` 意外消失但工作树文件完整（且远端有完整历史），执行 `git init -b main` → `git remote add origin git@github.com:hibiscusy/EazinOC.git` → `git fetch --depth 1 origin main`（需关 sandbox）→ `git reset --hard origin/main` 即可恢复，工作树=fetch 到的远端最新提交。恢复前可 `cp -r` 整目录到同级 `.SAFEBACKUP` 作保险。

## 内容排序约定
- **时间倒序（用户明确要求，2026-08-04）**：所有故事页内的内容卡片（日常 tab、日记 tab，以及未来新增的同类内容块）一律按「发布时间」**倒序**排列——**最新的在最前面，最旧的在最后**。新增内容时直接插到对应 tab 顶部；同日内容按逻辑先后，新发布的在上。塔拉撒里昂日记tab已据此把（二）08.04 置于（一）08.01 之前。
