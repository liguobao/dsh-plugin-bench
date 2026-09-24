# agentflow

<p align="center">
  <strong>AI Agent 团队的软件项目生命周期编排引擎</strong>
  <br>
  <em>A local lifecycle orchestrator for AI agent teams</em>
</p>

---

<p align="center">
  <a href="#中文概览">中文</a> ·
  <a href="#english-summary">English</a>
</p>

---

## 中文概览

agentflow 是一个**本地优先、MCP 原生、git/worktree-aware** 的 AI agent 项目生命周期编排引擎。

它把项目初始化、任务拆解、分支执行、review handoff 和项目记忆串成一条真实工作流：
- `project_init` 把本地代码仓库绑定到 namespace
- DAG 表达 branch-scoped 工作流，task 表达可依赖、可审查、可恢复的工作单元
- leader / worker / reviewer 三个角色按默认 behavior tree 推进主链
- docs / handbooks / diaries 持久化项目知识与交付记录

运行形态：
- **Go MCP server**：系统事实源、状态机、工具注册、SQLite 持久化
- **Python BT sidecar**：leader / worker / reviewer 默认行为树执行层
- **Git + worktree**：每个 DAG 绑定分支、每个 task 绑定 worktree

## 核心模型

| 概念 | 含义 |
|------|------|
| `namespace` | 一个项目的隔离边界 |
| `DAG` | 一条 branch-scoped 的工作流，通常对应一个功能分支 |
| `task` | 一个有状态、有依赖、有审查流转的工作单元 |
| `worker` | 执行任务的角色，跨 DAG 共享 |
| `reviewer` | 读取提交元数据并做 `pass / rework` 决策的角色 |
| `leader` | 负责 phase 判断、派发、监控、阻塞汇报、完成收口 |

除了任务状态，agentflow 还内建项目记忆面：
- `doc_*`：项目文档
- `worker_handbook_*` / `find_knowledge` / `find_pitfalls`：Worker 经验库
- `worker_diary_*`：Worker 工作日记
- `leader_diary_*`：Leader 项目日记

## 生命周期总览

项目不是直接从“建 task”开始，而是按 phase 推进：

```text
setup -> shape -> plan -> execute -> stuck -> done
```

| Phase | 含义 |
|------|------|
| `setup` | 还没有完成项目初始化 |
| `shape` | 正在确认最终形态、范围和角色分工 |
| `plan` | 已有 worker / namespace，但还没拆出 DAG / task |
| `execute` | 已有任务主链，正在 dispatch / 实现 / review |
| `stuck` | 当前没有可派发任务，也没有活跃任务，需要人工处理阻塞 |
| `done` | 当前 DAG / 项目任务已完成 |

高层入口：
- `project_next_steps`：看项目当前在哪个 phase、下一步该做什么
- `leader_tick`：让 leader 默认 BT 按 phase 做一次调度
- `lifecycle_tick`：在一条调用里串 leader -> worker -> reviewer 的完整主链

## 执行模型：Git / Branch / Worktree

这是当前系统最重要的运行约束之一。

### 1. `project_init` 是推荐入口

`project_init` 会：
- 创建或绑定 namespace
- 校验 / 初始化 git 仓库
- 设置主分支信息
- 记录 workdir / worktree root
- 写入 `.claude/agentflow-git.md`

`.claude/agentflow-git.md` 是 repo-local 的执行规则文件，约束 worker 如何在 worktree 中工作、如何提交、哪些动作被禁止。

### 2. 一 DAG 一分支

每个 DAG 绑定一个 feature branch。DAG 不是纯逻辑分组，而是和 git 分支直接关联的执行单元。

### 3. 一 task 一 worktree

task 在自己的 worktree 中执行，而不是直接在 repo root 改文件。

典型约束：
- worker 只修改自己的 `worktree_path`
- task 的 git branch 必须和 DAG branch 一致
- `start` / `resume` 会准备 task 的 git runtime
- `git_status` / `worktree_get` 用来检查当前 git/worktree 状态

### 4. `submit` 是带交付契约的

`submit` 不只是一次状态转换。对 git-backed task，提交前需要满足：
- clean worktree
- 已有 worker diary
- 能记录 `review.commit`
- 能记录 `review.diff`

