<p align="center">
  <img src="assets/banner.svg" alt="DSH Plugins — DeepSeek Harness 插件中文导航" width="100%">
</p>

<h1 align="center">DSH Plugins</h1>

<p align="center">
  <strong>别再一个个翻仓库了。好用的、热门的、有点意思的 DSH 插件，都在这里。</strong>
</p>

<p align="center">
  不只给你一串链接——每个插件都写清楚：<strong>能做什么、适合谁、怎么安装、装完第一步怎么用，以及哪里容易踩坑。</strong>
</p>

<p align="center">
  <a href="https://awesome.re"><img alt="Awesome" src="https://awesome.re/badge-flat2.svg"></a>
  <a href="https://github.com/gityuanbao/DSH-Plugins/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/gityuanbao/DSH-Plugins?style=flat-square&logo=github&color=7c3aed"></a>
  <img alt="Curated plugins" src="https://img.shields.io/badge/精选插件-16-06b6d4?style=flat-square">
  <img alt="Categories" src="https://img.shields.io/badge/覆盖场景-7_类-22c55e?style=flat-square">
  <img alt="Last verified" src="https://img.shields.io/badge/最近核验-2026--08--16-f59e0b?style=flat-square">
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-64748b?style=flat-square"></a>
</p>

<p align="center">
  <a href="#-30-秒找到适合你的插件">30 秒选插件</a> ·
  <a href="#-直接抄作业4-套好用组合">直接抄作业</a> ·
  <a href="docs/PLAYBOOKS.md">上手玩法</a> ·
  <a href="#-全部-16-个插件一张表看完">全部插件</a> ·
  <a href="#-热门精选逐个看">详细介绍</a> ·
  <a href="https://github.com/gityuanbao/DSH-Plugins/issues/new/choose">推荐新插件</a>
</p>

> DSH 的插件生态正在快速长大，但 GitHub Topic 里也混进了大量“只有标签、不能安装”的项目。这个仓库替你做第一轮筛选，再把真正影响选择的信息翻译成人话。

<p align="center">
  <strong>如果它帮你少翻了几个仓库、少踩了一个坑，点一下右上角 ⭐ Star。</strong><br>
  下次想给 DSH 加能力时，你还能很快找到这里。
</p>

## ✨ 这个合集能帮你什么

| 🔍 更快找到 | 🧭 更容易选对 | 💡 装完真会用 |
|---|---|---|
| 按工作台、视觉、多 Agent、安全、效率等场景整理 | 告诉你“适合谁”，也告诉你哪些插件功能重叠 | 每个项目都有一条实测思路或贴心 Tips |
| 热门项目与刚冒头的新锐项目分开 | 不拿 Star 数直接等同于质量 | 把作者 README 里最好用的步骤压缩成中文玩法 |

## 🎯 30 秒找到适合你的插件

