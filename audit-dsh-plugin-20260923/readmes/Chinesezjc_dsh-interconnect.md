# dsh-interconnect

跨实例消息互通与事件通知插件，用于 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (DSH)。
让一个 DSH 实例能向同一个实例、另一台机器、或另一台机器上的别的 DSH 实例发送消息、探测活性，并在实例之间双向推送事件。

> **项目状态（2026-09-16）**：本仓库是该插件的**树外（out-of-tree）主源**。并入 DSH monorepo 的计划（PR #3243）已按「保持树外」的评审意见关闭；插件继续经 npm 分发（`dsh-interconnect`），并由团队内部的插件集合仓以 git submodule 引用本仓库。

## 包含三个插件

**`interconnect`** —— host 服务（`ctx.interconnect`）：

- 全走持久 WebSocket 链接：跨实例、跨机器投递消息、枚举 live session、探测活性（`send`/`reply`/`ping`/`list` 经 `/interconnect/link` 的 `msg`/`query` 帧）
- `/interconnect/link` WebSocket 端点：双向实时事件推流，含心跳与指数退避重连；也承载
  `send`/`reply` 消息（`msg`/`msg-result` 帧，WS 优先 + HTTP 回退）
- 事件 fan-out（HTTP + WebSocket），入站事件以 `interconnect/event` 发出
- 共享密钥鉴权（`DSH_INTERCONNECT_TOKEN`，bearer，fail-closed，timing-safe 比较）

**`tool-interconnect`** —— 模型可见工具：

- `interconnect_send`：向对端实例的指定 session 投递消息；可选 `delivery` 选投递模式、`resume` 唤醒离线 session
- `interconnect_list`：列出对端实例的 live session（id + 标题 + 状态），用于在不预先知道 session id 时寻址
- `interconnect_ping`：探测对端实例活性与身份
- `interconnect_reply`：向记录过的发送方回传消息，只需文本；回信 session 是本 agent 自己的，无需再次寻址

**`skill-interconnect`** —— 配套 skill：

- 向模型注册 `dsh-interconnect` skill，说明 `list`/`ping`/`send`/`reply` 的完整用法、
  投递模式、`resume` 唤醒语义与失败处理。
- 明确告知模型：`interconnect_send` 会自动注入发送方的 `instanceId` 和 `sessionId`，
  接收方凭记录的 sender 即可用 `interconnect_reply` 回信，不需要手工传地址。
- 依赖 `interconnect` 服务，只有传输层存在时才注册进 `ctx.skills`。

## 用法

### 寻址（0.9 起用 instanceId，全走持久链接）

从 0.9 起，**传输只走 WebSocket 持久链接，不再有 HTTP 端点**，寻址参数从 `baseUrl` 改为 `instanceId`：

- `interconnect_send(instanceId="peer", sessionId=..., text=...)`
- `interconnect_ping(instanceId="peer")`
- `interconnect_list(instanceId="peer")`
- `interconnect_reply(text=...)`（只需文本；回信 session 是本 agent 自己的，目标从记录的 sender 解析）

`instanceId` 是 `interconnect` 行 `peers` 映射里的键；真正用来拨号的 origin 由该映射的值给出（例如隧道端点 `http://127.0.0.1:13080`），**instanceId 本身从不出现在线上**，也不参与路由——origin 才是唯一的拨号依据。到**未配置 / 未联通**的对端 `send`/`ping`/`list` 返回 `unreachable`（无 HTTP 回退）。

`interconnect_list` 返回对端**当前 live** 的 session，每一行的 `sessionId` 在调用时刻都是合法的投递目标：

```
session-264d37b0-…  重构 interconnect 插件  [idle]
session-b07326da-…                          [running]
```

`title` 与 `status` 是尽力而为的：标题来自可选的 title projection 服务，对端没装该服务、或
该 session 还没有标题时，**整个键不出现**（而不是空字符串），所以「无标题」与「该对端不提供
标题」可以区分。projection 抛错只会让那一行降级成只有 id，不会让整个列表失败。

只列 live session 是有意的：`send` 能到达的正好是这些。对端存在但没有运行 agent 的 session
不会出现在列表里，也收不到消息。

答案有双重上限：行数（`MAX_LISTED_SESSIONS`，100 行）与字节预算（`MAX_LIST_ROWS_BYTES`，等于链路
帧上限减去 4 KiB 的 `query-result` 信封）。整帧必须待在链路的帧上限内，ws 对超限帧会直接关闭
链路，所以 live session 极多、或标题很长时，对端只回答能装下的前若干行，而不是把传输打断。
对端不上报截断标志，所以 `interconnect_list` 只在收到的行数正好等于该上限时追加一行提示
（`100 of possibly more live sessions`）——满页**可能**被截断，缺失的目标仍可能 live。
ping 与 list 的答复还会按调用方问的 kind 校验形状，形状不符按「无答复」处理（对应 `unreachable`）。

