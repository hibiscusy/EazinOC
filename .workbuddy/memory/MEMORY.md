# 项目记忆 · 蒲熠星 OC 宇宙人物时间线页面

## 项目概况
- 主文件（索引/角色卡页）：`OC宇宙-人物时间线-蒲熠星.html`。
- **本地预览正确方式（重要）**：必须用「以 `dist/` 为根的本地 HTTP 服务」看图。`python -m http.server 8090 --directory dist` 启动，访问 `http://127.0.0.1:8090/index.html`（8090 当前在跑）。**坑**：用 `present_files` 传本地 html 文件路径会走 WorkBuddy 静态预览面板（`127.0.0.1:53081/static-html/...`），该面板**不加载 `crops/` 等相对子目录资源 → 图片全部不显示**。所以带图片的页面一律用 HTTP 服务 URL 预览，不要传文件路径。中文文件名 URL 在 http.server 下会 404，统一用英文入口 `index.html`。
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