reviewer 围绕这些 review metadata 做 pass / rework，而不是脱离 git 上下文推进状态。

## 默认 Behavior Tree 角色流

### Leader

`trees/leader-default.json` 的主线语义：

```text
refresh_phase
  -> setup_actions | shape_actions | plan_actions
  -> execute: dispatch_task | monitor_tasks
  -> stuck: report_stuck
  -> done: report_done
```

leader 负责判断项目处于哪个 phase，并按 phase 决定下一步动作。

### Worker

`trees/worker-default.json` 的默认链路：

```text
doc_search_prepare
-> task_get_confirm
-> enter_worktree
-> implement_code
-> git_commit_changes
-> doc_write_record
-> diary_write_entry
-> task_submit_for_review
```

这条链路明确表达：worker 的交付不是“改完代码就算结束”，而是要连同 commit、文档、日记和 review handoff 一起完成。

### Reviewer

`trees/reviewer-default.json` 的默认链路：

```text
fetch_work_diff
-> review_decide
-> task_review_pass | task_review_rework
```

reviewer 基于 `review.commit` / `review.diff` 决策，而不是脱离 git 上下文做抽象状态推进。

## MCP 能力面

README 不再硬编码工具数量；当前工具面请以 `pkg/server/mcp.go` 为准。

更适合按能力域理解：

### Bootstrap / Project Setup
- `project_init`
- `project_next_steps`
- `namespace_create`
- `namespace_get`
- `namespace_list`
- `namespace_delete`

### DAG / Task / Worker State
- `dag_create`, `dag_get`, `dag_list`, `dag_update`, `dag_report`, `dag_flowchart`
- `task_create`, `task_get`, `task_list`, `task_query`, `task_history`, `task_create_batch`, `task_transition`
- `worker_register`, `worker_get`, `worker_list`, `worker_update`, `worker_status`, `worker_prompt_get`

### Lifecycle / Behavior Trees
- `leader_tick`
- `lifecycle_tick`
- `bt_list_trees`
- `bt_show_tree`
- `bt_validate_tree`
- `bt_tick`

### Git / Worktree / Review Handoff
- `git_status`
- `worktree_get`
- task metadata 中的 `git.*`
- `review.commit` / `review.diff`

### Docs / Handbooks / Diaries
- `doc_write`, `doc_get`, `doc_list`, `doc_search`, `doc_delete`
- `worker_handbook_write`, `worker_handbook_get`, `worker_handbook_list`
- `find_knowledge`, `find_pitfalls`
- `worker_diary_write`, `worker_diary_get`, `worker_diary_list`
- `leader_diary_write`, `leader_diary_get`, `leader_diary_list`

### Reporting / Project Queries
- `project_next_tasks`
- `project_blockers`
- `project_report`
- `flow_ping`

## agentflow ↔ agent-hub：单向投影、soft-fail、默认关闭

