**交流 QQ 群：`346340389` · `647306826`** · <a href="https://x.com/IoKKFOvWAt12669"><img src="https://img.shields.io/badge/X-000000?style=flat-square&logo=x&logoColor=white" alt="X" /></a> · 喜欢就点个 ⭐ [Star](https://github.com/Justin-sky/ai-art-engine)

<div align="center">
  <img src="docs/assets/logo-mark.png" alt="" width="96" />

  <h1>AI Art Engine</h1>

  <p><b>专业 AI 创作工具 · 短剧 · 广告 · 成片</b></p>
  <p>
    本地工程与素材 · 分镜与节点图驱动生成 · 内置 MCP Server 可被 Claude Code 等 AI Agent 驱动<br />
    对接 OpenRouter · OpenAI · DeepSeek · 智谱 · Kimi · xAI · Google · vLLM · Ollama · LM Studio · 火山方舟 · 可灵 · MiniMax · 通义千问 · 魔塔 · ComfyUI · MagicRouter · Meshy · Tripo · Rodin（Hyper3D） · Luma AI · Lux3D · 自定义提供商（OpenAI 兼容 / Anthropic / Gemini 端点）<br />
    对象存储：火山 TOS · 阿里云 OSS · 腾讯云 COS
  </p>

  <p>
    <a href="https://github.com/Justin-sky/ai-art-engine/stargazers"><img src="https://img.shields.io/github/stars/Justin-sky/ai-art-engine?style=social" alt="GitHub stars" /></a>
    <a href="https://github.com/Justin-sky/ai-art-engine/network/members"><img src="https://img.shields.io/github/forks/Justin-sky/ai-art-engine?style=social" alt="GitHub forks" /></a>
    <a href="https://x.com/IoKKFOvWAt12669"><img src="https://img.shields.io/badge/X-000000?style=flat-square&logo=x&logoColor=white" alt="Follow on X" /></a>
    <a href="https://github.com/Justin-sky/ai-art-engine/releases"><img src="https://img.shields.io/github/v/release/Justin-sky/ai-art-engine?include_prereleases&label=release&style=flat-square" alt="release" /></a>
    <a href="https://github.com/Justin-sky/ai-art-engine/releases"><img src="https://img.shields.io/github/downloads/Justin-sky/ai-art-engine/total?label=downloads&style=flat-square" alt="downloads" /></a>
    <a href="https://github.com/Justin-sky/ai-art-engine/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPL--3.0-blue.svg?style=flat-square" alt="license" /></a>
    <a href="https://github.com/Justin-sky/ai-art-engine/blob/main/package.json"><img src="https://img.shields.io/github/package-json/v/Justin-sky/ai-art-engine?label=version&style=flat-square&color=orange" alt="version" /></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Local--First-本地优先-00B894?style=for-the-badge" alt="local" />
    <img src="https://img.shields.io/badge/Node_Graph-节点图-6C5CE7?style=for-the-badge" alt="graph" />
    <img src="https://img.shields.io/badge/Win%20%7C%20macOS%20%7C%20Linux-多平台-0984E3?style=for-the-badge" alt="platform" />
  </p>

  <p>
    <a href="https://justin-sky.github.io/ai-art-engine/"><b>官网</b></a> ·
    <a href="https://justin-sky.github.io/ai-art-engine/manual.html"><b>使用手册</b></a> ·
    <a href="https://justin-sky.github.io/ai-art-engine/guide-video.html"><b>视频生成指南</b></a> ·
    <a href="https://justin-sky.github.io/ai-art-engine/guide-short-video.html"><b>短视频教程</b></a> ·
    <a href="https://justin-sky.github.io/ai-art-engine/guide-comfyui.html"><b>ComfyUI 教程</b></a> · <a href="https://justin-sky.github.io/ai-art-engine/guide-mcp.html"><b>MCP 接入</b></a> ·
    <a href="https://space.bilibili.com/3707036976024122"><b>视频教程</b></a> ·
    <a href="https://github.com/Justin-sky/ai-art-engine/releases"><b>Download</b></a> ·
    <a href="https://github.com/Justin-sky/ai-art-engine"><b>GitHub</b></a> ·
    <a href="https://gitee.com/beijing_blue_whale_era_zhangjian/ai-art-engine"><b>Gitee</b></a> ·
    <a href="#交流"><b>交流</b></a> ·
    <a href="#features"><b>Features</b></a> ·
    <a href="#quick-start"><b>Quick Start</b></a> ·
    <a href="./README.en.md"><b>English</b></a>
  </p>
</div>

---

## 源码仓库

- GitHub（主仓库）：https://github.com/Justin-sky/ai-art-engine
- Gitee（国内镜像）：https://gitee.com/beijing_blue_whale_era_zhangjian/ai-art-engine

两个仓库的 `main` 分支保持同步；Release 与客户端自动更新仍以 GitHub 为准。

---

<a id="download"></a>

## Download

| Platform    | Package                   | Get it                                                                                                                                                      |
| ----------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Windows** | `.exe`                    | [GitHub Releases](https://github.com/Justin-sky/ai-art-engine/releases)                                                                                     |
| **macOS**   | `.dmg`（`x64` / `arm64`） | [GitHub Releases](https://github.com/Justin-sky/ai-art-engine/releases)：Intel 选 **x64**，Apple Silicon 选 **arm64**（仅 arm64 时 Intel Mac 会提示不支持） |
| **Linux**   | `.AppImage`               | [GitHub Releases](https://github.com/Justin-sky/ai-art-engine/releases)（`chmod +x` 后运行）                                                                |

推送 `v*` tag 可由 GitHub Actions 自动构建并发布多平台安装包。也可自行打包：

```bash
npm run dist:win    # Windows
npm run dist:mac    # macOS
npm run dist:linux  # Linux
```

---

<a id="features"></a>

## Features

**AIArtEngine** 是面向短剧、广告与成片制作的专业 AI 创作工具：资产、分镜、节点图在同一桌面端完成，工程本地优先，模型调用走你自己的 API Key。

### 特色功能：AI 对话 + MCP

> 应用内聊天即可驱动全部生成与编排能力；Claude Code / Codex 等外部 AI Agent 也能直连操作你的工程。

- **AI 对话面板** — 应用内 AI 助手（DeepSeek Harness 运行时）：在对话里 `@` 引用工程资产、让 Agent 调用 MCP 工具直接干活——生成图片 / 视频 / 3D / 语音、编辑节点图、运行工作流并查状态；多会话历史、模型可选任意已配置文本模型
- **MCP 工具服务** — 内置 MCP Server，Claude Code / Codex 等外部 AI Agent 可经 stdio 桥或 HTTP 直连操作你的工程（规划并落盘工作流、运行生成、读写资产与节点图）；token 跨重启持久复用、操作审计、并发闸门

### 特色功能：Skill 技能系统

> 技能是"职业手册"——告诉 Agent 怎么做（流程、规范、输出格式）；MCP 工具是"手脚"——真正动手执行。两者配合，对话才能"说到做到"。

- **内置创作技能** — 随对话自动就位，无需配置：分镜 / 动画（9 宫格分镜表、节拍拆解表、动态提示词表、4 宫格动态分镜表等）、导演审核、系统创作（剧本、图生提示词、图片 / 视频生成、声音、情绪、灯光、多角度、扩图、重绘、抠图、高清放大、界面图、界面拆分、世界提取、节拍拆分、节拍单元生成、策划案、肖像贴图、提示词优化、擦除）
- **自定义技能** — 设置 → **自定义技能**：把符合 dsh SKILL.md 格式（frontmatter `name` / `description` + Markdown 正文）的 `.md` 文件放进技能目录，下次对话自动生效；目录内一键「生成示例模板」
- **机制** — 技能清单以 `<available_skills>` 注入对话上下文，Agent 判断任务匹配时按需加载技能文件作为指令；内置技能由程序自动管理（快照 + 指纹去重），自定义技能不受影响。节点图节点也使用同一套技能定义节点行为

### 特色功能：Blender MCP Server（让 AI 直接操作 Blender）

> 本机 Blender 跑着，AI 就能在对话里搭场景、写材质、截图自查、导出 GLB —— **出站直连 addon，不需要 uv / Python / 子进程**。

- **直接驱动 Blender** — 9 个 MCP 工具覆盖「看清现状 → 写 bpy 建模 → 截图自查 → 导出 GLB」闭环：`get_scene_info` / `get_world_state_snapshot` / `get_object_info` 查场景与选中对象，`execute_blender_code` 在 Blender 进程内执行 Python（完整访问 bpy / bmesh / mathutils），`get_viewport_screenshot` 抓视口画面回给多模态客户端，`export_scene` 出 GLB / GLTF / FBX / OBJ / USD / STL（配 `asset_import` 一键入资产库），`describe_node_type` / `bpy_api_lookup` / `get_addon_status` 查节点端口、查 bpy API、查 addon 版本
- **双 addon 兼容** — 同时支持**社区方案** [blender-mcp](https://github.com/ahujasid/blender-mcp) 的 `addon.py` 与**官方方案** [Blender Lab「MCP Server」](https://projects.blender.org/lab/blender_mcp) 扩展，在「设置 → MCP → Blender 工具集」里切换；两种后端下工具名、入参、输出结构**完全一致**，模型侧无感
- **零额外依赖** — 不装 uv、不起 Python 子进程、不改 Blender 配置：应用主动出站连 addon 的 `localhost:9876` 监听端口；安装包 / 仓库 / 容器环境开箱即用
- **应用内对话 + 外部 Agent 同源** — 工作区左侧 ◈ AI 对话面板（在聊天里说「用 Blender 把这几个 Cube 拼成底座，做完截张图」）与 Claude Code / Codex 等外部 Agent 走**同一套** Blender 工具集；设置里关掉即整组从工具清单里消失，主工具集不受影响；面板的 Ask / Plan 模式同样约束 Blender 工具 —— 它不是绕过面板模式的侧门
- **模式兜底与截图边界** — `execute_blender_code` **不再做词法护栏**（可使用完整 Python / bpy 能力）；写入仍由 Ask / Plan 在请求级收窄。截图走一次性临时文件，画面只随 MCP 响应回给多模态客户端，不落工程也不进审计日志

详细工具清单、协议细节与安全设计见 [MCP 接入指南](./docs/MCP.md#⑤- blender-工具集可选需要本机-blender) / [MCP 接入教程](https://justin-sky.github.io/ai-art-engine/guide-mcp.html#blender)。

### 完整能力

- **本地工程** — 新建 / 打开 / 最近列表，JSON + 媒体目录落盘，数据不出本机
- **资产库** — 图片 / 视频 / 声音 / 3D 模型；AssetRef GUID；`.aipackage` 导入导出；**多选文件 / 多选目录拖拽到其它目录**（磁盘搬移 + descendant asset.relativePath 写回 + 成环检测 + 同名追加 " 2" / " 3"）
- **分镜与画布** — 镜头参数、Fabric 构图、可停靠布局
- **一键工作流** — 预设模板（短剧分镜、游戏UI界面、游戏买量、产品广告、电商带货、游戏3D资产、漫画出版、知识口播、3D白模预演等）或 AI 规划拓扑，一键创建可复用宿主资产（边界 I/O + Dive 内图）
- **节点图生成** — 文本 / 图片 / 视频 / 声音 / 3D 模型节点，指令面板与模型参数；生成锁定、图库双输出口；端口类型必须相同（单数不能进复数，选取节点只收列表口）；连线样式 / 小地图；任务队列复用共同上游、**任务容错模式**（节点失败降级不整链中断）；漫画页（分镜格 + 台词气泡，导出透明 PNG）、广告变体矩阵、媒体质检 / 返工（专用质检模型五维评分 → FAIL 自动注入原因重试）、2D 帧动画与帧动画序列图、图层分离（拆层后可导出