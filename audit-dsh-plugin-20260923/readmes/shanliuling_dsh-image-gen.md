<div align="center">

<img src="docs/assets/readme/hero-zh.webp" alt="dsh-image-gen 中文功能概览" width="100%" />

<br />

<p><strong>简体中文</strong> · <a href="README.en.md">English</a></p>

# 🎨 dsh-image-gen

### DeepSeek Harness 的原生 AI 图像创作套件

<p><b>AI 创作画布 · 对话生图与编辑 · Studio 批量创作 · 多模型对比 · 500+ Prompt 灵感 · 图库管理 · 本地 ComfyUI · 订阅免 Key</b></p>

<p>
  <a href="https://www.npmjs.com/package/dsh-image-gen"><img src="https://img.shields.io/npm/v/dsh-image-gen?style=flat-square&color=4f6ef7" alt="npm version" /></a>
  <a href="https://www.npmjs.com/package/dsh-image-gen"><img src="https://img.shields.io/npm/dm/dsh-image-gen?style=flat-square&color=10b981" alt="npm downloads" /></a>
  <a href="https://github.com/shanliuling/dsh-image-gen/actions/workflows/ci.yml"><img src="https://github.com/shanliuling/dsh-image-gen/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://dsh-insights.com/p/shanliuling/dsh-image-gen"><img src="https://dsh-insights.com/badge/shanliuling/dsh-image-gen.svg" alt="DSH Insights health" /></a>
  <a href="https://github.com/shanliuling/dsh-image-gen/stargazers"><img src="https://img.shields.io/github/stars/shanliuling/dsh-image-gen?style=flat-square" alt="GitHub stars" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-f5c542?style=flat-square" alt="License: Apache-2.0" /></a>
  <a href="https://linux.do/"><img src="https://img.shields.io/badge/LINUX%20DO-社区友链-555?style=flat-square" alt="LINUX DO" /></a>
</p>

<p>
  <a href="#快速开始">快速开始</a> ·
  <a href="#核心能力">核心能力</a> ·
  <a href="#provider-支持情况">Provider 支持</a> ·
  <a href="#常见问题">常见问题</a>
</p>

<br />

<img src="docs/assets/readme/canvas-generate.webp" alt="在无限画布中绘制草稿，并通过对话生成成图" width="46%" />
<img src="docs/assets/readme/canvas-edit.webp" alt="基于已有结果继续对话修改，在画布中持续迭代创作" width="46%" />
<br />
<sub>左：在画布中绘制草稿、摆放参考图，并通过对话生成成图。 · 右：基于已有结果继续对话修改，在画布中持续迭代创作。</sub>

<br />

<img src="docs/assets/readme/chat-generate.webp" alt="在对话中直接描述并生成图片" width="46%" />
<img src="docs/assets/readme/other-features.webp" alt="工作台批量创作、灵感库与图库等更多功能" width="46%" />
<br />
<sub>左：在对话中直接描述并生成图片。 · 右：工作台批量创作、灵感库与图库等更多功能。</sub>

</div>

**为 DeepSeek Harness 带来完整的 AI 图像创作工作流。**

`dsh-image-gen` 不只是简单的对话生图，而是为 DSH 补齐从 **对话生成与连续修图**、**AI 创作画布**、**Studio 批量创作**、**多模型横向对比**，到 **Prompt 灵感库** 与 **本地 ComfyUI** 的完整图像创作能力。

支持主流云端图像模型与本地私有化工作流，既可使用 BYOK（自带 Key），也支持通过订阅账号直接使用，生成结果支持按工作区隔离存储。

> **已有 ChatGPT、Grok 或 Google 订阅？直接登录即可生图，无需额外购买 API Key。**

支持：Gemini · OpenAI / Compatible · Seedream · DashScope · Grok Imagine · GLM-Image · 本地 ComfyUI

```bash
pnpm dsh plugin --profile web add dsh-image-gen@latest
```

> **版本更新提示：** 本次版本变化较大，老用户请更新至最新版本。

<img src="docs/assets/readme/workflow-overview.webp" alt="dsh-image-gen 完整 AI 图像创作工作流" width="100%" />

---

## 一个插件，覆盖完整 AI 图像创作流程