### 回复（`reply`）

`send` 的线负载带一个 `sender` 身份（**无地址**：`instanceId` + `sessionId`），收到消息的
instance 会按「本地 session id → 该 sender」记下这份身份。之后那个 session 回信**只需要文本**：
回信 session 就是执行 `interconnect_reply` 的 agent 自己的 session，工具据此查出记录的 sender，
不用再次给出本地 session id、对端 instanceId 或远程 session id——回信走的是本机到那个
instance 的持久链接。

```text
# 源实例 A 指定目标 B 的 session，并带上自己的身份（无 baseUrl）
interconnect_send(instanceId="b", sessionId=B-sess, text="…", sender={instanceId:A, sessionId:A-sess})

# B 回传：只给文本，回信 session 即执行该工具的 agent 自己的 session
interconnect_reply(text="reply")
```

- `sender` 是**自报**的，只用于 reply 归因与寻址，**不是**路由或鉴权依据——连接本身仍由
  共享密钥在每个 origin 上独立鉴权。
- 回复的消息也带 `sender`（本机恒带，不再需要配置 origin），所以对话可双向多轮延续。
- 只有当入站 send **带了 `sender`** 时 reply 才有目标；对端版本没带、或本 session 从未收过
  互联消息时，`reply` 返回 `delivered: false, reason: "no-sender-known"`。
- `sender` **不进模型上下文**（和 `source` 一样只落到持久化日志与 UI 归因）——这条消息的
  内容字面就是 wire 上传来的 `text`，模型看到的仍是普通 user 文本，只是不带任何结构化的
  发送方标记。

### 消息信道：全走 WS（`msg` / `query` 帧）

从 0.9 起**不再有任何 HTTP 端点**——`send`/`reply`/`ping`/`list` 全部在持久 WebSocket 链路
（`/interconnect/link`）上完成。`peers` 映射在激活时**自动 `link()` 每个对端**（心跳 + 指数退避
重连沿用既有实现），寻址按 `instanceId` 查对应链接。

| 帧 | 方向 | 作用 |
|---|---|---|
| `hello` | 双方 | 拨号方自报 instance id |
| `event` | 双方 | 生命周期事件推流 |
| `msg` | 请求方 → 接收方 | 携带 `kind`（`send`/`reply`）、`sessionId`、`text`、`sender`/`delivery`/`resume`、`reqId` |
| `msg-result` | 接收方 → 请求方 | 与 `reqId` 对应的 `SendResult` |
| `query` | 请求方 → 接收方 | `ping` / `list` / `event` 发现与事件查询 |
| `query-result` | 接收方 → 请求方 | 与 `reqId` 对应的查询结果 |

- **出站**：`interconnect_send`/`interconnect_reply`/`ping`/`list` 都发对应帧并等待匹配 `reqId`
  的结果（受 `requestTimeoutMs` 约束）。到**未配置或未联通**的对端直接返回 `unreachable`——
  **没有 HTTP 回退**，这是 0.9 的破坏性变化。
- **入站**：`msg` 帧携带 `send`，走 `deliver` 逻辑（sender 记录、subagent 封栏等），结果经同一 socket 回 `msg-result`；`query` 帧回 `query-result`。
- 心跳与指数退避重连沿用既有实现。

### 投递失败的原因

`delivered: false` 单独一个布尔值无法据以行动，因为不同失败需要不同应对，所以
`SendResult.reason` 会指明是哪一种：

| `reason` | 含义 | 应对 |
|---|---|---|
| `session-not-live` | 对端**答复了**，但那个 session 没有运行中的 agent | 重试同一个 id 无用；用 `interconnect_list` 换目标，或带 `resume` |
| `unreachable` | 没拿到可用答复（传输失败，或鉴权被拒） | 目标 session 可能完好，重试可能成功 |
| `resume-refused` | 请求了唤醒，但对端不允许（`allowResume: false`） | 再带 `resume` 也没用 |
| `resume-failed` | 允许唤醒且尝试了，但没得到 live agent（无此持久化 session，或被别的 owner 持有） | 换目标 |
| `session-owned-by-subagent` | 该 session 属于 subagent 路由，投递权在它的父 agent | 通过父 agent 触达，别直接投 |
| `no-sender-known` | `reply` 指向的本地 session 从未记录过发送方（它没收到过带 `sender` 的消息，或对端版本过旧没带 `sender`） | 先用 `interconnect_send` 主动建立联系 |

`reason` 恰好在 `delivered` 为 false 时出现。

