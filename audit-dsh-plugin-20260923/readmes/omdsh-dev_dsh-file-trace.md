# @dsh-external/dsh-file-trace


> 兼容 DSH `dsh-v0.1.2-alpha.3`（typecheck/build + 87 单测全绿，实机验证；本插件基于 alpha.1+ 编写，rc.2 下无可用版本）
DSH Web UI 文件追踪插件：像 Codex / Claude Code 一样**记录并查看模型读取、写入、编辑的每一个文件**。会话标题栏工具区出现「文件追踪」按钮（带操作数徽标），点击打开浮动窗口，按文件分组列出全部操作，点选任意操作查看带行号的内容或**逐行 diff**。零核心改动，纯浏览器 half 插件。

[English](./README.en.md) | **简体中文**

> **你的 DSH 版本决定装哪个插件版本**（装错会崩：常见症状 `useConversation is not a function`）
> - DSH **0.1.1-rc.2**：本插件按 **alpha.x** 编写，rc.2 下**无可用版本**
> - DSH **0.1.2-alpha.1 / alpha.2 / alpha.3 / alpha.4 / alpha.5 / rc.1**：装**新版**（下方默认命令）
## 安装（profile 模式）

```sh
# 方式一：git 依赖固定 tag（公开镜像，推荐；也可用 github:lhh010/dsh-file-trace）
dsh plugin --profile web add '@dsh-external/dsh-file-trace@github:lhh010/dsh-file-trace#v0.3.12'

# 方式二：本地 link（开发；克隆的仓库构建产物已入库，改源码后需 pnpm run build）
git clone https://github.com/lhh010/dsh-file-trace.git
cd dsh-file-trace && pnpm install
dsh plugin --profile web add link:/path/to/dsh-file-trace
```

配置行（`$DSH_HOME/profiles/web/cordis.patch.yml`，热重载，无需重启）：

```yaml
- insert:
    - id: dsh-file-trace
      name: '@dsh-external/dsh-file-trace'
```

> **安装提示**：pnpm 11 首次安装可能拦截 node-pty 等构建脚本——在 `~/.dsh/profiles/web` 下执行 `pnpm approve-builds --all` 放行后重跑安装命令；装完**硬刷新浏览器**（Ctrl/Cmd+Shift+R）。

## 智能版本门控更新提示 / DSH-gated update chip

更新浮标会结合**当前运行的 DSH 版本**（宿主端从 dsh 安装清单读取）与仓库根的 [`compatibility.json`](compatibility.json)（版本→支持的 DSH 列表，精确匹配）判定提示形态：

- 最新版支持当前 DSH → 正常「新版本 vX 可用，点击更新」；
- 最新版需要更高 DSH、但存在支持当前 DSH 的中间新版 → 提示更新到中间版，并注明「另有 vX 需更高 DSH」；
- 最新版需要更高 DSH、且当前 DSH 无任何可用新版 → 琥珀色信息条：「新版本 vX 支持更高 DSH 版本，当前 DSH vY 暂不可用」，不提供直接升级。

兼容数据拉取失败或无该版本条目时，自动回退为旧的普通升级提示（离线安全）。**发版时需同步维护 `compatibility.json`**（与版本表/变更记录同一步骤新增一行）。

### 提示词安装（让 DSH 自己装）

把下面这段提示词发给任意一个 DSH 会话，模型会替你完成安装：

> 帮我安装 dsh-file-trace 插件（DSH 文件追踪：记录并查看模型读写编辑的文件与 diff），步骤：
> 1. 执行 `dsh plugin --profile web add '@dsh-external/dsh-file-trace@github:lhh010/dsh-file-trace#v0.3.12'`（首次可能被 pnpm 11 拦截 node-pty 构建脚本而失败）
> 2. 在 `~/.dsh/profiles/web` 下执行 `pnpm approve-builds --all`（放行构建脚本）
> 3. 再执行一次第 1 步的安装命令
> 4. 完成后在 `~/.dsh/profiles/web/cordis.patch.yml` 追加 - insert 插件行（id: dsh-file-trace，name: '@dsh-external/dsh-file-trace'），并提醒我硬刷新浏览器（Ctrl/Cmd+Shift+R）
> 遇到报错先查 https://github.com/lhh010/dsh-file-trace README 的已知限制。

## 功能