| 入口          | 最适合           | 你可以做什么                             |
| :------------ | :--------------- | :--------------------------------------- |
| 💬 **对话**   | 快速表达想法     | 文生图、图生图、连续编辑、版本迭代       |
| ✏️ **画布**   | 表达视觉创意     | 草稿生成、参考图组合、空间创作、持续修改 |
| 🎛️ **工作台** | 精细控制创作参数 | 批量生成、多图参考、高级参数调整         |
| ✨ **灵感**   | 寻找创作方向     | Prompt 案例、风格探索、一键复用          |
| 🖼️ **图库**   | 管理生成结果     | 搜索、收藏、下载、重新使用               |

---

## 快速开始

### 1. 安装插件

环境要求：DeepSeek Harness 稳定版本，Node.js `^22.19.0` 或 `>= 24.0.0`。

在你的 DeepSeek Harness 项目根目录下运行：

```bash
pnpm dsh plugin --profile web add dsh-image-gen@latest
```

> 💬 **极客提示**：你也可以直接把这句话发送给 DSH 对话中的 Agent：<br />
> `帮我安装生图插件，在终端执行：pnpm dsh plugin --profile web add dsh-image-gen@latest`

<details>
<summary><strong>其他安装方式（全局 / GitHub 直装 / 本地调试）</strong></summary>

```bash
# 若已将 dsh 安装为系统全局命令：
dsh plugin --profile web add dsh-image-gen@latest

# 从 GitHub 仓库直接安装最新代码：
pnpm dsh plugin --profile web add git+https://github.com/shanliuling/dsh-image-gen.git

# 本地克隆源码开发安装：
git clone https://github.com/shanliuling/dsh-image-gen.git
pnpm dsh plugin --profile web add ./dsh-image-gen
```

</details>

### 2. 配置 Provider

重启 DSH 后进入：

**设置 → 插件 → 图像生成**

> DSH 0.1.5 及更早版本的入口为「设置 → 插件 → 插件配置 → 图像生成」，插件已同时兼容两种入口。

选择 Provider，填写自己的 API Key，并按需调整模型、Endpoint / Base URL 与工作区保存选项。填好 Key 后可点击**「测试连接」**验证可用性，或点击**「拉取模型」**一键获取该厂商支持的全部生图模型，无需手动查文档。使用 ComfyUI 时，请填写 DSH Host 可访问的服务地址，并导入 **API Format Workflow JSON**。

已有 ChatGPT、Grok 或 Google 订阅？无需填写 API Key：展开对应的订阅 Provider 行，点击**「登录」**并在浏览器完成授权，即可直接开始文生图与图生图。

### 3. 开始创作

在聊天框中直接描述你想要的图片：

```text
画一张雨夜霓虹街头的赛博朋克猫咪，电影感光线，16:9。
```

也可以直接上传参考图，让 Agent 进行风格重构或局部编辑：

```text
保持角色与构图不变，给猫咪戴上一副黑色墨镜。
```

<br />

<div align="center">
  <img src="docs/assets/readme/provider-settings.webp" alt="DSH 插件配置界面" width="46%" />
  <img src="docs/assets/readme/chat-example.webp" alt="对话生图与风格重构效果" width="46%" />
  <br />
  <sub>左：Provider 配置 · 右：在 DSH 对话中直接生图、图生图与连续编辑。</sub>
</div>

<br />

需要更细的参数控制时，点击会话顶部的 **画廊** 入口，进入 **图库 / 工作台 / 灵感 / 收藏**。

---

## 核心能力

### 💬 对话生图、编辑与版本切换

- 用自然语言完成文生图、图生图、多图参考和风格迁移。
- 直接修改原图 Prompt 重新生成，并在同一卡片中切换历史版本。

<br />

<div align="center">
  <img src="docs/assets/readme/regenerating.webp" alt="图片正在重新生成" width="46%" />
  <img src="docs/assets/readme/revision-switcher.webp" alt="在同一图片卡片中切换生成版本" width="46%" />
  <br />
  <sub>修改 Prompt 后原位重新生成，并在同一张图片卡片中切换历史版本。</sub>
</div>

<br />

### ✏️ 从草稿到成图：AI 创作画布

在无限画布中表达你的创意，通过对话将草稿、构图和想法转化为真实图片。

- 在画布中自由绘制草稿、添加参考素材并组织创意。
- 通过自然语言与 AI 对话，让草稿快速变成完整作品。
- 基于已有结果持续编辑、修改和生成新的方向，保留创作过程，让每一次探索都可以继续迭代。

