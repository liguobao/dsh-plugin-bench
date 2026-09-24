<p align="center">
  <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/流程编排.png" alt="界面预览" width="100%" />
</p>

<h1 align="center">Visual Workflow</h1>

<p align="center">
  为 <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a> 量身打造的可视化多 Agent 工作流设计器
</p>

<p align="center">
  <a href="README_EN.md">English</a> · <b>简体中文</b>
</p>

<p align="center">
  <a href="#"><img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-6-blue"></a>
  <a href="#"><img alt="React" src="https://img.shields.io/badge/React-19-blueviolet"></a>
  <a href="#"><img alt="Node" src="https://img.shields.io/badge/Node-%E2%89%A524-green"></a>
  <a href="#"><img alt="pnpm" src="https://img.shields.io/badge/pnpm-11-orange"></a>
  <a href="#"><img alt="vitest" src="https://img.shields.io/badge/test-vitest-cyan"></a>
  <a href="#"><img alt="license" src="https://img.shields.io/badge/license-MIT-lightgrey"></a>
  <a href="https://github.com/GZX2211/dsh-Visual-Workflow/releases"><img alt="version" src="https://img.shields.io/github/v/release/GZX2211/dsh-Visual-Workflow?label=version&color=0891b2&include_prereleases"></a>
</p>

---

## 核心亮点

<p align="center">
  <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/界面优化.png" width="100%" />
</p>

✦ **拖拽式编排**  
  - 零代码拖拽连线，纯 SVG 画布流畅交互、撤销重做一应俱全；无限画布、一键整理，复杂工作流触手可及。

✦ **双模式架构**  
  - **流程编排模式**：长流程多 Agent 智能调度，父代理自主推进，支持断点续跑与运行中实时编辑；
  - **API服务模式**：一键发布为独立 REST API 服务（OpenAI 兼容协议），多租户会话隔离，端口自动分配。

<table>
  <tr>
    <td width="65%" valign="top">
      <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/API服务模式.png" width="100%" />
    </td>
    <td width="35%" valign="top">
      <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/终端输出.png" width="100%" />
    </td>
  </tr>
</table>

> 将 DSH 作为独立后端服务部署，持久化 无头Agent 后台运行，可连接外部APP（如QQ机器人、飞书）或自建前端。

✦ **画布双向同步**  
  - 画布修改保存后，编排器实时感知最新拓扑（新增节点/连线即时生效）；运行状态（节点高亮、状态徽标）实时回显画布；双向变更防回环，运行锁保护跨会话冲突，编排与画布始终一致。

✦ **深度自定义**  
  - 每个子代理节点独立配置 system prompt、LLM 模型、思考强度、工具组合（内置预设 / 自定义组合）及 ReAct 迭代上限、回流重试上限；父代理亦可自由选择模型与调度模板，满足精细化编排需求。

<table>
  <tr>
    <td width="50%" valign="top">
      <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/组合管理页.png" width="100%" />
    </td>
    <td width="50%" valign="top">
      <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/MCP配置页.png" width="100%" />
    </td>
  </tr>
</table>

> 工具自由组合分配给各个代理，避免无用工具占据上下文；mcp服务器只需一行配置自动注册并支持热重载即时生效。

✦ **协作组与虚拟节点**  
  - 将多个角色节点拖入协作组，组内 Agent 并行执行并通过 `wf_ask_agent` 相互通信；虚拟节点作为主节点的别名引用，共享同一执行实例，拓扑复用更灵活。

✦ **定时触发**  
  - 工作台内置定时任务，选择工作流模板配置执行窗口与触发策略，自动创建实例并运行，错过窗口自动挂起/续跑，支持错峰调用api，省钱又省心。

<p align="center">
  <img src="https://raw.githubusercontent.com/GZX2211/dsh-Visual-Workflow/main/assets/images/定时任务管理.png" width="100%" />
</p>

> 全自动化运维管理，定时自动运行工作流，可支持峰谷时段错时调用，自动暂停，保存流程数据，谷时自动运行。

✦ **零官方包依赖**  
  - 所有 DSH 生态服务（LLM、子代理、工具、用户问题等）均通过 `ctx.get()` 运行时解析，Host 工具以纯对象定义注册，插件自身无任何官方包编译时依赖，升级兼容性更强。

---

## 核心概念