只有真的「尝试唤醒但失败」才是 `resume-failed`。没装 api-proxy 的部署里，`agent` lookup
退化成一次 registry 查询、根本没有唤醒能力，这时报 `session-not-live`——否则会让调用方去重试
一个永远不可能成功的操作。

### subagent 会话不可直投

`interconnect_send` 不会往 subagent 拥有的 session 里投递，`interconnect_list` 也不会把它们
列出来。那类 session 的投递权属于它的父 agent，从这里 splice 进 inbox 会和父 agent 抢。判定
逻辑镜像 Host 的 `hasApiSessionSubagentOwner`（`@deepseek-ai/dsh-api-session-controller`）：
Host 在 0.6 之后把这个谓词从 `@deepseek-ai/dsh-api-remotes` 移走，且没有公开导出——桌面端和
`npx @deepseek-ai/dsh web` 运行时里没有任何可 import 的 Host 绑定，所以这里逐字复制一份
（`isSessionOwnedBySubagent`，见 `src/interconnect/index.ts`）。这是安全规则，Host 改动该规则
时必须同步此副本；tests 覆盖 origin=subagent 与 parent-owned 两条封栏分支。

已实测：起一个真实 subagent 后，`interconnect_list` 不包含它；直接 `send` 到它的 id 返回
`session-owned-by-subagent`，消息**没有**进入 inbox。

### 唤醒离线 session（`resume`，默认关）

`SendPayload.resume: true` 让对端唤醒一个已持久化但没有运行 agent 的 session。

**默认关闭是有意的。** 实测确认：消息投递到 session 后会触发一次**完整的 agent 回合**——
`wakeDriver()` → `kick()` → `turn()` → `llm.stream()`，即一次计费的模型调用，且 assembly
里带着该 session 的完整工具集。在一个用户没打开、看不到、也无法中断的会话里启动这些，和
「推一下已经开着的会话」不是一个量级，所以必须由发送方显式请求。

两侧都有控制权：

- **发送方**按消息决定 `resume`（默认不唤醒）
- **接收方**用 `Config.allowResume`（默认 `true`）一票否决——因为花钱和跑工具的是它那台机器；
  拒绝时在跑 lookup 之前就短路，回 `resume-refused`

唤醒**不是**调本插件的 `ctx.agents.resume()`，而是走 Host 已配置的 `agent` lookup
（`typert.lookups.get('agent')`）。这一点是关键：`resume()` 返回的 handle 由**调用方
context** 拥有，实测确认插件 fiber 被 dispose 时会把 resume 出来的 agent 和 session 一起
拆掉（同一调用改用根 ctx 则两者都存活）。交给 Host 的 resolver 之后 owner 是 api-proxy，
而且它会按 session 日志里记录的 preset 重建工具集——不是空壳。

没有 Host lookup 的部署（headless、无 api-proxy 的 profile）会降级为 `session-not-live`，
不会报错。

唤醒**只把消息放进 inbox**，是否真的开始处理取决于 `delivery`：

```text
# 唤醒并让对方实际处理（会起一个计费回合）
interconnect_send(instanceId="peer", sessionId, text, resume=true, delivery="followup")

# 唤醒但不起回合：只写入上下文，等对方下次被唤醒时一起读
interconnect_send(instanceId="peer", sessionId, text, resume=true, delivery="inject")
```

已实测：`resume=true` + `inject` 之后目标从非 live 变 live（`interconnect_list` 计数 +1），
且该 session 日志里只多一条 `agent/inbox/spliced`、**后面没有 `turn/start`**。

**已知限制**：磁盘格式过旧的 session 无法唤醒，返回 `resume-failed`。这不是本插件的限制——
Host 自己的 resume 路径对同一个 session 报 `SessionFormatUnsupportedError`，同样失败。

### 投递模式

`delivery` 的三个取值各自对应一个 `Agent` 方法，即 `(inbox target, wakeup)` 组合：

| 模式 | inbox target | 唤醒 | 行为 |
|---|---|---|---|
| `followup` | `next-turn` | 是 | 排队成独立一轮，等接收方当前那轮结束 |
| `steer` | `next-step` | 是 | 插进运行中那轮的最近 step 边界，不等整轮结束；接收方 idle 时起新一轮 |
| `inject` | `next-step` | 否 | 只写入上下文，不唤醒 idle 的 agent，可能一直不被读到 |

紧急程度属于单条消息而非整条链路，所以发送方可以按消息覆盖接收方的默认模式；不带
该字段时沿用接收方 `Config.delivery` 的配置。`SendResult.delivery` 回报实际生效的
模式，发送方据此判断覆盖是否被采纳。

## 配置

`interconnect