<br />

<div align="center">
  <img src="docs/assets/readme/canvas-generate.webp" alt="在无限画布中绘制草稿，并通过对话生成成图" width="46%" />
  <img src="docs/assets/readme/canvas-edit.webp" alt="基于已有结果继续对话修改，在画布中持续迭代创作" width="46%" />
  <br />
  <sub>左：在画布中绘制草稿、摆放参考图，并通过对话生成成图。 · 右：基于已有结果继续对话修改，在画布中持续迭代创作。</sub>
</div>

<br />

### 🎛️ Studio 批量创作

- 支持多张参考图，一次生成多张候选图。
- 自由控制 Provider、模型、比例和清晰度，只保存满意的结果。

<br />

<div align="center">
  <img src="docs/assets/readme/studio-workbench.webp" alt="dsh-image-gen Studio 工作台" width="100%" />
  <br />
  <sub>在同一个 Studio 中完成参考图导入、参数控制、批量生成、结果筛选与保存。</sub>
</div>

<br />

### ⚖️ 多模型横向对比

使用同一组 Prompt 和参考图并发调用多个模型，在一张画布中比较并保存结果。

<br />

<div align="center">
  <img src="docs/assets/readme/multi-model-compare.webp" alt="同一 Prompt 的多模型生成对比" width="100%" />
  <br />
  <sub>在同一画布中比较不同模型结果，再批量保存满意的图片。</sub>
</div>

<br />

### ✨ 500+ Prompt 灵感案例

- 浏览和筛选 **500+ Prompt 案例**，支持收藏、复制及一键带入 Studio。
- 图片缓存在本地，浏览和学习不消耗 Token 或生成额度。

<br />

<div align="center">
  <img src="docs/assets/readme/inspiration-library.webp" alt="Prompt 灵感素材库" width="100%" />
  <br />
  <sub>先找灵感，再把 Prompt 带入工作台；全本地缓存，浏览或复制不消耗生成额度。</sub>
</div>

<br />

### 🖼️ 图库、收藏与批量管理

- 统一管理对话和 Studio 中保存的图片，并按工作区隔离。
- 支持搜索、筛选、收藏、下载、继续编辑、重新生成和批量管理。

<br />

<div align="center">
  <img src="docs/assets/readme/gallery-management.webp" alt="图库筛选、收藏与批量管理" width="100%" />
  <br />
  <sub>图库支持多维度筛选、收藏、批量管理与工作区数据隔离。</sub>
</div>

<br />

### 🧩 本地 ComfyUI 多工作流

灵活调用本地 GPU 算力，让私有化绘图无缝融入 Agent 对话。

- 导入并管理多个命名工作流，支持预设 Prompt 和常用占位符。
- Agent 可按名称选择工作流，在对话中完成文生图和图生图。

> ComfyUI 暂未接入 Studio 和多模型对比。

<br />

<div align="center">
  <img src="docs/assets/readme/comfyui-workflows.webp" alt="ComfyUI 多工作流配置" width="58%" />
  <br />
  <sub>为不同用途维护独立工作流，并通过名称让 Agent 精确选择。</sub>
</div>

<br />

---

## Provider 支持情况

| Provider                          | 对话生图 | 对话编辑 | Studio | 多模型对比 |
| :-------------------------------- | :------: | :------: | :----: | :--------: |
| **Google Gemini**                 |    ✅    | ✅ 多图  |   ✅   |     ✅     |
| **OpenAI Images**                 |    ✅    | ✅ 多图  |   ✅   |     ✅     |
| **OpenAI Compatible（中转站）**   |    ✅    | ✅ 多图  |   ✅   |     ✅     |
| **ByteDance Seedream / 火山方舟** |    ✅    | ✅ 多图  |   ✅   |     ✅     |
| **Aliyun DashScope / Qwen Image** |    ✅    | ✅ 多图  |   ✅   |     ✅     |
| **xAI Grok Imagine**              |    ✅    | ⚠️ 有限  |   ✅   |     ✅     |
| **智谱 GLM-Image**                |    ✅    |    —     |   ✅   |     ✅     |
| **Local ComfyUI**                 |    ✅    | ✅ 单图  |   —    |     —      |
| **ChatGPT 订阅（免 Key）**       |    ✅    | ✅ 多图  |   ✅   |     ✅     |
| **Grok 订阅