- **操作记录**：提取模型对文件的读取 / 写入 / 编辑，含执行中、出错标记、时间与载荷大小（递归覆盖 run_code 等宿主工具的子调用）。
- **读取视图**：显示被读取文件的**真实内容与真实行号**（剥掉 DSH 读工具响应外壳）。
- **Markdown 阅读模式 + Mermaid**：`.md / .markdown / .mdx` 文件的操作视图头部出现「阅读 / 原文」切换按钮（读取 / 写入 / 编辑三种操作均有）；阅读模式以 **Obsidian 风格**渲染完整文档——多级标题、表格（含对齐）、分割线、加粗/斜体/加粗斜体、删除线、高亮 `==`、行内代码、代码块、引用、有序/无序列表与任务清单、链接、`[[Wiki 链接]]`；图片按 URL 渲染，本地路径图片与非图片附件统一显示为带文件名的文件徽标；YAML frontmatter 显示为代码块。编辑操作优先用窗口内已知的前置内容重建变更后的完整文档。
- **Mermaid 图渲染（懒加载 + 安全清洗 + 缩放）**：阅读模式下 ```mermaid 围栏按需从宿主 `/dsh-file-trace/resources` 懒加载 mermaid chunk（单文件打包）渲染成图；`securityLevel: strict` + `htmlLabels: false` 之上再经**零依赖 SVG 白名单清洗**（剥离 foreignObject/script/事件属性/全部链接）才注入 DOM；**点击图打开全屏缩放**（滚轮缩放/拖拽平移/±0 键盘/双击遮罩或 Esc 关闭）；加载失败或离线时自动回退为原样代码块。
- **数学公式渲染（KaTeX，懒加载）**：阅读模式下 `$$...$$` 块公式与 `$...$` 行内公式按需从宿主 `/dsh-file-trace/resources` 懒加载 katex chunk（单文件打包，CSS 与全部字体 base64 内联，一次加载覆盖全文档）真正排版——上下标、分式、根号、希腊字母、\mathrm/\sqrt/\times/\quad 等均正常渲染；`throwOnError: false` 使单条公式语法错误只红字标注该条，不影响其余内容；chunk 加载失败或离线时自动回退为原文文本（v0.3.13 及以前的行为），只降级不崩溃。
- **出错统一展示**：读取 / 写入 / 编辑**失败**的操作点开即显示结果里的真实错误文本（红色错误块），不再渲染伪造 diff。
- **语法高亮**：按扩展名识别常见语言（C/C++、Java、C#、JS/TS（含 mjs/cjs/mts/cts）、Python、Go、Rust、cmd/batch、PowerShell、JSON/JSONC/JSON5/YAML/TOML/INI、SQL、CSS/SCSS/Less、HTML/XML/SVG/Vue、GraphQL、LaTeX/TeX（TeXstudio 风格初步渲染：命令/数学/注释/结构高亮）等），读取视图与 diff 行的**关键字 / 字符串 / 数字 / 类型 / 函数 / 注释 / 预处理指令**分别着色；修改行的行内变更底色与着色叠加。
- **写入视图**：新文件写入显示为**全量新增（每行绿色 +）**；覆盖修改时按真实差异做 del/add。
- **编辑视图（hunk 上下文折叠）**：用窗口内更早的写入/读取内容重建完整文件，保留**变更点 ±3 行上下文**；未变化区域**≥3 行才折叠**成「… N 行」（≤2 行直接显示），点击展开/收起。
- **长行折叠**：单行超过 120 字符自动折叠为省略号，点击展开/收起。
- **终端风格 diff**：等宽字体、行号 gutter、**删除红 / 新增绿 / 修改蓝** 的字体色（背景仅为对应色调弱化，保证可读）。
- **Ctrl+滚轮调字号**：历史操作列表区与文件内容区（diff/读取视图）字号**独立调节**（Ctrl + 鼠标滚轮，各自持久化到 localStorage）；限制 9–28px，达到边界时弹提示「已达最小/最大字号 N px」。
- **浮动窗口（可拖拽 / 可调大小 / 右侧吸附）**：拖动标题栏移动位置，拖左缘/底缘调整宽高（位置与尺寸持久化到 localStorage）；**拖到屏幕右缘释放自动吸附为全高右侧栏，主对话区同步右移避让不重叠，再拖标题栏即脱离**；底部 diff 区上方另有把手调整列表与 diff 的分配。
- **兼容自诊断**：apply 时探测所需客户端 API，不满足时不崩溃，而是渲染修复指引横幅；组件渲染出错时同样显示修复提示。

## 工作原理

- 数据完全来自会话 Chat 视图快照（`views.get('chat').legacy` 的 tool-result 节点与 runningCalls），每次渲染纯派生，无自建状态、无监听器，刷新/翻页自动对齐当前窗口。
- diff 为行级 LCS；del-run + add-run 重叠对标记为 mod（修改）。
- 注册进 `conversation.session.header.utilities`（session 作用域 list 槽位，经 `ctx.slots.inject`）。

## 版本兼容

| 插件版本 | DSH 版本 | 说明 |
| --- | --- | --- |
| `v0.3.16`（默认） | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.7-alpha.2`、`0.1.7-rc.1` | 声明支持 dsh-v0.1.7-rc.1（舰队扫检零错误零崩溃，零适配改动） |
| `v0.3.15` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.6-alpha.2`、`0.1.7-alpha.1`、`0.1.7-alpha.2` | **新增 DSH 版本门控更新提示**（舰队统一功能）；声明支持 dsh-v0.1.7-alpha.2；typecheck/112 单测/构建全绿，舰队扫检零错误 |
| `v0.3.14` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.6-alpha.1` | **数学公式渲染**：Markdown 阅读模式 `$$`/`$` 公式经懒加载 katex chunk（单文件，字体 base64 内联）真正排版，失败回退原文；typecheck/105 单测/构建全绿，chunk 路由实机 200 验证；宿主重启后新 client 生效 |
| `v0.3.13` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.6-alpha.1` | 声明支持 dsh-v0.1.6-alpha.1（npm 已发布，钉版本实机验证；client 插件面零代码差异，typecheck/105 单测全绿，热挂载实机验证） |
| `v0.3.12` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-rc.2` | **Markdown 阅读窗格加入 Ctrl+滚轮字号缩放**：md 正文/代码块/表格/文件徽章字号接入面板字号变量（此前 md 正文硬编码 13.5px 不随缩放），Ctrl+滚轮在 md 窗格内正确归入面板字号组（此前误缩文件列表）；typecheck/105 单测/构建全绿，热挂载即时生效，无需重启宿主 |
| `v0.3.11` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-rc.2` | 声明支持 0.1.5-rc.1~rc.2（npm 已发布，钉版本实机验证；rc.1 为 0.1.5 系列首个候选版本，client 插件面零代码差异；typecheck/build/105 单测全绿，热挂载实机验证） |
| `v0.3.10` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-alpha.2` | 声明支持 0.1.5-alpha.2（npm 已发布，钉版本实机验证；alpha.2 改动为 Sidebar 文档预览、模型文件交付、minimal 默认工具调整与 `fs-ext` 安装修复，client 插件面零代码差异；typecheck/build/105 单测全绿，启动清单确认加载） |
| `v0.3.9` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-alpha.1` | 声明支持 0.1.5-alpha.1（npm 已发布，钉版本实机验证；0.1.5 改动在会话格式 V3 / ctx.agent 移除 / 宿主 bundle 服务路由 `/plugins/??`，client 插件面零代码差异；typecheck/build/105 单测全绿，启动清单确认加载） |
| `v0.3.8` | 与 v0.3.7 相同 | **SVG 渲染预览**：`.svg` 操作预览头部新增「渲染/原文」切换——渲染源三级链（host asset 路由磁盘原始字节 → 会话 payload 经 DOMParser 校验后的 blob → 沙箱 iframe 兜底，禁脚本、SMIL 动画照常）；markdown 阅读模式内嵌本地 `.svg` 从文件 chip 升级为真实渲染；payload XML 非法时显示明确错误提示而非无声裂图 |
| `v0.3.7` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`、`0.1.3-alpha.2` | 修复：文档以 `---` 分界线开头且后方另有分界线时，标题与正文被误吞为 YAML frontmatter 渲染成代码块（client 渲染器修复，与 DSH 版本无关） |
| `v0.3.6` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`、`0.1.3-alpha.2` | 声明支持 0.1.3-alpha.2（npm 已发布，钉版本实机验证；alpha.2 改动全在 pi-ai/Web 顶栏/子代理消息/host 面，client 插件面零代码差异；typecheck/build/单测全绿） |
| `v0.3.4` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1` | **PDF 渲染预览**：`.pdf` 操作（读 / 写 / 编辑）预览头部可切换「渲染/原文」——文件字节经宿主 asset 路由流入显式 `application/pdf` Blob，浏览器原生 PDF 查看器内嵌打开；仅绝对路径可渲染（相对路径无法定位会话工作区） |
| `v0.3.3` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1` | **HTML 渲染预览**：`.html`/`.htm`/`.xhtml` 操作预览头部可切换「渲染/原文」——沙箱 iframe（allow-scripts、禁同源）渲染（脱敏后）文档——动画/交互可运行但不透明源隔离；相对路径资源不解析（安全取舍，详见已知限制） |
| `v0.3.2`| `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1` | 声明支持 0.1.3-alpha.1（npm 未发布，源码宿主实机验证；0.1.3 破坏性变更集中在 host/session 侧，client 插件面零代码差异；typecheck/build/96 单测全绿） |
| `v0.3.1` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1` | 文档更新：明确脱敏层定位——展示层便利（截图 / 分享场景），非安全边界，会话日志保留原始内容 |
| `v0.3.0` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1` | **敏感内容脱敏层**：敏感路径整文件遮罩（`.env`/`*secret*`/`*credential*`/`*token*`/`*api-key*`/私钥等）+ 普通文件按内容形态遮罩（`api_key:`/`Bearer `/`sk-`/`AKIA`/`ghp_`/PEM 头等），diff/阅读视图/Markdown 模式/错误文本统一生效；默认开启，面板工具栏一键开关（localStorage 记忆）；仅影响显示，不改会话日志 |
| `v0.2.9` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1` | 声明支持 rc.1（alpha.5→rc.1 为纯版本号提交，零代码差异；实机 rc.1 验证通过） |
| `v0.2.8` | `dsh-v0.1.2-alpha.1`~`alpha.5` | LaTeX/TeX 语法高亮（TeXstudio 风格初步渲染：命令→macro、数学→string、注释→灰、{}&^_#→structure、200+ 关键字） |
| `