| 概念 | 说明 |
|------|------|
| **模板** | 角色/文件/数据库/工作流的“蓝图”，存储在 `~/.dsh/visual-workflow/`；模板与实例深拷贝解耦，修改模板不影响已生成节点 |
| **实例** | 工作流或服务的具体运行实例（`workflows/` 与 `services/`），只能从工作流模板创建，可在画布中编辑并保存 |
| **节点** | 画布上的卡片，分为父代理、子代理、文件、数据库、阶段（启动/结束/暂停）、协作组、虚拟节点 |
| **连线** | 传递流程方向（流程线）、上下文内容（上下文线）、数据库标识（数据库线）；流程线可带条件标签（通过/不通过/内容），由父代理语义判断 |
| **父代理** | 编排的核心调度者，模式一中负责监督与调度（不执行具体任务），模式二中为最终回答者；可由用户指定调整编排流程 |
| **子代理** | 任务执行者，独立配置角色 Prompt（system prompt）、模型、工具等，由父代理按需创建与调度 |
| **编排** | 主 Agent 使用 `wf_run_node` / `wf_ask` / `wf_finish` 等工具自主推进流程，控制节点状态 |
| **模式** | 插件提供两种运行模式：流程编排模式（模式一）与 API 服务模式（模式二），通过顶栏切换，分别存储于不同目录 |
| **断点续跑** | 流程暂停或宿主意外中断后，已执行节点状态持久化，恢复后不重跑，从断点继续 |
| **协作组** | 将多个角色节点组合为一个并行执行单元，组内 Agent 可自由通信，组整体完成后再触发后续流程 |
| **虚拟节点** | 主节点的别名引用，不存储独立配置，共享主节点的执行实例，用于拓扑复用 |

> 区别：不同于官方 subagent 调度只能传递父的工具和模型，`wf_run_node` 创建的子代理节点可以自由组合任意工具、设定不同模型和系统提示词（system prompt）。

---

## 节点卡片

### 1. 角色节点（任务执行单元）

卡片形态（**左 3 入、右 2 出**）：

```
        ┌─────────────────────────┐
  左一 ●│  [角色卡片] 标题          │● 右一
（数据库）│  类型徽标 / 模型 /       │（上下文）
  左二 ●│  工具组合徽标            │● 右二
（上下文）│                         │（流程出）
  左三 ●│                         │
（流程入）│                         │
        └─────────────────────────┘
```

| 接点 | 名称 | 语义 |
|---|---|---|
| 左一 | 数据库输入 | 连接数据库节点，注入检索/查询工具 |
| 左二 | 上下文输入 | 接收上游上下文（不连接则不继承） |
| 左三 | 流程输入 | 控制执行顺序 |
| 右一 | 上下文输出 | 向下游传递本节点产出 |
| 右二 | 流程输出 | 顺序执行/条件分支（通过/不通过/内容） |

**属性配置**：

| 配置项 | 说明 |
|---|---|
| **名称** | 节点名称 |
| **system prompt** | 文本输入或引用 .md，设定角色系统提示词 |
| **LLM 模型** | 独立选择 provider + model |
| **思考强度** | 与官方下拉一致 |
| **工具组合** | 内置预设（标准/极简/ptc/创造）+ 自定义组合（组合管理中创建） |
| **ReAct 迭代上限** | 软截停：达上限后强制收尾（不发起新工具调用，输出已有结论），默认 50 |
| **回流重试上限** | 节点级尝试计数护栏，默认 3 |
| **输入/输出数据结构** | 文本/JSON 描述（辅助模型理解） |
| **系统提示词开关** | 控制官方系统提示词注入（默认开启）；两个开关分别控制官方人设/身份/系统/上下文段（「人设段」）与工具 `tool:*` 使用指引段（「工具散文段」）的注入。**关闭工具散文段不影响工具调用能力**（只去掉英文使用指引）；要真正禁用某个工具，请用「组合」管理里的全局工具开关 |

**虚拟节点**：点击“复制”可生成虚拟节点（虚线边框 + “↻ 引用”角标），与主节点共享配置与执行实例，删除主节点时级联清除。

### 2. 文件节点

- 文件内容直接存于模板（文本 / PDF 提取文本 / 图片等非文本文件以受管路径存储）
- 右侧属性面板可上传/替换文件，保存后所有引用节点同步
- 功能：用于给角色节点注入提示词、需求、压缩摘要等上下文
- 文本内容注入上限默认 20000 字符，超出截断并提示；非文本仅注入受管路径，代理通过官方读取工具访问

### 3. 数据库节点

- **本地类型**：支持 SQLite 文件，内置向量检索（bge-small-zh-v1.5，CPU 推理；模型资产缺失/加载失败自动降级 BM25）
- **服务器类型**：支持 MySQL / PostgreSQL，提供结构化只读查询与向量检索（本地构建索引）
- 右侧面板可配置连接信息、测试连接，并调整检索高级选项（召回条数、分块窗口、相似度阈值、索引容量）
- **数据库检索**，转换为 `wf_db_query` 工具（单工具三模式：search/query/schema）供代理调用，代理需通过 db-in 连线获得该工具

### 4. 阶段节点

