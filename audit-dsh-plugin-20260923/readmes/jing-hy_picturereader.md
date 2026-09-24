# picturereader

> **v3.4.0** — 给纯文本模型（DeepSeek / text-only）的全能「看图 / 读文档 / 修图」能力。
> 融合 **视觉孪生 adapter**（把任意文本模型原位包装成「支持图片」→ DSH 原生缩略图 + 图片块自动分析）、**三模式路由**、**本地像素级工具链**（scan / OCR×4 引擎 / crop / palette / compare / batch）、**文档转图片**（pdf / word / excel / ppt）、**本地修图工具 `image_edit`**（Pillow/OpenCV 纯 CPU：缩放 / 旋转 / 滤镜 / 合成 / 水印 / 去背景 / 超分等）与**可选外部 VLM 桥**。一个插件全包。
>
> **v3.4.0 新增**：**原生识图能力感知**。插件现在从**模型能力元数据**（`inputModalities`，与 DSH 内核的图片门控同源）判断当前会话的模型是否**自己就能看图**：命中时在系统提示词里明确说明「**不要**用 `image_scan` / `image_sample` 这类"伪多模态"替代路径，**但 `image_ocr` 仍应正常使用**」，并让粘贴/读取的图片**直通**该模型、不再降级成文本引导；纯文本模型与元数据缺失（未知）时行为与 v3.3.3 完全一致。判定走**未包装的原始 adapter**，因此不会被本插件自己的视觉孪生误判成原生识图。
>
> **v3.3.0 新增**：**macOS 原生 Vision OCR 引擎**（`engine="macos"`，`scripts/setup-macos.mjs` 一键编译，PR #4 合入）；OCR 引擎选项按平台条件显示（macos 仅 macOS、windows 仅 Windows，paddle/rapid 跨平台始终显示）；修复 PaddleOCR 新环境首次调用三个缺陷（stdout 污染 / w/h→width/height / 缓存路径写死，issue #2）；设置卡 UI 重做（settings-panel 设计语言）；调试日志门控（llm/stream 桥不再刷屏）；peerDependencies 兼容 DSH 0.1.1-rc.2（issue #3）。

