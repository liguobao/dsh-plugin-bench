# Agent Handoff Skill

<p align="center">
  <a href="README.md">中文</a> | <a href="README_en.md">English</a>
</p>

<p align="center">
  <a href="https://www.dsh.so/artifact/agent-handoff-skill/"><img src="https://www.dsh.so/badge/agent-handoff-skill.svg" alt="dsh.so security" /></a>
</p>

<p align="center">如果这个 skill 对你的 Agent 接力流程有帮助，欢迎给仓库点一个 Star，让更多人更容易找到它。</p>

![Agent Handoff Skill hero](assets/readme/hero.png)

一个给 Codex / Claude Code / DeepSeek Harness（DSH）使用的 **可持续接力机制 skill**。

它解决的问题很朴素：AI Agent 很强，但会话窗口不是可靠的项目记忆。上下文会压缩，会话会中断，Agent 会更换，开发任务却还要继续。`agent-handoff` 的目标就是把“上一位 Agent 脑子里的状态”沉淀成仓库内可维护、可验证、可接手的项目文档。

它不是聊天总结工具，也不是把所有历史都塞进一个 Markdown 文件。它更像一份轻量的“项目飞行记录仪”：记录当前目标、状态、活跃文件、关键决策、验证结果、风险、阻塞点和下一步，让下一位 Agent 能快速、安全地继续工作。现在它还包含确定性的容量治理脚本，避免 snapshot 和历史日志在长期使用后无限膨胀。

## 平台兼容性

这个仓库里的 skill 不是只给 Codex 用。它采用通用的 `SKILL.md + references/ + scripts/` 结构，可以按不同工具的发现路径安装：

| 平台 | 安装位置 | 触发方式 |
| --- | --- | --- |
| Codex | `~/.codex/skills/agent-handoff` | Codex 根据 skill 描述自动触发，或用户明确要求使用该 skill。 |
| Claude Code 个人级 Skill | `~/.claude/skills/agent-handoff` | Claude Code 自动发现，或用 `/agent-handoff` 显式调用。 |
| Claude Code 项目级 Skill | `<repo>/.claude/skills/agent-handoff` | 只对当前仓库生效，适合团队随仓库共享。 |
| DSH 个人级 Skill | `~/.dsh/skills/agent-handoff` | DSH 自动加入模型目录，也可用 `/agent-handoff` 显式调用。 |
| DSH 共享 Agent Skill | `~/.agents/skills/agent-handoff` | 使用 DSH 的共享 Agent Skills 根目录。 |
| DSH 项目级 Skill | `<repo>/.dsh/skills/agent-handoff` 或 `<repo>/.agents/skills/agent-handoff` | 只对当前 Git 仓库生效，项目目录优先于个人目录。 |

DSH 不会扫描 `~/.codex/skills`、`~/.claude/skills` 或 `<repo>/.claude/skills`，需要把仓库安装或链接到上表中的 DSH 根目录。安装到默认根目录不需要修改 DSH profile、patch 或 settings。当前仓库里的 `agents/openai.yaml` 是 Codex UI 元数据；Claude Code 和 DSH 会忽略它。

### dsh.so 市场元数据

仓库根目录的 `package.json` 是给 dsh.so 等目录服务读取的最小市场 manifest，包含 `name`、`license`、`description`、仓库地址和文件清单。它设置为 `private`，不代表这个 Skill 要发布到 npm，也不会改变 DSH 按 `SKILL.md` 发现和加载 Skill 的方式。

这个 manifest 主要解决 dsh.so 的 L2 结构化元数据检查；L3 还需要可解析的安装规范和声明的 DSH 版本，L4 才会在沙箱中实际安装。当前 Skill 不声明 npm 安装或 Cordis bundle 安装命令，因此不能把加入 `package.json` 误解为安装测试已经通过。

如果希望 dsh.so 通过 GitHub topic 自动识别仓库，可以在 GitHub 仓库设置中添加 `dsh-plugin` topic。这个 topic 是市场索引信号，不是 DSH profile 配置；当前仓库的实际运行入口仍然是 `SKILL.md`。

## 为什么会有这个 Skill

在长时间使用 AI Coding Agent 做真实项目时，常见断点通常不是“代码不会写”，而是这些更现实的问题：

- 新窗口打开后，Agent 不知道上一轮真正做到哪里。
- 上一位 Agent 做过技术决策，但没有记录原因和证据。
- 用户说“继续”，但当前目标、活跃文件、验证状态已经散落在旧聊天里。
- 一个复杂任务跨越多天、多模块、多次中断，最后没人能判断哪些内容已经完成。
- 接力文档越写越像聊天流水账，下一位 Agent 反而要读更多无关内容。
- 项目里有 `CLAUDE.md`、`AGENTS.md`、`.claude/CLAUDE.md` 等规则文件，但每个仓库的维护方式不一致。

`agent-handoff` 把这些经验固化为一个可复用 skill：它会指导 Agent 在仓库内创建或修复一套稳定的接力机制，并提供一个幂等 bootstrap 脚本，减少重复复制提示词和手工拼模板的错误。

