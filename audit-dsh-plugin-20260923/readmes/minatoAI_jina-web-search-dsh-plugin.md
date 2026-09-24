[English](README.en.md) | **简体中文**

# dsh-jina

DeepSeek Harness 的 [Jina AI](https://jina.ai/) 插件（bundle）：把 jina-cli 的全部 API 能力以模型工具的形式装进 dsh，并在 Web 的 **Plugins** 侧边栏页（`dsh-jina` bundle 卡片）提供配置表单来设置**多个 API key（额度耗尽自动切换）**与**本地代理地址**；旧版 harness 上则回落到 **设置 → 插件 → 配置** 的同名卡片。

## 更新日志

> 此处仅展示最新版本，完整版本历史见 [change-log.md](./change-log.md)。

### 0.10.0（2026-09-24）

- **feat** **新增 `jina_read_pdf`：`jina-ocr-v1` 只归 PDF 专用工具**。起因是一次实测事故：`jina-ocr-v1` 一次只吃**一张页面图**，而 Reader 会把整个网页渲染成**一张**图再交给模型——长 HTML 页被压进 1024×1024 的全局视图后文字糊到读不出来，模型就"续写"出**假论文**（同一篇 arXiv 论文：HTML 版返回伪造的"遗传算法测试用例"论文，PDF 版逐页读完全正确）。所以 OCR 不再是一个全局开关，而是**只属于 PDF 的专用工具**：固定 `X-Respond-With: jina-ocr-v1`、**逐页**请求（`X-Page`）、默认前 5 页（`maxPages`，硬上限 50）、`pages` 支持 `"3"` / `"1-5"` / `"2,4,7"`。
- **feat** **自动识别文档结尾**：实测**超出页数的 `X-Page` 不报错，而是静默返回第 1 页**（"循环到空为止"会死循环）。工具改为逐页指纹去重：某页重复了之前的页 ⇒ 判定读到末尾并停止，结果里写明原因。
- **feat** **结果自带来源标记**：模型管线（`jina-ocr-v1` / `readerlm-v2`）的输出**是生成的，不是抽取的**，结果末尾会追加 `[Reader pipeline: … verify anything load-bearing against the source.]`——最便宜的一道防线。
- **feat** **默认管线从 OCR 换成 ReaderLM-v2**：卡片选项 `useOcr` → **`useReaderLm`**（「使用 ReaderLM-v2 解析 HTML」），走官方为**网页**指定的 `X-Respond-With: readerlm-v2`（实测同一页：OCR 返回伪造论文，ReaderLM-v2 返回**正确全文**，计费 **3×** 且有 4000 token 起步，OCR 是 40×）。旧设置里的 `useOcr` 被忽略。
- **fix** **ReaderLM-v2 不再携带选择器组**：实测 `readerlm-v2` **叠加** `X-Target-Selector` 时，只要选择器命中不到就返回 **422 `No content available`**；去掉即恢复。模型管线消费整页，选择器只属于 DOM 抽取路径。
- **fix** **`.pdf` 不会被 ReaderLM 接管**：`jina_read` 识别出 PDF 后保持普通抽取（逐字、比 OCR 便宜约 40×），并在结果里提示"要读扫描件请用 `jina_read_pdf`"。
- **fix** **422 按报文分流**：`Screenshot of the page is not available` = **渲染失败**（正是 OCR 会伪造内容的那一步）、`with target selector …` = 选择器命中不到、`No content available` = 抽不到内容，三者给不同修复提示；503 补上官方说明——模型是 serverless，**冷启动返回 503，建议 30–60 秒后重试**。
- **change** **API key 池改为均流（round-robin）轮换**：原先"粘性优先"（上次成功的 key 一直领跑），现在**每次调用都从上一个用过的 key 的下一个开始**，N 个 key 各摊约 1/N 流量——Jina 限流按 key 计，摊开才少撞 429。冷却中的 key 依旧跳过；**只有真正失败导致的换 key 才显示 `[已自动切换 API key：…]`**，计划内轮换不冒充"key 用完了"。
- **test** 全套 **169 例：168 通过 / 1 例（`JINA_LIVE_PROXY`）按需跳过 / 0 失败**；并做**真机端到端验证**（真实 API + 真实 subprocess）：`jina_read_pdf` 对 1 页 PDF 请求 1–3 页 → 只读 1 页后以"page 2 repeated page 1"停止并标注来源；`jina_read` + readerlm 正常返回。

## 功能

安装后所有会话（所有 agent preset）都会获得 13 个 `jina_*` 工具：

| 工具 | 对应 jina-cli 命令 | 说明 |
| --- | --- | --- |
| `jina_web_search` | `jina search` | 通用网页搜索（默认 web 域；images / blog 域，支持时间过滤与地区/语言提示） |
| `jina_search_arxiv` | `jina search --arxiv` | arXiv 预印本检索（CS / ML / 数学 / 物理等，返回 arxiv.org 官方论文直链） |
| `jina_search_ssrn` | `jina search --ssrn` | SSRN 论文检索（经济 / 金融 / 法律 / 管理等社会科学，返回 papers.ssrn.com 直链） |
| `jina_read` | `jina read` | 把网页读成干净的 markdown；可选 `readerlm` 走 ReaderLM-v2（官方为网页指定的 HTML→Markdown 模型），支持正文选择器与噪声过滤（见下节）。**PDF 一律走普通抽取**——逐字，且比 OCR 便宜约 40× |
| `jina_read_pdf` | `jina read` + `X-Respond-With: jina-ocr-v1` | **专门用 `jina-ocr-v1` 逐页读 PDF**：扫描件 / 图片型 PDF 唯一可用的路径。`pages` 选页（`"3"` / `"1-5"` / `"2,4,7"`），默认前 5 页（`maxPages`，上限 50）。**一次一页**（API 对超出页数的 `X-Page` 会静默返回第 1 页，工具据此判定文档结尾）；结果自带来源标记 |
| `jina_screenshot` | `jina screenshot` | 网页截图，返回托管图片 URL（支持整页截图） |
| `jina_datetime` | `jina datetime` | 推测网页的发布/更新时间 |
| `jina_expand` | `jina expand` | 把搜索词扩展成一组相关查询 |
| `jina_embed` | `jina embed` | 文本向量化（默认 jina-embeddings-v5-text-small） |
| `jina_rerank` | `jina rerank` | 按相关性重排文档（默认 jina-reranker-v3.5） |
| `jina_classify` | `jina classify` | 文本分类 |
| `jina_pdf` | `jina pdf` | 从 PDF 提取图表/公式（支持 arXiv ID） |
| `jina_primer` | `jina primer` | 获取当前上下文：主机时钟（ISO 时间/unix/时区/UTC 偏移）、网络事实（公网 IP 与位置，尽力而为）与 Jina 账户状态（身份/余额） |

## 阅读工具选项（`jina_read`）

卡片里的「阅读工具选项」区块（也可直接改 `settings.yaml` 的 `jina-tools` 段）决定 `jina_read` 的默认行为；每个选项都能被同名调用参数**单次覆盖**。

| 选项 | 字段 | 默认 | 作用与代价 |
| --- | --- | --- | --- |
| ReaderLM-v2 解析 HTML | `useReaderLm` | 关 | 走 `X-Respond-With: readerlm-v2`：官方为**网页**指定的 HTML→Markdown 模型，适合普通抽取器处理不好的页面。**约 3× token** 且有 **4000 token 起步**，**必须有 API key**——官方对匿名请求返回 401，本插件因此直接不发请求并给出提示。**`.pdf` 会自动跳过它**（PDF 交给普通抽取，扫描件交给 `jina_read_pdf`） |
| 图片保留策略 | `imagePolicy` | `all` | `all` = 官方默认；`alt` = 只保留 alt 文本（省 token）；`none` = 不保留图片 |
| 生成图片 alt 文本 | `autoAltText` | 关 | `X-With-Generated-Alt`：为缺说明的图片生成描述。**需 API key**（匿名 401），且**与 OCR 互斥**（指定 `X-Respond-With` 时该功能不生效）；又因为**带 key 的请求会计费**，默认关闭，需要时显式打开 |
| 选择器组 | `useSelectors` | 开 | 默认发保守的 `X-Target-Selector`（只含 `article` / `main` / `[role="main"]` / `.markdown-body` 等正文容器）与 `X-Remove-Selector`（页眉页脚、导航、cookie 横幅、广告、侧栏、评论等）。命中不到时**自动回退整页重试**，不会返回空 |
| 正文 / 排除选择器 | `targetSelector` / `removeSelector` | 空 = 内置列表 | 覆盖内置选择器（站点结构特殊、默认列表误伤时用） |

每次 `jina_read` 还会固定发送三个零副作用参数：`X-Preset: agent`（官方为 AI agent 预调的预设；官方文档明确 preset **只填充调用方未显式设置的选项**，所以不会覆盖任何显式参数）、`X-Base: final`（用重定向后的最终 URL 解析相对链接）、`X-Timeout: 120`（与客户端自己的 120s 上限对齐——若发官方的上限 180，客户端会先超时并报自己的错误，多出来的耐心是浪费的；要改就两边一起改）。

调用级参数（`jina_read`）：`readerlm`、`targetSelector`、`waitForSelector`、`removeSelector`、`noCache`，以及原有的 `links` / `images` / `json` / `apiKey`。
调用级参数（`jina_read_pdf`）：`url`、`pages`、`maxPages`、`allowNonPdf`、`apiKey`。非 `.pdf` 的 URL 会被拒绝（`allowNonPdf: true` 可强制放行）——因为 `jina-ocr-v1` 在普通网页上会**编造内容**。

> 关于"为什么默认这样"：这三项是官方 Reader API 里**最坏情况不损失什么**的参数；而 ReaderLM-v2 与 alt 生成需要 key、会计费或与其它参数互斥，所以一律默认关闭。`X-Remove-Overlay` / `X-Detach-Invisibles` 这两个未在官方参数面板文档化的隐藏参数**没有**被默认启用（后者官方明确要求 browser 引擎且禁用缓存）。

## 效果实测（与内置 web_search 交叉对比）

为了让模型**不用记住参数**就能用对检索域，学术检索单独拆成了 `jina_search_arxiv` / `jina_search_ssrn` 两个专用工具（对应 `jina search --arxiv` / `--ssrn`）——工具名即用途，模型看到用户要论文会直接调用它们。以下为 2026-08-13 在同机真实网络环境（VPN 系统代理）下的抽样对比：同一查询分别调用本插件与 dsh 内置 `web_search`，人工核对结果。

| 场景 | 本插件（dsh-jina） | 内置 web_search | 结论 |
| --- | --- | --- | --- |
| 学术检索（arXiv） | `jina_search_arxiv`「retrieval augmented generation survey」→ **9/9 全部为 arxiv.org 官方直链**：2312.10997（RAG 经典综述）、2506.00054、2410.12837、2501.09136（Agentic RAG）、2405.07437、2504.08748 等，篇篇主题契合、摘要准确 | 同查询返回 arXiv **镜像站**（ezproxy.obspm.fr、ar5iv、sinoxiv.napstic.cn）与 BibTeX 链接，官方直链缺失 | ✅ jina 胜：官方直链 + 精准召回 |
| 学术检索（SSRN） | `jina_search_ssrn`「large language models financial markets」→ **9/9 全部为 papers.ssrn.com 原文**：市场情绪预测、LLM 模拟交易、AI 羊群效应、投资者分歧等，契合度极高 | 无 SSRN 专用检索能力 | ✅ jina 胜：独占 SSRN 域 |
| 中文新闻 / 社区 / 官方源 | `jina_web_search` 官方源（政府 / 公司官网）置顶，可加 `time` 过滤时效 | 同查询结果相关，但官方源不置顶 | ✅ jina 优：权威源优先 + 时效过滤 |
| 泛学术检索（未指定域） | 默认 web 域对 Springer / IEEE / ACL 等覆盖面一般（学术检索请改用上面的专用工具） | Springer / IEEE / ACL 覆盖面广 | ✅ web_search 优：泛学术检索用它 |

**结论与分工用法**：学术论文 → `jina_search_arxiv` / `jina_search_ssrn`；中文时效新闻 → `jina_web_search`（+ `time`）；泛学术 / 工程文档 → 内置 `web_search`。两者互补，覆盖全部检索场景。

> 注：上表为单轮抽样对比（非严格 benchmark），结果受当天网络与查询选择影响；两个工具链均真实可用，结论供选型参考。

## 安装

仓库地址：https://github.com/minatoAI/jina-web-search-dsh-plugin

插件按 [bundle](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/user/develop/basic/publish.md) 方式分发，用 `dsh plugin` 安装进 profile（从源码 checkout 运行时用 `pnpm dsh` 代替 `dsh`）：


> 从 GitHub 安装（本项目无 build 脚本，无需 allowBuilds 授权）

```sh
dsh plugin --profile web add github:minatoAI/jina-web-search-dsh-plugin
```

> 更稳妥：固定到某个 commit，避免后续推送改变实际安装到的代码

```sh
dsh plugin --profile web add github:minatoAI/jina-web-search-dsh-plugin#<commit-sha>
```

> 或本地文件夹安装（开发调试用）

```sh
dsh plugin --profile web add ./jina-dsh-plugin
```

安装完成后**重启** dsh（新 bundle 在下次启动时生效）：

```sh
dsh --profile web
```

然后打开 Web 界面 → 设置 → **插件** → **配置** 选项卡 → 展开 **Jina Tools** 卡片 → 在 **API key** 区块里粘贴 key → 点「添加」。可以**一直往里加**：每次点「添加」都会保存一个新 key，卡片不显示也不需要管理任何单个 key。免费 key 在 https://jina.ai/ 获取。**建议至少加两个**：任一 key 失效或额度耗尽时插件会自动丢弃它并切换到下一个，任务不会中途断掉（见下节）。

## 更新

插件是 profile 的一个依赖，升级 = **让 profile 重新拉取远端代码 + 重启 dsh**。以 `web` profile 为例：

1. 让 profile 拿到新版本（三选一）：

   ```sh
   # A. 命令行：重新解析 GitHub 依赖（推荐）
   cd "$DSH_HOME/profiles/web"        # Windows: C:\Users\<你>\.dsh\profiles\web
   pnpm update dsh-jina

   # B. 命令行：先卸载再安装（与 A 等效，会重新拉取分支最新 commit）
   dsh plugin --profile web remove dsh-jina
   dsh plugin --profile web add github:minatoAI/jina-web-search-dsh-plugin

   # C. Web 界面：侧边栏「插件」页 → 卸载 dsh-jina → 用上面的 GitHub 地址重新安装
   ```

2. **重启** dsh 让新代码生效：

   ```sh
   dsh --profile web
   ```

3. 核对是否更新成功：

   ```sh
   