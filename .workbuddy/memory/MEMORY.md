# 项目记忆 · 蒲熠星 OC 宇宙人物时间线页面

## 项目概况
- 主文件（索引/角色卡页）：`OC宇宙-人物时间线-蒲熠星.html`。
- **本地预览正确方式（重要）**：必须用「以 `dist/` 为根的本地 HTTP 服务」看图。用项目根 `serve.py` 启动线程池服务（`python serve.py`，端口 8090，ThreadingHTTPServer 多线程），访问 `http://127.0.0.1:8090/index.html`。**坑**：用 `present_files` 传本地 html 文件路径会走 WorkBuddy 静态预览面板（`127.0.0.1:53081/static-html/...`），该面板**不加载 `crops/` 等相对子目录资源 → 图片全部不显示**。所以带图片的页面一律用 HTTP 服务 URL 预览，不要传文件路径。中文文件名 URL 在 http.server 下会 404，统一用英文入口 `index.html`。⚠️ **不要用 `python -m http.server`**（单线程会间歇性假死导致裂图）；重启前先 `netstat -ano | grep :8090` 查旧进程并 `taskkill` 掉，再 `python serve.py`。
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
- ⚠️ **本环境 git fetch/pull 被 sandbox 静默 kill**：`git ls-remote` 能成功（仅取 ref，数据小），但 `git fetch`/`git pull` 传输 pack 数据时整个进程被 killed（连后续 `echo` 都不执行、无报错）。修复：对含网络传输的 git 命令加 `dangerouslyDisableSandbox: true`（工具会请求授权）。纯本地 git 操作（`reset`/`commit`/`add`）不受影响，无需关 sandbox。
- **`.git` 丢失恢复法**：若 `.git` 意外消失但工作树文件完整（且远端有完整历史），执行 `git init -b main` → `git remote add origin git@github.com:hibiscusy/EazinOC.git` → `git fetch --depth 1 origin main`（需关 sandbox）→ `git reset --hard origin/main` 即可恢复，工作树=fetch 到的远端最新提交。恢复前可 `cp -r` 整目录到同级 `.SAFEBACKUP` 作保险。

## 内容排序约定
- **时间倒序（用户明确要求，2026-08-04）**：所有故事页内的内容卡片（日常 tab、日记 tab，以及未来新增的同类内容块）一律按「发布时间」**倒序**排列——**最新的在最前面，最旧的在最后**。新增内容时直接插到对应 tab 顶部；同日内容按逻辑先后，新发布的在上。塔拉撒里昂日记tab已据此把（二）08.04 置于（一）08.01 之前。