它还会把更保守的文件读取协议写进项目规则：`Read` 范围默认不超过 240 行，`offset` 必须按行号处理，遇到 offset 漂移、空输出、stale snippet 或 API termination 时停止继续分页读取，并用搜索或只读 shell 命令重新锚定后再行动。

## 它创建什么

默认机制现在是 **多文档结构**，同时保留旧版单文档模式。

| 文件 | 作用 |
| --- | --- |
| `AGENT_HANDOFF.md` | 多文档模式下是入口索引和恢复路线；单文档模式下保存全部接力状态。 |
| `.agent-handoff/snapshot.md` | 多文档模式下保存当前目标、状态、下一步、活跃文件、阻塞点和开放问题。 |
| `.agent-handoff/workspace.md` | 项目结构、入口、测试命令、文档和长期项目背景。 |
| `.agent-handoff/decisions.md` | 重要决策、原因和证据。 |
| `.agent-handoff/work-log.md` | 近期仍有操作价值的工作日志。 |
| `.agent-handoff/validation.md` | 验证命令、结果、失败原因和未跑测试说明。 |
| `.agent-handoff/backlog.md` | 待办和 follow-up。 |
| `.agent-handoff/risks.md` | 风险、阻塞点、`UNKNOWN` 和需要确认的信息。 |
| `.agent-handoff/archive.md` | 压缩后的旧历史，不参与默认恢复。 |
| `.agent-handoff/archive/` | 自动轮换出的完整历史分片，单个文件不超过 128 KiB。 |
| `AGENTS.md` | Codex 与 DSH 共用的项目级 instructions 文件，写入平台中性的接力维护规则。 |
| `.claude/CLAUDE.md` | 项目级 Claude Code 规则，要求未来 Agent 启动时读取接力文档，并在收尾前更新。 |
| `AGENT_SESSION_PROMPTS.md` | 可选文件，保存新窗口启动、继续任务、收尾、接力质量审查等常用提示词。 |
| `.claude/settings.json` | 可选文件，仅在用户要求时合并安全的只读查询权限或 Claude Code 软提醒 hook 条目。 |
| `.claude/hooks/handoff-watch.mjs` | 可选 Claude Code hook 脚本，仅在显式使用 `--install-hooks` 时创建。 |
| `.gitignore` | 可选更新，把本地接力文档设为不提交，除非项目决定把它纳入版本控制。 |

核心约束是 **幂等**：项目级规则使用固定 marker 包裹。

```markdown
<!-- AGENT_HANDOFF_PROTOCOL:START -->
...
<!-- AGENT_HANDOFF_PROTOCOL:END -->
```

如果 marker 已存在，就替换区块；如果不存在，就追加区块；不会每次执行都重复堆一份规则。

## 它怎么工作

![Agent Handoff workflow](assets/readme/workflow.png)

`agent-handoff` 的运行逻辑可以理解为一个闭环：

1. **Inspect**：先看仓库结构，不直接写模板。
2. **Bootstrap**：创建或合并必要的接力文件和项目规则。
3. **Maintain**：任务过程中持续记录目标、决策、活跃文件、验证和风险。
4. **Compact / Rotate**：检查容量，先归档再压缩 snapshot，并按完整记录轮换过长日志。
5. **Closeout**：非纯聊天任务结束前，主动刷新并维护 `AGENT_HANDOFF.md` 或相关 `.agent-handoff/` 文件。
6. **Recover**：下一位 Agent 从接力文档恢复状态，再按需读取源码。

这个闭环的重点不是让 Agent 少读源码，而是让 Agent 少读无关历史。`AGENT_HANDOFF.md` 只负责告诉下一位 Agent “从哪里开始读”，具体实现仍然必须从源码和测试中验证。

多文档模式下，恢复读取顺序是：

1. `AGENT_HANDOFF.md`
2. `.agent-handoff/snapshot.md`
3. `.agent-handoff/risks.md`
4. `.agent-handoff/backlog.md`
5. `.agent-handoff/validation.md`，仅当验证状态影响当前任务
6. `.agent-handoff/decisions.md`，仅当要修改架构、行为、依赖或既有决策
7. `.agent-handoff/workspace.md`，仅当需要项目结构、命令或子项目边界
8. `.agent-handoff/work-log.md`，仅当需要近期实现细节
9. `.agent-handoff/archive.md`，仅当确实需要旧历史

## 主要应用场景

![Agent Handoff scenarios](assets/readme/scenarios.png)

### 1. 新项目初始化

当你打开一个新仓库，希望以后每个 Agent 都能自动维护接力状态，可以在 Codex、Claude Code 或 DSH 中使用这个 skill：

```text
使用 agent-handoff skill，为当前项目初始化接力机制。
```

它会检查仓库结构，创建 `AGENT_HANDOFF.md`，并按平台把 Durable Handoff 规则合并到：

