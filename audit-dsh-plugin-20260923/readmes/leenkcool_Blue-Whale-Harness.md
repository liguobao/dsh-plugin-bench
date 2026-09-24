# Blue-Whale-Harness

[![Stars](https://img.shields.io/github/stars/leenkcool/Blue-Whale-Harness?style=flat-square)](https://github.com/leenkcool/Blue-Whale-Harness/stargazers) [![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=flat-square)](./LICENSE) [![Last commit](https://img.shields.io/github/last-commit/leenkcool/Blue-Whale-Harness?style=flat-square)](https://github.com/leenkcool/Blue-Whale-Harness/commits/main) [![Plugins](https://img.shields.io/badge/repos-1972-orange?style=flat-square)](https://leenkcool.github.io) [![Online catalog](https://img.shields.io/badge/site-leenkool.github.io-brightgreen?style=flat-square)](https://leenkcool.github.io)

> **DeepSeek Harness（DSH）插件总目录** — 收录 GitHub 上散落各处的 DSH 插件、Skill、MCP Server 与周边工具，逐个校验「是否为真插件」，并做成可搜索、可筛选、可导出的在线总表。

🌐 **在线总表：[leenkcool.github.io](https://leenkcool.github.io)** — 中英文搜索、分类筛选、按 STAR 排序、CSV 导出。

> 自动生成于 2026-09-12 ｜ 共 **1972** 个仓库 ｜ 真·DSH 插件 **1832** 个 | QQ Group:839509497 |Tg Group: [http://t.me/deepseekdsh](http://t.me/deepseekdsh)

### 怎么用

1. **找插件** — 直接开 [在线总表](https://leenkcool.github.io)，按关键词 / 分类 / STAR 检索，比翻 README 快得多。
2. **翻清单** — 不想开网页就往下看「插件清单」，或下载 [plugins.csv](https://leenkcool.github.io/plugins.csv) 自己筛。
3. **提交收录** — 发一个 issue（模板 `catalog-intake`）写出仓库地址与分类，或按 `repos.txt` 格式提 PR。

> 收录标准：仓库含 `cordis.patch.yml` 判为**真·DSH 插件**，其余按「相关生态」单独标记，两者都进表、不混算。


![微信群](https://leenkcool.github.io/wechat.jpg)
![频道](https://leenkcool.github.io/pindaoh.png)

## 统计

- 仓库总数：**1972**
- 真·DSH 插件：**1832**
- 在线浏览：https://leenkcool.github.io （[中文版](https://leenkcool.github.io/plugins.zh.html) ｜ [English](https://leenkcool.github.io/plugins.en.html) ｜ [CSV 数据](https://leenkcool.github.io/plugins.csv)）

## 分类索引

- **llm** — 166 个仓库，★101293
- **utility** — 375 个仓库，★66624
- **session** — 236 个仓库，★27296
- **skills** — 53 个仓库，★25583
- **tools** — 627 个仓库，★24534
- **orchestration** — 200 个仓库，★18855
- **ui** — 214 个仓库，★15341
- **uncategorized** — 1 个仓库，★3779
- **sandbox** — 12 个仓库，★743
- **acp** — 65 个仓库，★718
- **memory** — 9 个仓库，★132
- **skin** — 11 个仓库，★40
- **preset** — 2 个仓库，★4
- **notify** — 1 个仓库，★2

## 插件清单

> 按分类分组，组内按 STAR 倒序。点击仓库名即可跳转原项目。

### llm（166）

| 仓库 | 意图(中文) | Intent(English) | STAR | 语言 | 真DSH |
|---|---|---|---|---|---|
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | 开源的 Claude Design 替代方案。🖥️ 本地优先的桌面应用。🖼️ 让你的编码智能体变身设计引擎：原型、落地页…… | 🎨 The open-source Claude Design alternative. 🖥️ Local-first desktop app. 🖼️ Your coding | 92007 | TypeScript | yes |
| [liustack/modlens](https://github.com/liustack/modlens) | DeepSeek Harness 首个视觉插件，纯文本模型看图。 | The first vision plugin for DeepSeek Harness — let text-only models see. | 3725 | TypeScript | yes |
| [Anionex/agent-vision-toolkit](https://github.com/Anionex/agent-vision-toolkit) | 为纯文本模型看图设计的视觉工具箱与技能：多图理解、图片问答、UI 还原、GUI 自动化。 | Vision toolbox & skills for text-only models: multi-image QA, UI reconstruction, GUI autom | 1114 | Python | yes |
| [ysr666/dsh-vision-router](https://github.com/ysr666/dsh-vision-router) | 视觉路由。 | Vision router. | 1007 | JavaScript | yes |
| [PicGo/PicGo-Core](https://github.com/PicGo/PicGo-Core) | ⚡ 极致图床上传引擎，同时支持命令行与 API。 | :zap:The ultimate image uploading engine. Both CLI & API supports. | 981 | TypeScript | no |
| [Anionex/dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | 给纯文本模型加视觉：图片问答、长截图 OCR、UI 还原 | Vision for text-only models: image QA, screenshot OCR, UI reconstruction | 837 | TypeScript | yes |
| [V1ki/dsh-plugin-subscriptions](https://github.com/V1ki/dsh-plugin-subscriptions) | 将 ChatGPT（Codex）、Claude 与 Grok（X Premium）订阅作为 DeepSeek Harness 的 LLM 提供方——Web UI 中 OAuth 登 | Use ChatGPT (Codex), Claude, and Grok (X Premium) subscriptions as DeepSeek Harness LLM pr | 289 | TypeScript | yes |
| [zh667/TokenLedger](https://github.com/zh667/TokenLedger) | DeepSeek Harness 的 Token 用量核算，与 New API 及 Sub2API 中转站账单对账 | Token usage accounting for DeepSeek Harness, reconciled against New API and Sub2API relay- | 171 | JavaScript | yes |
| [Mars-Sea/dsh-commandcode-provider](https://github.com/Mars-Sea/dsh-commandcode-provider) | Command Code 的非官方 DeepSeek Harness LLM 提供商插件：实时模型目录、推理强度支持、模型页卡片。移植自…… | Unofficial DeepSeek Harness LLM provider plugin for Command Code: live model catalog, reas | 114 | TypeScript | yes |
| [oil-oil/dsh-vision](https://github.com/oil-oil/dsh-vision) | 为 DeepSeek Harness 提供近乎原生的图像理解能力 | Near-native image understanding for DeepSeek Harness | 88 | TypeScript | yes |
| [dclichang2022/dsh-green-meter](https://github.com/dclichang2022/dsh-green-meter) | DeepSeek Harness 的能耗与碳排计量：按轮次/按请求的能耗、缓存碳减排、电费。 | Energy & carbon metering for DeepSeek Harness: per-turn/per-request energy, cache carbon s | 80 | TypeScript | yes |
| [labring/sealos-skills](https://github.com/labring/sealos-skills) | Sealos 的 AI 智能体技能——一条命令部署任意项目、开通数据库、对象存储等。兼容 Claude Code、Gemin…… | AI agent skills for Sealos — deploy any project, provision databases, object storage & mor | 77 | Python | yes |
| [william-jin-cmu/dsh-vision](https://github.com/william-jin-cmu/dsh-vision) | view_image 工具桥接任意 OpenAI 兼容 VLM | view_image tool bridging any OpenAI-compatible VLM | 35 | TypeScript | yes |
| [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) | 电脑控制插件（Accessibility 观测 + 作用域权限） | Computer-use plugin (accessibility observation + scoped permission) | 33 | TypeScript | yes |
| [BeforeWave/dsh-with-chatgpt](https://github.com/BeforeWave/dsh-with-chatgpt) | 把 ChatGPT 的推理能力带到本地代码库：可直接工作，或把更大任务委派给 DSH。 | Bring ChatGPT's reasoning to your local codebase. Work directly, or delegate larger tasks  | 33 |  | yes |
| [Make0209/dsh-usage-stats](https://github.com/Make0209/dsh-usage-stats) | DeepSeek Harness 插件：GitHub 风格用量热力图 + Token / 缓存命中 / 账户余额看板 + 工作区别名管理。 | A DeepSeek Harness plugin: a GitHub-style usage heatmap plus a dashboard for token / cache | 27 | JavaScript | yes |
| [AtlasCloudAI/atlas-cloud-skills](https://github.com/AtlasCloudAI/atlas-cloud-skills) | 面向 Claude Code、Codex 与 Gemini CLI 的 Atlas Cloud 技能——从你的编码智能体生成图片/视频并调用 300+ AI 模型。 | Atlas Cloud skills for Claude Code, Codex & Gemini CLI — generate images/videos and call 3 | 26 | JavaScript | no |
| [WSL043/dsh-codex-subscription](https://github.com/WSL043/dsh-codex-subscription) | 在 DSH 里直接使用 ChatGPT 订阅的 Codex 模型，支持订阅搜索、普通 Codex 与 Spark 独立额度显示。 | Use Codex models from a ChatGPT subscription in DSH, with subscription search and separate | 24 | JavaScript | yes |
| [Axiaohungry/dsh-llm-codebuddy](https://github.com/Axiaohungry/dsh-llm-codebuddy) | 在deepseek harness中使用workbuddy api，因为公司只提供workbuddy积分 | Use the WorkBuddy API inside DeepSeek Harness, since the company only provides WorkBuddy c | 24 | JavaScript | yes |
| [zp-home/dsh-recommend](https://github.com/zp-home/dsh-recommend) | DSH 插件生态透明排行与推荐：每日自动抓取 dsh-plugin 话题 + 公开评分模型 + 排行/推荐插件与静态站 | dsh-recommend — DSH plugin (llm) | 19 | JavaScript | yes |
| [yequ172672/dsh-codex-subscription](https://github.com/yequ172672/dsh-codex-subscription) | DSH 插件:直接复用 Codex CLI 本地登录订阅凭证,在 DeepSeek Harness 中使用 ChatGPT 订阅模型,无需 API Key | DSH plugin | A DSH plugin that reuses your Codex CLI local subscription login to use ChatGPT subscripti | 19 | JavaScript | yes |
| [akqwpeter-prog/dsh-media-skills](https://github.com/akqwpeter-prog/dsh-media-skills) | 给 DeepSeek Harness 装上「眼睛」和「画笔」——免费读图 + 免费生图 Skill。Eyes & brush for DeepSeek Harness: free  | Give DeepSeek Harness eyes and a brush — free image reading + free image generation skills | 18 | Python | yes |
| [omdsh-dev/dsh-llm-fallbacks](https://github.com/omdsh-dev/dsh-llm-fallbacks) | An dsh plugin for role-based LLM retry&fallback strategy. 基于角色的模型重试备用策略插件 | A DSH plugin for role-based LLM retry and fallback strategy. | 17 | TypeScript | yes |
| [LAN-TINA-WS/dsh-gui-customization](https://github.com/LAN-TINA-WS/dsh-gui-customization) | Nous Blue theme, ambient glow and background image customization for DeepSeek Harness Web  | Nous Blue theme, ambient glow, and background-image customization for the DeepSeek Harness | 17 