- **启动（模式一） / 输入（模式二）**：流程入口；模式二下自动接收外部用户问题作为初始上下文
- **结束（模式一） / 输出（模式二）**：流程终点；模式二下汇聚父代理最终输出并流式返回
- **暂停（仅模式一）**：流程门，运行至此暂停并保存断点（人工审查点），再次运行从右出继续

### 5. 协作组节点

- 将多个角色节点拖入协作组，组内角色并行启动（组内角色仅保留上下文/数据库连线）
- 协作 Prompt 追加到每个成员的首条用户消息末尾，并自动列出所有成员的 ID 与角色名称
- 组内 Agent 通过 `wf_ask_agent` 阻塞通信、通过 `wf_ask` 向用户交流提问
- 组卡片左入流程、右出流程；组内成员节点支持跨组上下文/数据库连线
- 卡片支持拉伸（八方向），内部成员列表可滚动

---

## 连线

**连线类型与颜色**：

| 连线类型 | 语义说明 | 颜色 |
|----------|----------|------|
| 流程连线 | 控制执行顺序 | ⚪ 冷灰 / 银白 |
| 上下文连线 | 传递文本内容、文件索引 | 🟡 琥珀金 |
| 数据库连线 | 传递数据库服务标识 | 🔵 天蓝 |
| 条件：通过 | 条件判断为真，执行该分支 | 🟢 翠绿 |
| 条件：不通过 | 条件判断为假，执行该分支或回流 | 🔴 珊瑚红 |
| 条件：内容 | 自定义语义判断（路由标签） | 🟣 紫罗兰 |

> 编辑条件后，条件颜色覆盖初始颜色；条件判断由父代理进行语义判断。

---

## 编排工具

各 Agent 通过以下工具自主调度（插件提供护栏与持久化）：

| 工具名称 | 参数 | 功能说明 |
| :--- | :--- | :--- |
| **`wf_run_node`** | `nodeId` – 节点ID<br>`thinking?` – 思考强度<br>`iterationLimit?` – ReAct 迭代上限<br>`retryLimit?` – 回流重试上限 | 异步启动节点子代理，立即返回 `started`；若为暂停节点则返回 `paused` 并持久化断点。 |
| **`wf_run_node_wait`** | `nodeId` – 节点ID<br>`thinking?` – 思考强度<br>`iterationLimit?` – ReAct 迭代上限<br>`retryLimit?` – 回流重试上限 | 阻塞等待节点执行完成，返回 `ok/fail` 及最终输出。 |
| **`wf_ask`** | `questions[]` – 问题列表（支持多问）<br>`options?` – 可选项配置<br>`multi_select?` – 是否允许多选 | 向用户提问，渲染官方提问卡片，阻塞等待用户回答。 |
| **`wf_ask_agent`** | `cmd: ask/reply/resolve` – 命令类型<br>`targetChildId` – 目标代理ID<br>`message?` – 消息内容<br>`askId?` – 提问ID（用于回复/裁决） | Agent间阻塞通信：`ask` 发起提问并挂起，`reply` 定向回复，`resolve` 由父代理进行超时裁决（继续/重发/终止）。 |
| **`wf_db_query`** | `dataId` – 数据节点ID<br>`mode: search/query/schema` – 查询模式<br>`query?/sql?` – 查询语句<br>`topK?` – 返回条数 | 数据库只读访问：向量检索、结构化查询（仅 SELECT）、查看表结构。 |
| **`wf_finish`** | `status?` – 完成状态（completed/failed）<br>`summary?` – 总结信息 | 工作流收尾，标记完成或失败，释放运行锁（幂等）。 |

---

## 安装（Windows）

> **版本适配**：本插件适配 **DeepSeek Harness `0.1.5-rc.1`**（宿主侧提示词段名、子代理投递 API、会话 cwd 读取与客户端插槽均按该版本取证适配）。请先安装或升级宿主（升级前先在外部终端**完全停止 dsh 进程**）：
>
> ```bash
> npm install -g @deepseek-ai/dsh@0.1.5-rc.1
> ```

1. **文件管理器定位**：`%USERPROFILE%\.dsh\profiles\web\pnpm-workspace.yaml`,在其中添加：

```yaml
allowBuilds:
  onnxruntime-node: true
  protobufjs: true
  sharp: true
```

2. **运行插件安装命令**:

```bash
dsh plugin --profile web add "github:GZX2211/dsh-Visual-Workflow#main"
```

3. **验证挂载**：（可选）

```bash
dsh --profile web --dump-config | findstr "visual-workflow"
```

4. **重启** `dsh web`。打开工作台：点击官方**左侧边栏底部的「工作流」入口**（在官方「设置」旁）→ 官方**右侧 Sidebar** 打开「工作流」标签页即完整工作台（再次点击只是回到该标签页，工作台状态常驻保留，不会重新加载）。

5. 