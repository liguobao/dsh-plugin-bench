<div align="center">
  
# AI Animation Skills

**一套用 AI 生成炫酷 HTML 动画的 [Agent Skills](https://support.claude.com/en/articles/12512176-what-are-skills) 集合 · A collection of skills for generating cool HTML animations with AI**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](./LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](#贡献与许可)
[![Skills count](https://img.shields.io/badge/Skills-9-orange?style=flat-square)](#skills-gallery)
[![Spec](https://img.shields.io/badge/Spec-SKILL.md-black?style=flat-square)](https://agentskills.io)

🌐 **English version**: [`README_EN.md`](README_EN.md)

</div>

---

### 项目简介

本仓库是基于 WorkBuddy / Claude Code / Cursor 等 AI Agent 的**动效 Skill 集合**。每个 Skill 是一个自包含文件夹，包含 `SKILL.md`（Agent 执行指令）、`README.md`（人类文档）、`references/`（Prompt 参考）和 `assets/`（模板 HTML）。安装后，AI Agent 会根据你的描述自动激活对应 Skill，生成完整的单文件 HTML 动画。

一句话生成：
- 📊 **PPT 风格演示** — 科普、技术讲解、视频配套演示
- 📈 **流程图 / 原理演示** — 流程图、概念图、对比图、时序图、AI 模型可视化等
- 🌐 **网络协议可视化** — TCP/IP、IPv4、以太帧、路由、DHCP 等
- 🏗️ **动态架构图** — 系统架构、流程图、时序图、数据流图、状态机，带流动动画 + 多格式导出
- 📝 **学霸笔记** — 手写笔记本风格的精美 HTML 学习笔记，两种模板风格
- 🎴 **卡片剧场** — 侧边栏叙事 + 3D 卡片轮播，协议流程 / 产品特性 / 分步讲解的叙事感演示
- 🎬 **视频分镜演示** — 电影级"一个镜头一个 HTML"演示动画：29 种风格轮换、镜头推拉、WebAudio 音效、角色表情吐槽，全屏录屏即成片
- 📱 **手机系统 UI 演示** — 一台"真手机"的电影化编排录屏：锁屏通知、聊天、设置页、App 界面逐镜头呈现，HyperOS 级手感动效 + 3D 姿态手机演员
- 🗂️ **叠放数据卡** — 论点卡从底部依次弹入、旧卡左叠成牌堆：折线描边 / 数字滚动 / 环形仪表按毫秒级时间线级联入场，自动播放对齐口播，录屏即成片

<div align="center">

**👇 点击预览图查看各 Skill 详情**

</div>

<table>
<tr>
<td width="25%" valign="top" align="center">
<a href="#ppt-animation"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/a6576e08-210b-4fda-867c-c0bd1a847d13" /></a>
<br/><a href="#ppt-animation"><strong>ppt-animation</strong></a>
<br/><sub>PPT 演示 / 翻页动画</sub>
</td>
<td width="25%" valign="top" align="center">
<a href="#flowchart"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/90414d79-80a5-47bc-bc5b-ee567160d021" /></a>
<br/><a href="#flowchart"><strong>flowchart</strong></a>
<br/><sub>流程图 / 概念图 / 原理演示</sub>
</td>
<td width="25%" valign="top" align="center">
<a href="#network-protocol-viz"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/39d12d3d-3c15-4e83-b2f4-0186fc9e5e2e" /></a>
<br/><a href="#network-protocol-viz"><strong>network-protocol-viz</strong></a>
<br/><sub>网络协议 / 数据包演示</sub>
</td>
<td width="25%" valign="top" align="center">
<a href="#dynamic-archify"><img width="2537" height="1440" alt="image" src="https://github.com/user-attachments/assets/61e42d50-1dfb-487a-9e5a-29e956a10e7f" /></a>
<br/><a href="#dynamic-archify"><strong>dynamic-archify</strong></a>
<br/><sub>动态架构图 / 流程图 / 时序图</sub>
</td>
</tr>
<tr>
<td colspan="2" width="50%" valign="top" align="center">
<a href="#scholar-notes"><img width="2534" height="1440" alt="image" src="https://github.com/user-attachments/assets/e7bd4d61-37d3-4c5c-b47a-94114f609aa3" /></a>
<br/><a href="#scholar-notes"><strong>scholar-notes</strong></a>
<br/><sub>学霸笔记 / 手写笔记本风格</sub>
</td>
<td colspan="2" valign="top" align="center">
<a href="#card-theater"><img width="2560" height="1440" alt="card-theater" src="https://github.com/user-attachments/assets/51ace25a-fde6-45db-97f5-3c30582fb85f" /></a>
<br/><a href="#card-theater"><strong>card-theater</strong></a>
<br/><sub>卡片剧场 / 3D 卡片轮播</sub>
</td>
</tr>
<tr>
<td colspan="2" valign="top" align="center">
<a href="#phone-ui-demos"><img width="2560" height="1440" alt="phone-ui-demos" src="https://github.com/user-attachments/assets/653d8b46-fc07-43d9-bf36-4899dfc35c7b" /></a>
<br/><a href="#phone-ui-demos"><strong>phone-ui-demos</strong></a>
<br/><sub>手机系统 UI / 编排录屏动画</sub>
</td>
<td colspan="2" valign="top" align="center">
<a href="#video-shot-demos"><img width="2560" height="1440" alt="video-shot-demos" src="https://github.com/user-attachments/assets/ee93829f-91c5-48df-925e-342cd2be4557" /></a>
<br/><a href="#video-shot-demos"><strong>video-shot-demos</strong></a>
<br/><sub>视频分镜演示 / 电影级镜头动画</sub>
</td>
</tr>
<tr>
<td colspan="4" valign="top" align="center">
<a href="#stacked-data-cards"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/ac863d4f-0d48-4c05-a0c2-2e28874a1c62" /></a>
<br/><a href="#stacked-data-cards"><strong>stacked-data-cards</strong></a>
<br/><sub>叠放数据卡 / 时间线论点动画</sub>
</td>
</tr>
</table>

---

### Skills Gallery

<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->

#### `ppt-animation`

<a href="./skills/ppt-animation">
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/221ac125-02f7-4bac-b179-25085034ff67" />
</a>

**分类:** PPT 演示 / 翻页动画
**适用于:** 视频录制、技术科普、教学演示、直播课件——需要"PPT 翻页 + 元素依次缓入"动画效果的场景。

`ppt-animation` 生成 PPT 风格的单文件 HTML 翻页演示。每次翻页后页面内元素依次缓入出现，支持暗色科技风、暖色报纸风、简约白色、赛博朋克红橙、渐变暗色等多套主题。键盘 / 滚轮 / 点击均可翻页，适配全屏播放和录屏。

亮点:
- 16:9 宽高比，适配全屏播放与录屏
- 每次翻页后元素依次缓入出现（细化到每行文字）
- 5 套内置主题：`dark-tech` / `warm-paper` / `clean-white` / `cyber-red` / `gradient-dark`
- 核心概念用图形化元素（图表、流程图、示意图）展示，不依赖外部图片
- 支持以已有模板为基础重构（`以 assets/xxx.html 为模板演示以上内容`）

<table>
<tr>
<td align="center" width="20%"><a href="./skills/ppt-animation/README.md#主题画廊"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/dbc2ddbc-3ec9-4d3e-892c-59e04f629124" /></a><br /><sub><code>dark-tech</code><br />暗色科技风</sub></td>
<td align="center" width="20%"><a href="./skills/ppt-animation/README.md#主题画廊"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/939788e1-3a77-451f-84de-aa10fb2f4c4c" /></a><br /><sub><code>warm-paper</code><br />暖色报纸风</sub></td>
<td align="center" width="20%"><a href="./skills/ppt-animation/README.md#主题画廊"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/30601c48-32c4-42ab-86a3-2699a3e01a58" /></a><br /><sub><code>clean-white</code><br />简约白色</sub></td>
<td align="center" width="20%"><a href="./skills/ppt-animation/README.md#主题画廊"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/8829f50c-2162-4c7b-a8ea-aac458962112" /></a><br /><sub><code>cyber-red</code><br />赛博朋克红橙</sub></td>
<td align="center" width="20%"><a href="./skills/ppt-animation/README.md#主题画廊"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/e5cdadf4-b0fd-41d2-90d8-3f12e63e2ec8" /></a><br /><sub><code>gradient-dark</code><br />渐变暗色</sub></td>
</tr>
</table>

<sub>↑ 5 套主题一览 — <a href="./skills/ppt-animation/README.md#主题画廊"><b>打开完整画廊</b></a> 查看预览与适用场景。</sub>

Links: [README](./skills/ppt-animation/README.md) · [SKILL.md](./skills/ppt-animation/SKILL.md)

---

<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->

#### `flowchart`

<a href="./skills/flowchart">
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/0cefab32-b583-4342-b25d-39b5b8c4bf83" />
</a>

**分类:** 流程图 / 概念图 / 原理演示
**适用于:** 视频科普、技术讲解、PPT 配图——需要动画流程图、概念对比、原理演示的场景。

`flowchart` 生成教育/科普类流程图与原理演示的动画 HTML。暗色科技风格，节点发光、箭头流动、数据粒子效果。不只是 AI 模型——任何概念、流程、对比、交互都能用动画呈现。与 `dynamic-archify` 互补：flowchart 偏教育演示（好看 + 直观），dynamic-archify 偏工程架构（精确 + 可导出）。

亮点:
- 7 种图表类型：流程图 / 概念图 / 原理演示 / 时序图 / 对比图 / 时间线 / 系统概览
- AI/ML 模型可视化完整保留（RNN / LSTM / GRU / MLP / Word2Vec / GPU）
- 暗色科技风：深色背景 + 蓝/紫/橙渐变节点 + 发光效果
- 连接线流动动画 + 数据粒子效果，页面始终保持动态感
- 支持自动播放 / 手动步进 / hover 高亮三种交互模式

<table>
<tr>
<td align="center" width="25%"><a href="./skills/flowchart/README.md#支持的图表类型"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/4c6fcc04-7b36-4a65-87a1-b6eb01949179" /></a><br /><sub><code>RNN</code><br />RNN流程图</sub></td>
<td align="center" width="25%"><a href="./skills/flowchart/README.md#支持的图表类型"><img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/267231a2-2b93-4e55-bfb2-577c2a73927f" /></a><br /><sub><code>LSTM</code><br />LSTM流程图</sub></td>
<td align="cente