agentflow 可以把任务与分支状态**单向投影**到 [agent-hub](https://hub.stifer.xyz) 控制平面，让多机团队看到同一张任务大盘。三条铁律：

1. **单向 L→H**：只从 agentflow 推送到 Hub，**从不**把 Hub 状态读回本地。`agentflow` 的 SQLite 永远是唯一真源。
2. **soft-fail**：Hub 的任何故障（连接拒绝 / 超时 / 401 / 500）都**不会**让 MCP 工具调用失败，也**不会**回滚本地状态。发生了什么只体现在返回值里的一个 note 字符串。
3. **默认关闭**：没有绑定 team code **或**没有凭据 ⇒ 直接跳过，**零出网请求**。不配置就不会有"用户不知情就被上报"。

### 接线了哪些时机

| 工具 | 投影内容 | 回填的 note 键 |
|------|----------|----------------|
| `task_create` | 任务行 8 字段 | `hub_note` |
| `task_prepare_start` | 任务行（带 `branch`/`head_sha`）+ 分支上报（`bind_type=task`） | `hub_note` + `hub_branch_note` |
| `task_transition` | 任务行；`submit` 起带 reviewer 将看到的 `review.commit` | `hub_note` |
| `task_create_batch` | **每个**任务各一条 | 每个 item 的 `hub_note` |

note 形如：

```text
hub_task_sync_ok
hub_task_sync_skipped: no login token / business_code     ← 没配置，什么都没发
hub_task_sync_disabled: HUB_SYNC/HUB_ENABLED off           ← 被 kill switch 关掉
hub_task_sync_failed: status 401 forbidden                 ← 试过了，失败了；本地不受影响
```

### 怎么打开

```jsonc
// 1) 登录取 JWT（两段式设备码；JWT 落 ~/.agent-hub/config.json）
//    hub_login({})                 // → code + verification_url
//    浏览器打开 verification_url 并点 Approve
//    hub_login({ "code": "<code>" })  // → status=pending_approval 就再调一次；ok 即落盘
//    hub_list_teams({})            // → 发现你的 4 位 code（需 JWT；只有 API key 会 skipped）

// 2) 绑定团队（唯一产品真源：namespace metadata）
//    hub_bind_team({ "namespace_id": "insighttutor", "business_code": "z8gw" })

// 3) 提供凭据（env 优先；也可放 {workdir}/.mycompany/hub-client.json）
//    HUB_TOKEN=<Hub JWT>        # 推荐；只有 API key 时部分能力不可用
//    HUB_BASE_URL=https://hub.stifer.xyz
```

关闭方式（任一）：`HUB_DISABLED=1`、`HUB_SYNC=0`、`HUB_ENABLED=false`。**kill switch 永远优先于凭据。**

### 边界（照代码写实）

- `~/.agent-hub/config.json` 是 **JWT-only**：它**永远不提供 team code**（否则同机两个 namespace 会争抢同一个团队）。team code 只可能来自 env / namespace metadata / workdir 文件。
- MCP 工具表里有四个 Hub 工具：`hub_login`（两段式设备码登录）、`hub_list_teams`（发现团队 code，需 JWT）、`hub_status`、`hub_bind_team`。登录成功后 JWT 落 `~/.agent-hub/config.json`，且**不会**发明 team code。
- 没有重试队列、没有离线补发、没有顺序保证，也没有 H→L 对账。
- 完整字段白名单见 [`docs/SYNC_CONTRACT.md`](docs/SYNC_CONTRACT.md)，逐面完成度矩阵见 [`docs/HUB_ALIGNMENT.md`](docs/HUB_ALIGNMENT.md)。

## 安装与快速开始 (Installation & Quick Start)

agentflow 提供多种宿主集成方案，推荐优先使用 DeepSeek Harness (DSH) 原生插件体验完整的多 Agent 协同与 4D 动态画布能力；同时也支持作为独立 MCP 服务接入 Claude Code、Codex 等终端工具，或连接 Agent Hub 进行多机分布式团队协同。

### 推荐方式一：DeepSeek Harness (DSH) 原生插件安装（首推）

通过 DSH 插件体系可实现核心状态机、技能与交互式拓扑画布的开箱即用：

1. **社区市场安装 (1024Store / dshfind)**：
   - 打开 DSH 插件市场 / 社区合作提供方（如 [dshfind](https://dshfind.com/en/plugins/toustifer/agentflow)），搜索 `@stifer/dsh-agentflow`，点击一键安装；
2. **CLI 命令行快速安装**：
   ```bash
   dsh plugin --profile web add @stifer/dsh-agentflow
   ```
3. **配置启用**（在 `<dshHome>/profiles/web/cordis.patch.yml` 中追加）：
   ```yaml
   - insert:
       - id: agentflow
         name: '@stifer/dsh-agentflow'
   ```
4. **验证与体验**：
   - 启动 DSH 后在会话中输入 `/agentflow` 即可唤起引导；
   - 自动挂载 `mcp__agentflow__*` (61+ 工具)；
   - 原生集成 Live-Spec 4D 动态可视化拓扑画布（自动适配半宽与全宽视口），实时推演任务依赖与流转。

---

### 方式二：Claude Code / Codex 独立安装

适用于基于独立二进制或 CLI 终端的代码协作环境：

1. **一键安装脚本（自动下载二进制与技能包）**：
   - **Windows (PowerShell)**：
     ```powershell
     irm https://raw.githubusercontent.com/toustifer/agentflow/master/scripts/install.ps1 | iex
     ```
   - **Linux / macOS (Bash)**：
     ```bash
     curl -fsSL ht