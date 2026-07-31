# 项目记忆 · 蒲熠星 OC 宇宙人物时间线页面

## 项目概况
- 主文件（索引/角色卡页）：`OC宇宙-人物时间线-蒲熠星.html`（本地预览服务 127.0.0.1:8123）
- **多页结构（2026-07-31 重构）**：每个 OC 角色拥有独立故事页，索引页角色卡点击进入。
  - 故事页：`story-jx.html`(烬行) `story-dy.html`(度漪) `story-cb.html`(赛博恩) `story-chen.html`(谶) `story-ll.html`(铃兰) `story-swd.html`(斯沃德·麦伦) `story-tl.html`(塔拉撒里昂)
  - 兄弟线（烬行&赛博恩）内容同时存在于 `story-jx.html` 与 `story-cb.html`
  - 故事页含：返回链接 + 角色头图(hero) + 该角色 `<section class="line">` 时间线 + footer
  - 塔拉撒里昂页中"见谶线"链接已改为 `story-chen.html#line-chen` 跨页锚点
- 共享样式：`theme.css`（从原 `<style>` 抽出，索引页与所有故事页均 `<link>` 引用；含 `.role-link`/`.story-hero`/`.back` 等追加样式）
- 角色图：`crops/anime_1~7.png`（按文件名对应）；本人照 `crops/pyx-photo.jpg`。
- 云端分享：CloudStudio 沙箱（旧版），需重新部署（把整个工作区含 theme.css/story-*.html/crops 一起打包到 deploy/oc-share）才同步最新。
- 生成脚本：`build_stories.py`（可重跑重建故事页；注意角色卡 id 是 `r-ch` 不是 `r-chen`）

## 默认样式约定
- **小标题默认样式 = `.sec-title`**：14px、字距 .2em、`var(--accent)` 蓝字、左侧 5×18px 渐变色条（`::before`）。所有分区小标题统一用它（如"故事总时间线 · 概览""宇宙 · 角色"）。
- 大标题（角色线）用 `.line-head`（emoji + h2 + 右侧 sub2）。
- 页面深色星空主题，配色变量 `--accent`(蓝) `--accent2`(粉) `--bg` `--panel` `--line` `--muted` `--soft` `--glow`。
- 全局非斜体：`em,i,q,blockquote,cite,.poem{font-style:normal}`。

## 角色英文名（用户指定）
烬行=JINXING · 铃兰=LYNPHREDIL · 谶=CHAIN · 度漪=DU YI · 赛博恩=CYBORN · 斯沃德麦伦=SWORD MELON · 塔拉撒里昂=THALASSARION