| 你现在最想做什么 | 直接看它 | 为什么 |
|---|---|---|
| 我刚开始玩 DSH，不知道装什么 | [dsh-market](#dsh-market) | 像逛应用商店一样找、装、更新插件 |
| 我想一步到位，把 Web UI 变成完整工作台 | [dsh-web-ui](#dsh-web-ui) | 看板、文件、Git、远程、视觉、主题基本全包 |
| 我只想要一个轻量 IDE，不想装全家桶 | [DSH-better-sidebar](#dsh-better-sidebar) | 文件、终端、Git、预览集中在右侧栏和底部面板 |
| 我想让纯文本 DeepSeek 看懂图片 | [ModLens](#modlens) | 粘贴图片就能拿到 OCR、布局和结构化证据 |
| 我是终端党，不想一直开浏览器 | [dsh-TUI](#dsh-tui) | Claude Code 风格的全屏终端体验 |
| 我想让 Agent 做长任务时少跑偏 | [Aegis](#aegis) | 给任务加上基线、验证、漂移检查和完成前复核 |
| 我想同时调度多个 Agent | [dsh-agent-teams](#dsh-agent-teams) | Captain、子 Agent、依赖任务和团队状态都有了 |
| 我想给危险命令和敏感信息加道提醒 | [dsh-guardian](#dsh-guardian) | 执行前识别风险，返回后尝试脱敏 |
| 我知道想要什么，但不知道插件名字 | [dsh-find-plugin](#dsh-find-plugin) | 直接让 Agent 帮你搜索 DSH 插件 |

## 🚀 直接抄作业：4 套好用组合

### ① 新手不折腾

`dsh-market` + `dsh-at-file` + `ModLens`

先补齐“找插件、引用文件、看图片”三个高频能力，几乎不改变你原来的工作方式。第一次玩 DSH，从这套开始最容易感受到插件的价值。

### ② Web 工作台

`dsh-web-ui` **或** `DSH-better-sidebar` + `dsh-at-file`

想一步到位选前者，想轻量可控选后者。两个重型工作台不要第一天一起装；先选一个，跑完真实任务再决定要不要叠加。

### ③ 复杂项目交付

`Aegis` + `dsh-agent-teams` + `brooks-lint`

用 Aegis 管过程、Agent Teams 做并行、brooks-lint 做最终审查。三者职责分开，比让每个插件都接管全流程更稳定。

### ④ 好看又好玩

`dsh-deep-whale` + `dsh-ads`

一个负责把工作台变成鲸鱼娘主题，一个负责把等待过程变成 2005 年门户网站。适合直播、演示和想让 DSH 更有个性的人。

## 🧪 不只是收录：这里还有 16 份「装完就能抄」的玩法

很多插件不是装上就会用。我们继续读完了作者 README，把最有价值的操作缩成一份 [中文玩法手册](docs/PLAYBOOKS.md)：

| 装完以后 | 你可以直接抄什么 |
|---|---|
| 第一次让 DeepSeek 看图 | ModLens 健康检查 + 一段结构化看图提示词 |
| 第一次做视觉验证 | `定位 → 裁剪 → 看细节` 与像素对比工作流 |
| 第一次做代码体检 | `Health → Review → Audit → Sweep` 的安全顺序 |
| 第一次组 Agent 小队 | 性能 / 安全 / 产品三角色审查提示词 |
| 第一次用终端版 DSH | 最值得先记住的 6 个快捷键 |
| 第一次验证安全插件 | 用虚构凭证测脱敏，不拿危险命令“试刀” |

<p align="center">
  <strong><a href="docs/PLAYBOOKS.md">打开完整玩法手册：16 个插件逐个照着做 →</a></strong>
</p>

## 🗺️ 全部 16 个插件，一张表看完

| 类别 | 插件 | 它最擅长什么 | 最适合谁 |
|---|---|---|---|
| 🖥️ 工作台 | [dsh-web-ui](#dsh-web-ui) | Web UI 全家桶 | 想一步到位的重度用户 |
| 🖥️ 工作台 | [DSH-better-sidebar](#dsh-better-sidebar) | 轻量 IDE 式侧边栏 | 想要文件、终端、Git 的开发者 |
| ⌨️ 终端 | [dsh-TUI](#dsh-tui) | 全屏终端交互 | 键盘党、终端党 |
| 👁️ 视觉 | [ModLens](#modlens) | OCR、布局与结构化图像证据 | 前端、截图排错、文档分析 |
| 👁️ 视觉 | [DSH Vision Toolkit](#dsh-vision-toolkit) | 裁剪、取色、坐标、像素级验证 | 设计 QA、GUI 自动化 |
| 🛍️ 视觉 | [WeShop for DSH](#weshop-for-dsh) | 电商图、试穿、背景与短视频 | 电商运营、视觉营销 |
| 🧠 工程 | [Aegis](#aegis) | 长任务方法论与验证 | 复杂修复、架构改造 |
| 🧠 工程 | [brooks-lint](#brooks-lint) | 代码、架构和技术债审查 | Reviewer、遗留系统团队 |
| 🧪 实验 | [dsh-anchored-standard](#dsh-anchored-standard) | 首轮提示词与工具锚定 | 做基准测试的高级用户 |
| 🤝 多 Agent | [dsh-agent-teams](#dsh-agent-teams) | Captain + 持久化子 Agent 团队 | 并行研究、代码审查、交付拆解 |
| ⚡ 效率 | [dsh-at-file](#dsh-at-file) | 输入 `@` 快速引用文件 | 经常指定文件和目录的人 |
| 🧩 发现 | [dsh-market](#dsh-market) | 图形化插件市场 | 新手、Web 用户 |
| 🧩 发现 | [dsh-find-plugin](#dsh-find-plugin) | 让 Agent 搜索插件 | 只知道需求、不知道名字的人 |
| 🛡️ 安全 | [dsh-guardian](#dsh-guardian) | 危险操作提醒与结果脱敏 | 常让 Agent 执行命令的人 |
| 🎨 主题 | [dsh-deep-whale](#dsh-deep-whale) | 鲸鱼娘主题皮肤 | 直播、展示、个性化用户 |
| 🎮 整活 | [dsh-ads](#dsh-ads) | 复古广告与推理中插播 | 社区演示、直播整活 |

> 表里的 Star、版本和安装方式首次核验于 **2026-08-15**，玩法文档复核于 **2026-08-16**。DSH 仍处于 Developer Preview，升级后请顺手回到原项目 README 看一眼最新说明。

## 🔥 热门精选，逐个看

<a id="dsh-web-ui"></a>
### 01 · [dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) — DSH Web 的「全家桶」

`🔥 2.2k+ Stars` · `工作台` · `Apache-2.0`

一句话：把任务看板、Git 图谱、文件预览、移动端远程、SSH、图像理解、用量统计、宠物和皮肤中心全部塞进 DSH Web。

- **适合你，如果：** 你准备把 DSH 当主力工作台，希望一次补齐大部分界面能力。
- **💡 好用 Tips：** 只需要看板、SSH 或宠物时，优先安装对应子包；冲突更少，排错也更容易。
- **🚀 第一次这样用：** [先跑全家桶，再按需做减法 →](docs/PLAYBOOKS.md#play-dsh-web-ui)
- **⚠️ 装前知道：** 全家桶权限面较大。第一次不要同时叠加另一个重型侧边栏框架；pnpm 11 用户还要看项目里的 hoisted 布局说明。

```sh
dsh plugin --profile web add @linxin666/dsh-web-ui-all
```

<a id="modlens"></a>
### 02 · [ModLens](https://github.com/liustack/modlens) — 给纯文本模型装上一双眼睛

`🔥 1.4k+ Stars` · `视觉 / OCR` · `MIT`

一句话：粘贴图片后，为 DeepSeek、GLM 等纯文本模型补上 OCR、布局、实体与关系等结构化证据。

- **适合你，如果：** 你要做前端还原、截图排错、文档 OCR 或看图问答，又不想更换主模型。
- **💡 好用 Tips：** 第一次先跑项目提供的健康检查，再选择名字里带 `(modlens vision)` 的路由；固定版本比追 `latest` 更容易复现。
- **🚀 第一次这样用：** [跑健康检查，再照抄结构化看图提示词 →](docs/PLAYBOOKS.md#play-modlens)
- **⚠️ 装前知道：** 图片可能会发往你配置或复用的外部视觉服务，先确认实际调用哪家引擎、消耗哪份额度。

```sh
npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens@3.16.6
```

<a id="brooks-lint"></a>
### 03 · [brooks-lint](https://github.com/hyhmrright/brooks-lint) — 让代码审查不再只靠感觉

`🔥 1.3k+ Stars` · `代码审查 / 架构` · `MIT`

一句话：把 12 本经典软件工程著作变成代码、架构、技术债和测试的检查清单，并给出有出处的修改建议。

- **适合你，如果：** 你负责 Code Review、维护遗留系统，或者希望 Agent 的建议更有工程依据。
- **💡 好用 Tips：** 先用 `/brooks-review` 或 `/brooks-health` 做只读体检，再决定要不要执行自动修复。
- **🚀 第一次这样用：** [按 Health → Review → Sweep 的顺序体检 →](docs/PLAYBOOKS.md#play-brooks-lint)
- **⚠️ 装前知道：** 它是 DSH 可发现的 Skill Pack，不是 Cordis Bundle；安装时要保留项目要求的扁平目录结构。

```sh
./scripts/install.sh dsh
```

<a id="dsh-anchored-standard"></a>
### 04 · [dsh-anchored-standard](https://github.com/xiaobright/dsh-anchored-standard) — 给首轮请求做一次「锚定」

`🔥 1.2k+ Stars` · `实验 Preset` · `未声明标准许可证`

一句话：首轮使用 Minimal 的提示词和真实工具 Schema，随后切回 Standard 的完整工具集。

- **适合你，如果：** 你在做模型基准测试，或研究首轮工具分布对 DeepSeek 表现的影响。
- **💡 好用 Tips：** 一定从空白会话开始，并按项目 Verify 清单检查前两次 `request/header`。
- **🚀 第一次这样用：** [做一组可复现的 Standard / Anchored 对照 →](docs/PLAYBOOKS.md#play-anchored-standard)
- **⚠️ 装前知道：** 特定 Project2 高分不能外推成通用性能提升；当前主要兼容证据针对 DSH `0.1.0-rc.5`。

```sh
cp -R preset ~/.dsh/.agent-presets/anchored-standard
```

<a id="dsh-tui"></a>
### 05 · [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) — 终端党会喜欢的 DSH

`🔥 1k+ Stars` · `终端工作台` · `MIT`

一句话：Claude Code 风格的全屏终端，带流式 Markdown、工具卡、`@` 文件引用、会话恢复、TPS、Skills、MCP 和子 Agent。

- **适合你，如果：** 你长期待在终端、偏好键盘操作，也想实时观察 Agent 状态。
- **💡 好用 Tips：** macOS Terminal 会抢走部分 `⌘` 快捷键，优先记住项目提供的 `Ctrl` 组合。
- **🚀 第一次这样用：** [先记住 6 个键，再恢复一段旧会话 →](docs/PLAYBOOKS.md#play-dsh-tui)
- **⚠️ 装前知道：** 要求 Node `^22.19` 或 `>=24`；它复用 DSH 当前 Profile 的安全边界，不另送一套沙箱。

```sh
npm install -g @deepseek-ai/dsh @deepseek-harness-tui/dsh-tui
```

<a id="aegis"></a>
### 06 · [Aegis](https://github.com/GanyuanRan/Aegis) — 给长任务加上工程纪律

`🔥 1k+ Stars` · `方法论 / 验证` · `MIT`

一句话：为长任务加入基线、证据验证、漂移检查、系统化调试和完成前复核。

- **适合你，如果：** 你要做架构改造、复杂修复或规格驱动开发，最怕 Agent “凭感觉完工”。
- **💡 好用 Tips：** 安装后用 `dsh --profile web --dump-config` 确认只出现一个 `aegis-method-pack`，再在新会话显式加载 `using-aegis`。
- **🚀 第一次这样用：** [用一句 Aegis goal 锁定边界和成功证据 →](docs/PLAYBOOKS.md#play-aegis)
- **⚠️ 装前知道：** 不要同时把 Aegis 放进多个 Skills 目录，