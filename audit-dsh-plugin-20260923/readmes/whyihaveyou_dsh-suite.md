# dsh-suite

![GitHub stars](https://img.shields.io/github/stars/whyihaveyou/dsh-suite?style=flat-square&color=facc15)
![Plugins](https://img.shields.io/badge/plugins-1949-facc15?style=flat-square)
![Daily compat](https://img.shields.io/github/actions/workflow/status/whyihaveyou/dsh-suite/compat.yml?branch=main&label=daily-compat-check&style=flat-square)
![License](https://img.shields.io/badge/license-MIT-3b82f6?style=flat-square)

> 🌐 中文 · [English](README.en.md)

**别再翻 `dsh-plugin` topic 了，这里都是还能跑的插件。**

`dsh-suite` 是 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）插件的**活目录**——**每小时自动刷新、每日兼容实测**——外加 DSH 内置**插件商店**、`create-dsh-plugin` 脚手架、几个自研插件，以及一个**[一体化工作台](https://github.com/whyihaveyou/dsh-workstation)**（🚧 开发中）。

[![目录网站](https://img.shields.io/badge/🌐_目录网站-whyihaveyou.github.io/dsh--suite-4d6bfe?style=for-the-badge)](https://whyihaveyou.github.io/dsh-suite/zh.html)

[![dsh-suite 目录网站](https://whyihaveyou.github.io/dsh-suite/preview/2026-08-14/home-zh.png)](https://whyihaveyou.github.io/dsh-suite/zh.html)

**🧭 生态 / Ecosystem**

- 🌐 [目录网站](https://whyihaveyou.github.io/dsh-suite/zh.html) — 在线逛全部插件
- 📖 [DSH 中文文档 · dsh-docs.com](https://dsh-docs.com) — 中文教程与文档，开箱即用无需翻墙
- 📕 [DSH 插件开发指南](https://github.com/whyihaveyou/dsh-plugin-tutorial) — 中英双语成书
- 🎨 [皮肤画廊](https://whyihaveyou.github.io/dsh-themes/) — 151 款皮肤昼夜双预览

---

## 为什么做 dsh-suite

DSH 发布时没有官方插件 registry。现在找插件只能翻 GitHub 的 `dsh-plugin` topic（50+ 个零散小插件）和当天冒出来的几个静态 awesome-list——而 DSH 自己还在发**破坏性变更**（breaking changes）。

所以我们做了四件事：

1. **一个「活」目录**——880+ 精选插件，CI **每小时**刷新数据、**每天**把收录的包真实装进临时 profile 重测兼容性。
2. **一个内置插件商店**——`@dsh-suite/plugin-manager` 在 DSH Web UI 的设置页里加一个 **Store** 标签：逛目录、搜索、看徽章、一键安装，全程不用离开 DSH。
3. **一个脚手架**——`npm create dsh-plugin` 一条命令生成可跑的 `dsh.bundle` + Cordis 骨架。官方没给脚手架，而「怎么迁移我的插件」是社区呼声最高的需求之一。
4. **几个自研插件**——不是纯搬运，有第一方产出。
5. **一个一体化工作台**——[dsh-workstation](https://github.com/whyihaveyou/dsh-workstation)，开箱即用版（🚧 开发中）。

## 快速开始

```bash
# 1. 逛目录网站
open https://whyihaveyou.github.io/dsh-suite/zh.html

# 2. 把插件商店装进你的 DSH Web UI
npx @deepseek-ai/dsh plugin --profile web add @dsh-suite/plugin-manager
#    → 重启 Web UI，然后 设置 → Plugins → Store

# 3.（开发者）造一个自己的插件
npm create dsh-plugin@latest my-plugin
```

![DSH Web UI 里的插件商店 Store 标签页](site/assets/store-tab.png)

## 📚 插件目录

<!-- CATALOG:START -->
### ⭐ 精选

| 插件 | ⭐ | 兼容 | 描述 |
|---|---|---|---|
| [dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | 7963 | 🟢 ok | DSH Web UI 插件与皮肤合集：任务板、Git 面板等 |
| [DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 3731 | 🟢 ok | 侧边栏完整工作台：文件渲染/终端/Git/子代理 |
| [dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale) | 2191 | ⚪ unknown | DSH Web 鲸鱼娘皮肤系列（深海女仆工坊） |
| [dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | 883 | 🟢 ok | 给纯文本模型加视觉：图片问答、长截图 OCR、UI 还原 |
| [dsh_workflow](https://github.com/icetomoyo/dsh_workflow) | 129 | 🟢 ok | 把 Claude Code 的 UltraCode 模式带给 DSH，多 Agent 调度可治理 |
| [dsh-turn-rewind](https://github.com/Anionex/dsh-turn-rewind) | 118 | 🟢 ok | 对话回退：回滚会话与工作区状态 |
| [mstar-harness](https://github.com/btspoony/mstar-harness) | 62 | ⚪ unknown | Skill 驱动的 Harness/Loop 工程工作流插件 |
| [ui-status-label](https://github.com/alingalingling/ui-status-label) | 48 | 🔴 broken (failed once, retried — install blocked by pnpm build-script policy (allowBuilds) — plugin likely OK, CI policy blocks git prepare scripts) | 自定义「鲸鱼娘」思考状态的显示 |
| [dsh-share](https://github.com/hellodigua/dsh-share) | 34 | 🟢 ok | DSH 对话分享插件 |
| [distill](https://github.com/LoserFox/distill) | 27 | ⚪ unknown | 自动对话蒸馏：后台 subagent 反省 + 技能更新 |
| [dsh-custom-tool](https://github.com/omdsh-dev/dsh-custom-tool) | 23 | 🟢 ok | Monaco 编辑器创建沙箱 JS 工具 |
| [all (全家桶)](https://github.com/whyihaveyou/dsh-suite) | 15 | 🟢 ok | 全家桶聚合包：一次安装带入第一方全家桶——插件商店、IM 通知、会话导出、多 agent 任务板。 |
| [themes (皮肤中心)](https://github.com/whyihaveyou/dsh-themes) | 11 | 🟢 ok | 皮肤中心：151 款昼夜成对皮肤一包打尽——网格预览、搜索、一键试穿，支持收藏、最近试穿与随机换肤。 |
| [dsh-acp-for-bitfun](https://github.com/bobleer/dsh-acp-for-bitfun) | 10 | 🟢 ok | BitFun 与 DSH ACP 交互对接 |
| [plugin-manager](https://github.com/whyihaveyou/dsh-suite) | 7 | 🟢 ok | DSH Web UI 内置插件商店：浏览 dsh-suite 目录、搜索/筛选/排序、兼容徽章、一键安装——设置页插件区的 Store 标签页。 |
| [plugin-team-board](https://github.com/whyihaveyou/dsh-suite) | 7 | 🟢 ok | 多 agent 会话共享任务看板：跨 subagent 创建/认领/更新/查询任务，基于 append-only 会话日志持久化。 |
| [plugin-session-export](https://github.com/whyihaveyou/dsh-suite) | 3 | 🟢 ok | 把 append-only 会话日志导出成人读的 Markdown / HTML，按来源分组渲染（系统提示 / 思维链 / 工具调用 / 子agent）。 |
| [create-dsh-plugin](https://github.com/whyihaveyou/dsh-suite) | 3 | 🟢 ok | 一键脚手架生成 DeepSeek Harness (DSH) 插件：tool / events / webui 三套模板、next 标签版本锁定、内置 --verify 冒烟测试。 |
| [plugin-notify](https://github.com/whyihaveyou/dsh-suite) | 3 | 🟢 ok | 回合完成 / 出错 / 待审批时，把通知推到 IM webhook（飞书 / 企业微信 / 钉钉 / Slack / Discord / 自定义）+ 本机系统通知。 |
| [preset-center (场景预设)](https://github.com/whyihaveyou/dsh-suite/tree/main/packages/preset-center) | 1 | 🟢 ok | 中文开箱即用预设全家桶：小红书笔记助手 / 中文文案润色 / 日报周报生成器，一键应用到官方 Agent presets，无需重启、选择器立即可见。 |
| [plugin-deus (神模扳机)](https://github.com/whyihaveyou/dsh-suite/tree/main/packages/plugin-deus) | 1 | 🟢 ok | 神模扳机：一键触发实测验证过的 Minimal 行为，起手指纹自动识别回复模式，本地触发率统计（Wilson CI）。提示词实验台，不承诺任何隐藏能力。 |

### 🧰 工具

| 插件 | ⭐ | 兼容 | 描述 |
|---|---|---|---|
| [open-managed-agents](https://github.com/openma-ai/open-managed-agents) | 302 | ⚪ unknown | Claude Managed Agents API 的开源自托管平台（Cloudflare Workers） |
| [role-model](https://github.com/try-works/role-model) | 118 | ⚪ unknown | 按任务把请求路由到「正确的模型」（本地/云） |
| [irmia_devkit_open](https://github.com/irmia2026/irmia_devkit_open) | 42 | ⚪ unknown | Python 开发工具包（无描述） |
| [HoloGram](https://github.com/834063245-creator/HoloGram) | 25 | ⚪ unknown | 3D 代码依赖拓扑图生成器（14 语言） |
| [dsh-custom-tool](https://github.com/omdsh-dev/dsh-custom-tool) | 23 | 🟢 ok | Monaco 编辑器创建沙箱 JS 工具 |
| [dsh-acp-for-bitfun](https://github.com/bobleer/dsh-acp-for-bitfun) | 10 | 🟢 ok | BitFun 与 DSH ACP 交互对接 |
| [fabric](https://github.com/omdsh-dev/fabric) | 18 | ⚪ unknown | 类似 MC Fabric 的 hook 处理器 |
| [dsh-git-identity](https://github.com/LoserFox/dsh-git-identity) | 6 | ⚪ unknown | git 提交固定使用环境作者身份 |
| [Hypr-Agent-Protal](https://github.com/gfhdhytghd/Hypr-Agent-Protal) | 6 | ⚪ unknown | Hyprland 的 Computer Use MCP |
| [telegram](https://github.com/LoserFox/telegram) | 7 | ⚪ unknown | Telegram Bot API 桥接（长轮询） |
| [agent-knock-knock](https://github.com/scotthuang/agent-knock-knock) | 6 | ⚪ unknown | OpenClaw 插件：共享 tmux 控制本地 Codex/Claude Code |
| [dsh-bash-encoding](https://github.com/lhh010/dsh-bash-encoding) | 8 | ⚪ unknown | bash 输出编码自动识别（UTF-16LE/UTF-8/GBK） |
| [dsh-data-agent](https://github.com/omdsh-dev/dsh-data-agent) | 198 | 🟢 ok | 连数据库、写 SQL 的插件 |
| [dsh-doctor](https://github.com/coppynight/dsh-doctor) | 5 | 🟢 ok | flutter-doctor 风格诊断与安全自动修复 |
| [dsh-interconnect](https://github.com/Chinesezjc/dsh-interconnect) | 33 | 🟢 ok | 跨实例消息/事件交接插件 |
| [dsh-openbiliclaw](https://github.com/whiteguo233/dsh-openbiliclaw) | 59 | 🔴 broken (dump-config exit=0 but plugin not found in composed tree) | OpenBiliClaw 内容推荐 Agent 接入 DSH |
| [dsh-plugin-check](https://github.com/omdsh-dev/dsh-plugin-check) | 26 | 🟢 ok | 扫描插件仓库清单协议/patch 格式/构建陷阱 |
| [dsh-security-audit](https://github.com/omdsh-dev/dsh-security-audit) | 14 | 🟢 ok | 本机安全审计：配置/插件来源/会话/网络暴露面 |
| [dsh-tool-csv](https://github.com/omdsh-dev/dsh-tool-csv) | 4 | ⚪ unknown | CSV 解析/查询/统计/转换工具 |
| [dsh-toolkit](https://github.com/omdsh-dev/dsh-toolkit) | 27 | ⚪ unknown | 零依赖工具包合集（time/encoding/json/csv/regex） |
| [atomstudio](https://github.com/AtomicsLaboratory/atomstudio) | 0 | ⚪ unknown | 可执行文档工程环境 |
| [dsh-cc-connect](https://github.com/whiteguo233/dsh-cc-connect) | 3 | ⚪ unknown | 通过 cc-connect 远程使用 DSH |
| [dsh-mnemon](https://github.com/omdsh-dev/dsh-mnemon) | 400 | 🟢 ok | Mnemon 三层记忆体深度集成 |
| [dsh-paseo](https://github.com/renat3u/dsh-paseo) | 4 | ⚪ unknown | DSH 的 paseo 插件扩展支持 |
| [dsh-plugin-dev](https://github.com/omdsh-dev/dsh-plugin-dev) | 14 | ⚪ unknown | DSH 插件开发踩坑档案（