- Codex / DSH：`AGENTS.md`
- Claude Code：`.claude/CLAUDE.md`

适合：

- 新 SaaS 项目
- 多模块 monorepo
- 需要长期维护的客户项目
- 经常切换 AI Agent 或会话窗口的仓库

### 2. 长任务跨窗口继续

一个功能开发可能跨越多次对话，例如：

- 第一天梳理架构和方案。
- 第二天实现后端 API。
- 第三天补前端和测试。
- 第四天修验证失败和边界条件。

如果没有接力机制，新 Agent 只能靠旧聊天恢复上下文。`AGENT_HANDOFF.md` 则会明确记录：

- 当前目标是什么。
- 哪些文件正在修改。
- 做过哪些决策。
- 跑过哪些验证命令。
- 哪些测试没跑，为什么没跑。
- 还有哪些风险和下一步。

继续任务时可以说：

```text
请读取 AGENT_HANDOFF.md，接着完成当前任务。
```

如果你遇到过 `Continue from where you left off.` 后 Agent 输出 `No response requested.` 或静默停止，可以使用更明确的继续提示：

```text
继续刚才的任务。不要回复 No response requested，也不要静默停止。请先说明你认为上一轮做到哪里、下一步具体动作是什么，然后继续执行。如果上下文不足，请读取 AGENT_HANDOFF.md 和必要的接力文件恢复状态。
```

### 3. Agent 更换或上下文压缩后恢复

当会话上下文被压缩，或者换了新的 Agent，最危险的是“看起来知道项目，实际上缺少关键状态”。这个 skill 的规则会要求新 Agent：

1. 先读取 `AGENT_HANDOFF.md`。
2. 明确当前目标、状态、下一步和阻塞点。
3. 只读取当前任务相关的源码。
4. 不把接力文档当作源码事实的替代品。

这样能降低两类常见风险：

- 新 Agent 重复做已经完成的工作。
- 新 Agent 基于过期或误解的上下文继续改代码。

### 4. 接力文档修复和瘦身

很多团队一开始会写接力文档，但写久了会变成：

- 聊天总结
- 长日志粘贴
- 没有路径的笼统描述
- 没有原因的决策
- 已经过期的待办
- 互相矛盾的状态

这时可以用：

```text
使用 agent-handoff skill，审查并修复当前项目的 AGENT_HANDOFF.md。
```

skill 会参考 `references/quality.md`，把文档重新整理成可接手的操作状态。

## 安装

### 方式一：作为 Codex 本地 Skill 使用

把仓库克隆或复制到你的 Codex skills 目录：

```powershell
git clone https://github.com/WeirdSky924/agent-handoff-skill C:\Users\<you>\.codex\skills\agent-handoff
```

如果你已经下载到本地，也可以复制：

```powershell
Copy-Item -Recurse -Force E:\_workspace\agent-handoff-skill C:\Users\<you>\.codex\skills\agent-handoff
```

然后在新的 Codex 会话里说：

```text
使用 agent-handoff skill，为当前项目初始化接力机制。
```

### 方式二：作为 Claude Code 个人级 Skill 使用

把仓库克隆或复制到 Claude Code 的个人级 skills 目录：

```powershell
git clone https://github.com/WeirdSky924/agent-handoff-skill C:\Users\<you>\.claude\skills\agent-handoff
```

如果你已经下载到本地：

```powershell
Copy-Item -Recurse -Force E:\_workspace\agent-handoff-skill C:\Users\<you>\.claude\skills\agent-handoff
```

然后在 Claude Code 中可以直接说：

```text
请使用 agent-handoff skill，为当前项目初始化接力机制。
```

或显式调用：

```text
/agent-handoff 为当前项目初始化接力机制
```

### 方式三：作为 Claude Code 项目级 Skill 使用

如果你希望团队成员拉取仓库后都能使用这个 skill，可以把它放进目标项目：

```powershell
mkdir .claude\skills
git clone https://github.com/WeirdSky924/agent-handoff-skill .claude\skills\agent-handoff
```

项目级安装适合团队标准化接力流程。个人级安装适合你在所有项目中复用。

### 方式四：作为 DeepSeek Harness Skill 使用

DSH 个人级安装：

```powershell
git clone https://github.com/WeirdSky924/agent-handoff-skill C:\Users\<you>\.dsh\skills\agent-handoff
```

也可以使用 DSH 支持的共享 Agent Skills 根目录：

```powershell
git clone https://github.com/WeirdSky924/agent-handoff-skill C:\Users\<you>\.agents\skills\agent-handoff
```

项目级安装：

```powershell
mkdir .dsh\skills
git clone https://github.com/WeirdSky924/agent-handoff-skill .dsh\skills\agent-handoff
```

DSH 会默认扫描这些目录，不需要修改 profile、`cordis.patch.yml` 或 `settings.yaml`。安装后可由模型自动加载，也可以显式输入：

```text
/agent-handoff 为当前项目初始化接力机制
```

### 方式五：只使用脚本

如果你不想注