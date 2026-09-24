<div align="center">

#  dsh-knowledge

**DSH 的知识库插件**

[**English**](./README.en.md) · [**中文**](./README.md)

[![npm version](https://img.shields.io/npm/v/dsh-knowledge?color=cb3837&logo=npm)](https://www.npmjs.com/package/dsh-knowledge)
[![npm downloads](https://img.shields.io/npm/dm/dsh-knowledge?color=cb3837&logo=npm)](https://www.npmjs.com/package/dsh-knowledge)
[![Node.js >= 22](https://img.shields.io/badge/node.js-%3E%3D22-brightgreen?logo=nodedotjs)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue?logo=typescript)](https://www.typescriptlang.org/)
[![SQLite](https://img.shields.io/badge/SQLite-node%3Asqlite-%23003B57?logo=sqlite)](https://www.sqlite.org/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)

一个深度的**知识库系统**，作为 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）的独立、可开源 bundle 插件。提供知识库（含**分组**）与文档管理、文本分块、向量化（OpenAI 兼容 / Ollama / **本地模型** / 关键词降级）、检索，以及模型可见工具与浏览器管理面板。

<img width="1000" height="667" alt="image" src="https://github.com/user-attachments/assets/8fab3aed-709e-4a59-87fa-c1a52c29c11e" />

</div>

---

## 为什么选择 dsh-knowledge

dsh-knowledge 把文档导入、解析、分块、检索、证据组织和模型续读整合进 DSH。它既可以零向量配置运行，也可以完全使用本地模型，不要求额外部署独立的知识库服务。

| 能力 | 说明 |
|---|---|
| 文档来源 | 文件、目录、网页和文本笔记；本地路径可持续重扫和重新索引 |
| 混合检索 | FTS5 BM25、向量召回、RRF 融合、MMR 去重以及可选重排 |
| 证据上下文 | 按文档顺序动态生成 `ContextWindow`，支持围绕命中位置继续阅读 |
| 本地运行 | 本地 embedding、本地 rerank、本地 OCR；也支持 OpenAI 兼容接口和 Ollama |
| 文档处理 | 常见办公格式、扫描 PDF、PaddleOCR、Tesseract 回退及可选 MinerU |
| 管理界面 | 知识库分组、批量导入、预览、召回测试、模型管理和索引重建 |

---

## 快速开始

### 1. 准备环境

- Node.js：`^22.19.0 || >=24.0.0`
- pnpm：`>=10`
- 已安装并初始化 DeepSeek Harness

在安装插件之前，将以下构建许可**合并到**目标 profile 的 `pnpm-workspace.yaml` 中已有的 `allowBuilds` 映射。不要重复添加第二个 `allowBuilds:` 键，否则 YAML 会失效。这些依赖包含安装期构建；pnpm 10 默认拒绝执行时，`dsh plugin add` 会在登记 bundle 前退出。

```yaml
allowBuilds:
  esbuild: true
  onnxruntime-node: true
  protobufjs: true
  sharp: true
  tesseract.js: false
```

### 2. 安装插件

```bash
dsh plugin --profile <name> add dsh-knowledge
```

插件安装在 profile 层。无论 DSH 来自 npm 还是源码 checkout，都使用同一条命令。安装完成后重启 web 服务，并刷新页面加载管理面板。

### 3. 完成首次配置

1. 点击侧边栏底部、设置旁的“知识库”入口。
2. 新建知识库并导入文件、目录、网页或文本。
3. 如需本地向量检索，在“设置 > 本地模型”下载 embedding 模型；也可以配置 OpenAI 兼容服务或 Ollama。
4. 如需识别扫描件，再下载约 21 MB 的 OCR 模型。
5. 在“召回测试”中检查结果，再让模型通过 `knowledge_search` 使用知识库。

不下载模型也可以使用关键词检索。扫描件 OCR、本地 embedding 和本地 rerank 只有在对应模型已下载并通过就绪检查后才启用。

<details>
<summary>其他安装方式</summary>

```bash
# GitHub Release 或 npm pack 生成的 tarball
dsh plugin --profile <name> add ./dsh-knowledge-0.4.1.tgz

# 本地源码目录，需要先完成构建
dsh plugin --profile <name> add file:/path/to/dsh-knowledge
```

如果第一次安装因 pnpm 构建许可失败，请补全 `allowBuilds` 后重新运行 add。包通常已经进入 `node_modules`，第二次执行会继续完成 bundle 登记。

</details>

<details>
<summary>恢复 <code>ERR_PNPM_WORKSPACE_MANIFEST_WRITER_PARSE</code></summary>

这表示 pnpm 无法解析 DSH profile 自己的 `pnpm-workspace.yaml`，发生在下载或构建本插件之前。先备份文件，再修复错误信息指出的 YAML 行：

- Windows：`%USERPROFILE%\.dsh\profiles\<profile>\pnpm-workspace.yaml`
- macOS / Linux：`~/.dsh/profiles/<profile>/pnpm-workspace.yaml`

不要在不清楚原有设置用途时覆盖该文件。如果 profile 没有其他有意保留的 pnpm 设置，可恢复为以下最小有效配置，再将上方的 `allowBuilds` 合并进去：

```yaml
packages:
  - .

nodeLinker: hoisted
autoInstallPeers: false

allowBuilds:
  esbuild: true
  onnxruntime-node: true
  protobufjs: true
  sharp: true
  tesseract.js: false
```

随后重新执行同一条 `dsh plugin --profile <profile> add ...` 命令。若修复 YAML 后出现 `ERR_PNPM_IGNORED_BUILDS`，这是独立的构建授权问题；仅按 pnpm 输出的确切包名补充授权，不要宽泛地允许所有脚本。

</details>

---

## 核心能力

### 文档与来源管理

- 创建、重命名、分组和删除知识库；侧边栏支持分组折叠和库间移动。
- 从文件、绝对路径、目录、URL 或纯文本导入文档。目录来源保留稳定 ID、类型和原始路径，可重新扫描磁盘变化。
- 批量上传单次最多 20 个文件、单文件最大 22 MB，并使用 5 路后台导入池。
- 同名冲突由服务端统一检测，可选择重命名、替换或取消；内容哈希用于避免重复导入。
- 文档列表展示等待、解析、embedding、完成和失败状态；支持 PDF 原文、文本和完整分块预览。
- 原始文件保存到知识库 raw 存储。不同目录根的同名相对路径互不冲突，失败的替换重建不会破坏上一份已提交内容。

<details>
<summary>支持的文档格式与目录行为</summary>

目录导入递归扫描 `txt`、`md`、`csv`、`html`、`json`、`pdf`、`docx`、`doc`、`pptx`、`ppt`、`xlsx`、`xls`、`epub` 等格式，并在界面中保留可下钻的文件夹树。

重新扫描目录时会导入新增文件、重建已修改文件并移除已不存在的文件。单个文件失败不会隐藏其他成功结果，服务端和界面都会保留逐文件错误信息。

**更新已导入目录的正确方式**：重新导入同一路径，或在界面中对目录容器执行重扫——两者现在走同一条同步路径，都只会原地更新原来那棵树。目录来源以“知识库 + 规范化真实路径”确定身份，所以重复导入不会再新建第二棵树。目录中的文件以“目录来源 + 相对路径”确定身份；只有名称和类型都唯一的旧文件才会被认领，出现两个候选时报告 `ambiguous_source`，不会猜测、合并或自动删除。管理 API 的文档详情会返回目录容器的 `sourcePath`，客户端可据此找到该重扫哪一个容器。

</details>

### 检索与证据链

- 未配置 embedding 时使用 CJK 二元组和拉丁词 BM25；配置向量后可使用 hybrid、vector、lexical 或 auto 模式。
- 混合检索通过 Reciprocal Rank Fusion 合并 BM25 与向量结果，并支持相似度阈值、MMR 多样性和多查询融合。
- 可选远程或本地 cross-encoder 重排。重排失败、超时或返回无效分数时保留原始召回顺序。
- 每个命中动态生成有序的 `ContextWindow`，按 `before → anchor → after` 组织证据，不把桥接文本写入索引或 embedding。
- 自动检索默认开启；它在模型回答前注入高相关证据，同时限制延迟、重复内容和单个知识库占用的上下文份额。
- 召回测试展示来源、相关度、关键词/向量分数、耗时和重排状态，并支持复制引用与重放历史查询。

<details>
<summary>ContextWindow 与自动检索细节</summary>

`SearchHit.text` 始终保留完整 canonical anchor。`contextWindow` 默认不跨标题路径；超长锚点围绕查询命中按句子边界裁剪，相邻 chunk 的重复前后缀会被移除。旧字段 `siblingContext` 在 0.3.x 中继续兼容，但新调用方应优先使用 `contextWindow`。

`knowledge_get_document` 支持普通 `chunkOffset` / `chunkLimit` 分页，也支持通过 `anchorChunkId` 或 `anchorIndex` 进入锚点模式。锚点模式可控制 `before`、`after`、`maxTokens`、`focus` 和 `crossHeading`。

自动检索的首 Token 路径不会启动本地 reranker；远程 rerank 最多调用一次，并共享 4 秒总预算。取消、超时或 provider 故障不会污染注入记忆，也不会把检索范围扩大到无关知识库。

</details>

### 分块、解析与 OCR

- 标题感知分块保留 Markdown 标题路径和代码围栏，并把文档标题与标题路径作为检索上下文。
- `chunkSize` 与 `chunkOverlap` 使用 Token 预算；长文本按标题、代码、段落、句读、列表和换行的优先级寻找断点。
- 可选语义分块会合并相邻的相似段落；可选 Token 上限会继续在句号、逗号或空格附近细分超长块。
- 扫描 PDF、无文本层矢量 PDF、损坏文本层和逐字符排版 PDF 可自动进入整页 OCR 路径。
- PaddleOCR PP-OCRv5 为首选本地识别器，识别失败时回退 Tesseract；1-bit JBIG2/CCITT 扫描件也包含在处理路径中。
- 可选 MinerU 远程处理可将公式、表格和复杂版式恢复为 Markdown；未配置时继续使用本地解析与 OCR。

### 模型与管理界面

- 每个知识库可以覆盖 embedding、rerank、分块、topK、自动检索、冲突策略和文档处理设置；空字段继承全局值。
- embedding 支持 OpenAI 兼容 `/embeddings`、Ollama 和 transformers.js 本地模型。
- 本地模型页面管理 embedding、rerank 和 OCR 模型的下载、重试、删除、进度与健康状态。
- 模型缓存目录支持原生文件夹选择、打开目录和安全迁移，可把较大的本地权重移出系统盘。
- Ollama 页面支持查看、拉取、取消和删除模型；浏览或拉取不会隐式更改当前 embedding 配置。
- 管理面板提供知识库导航、资料表格、批量重建/删除、原文与分块预览、召回测试、全局和每库设置及 Toast 反馈。

<details>
<summary>本地模型运行方式</summary>

默认本地 embedding 模型为 `onnx-community/Qwen3-Embedding-0.6B-ONNX`，约 585 MB、1024 维。它在带版本 IPC 的独立 child process 中运行；空闲时可释放 ONNX session，崩溃或硬超时后只重建干净的子进程，无需重启 DSH。下载使用模型专属 staging 目录，只有隔离加载和真实向量 probe 成功后才会提升到正式缓存，并写入带文件指纹的 readiness marker。

`rerankModel: local:Xenova/bge-reranker-base` 在另一个独立 child process 中运行，与 embedding process 生命周期完全隔离。搜索不会隐式下载 rerank 模型；模型必须先在本地模型页面下载并通过健康检查。自定义 Hugging Face ONNX reranker 属于实验性能力，需要通过单 logit 能力验证和正负样例自检。

本地模型默认缓存在 `<DSH_HOME>/cache/dsh-knowledge/local-models`。下载端点可通过界面的 `hfEndpoint` 或环境变量 `HF_ENDPOINT` 调整；OCR 默认使用 `hf-mirror.com`，海外用户可改为 `https://huggingface.co`。

下载**不与发起它的那一次 HTTP 请求绑定**：请求返回后传输在后台继续，浏览器关闭或客户端超时都**不会**取消下载，进度通过本地模型状态持续上报。要停止下载必须显式调用取消；取消只中止进行中的传输，已完成并通过校验的模型不会被删除（删除请用「删除」）。下载的请求预算按进度重置，因此慢速链路不会被「总时长」误杀，只有**长时间无进度**才会被判为卡死。

</details>

### 模型工具

插件向模型提供 14 个工具。所有读取、写入和自动检索都遵守“已启用知识库”边界；空或失效选择匹配零个知识库，不会静默扩大到全库。永久删除必须经过宿主确认。

<details>
<summary>查看全部工具</summary>

- `knowledge_search`
- `knowledge_list_bases`
- `knowledge_create_base`
- `knowledge_delete_base`
- `knowledge_add_document`
- `knowledge_list_documents`
- `knowledge_delete_document`
- `knowledge_import_url`
- `knowledge_refresh_url`
- `knowledge_stats`
- `knowledge_get_document`
- `knowledge_read_document`
- `knowledge_reindex_document`
- `knowledge_reindex_base`

`knowledge_search` 返回 citations、`chunkIndex` 和有序 `ContextWindow`。`knowledge_read_document` 支持字符区间读取和正则定位，`knowledge_get_document` 支持分页及围绕检索锚点续读。

</details>

### 存储与索引

- 知识库、文档和运行时配置通过 DSH `storageDomain` 持久化。
- 分块保存在独立 SQLite 文件 `<DSH_HOME>/storages/knowledge-chunks.sqlite`，可通过 `chunkStorePath` 调整。
- 词法检索使用 SQLite FTS5 trigram 索引；向量使用 Float32Array 常驻缓存并精确失效。
- 旧 JSON 分块数据在首次启动时执行幂等迁移；没有存储后端时自动退化为内存模式。
- 修改分块或 embedding 配置后，可以重建单条资料或整个知识库的索引。

---

## v0.4.1 更新重点

- **MinerU 失败的导入不再走进死路**（issue #30）：MinerU 提取失败、退回本地解析也失败时，文档会留下一条只有原始 PDF、没有正文和分块的占位行，点「重建」只会报 `has no source text to reindex`，从界面和 API 都无法脱困。现在导入、单文档重建与启动恢复走同一条提取链，重建会重新尝试 MinerU；双重失败时同时报出 MinerU 与本地解析两个原因，而不是只把 MinerU 的真实原因写进日志。
- **关闭 0.4.0 审计