[![dsh-plugin](https://awesome-dsh-plugin.com/badge.svg)](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) [![dsh.so security](https://www.dsh.so/badge/picturereader.svg)](https://www.dsh.so/artifact/picturereader) [![dsh.so install](https://www.dsh.so/badge/install/picturereader.svg)](https://www.dsh.so/artifact/picturereader)

---

## 定位

DeepSeek 等纯文本模型没有视觉编码器，无法直接看图片；DSH 原生缩略图也需要模型被声明为「支持图片」才会渲染。

> ⭐ **已支持外部视觉 API（OpenAI 兼容端点 / LM Studio / 云端 VLM），由 LLM 自行按需调用**：配置好端点后，模型会在智能/严谨模式下自主判断"这张图值不值得外呼视觉模型"，需要时用 `vision_analyze` 调外部 API 做语义理解，简单内容则本地像素/OCR 搞定——**外部 API 是即插即用的增强能力，不是必须依赖**。

picturereader 现在解决三件事：

1. **把「看图/读文档」翻译成纯文本模型能理解的结构化证据**（像素级 hue/结构/材质分析 + OCR 实读 + 可选 VLM 语义描述），并沉淀为读图方法论 skill。
2. **通过「视觉孪生 adapter」让纯文本模型在 DSH 里获得原生缩略图体验**：勾选模型即生成「(视觉)」变体，粘贴图片显示原生缩略图、图片块进会话、并被自动分析成文本路径 + 本地证据再交给模型。即使上游先降级为 `attachment sha256` 文本，图片桥也会仅从本机附件对象库恢复经过文件头校验的图片并注入本地工具路径；模型拿到的永远是纯文本，不会触发 `UNSUPPORTED_CONTENT`。
3. **本地直接修图 / 批量处理图片**：`image_edit` 提供缩放、旋转、滤镜、合成、水印、去背景、拼接、透视校正等纯 CPU 动作，图片不出本机。

> **版本兼容性**：本版本专门兼容 **dsh 0.1.3-alpha.1 / dsheac 5.4.0**，同时向后兼容 **dsh 0.1.1-rc.2** 与 **dsheac 5.1.0**，以及 DeepSeek Harness EAC 4.2.0 与 `@deepseek-ai/dsh-client-ui-workspace` rc.7。`peerDependencies` 采用 `^0.1.0-rc.6 || ^0.1.1-rc.2 || ^0.1.3-alpha.1` 联合区间，覆盖三条 0.1.x 发布线。
>
> ⚠️ **升级到 dsh 0.1.3 必须使用 v3.3.2 之后的版本**：内核 0.1.3 起 `@deepseek-ai/dsh-settings` 不再导出 `settingsNamespace()` 品牌函数（命名空间校验收进 `register()` 内部）。ESM 静态导入不存在的符号会让模块**整体加载失败**，进而拖垮整棵插件树、触发 EAC 的 guard 安全模式（表现为「一对话就报错」+ 插件大范围消失）。v3.3.3 已适配。

> 🚀 **后续将作为 DeepSeek Harness EAC 的内置视觉插件**：本插件计划替换内置的 `dsh-tool-vision`，随 DSH EAC 桌面版直接捆绑发布，开箱即用。作为独立包发布的目的，是让非 EAC / 旧版用户也能通过 `dsh plugin add picturereader` 或 Git/npm 安装获得同等「看图 / 读文档」能力。

## 功能总览

### ① 视觉孪生 adapter（原生缩略图 + 自动分析）

- **Proxy 原位包装**：对被勾选的模型所属 provider，用 `Proxy` 把其 adapter 包装成「孪生」并原位替换（`registerTwinAdapters`，卸载经 `ctx.effect` 还原），不重复注册。
- **`listModels` / `resolveModel`**：对被勾选模型声明 `inputModalities: ['text','image']`、名称加「(视觉)」后缀 → DSH 认为它支持图片 → **原生缩略图渲染、图片块进会话、粘贴准入**全部解锁。
- **`stream` 拦截**：捕获请求里的 `image` block → 导出到 `~/.dsh/picturereader-vision/images/` → 替换成文本路径 + 本地工具链引导 → 转发给原始 adapter。**pi-ai 收到的是纯文本，不会报 `UNSUPPORTED_CONTENT`**；`opencode-go` 等走 `@earendil-works/pi-ai` 的 provider 同样经此孪生获得原生缩略图能力。
- 隐私模式下分析只走本地工具，绝不外发。

### ② 智能路由（隐私 / 智能 / 严谨 三模式）

**这是 picturereader 的"大脑"**：统一在 `routing.js` + `runtime.js` 收敛「什么时候走外部 VLM、什么时候只用本地、要不要交叉验证」，供各工具 / 图片桥 / 视觉孪生 `stream` / `vision_analyze` 共享，保证整条图链都遵守同一套路由策略。

#### 路由决策原理

每次看图，模型面对的问题其实是同一个：「这张图，值得花什么成本、用哪条路线读懂它？」picturereader 把答案预置成三种策略，模型据此自主决策，同时 host 侧做硬约束兜底：

```
图片进来 → 孪生 stream 拦截 / 工具被调用
        → 读入当前「模式」→ 得到该模式的路由策略
        → 模型 / 工具按策略选路线：
            本地像素分析（image_scan / image_sample）
            本地文字识别（image_ocr：windows / macos / paddle / rapid）
            外部语义理解（vision_analyze include_vlm=true → VLM）
            交叉验证（多路证据对照）
```

核心决策函数 `visionAnalyzeDefaults(mode)` 定义各模式"默认的证据组合"：

| 模式 | 默认 include_scan | 默认 include_ocr | 默认 include_vlm | allow_low_info |
|---|---|---|---|---|
| **隐私（privacy）** | ✅ | ✅ | ❌（硬禁） | ❌ |
| **智能（smart）** | ✅ | ❌（按需） | ✅（值得才调） | ❌ |
| **严谨（strict）** | ✅ | ✅ | ✅ | ❌ |

#### 三种模式的路线策略

**🕶 隐私模式（Privacy）——零外呼硬门禁**
- **绝不调用**任何外部视觉端点，即使你在设置卡配了 API。
- 约束是 host 侧强制：`runtime.js` 使 `isVlmConfigured()` 恒为 `false`，`vision_analyze` 强制 `include_vlm=false`，视觉孪生 `stream` 的降级文本也明确"只用本地工具"。
- 模型只能用本地工具：`image_scan` / `image_ocr` / `image_sample` / `image_crop` / `image_palette` / `image_compare` / `image_edit`。图片字节不出本机。
- 适用：敏感图片（身份证、合同、私人截图）、离线、零外部流量审计场景。

**⚡ 智能模式（Smart）——省轮数、省时间（默认）**
- 目标：**先把成本压到最低，复杂内容才值得外呼**。
- 决策流程：先 `image_scan` 快速看整体 → 自行判断：
  1. 图片以文字为主 → `image_ocr` 读文字即可，**不必调 VLM**；
  2. 普通图表 / 界面 / 简单内容 → `image_scan` + `image_sample` 自己看就能说清，**不必调 VLM**；
  3. 仅当内容复杂、需语义理解（照片、抽象画面）**且配置了端点**时，才 `vision_analyze(include_vlm=true)` 走外部 VLM。
- 视觉孪生死活都会先把图片导出成本地路径，模型可随时本地深挖，不会被困在"必须外呼"的死路。

**🎯 严谨模式（Strict）——交叉验证、细看细节**
- 目标：**可靠性优先**，不贪省。
- 决策：先 `image_scan` 了解整体 → 必要时 `image_ocr` 读文字、`image_sample` 细看细节 → 对关键判断做**交叉验证**（把像素证据、OCR 证据、（可选）VLM 语义描述相互对照，不轻信单一来源）。
- 允许使用外部 VLM（需配置），但强度更高、可追溯。
- 适用：需要高准确率与可复现结论的场景（审图、校对、数据分析）。

> **隐私硬门禁贯穿所有入口**：无论走哪个工具/桥，`runtime.js` 的模式快照都会在调用点做校验，`routePolicyText(mode)` 还会把当前策略注入给模型的提示里，双保险。

#### 与视觉孪生 adapter 的协同

三模式不仅约束 `vision_analyze`，也约束视觉孪生 `registerTwinAdapters` 的 `stream` 拦截：图片块总是被**无条件**替换成文本（路径 + 本地证据引导，这是模型能读懂的前提），但**是否/何时进一步外呼 VLM** 由当前模式决定——隐私模式恒不透传图片、不发起外部调用；智能/严谨模式在需要且已配置时才走外部语义理解。因此"原生缩略图"与"隐私零外呼"可以同时成立，互不冲突。

### ③ 本地工具链（纯本地读取）

| 工具 | 作用 |
|---|---|
| `image_scan` | 全局/区域扫描：颜色网格 + regions 色块 + shade diversity + texture + structure + hue families；支持 `focus`/`region`/`px_per_cell` 定向放大 |
| `image_ocr` | 文字识别**四引擎**：`windows`（内置）/ `macos`（macOS 原生 Vision，免装第三方，首次一条命令编译）/ `paddle`（选装，发光/弯曲/游戏字更强）/ `rapid`（选装，轻量快速）；paddle/rapid 缺失自动降级不崩溃 |
| `image_sample` | N×N 精确像素取样，判断材质/纹理 |
| `image_crop` | 按 region 裁剪并导出 PNG |
| `image_palette` | 颜色提取：主色列表（hex + 命名单 + 占比）+ 色相家族 |
| `image_compare` | 两图/两区域像素对比：mean_diff / diff_ratio / diff_box / verdict，可选差异可视化预览 |
| `image_batch` | 批量规模/上下文验证：批量扫描 + 类型判定 + 自动全量 OCR + 是否值得深入建议 |
| `vision_analyze` | 统一入口：低信息拦截 + 可选像素扫描 / OCR / VLM，按模式路由，返回多路证据 |

> **OCR 引擎平台说明**：`windows` 引擎仅在 Windows 平台可用、`macos` 引擎仅在 macOS 平台可用（设置卡按平台条件显示对应选项）；`paddle` / `rapid` 为跨平台选装引擎，任何平台都可使用。未配置时默认跟随当前平台原生引擎（Windows→windows、macOS→macos、其他→paddle），跨平台迁移的旧配置会自动回落到平台默认值。

### ④ 文档转图片 `document_to_image`

把 **pdf / docx / doc / xlsx / xls / pptx / ppt** 逐页转成 PNG（LibreOffice headless → PDF → PyMuPDF），供模型逐页 OCR / 扫描分析。纯本地、零网络；支持 `dpi` / `max_pages` / `out_dir` / 批量 `file_paths`。

### ⑤ 外部 VLM 桥（已支持，由 LLM 自行调用）

**已支持外部视觉 API，且调用时机完全交给 LLM 自主判断**：配置好 OpenAI 兼容端点后（LM Studio / llama-server / 云端网关 / GLM-4V-Flash 免费模型），模型在**智能 / 严谨模式**下会自行判断"这张图是否值得外呼视觉模型"——简单内容用本地像素/OCR 就够，复杂内容（照片、抽象画面、需语义理解）才通过 `vision_analyze(include_vlm=true)` 调 `sendVisionRequest` 以 data URI 送图给外部 VLM，取回语义描述。**baseURL 自动补 `/v1/chat/completions`**（无需手写完整路径）。

- LLM 自行调用 = 你不用手动切模型/手动发图，模型按模式策略在该外呼时自己调外部 API。
- 隐私模式仍为硬门禁：即使配置了外部 API 也绝不调用、绝不外发图片字节。

### ⑥ 设置卡片「图片阅读」

Web 设置页注册「图片阅读」卡片（settings-panel 设计语言：卡片分组 + 胶囊按钮 + 折叠高级项）：使用模式、外部视觉 API、视觉桥模型多选、OCR 引擎（平台条件显示）、高级设置（详见「设置卡字段」）。改动写 `~/.dsh/settings.yaml` 即时生效。

### ⑦ 粘贴即用 + 缩略图

开启视觉孪生并选择「(视觉)」模型变体后：粘贴/拖入图片 → 原生缩略图 → 图片块进会话 → 被孪生 `stream` 拦截 → 导出文本路径 + 本地证据 → 纯文本模型拿到结果，可继续用 `image_scan` / `image_ocr` 深挖。

### ⑨ 原生识图能力感知（v3.4.0）

**给"自己就能看图"的模型让路**：picturereader 的本地工具链是为**没有视觉编码器**的模型准备的替代路径，而原生多模态模型用它们只会更慢更不准。插件因此从底层元数据判断能力，并据此调整提示词与图片链路。

- **判定与内核同源**：读 `llm` 适配器的 `inputModalities`（`'text' | 'image'`），三态语义与内核一致 —— 显式含 `image` = **原生识图**；显式不含 = **纯文本**（negative capability）；字段缺失 = **未知**（不注入、不改变行为，零回归）。
- **提示词注入**：以 `ctx.systemPrompt.section()` 注册动态 section（name `picturereader:image-capability`，order `3000`）。原生识图时注入：**不建议**用 `image_scan` / `image_sample` 这些把图片降采样成像素网格的替代手段（信息损失大、易把结论建立在残缺数据上），**`image_ocr` 仍应正常使用**（原生视觉对小字／发光字／艺术字会幻觉，文字以 OCR 实读为准），`image-reading` skill 的 5 步扫描流程也不必遵循。
- **图片直通**：判定为原生识图（或命中 `multimodal_models` 白名单）时，`llm/stream` 图片桥**不再降级**图片块，粘贴的图直达模型；`read_image` 返回的图片块同样不再被替换成文本说