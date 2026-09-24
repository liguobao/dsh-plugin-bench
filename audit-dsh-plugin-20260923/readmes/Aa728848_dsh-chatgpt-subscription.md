# DSH ChatGPT Subscription

让 DSH（DeepSeek Harness）通过 ChatGPT 订阅使用 Gpt 系列模型的插件。

插件注册 `codex-chatgpt` Provider（显示名 **“Codex（ChatGPT 订阅）”**），以当前 Host 用户的 ChatGPT OAuth 登录态访问模型，并在设置页展示账号信息、连接状态与订阅额度。支持 Windows 与 Linux。

## 目录

- [功能特性](#功能特性)
- [模型目录](#模型目录)
- [环境要求](#环境要求)
- [安装](#安装)
- [使用](#使用)
- [Kimi Code 线路](#kimi-code-线路)
- [Command Code 线路](#command-code-线路)
- [WorkBuddy 线路](#workbuddy-线路)
- [GLM（智谱 Coding Plan）线路](#glm智谱-coding-plan线路)
- [子代理模型授权](#子代理模型授权0215-起)
- [随包分发的 Agent Preset](#随包分发的-agent-preset)
- [升级、降级与卸载](#升级降级与卸载)
- [安全边界](#安全边界)
- [插件路由](#插件路由)
- [开发与验证](#开发与验证)
- [故障排查](#故障排查)

## 功能特性

**登录与会话**

- Authorization Code + PKCE（S256）登录，一次性 localhost 回调；
- 支持 token 刷新、登录取消与账号注销；
- Windows 使用 CurrentUser DPAPI 加密存储 token；Linux 使用当前用户独占的 `0600` 文件存储；明文不发送给 Client；
- 设置页会明确显示当前存储类型，并在 Linux 上提示文件存储未额外加密。

**模型接入**

- 固定 Codex Responses 地址，支持流式文本、reasoning summary、图片输入与工具调用/结果；
- Antigravity（Gemini / Claude）线路同样接受图片输入：DSH 以 `{ type: 'image', attachment }` 下发的粘贴图片会经附件服务读出字节并按 Gemini `inlineData` 发出，读不出的图片降级为一条可见的说明文本而不是被静默丢弃。单次请求的图片 base64 负载超过 12 MiB 时，最旧的图片按上游同款占位文案替换为文本，避免整条请求被体积上限拒绝；
- 原样转发 DSH 暴露的工具 schema；命令工具兼容 `pwsh` / `powershell`、`bash`、`sh` 与 `shell`，并按 PowerShell、Bash 或 POSIX sh 注入对应说明；
- 429/5xx 由 DSH retry policy 接管；401 只强制刷新并重试一次，支持 `AbortSignal`；
- Codex、Code review 及上游返回的额外窗口额度，支持 Credits、月度消费控制与 reset credits 展示；60 秒缓存、15 秒上游节流并遵守 `Retry-After`；
- 提供 ChatGPT 订阅侧 Codex 搜索 provider，可在设置页切换 DSH 默认搜索或 Codex 订阅搜索；
- 新增 `codex_image_generate` 工具，生成图片后通过 DSH 附件系统保存并在会话中渲染；
- 可选 composer 快捷用量徽标，按当前 `codex-chatgpt` 模型显示最紧张窗口的剩余额度。


**Command Code 线路**

- 注册 `command-code` Provider，使用 Command Code 的 Provider API 与账户 API；模型 id 决定线路：`claude-*` 走 Anthropic Messages（`/provider/v1/messages`），其余模型走 OpenAI Chat Completions（`/provider/v1/chat/completions`），因为该 API 会拒绝把模型发到格式不符的端点；
- 浏览器登录复刻官方 CLI 的回环回调契约（`127.0.0.1:5959` 起顺延，`/callback` 接受 Studio 页面的跨域 POST），也可在设置页手动粘贴 API Key；两条路径都先用 `/alpha/whoami` 验证再加密保存；
- 模型目录取自公开的 `/provider/v1/models`，每个模型的 `context_length` 作为默认上下文窗口，可逐模型覆盖；
- **模型能力逐模型查表**（`src/host/command-code/model-catalog.ts`，转录自官方 CLI 的模型注册表）：是否接受图片输入、支持哪些思考档位由该表决定，未知模型回落纯文本。图片能力不能靠厂商/模型名前缀推断——`deepseek/deepseek-v4.1-flash` 与 `deepseek/deepseek-v4-flash-vision-exp` 支持图片而 `deepseek/deepseek-v4-flash`、`deepseek/deepseek-v4-pro` 不支持，`z-ai/glm-5.3-flash` 支持而 `zai-org/GLM-5.3` 不支持；
- 额度与用量来自账户 API 的账单/用量线路，任一条失败不影响其余；
- **瞬时失败按 DSH retry policy 有界重试**：`command-code` 路由显式声明 `normal` 策略（最多 3 次，1.5s 起指数退避、15s 上限、0.2 抖动），覆盖 `RATE_LIMIT`、`SERVER`、`TIMEOUT`、`TRANSPORT`。上游模型供应商临时不可用（502/503/504/500，典型响应体是 `{"error":{"type":"server_error"}}`）被归类为 `SERVER` 并自动重试，429 会带上上游的 `Retry-After` 让退避按对方的节奏走；401/403 与 `ABORTED` 明确不重试；
- 模型勾选（含线路标签）、思考深度、上下文窗口覆盖与额度在「设置 → 订阅服务 → Command Code」标签页中配置，输入框右侧另有额度胶囊。

**Kimi Code 线路**

- 注册 `kimi-code` Provider，接入 Moonshot 的 **Kimi Code 订阅**（`https://www.kimi.com/code`）。它与 Moonshot 开放平台（pay-as-you-go）是两套互不通用的系统：订阅的模型接口是 `https://api.kimi.com/coding/v1`，凭据只来自订阅 OAuth；把开放平台的 key 或 base URL 用在这里会被判为 `401 Invalid Authentication`；
- 登录用 **RFC 8628 设备码流程**（`auth.kimi.com`）：设置页点「设备码登录」后直接展示用户码与一次性链接（浏览器会自动打开），装好后无需回调端口、无浏览器环境也能手工完成；`slow_down` 会按 RFC 调宽轮询间隔，设备码过期会自动重新申请而不是直接失败；
- 访问令牌到期前按 `max(300s, expires_in×0.5)` 自动续期，同进程并发调用共用一次刷新；被拒的 refresh token 进入冷却并提示重新登录；
- **瞬时失败按错误类别重试**（`src/host/kimi-code/adapter.ts`）。上游模型供应商临时不可用（典型是 502 `{"error":{"message":"Upstream model provider is temporarily unavailable. Please try again in a moment.","type":"server_error"}}`）、真正的 429 背压（`too many requests` / `engine is currently overloaded`）、连接失败与流停滞都会走有界退避（最多 3 次，1.5s 起步、15s 上限、0.2 抖动），并遵守上游的 `Retry-After`；而**配额耗尽型的 429、403 的账号额度上限、401 里的套餐权限不足、400 请求格式错误都不重试**——服务把这些含义压进同一个状态码，因此分类读响应正文而不只看状态码，重试无望时直接给出可操作的提示（换模型 / 降上下文 / 等窗口重置 / 重新登录）；
- 模型目录为订阅侧的四款模型：`k3`（1M 上下文，需 Allegretto+；Moderato 上限 256K，故默认按 256K 计算，可用上下文覆盖升到 1M）、`k3-256k`、`kimi-for-coding`（K2.8 Preview）、`kimi-for-coding-highspeed`（约 6× 速度、3× 额度），运行时以 `GET /v1/models` 为准；
- **K3 行为按其官方文档实现**：思考档位只发 \`low\` / \`high\` / \`max\`（其余写法收敛映射，未知档位不发送），关闭思考发 \`thinking:{type:"disabled"}\`，开启时发 \`thinking:{type,effort,keep:"all"}\`；**开启思考时每条 assistant 消息都回传 \`reasoning_content\`**（无推理则回传空串——服务要求的是空值而非省略，否则 400）；不发送 \`temperature\`（采样参数按模型固定，显式值会报错）；工具调用 id 截断到 64 字符；\`stop\` 按上限裁剪为最多 5 条、每条 ≤32 字节，超长整条丢弃（截断的停止串会在错误位置终止生成）；
- **K3 的长思考不会被截断**：输出上限跟随上下文窗口（保留 4096 余量），因为 \`reasoning_content\` 计入输出，固定 32K 会把 \`max\` 档的长推理中途截断并返回 \`length\`；调用方已知 prompt 规模时上限会被下调到放得下，未知时不做猜测；
- **请求体超 2 MB 本地即拒绝**：该端点最常见的 400 是 \`total message size N exceeds limit 2097152\`，官方文案不给建议，这里直接按真实序列化体积拦截并提示压缩会话或检查大工具结果；
- **缓存是自动的，且无法手动干预**：Kimi 按请求内容哈希命中前缀缓存，实测 \`prompt_cache_key\` 与 Anthropic \`cache_control\` 标记**均被忽略**（设与不设、同 key 与异 key 命中的是同一缓存），设备 id 与协议切换也不影响；TTL 实测在 300–1800 秒之间，按 256 token 对齐，\`/messages\` 与 \`/chat/completions\` **共享同一缓存**。真正决定命中率的是**内容稳定性**：同一会话内 \`system\` 或工具列表一旦变化会使整个前缀缓存失效（实测归零），因此应保持工具集合稳定、把新增内容追加在末尾。卡片会显示滚动命中率，方便验证效果；
- **视频输入可用**（`k3`、`kimi-for-coding`）：DSH 的模态词表只有 `text`/`image`，但它是可合并扩展的接口，本插件用 TypeScript 模块增强把它扩到 `video`（**未改动 DSH 任何代码**），因此视频走 DSH 真实的能力通道，而不是只能显示在提示里。适配器把视频映射为服务文档的 `{type:'video_url',video_url:{url:'data:…'}}`。视频与图片**各有独立预算**（图片 2 MB、视频 48 MiB base64，最旧优先省略），请求体校验只在确实带视频时才放宽到 64 MiB。`k3-256k` 只接受图片、文档白名单外的容器、以及未文档化视频内容块的 **Anthropic 线路**，都会把视频降级为明确的文字说明而不是猜字段发出去；
- **`dynamically_loaded_tools`（仅 K3）已实现**：K3 接受**消息级工具声明**（`messages[].tools`），可在会话中途用「无 `content` 字段的 system 消息」注入完整工具定义。官方把「保持顶层 `tools` 字节稳定」列为该特性的目的之一——中途修改/删除已发出的声明会使缓存从该点起失效，而在末尾追加不影响已缓存前缀，所以这是提升缓存命中的正道。声明按请求重发（服务端不保留），且仅在模型声明该能力时发送；
- 额度卡片区分 **5 小时 / 7 天 / 月度（会员共享池）/ 月度（Kimi Code 池）** 四个窗口并显示重置时间，另可显示加油包余额；设置页为「设置 → 订阅服务 → Kimi Code」标签页，对话输入框右侧有该线路的额度胶囊。

**WorkBuddy 线路**

- 注册 `workbuddy-subscription` Provider，接入腾讯 **WorkBuddy / CodeBuddy 订阅**。该 ID 特意与用户常用的自定义 OpenAI 兼容线路 `workbuddy` 分开，安装插件不会覆盖或隐藏原有自定义 API。可直接扫描 CodeBuddy 桌面端已登录的 `*.info` 凭据，也可从设置页选择国区/国际区并通过官方浏览器授权添加账号；插件添加的凭据保存在系统加密存储中（Windows DPAPI / macOS Keychain / Linux Secret Service），token 只留在 Host 进程内，不进入浏览器；
- **多账号号池，与另外四条线路同源**：WorkBuddy 走共享内核 `AccountPoolCore`（`src/host/common/account-pool.ts`）并复用同一张设置卡片（`src/client/common/AccountPoolSection.tsx`），因此具备**顺序耗尽 / 轮询调度 / 粘性会话**三种策略、429 冷却换号、401/403 账号级失效（保留账号、重新登录即恢复）、设为主账号、账号备注、清除冷却与重新登录。桌面端扫描到的账号与插件内添加的账号**在同一号池里参与调度**；
- **桌面账号归 IDE 所有，不可删除**：卡片只对插件自己添加的账号显示「删除」，桌面账号显示「隐藏 / 恢复」——隐藏只把它移出本插件的调度，绝不改动 CodeBuddy 的凭据文件；号池层同样拒绝删除桌面账号（双保险，均有测试）；
- **续期后原子写回**原凭据文件（只改 `auth` 块），以免桌面端掉线——桌面账号的 refresh token 会轮换，若只写进插件自己的加密存储，IDE 手里就只剩一个已作废的 token。同一进程内的并发调用**共用一次刷新**，且不会二次刷新；
- 上游是 OpenAI 兼容的 `POST {backend}/v2/chat/completions`，但有两条硬约束：**只支持流式**（`stream:false` → 400 `code 11101`），且**首条消息必须是 system**（否则国际区返回 400 `code 11128`）。因此请求构造器始终发送 `stream:true`，并在调用方没给系统提示时补一条中性的，避免手搓的一次性请求踩到这条规则；
- **区域是凭据属性，不是请求属性**：`*.workbuddy.ai` / `*.codebuddy.ai` 走国际区 `https://www.<apex>`，其余走国区 `https://copilot.tencent.com`。账号卡片逐条标注每个账号的**国区 / 国际区**并允许选择；切换后，模型目录、额度和后续对话都使用该账号。历史凭据快照按账号身份自动去重。插件托管账号可真正删除；桌面扫描账号只能从本插件隐藏/恢复，永不删除 CodeBuddy 的原文件。两区模型清单不同，把模型发到不服务它的区会返回 400 `code 11102`，因此模型选择器**按当前账号区域过滤**；
- **模型目录取自网关自己的 `/v3/config`**（官方 CLI 启动时读的就是它）：每个模型的真实上下文上限、输出上限、是否接受图片、以及可用的思考档位都在这里，不做任何按模型名猜测。`/v1/models` 在这条线路上是 404，所以此前只能靠内置表——现在内置表只作为离线兜底，且是**从真实 `/v3/config` 转录**的（早期手写版本把 `glm-5.3`、`kimi-k3` 的窗口猜成 200K/256K，实际都是 1M）；
- 目录同时区分**默认服务的上下文长度**与**模型上限**（如 `deepseek-v4.1-flash` 默认 300K、最大 1M）。本线路不发送显式长度参数，所以 DSH 的压缩与溢出判断按**默认服务长度**计算，不会让请求越过后端实际接受的窗口；
- 思考档位**逐模型**取目录声明的档位表，回落顺序为「调用方显式指定 → 用户配置的默认档 → 目录为该模型声明的默认档」。最后一档不能省：上游在请求不带 `reasoning_effort` 时返回**空的 `reasoning_content`**（实测同一提示：不带字段 0 字符，带字段 130–215 字符），不发送就等于静默丢弃模型的思考。目录里的单个 `effort` 字段是**默认值**，既不是完整档位表也不是「只此一档」：实测这类模型接受 `low` / `high` / `max`，其余取值会被上游收敛到最近的档位，因此它们使用这三档的标准表（`WORKBUDDY_STANDARD_EFFORTS`）；显式声明了 `supportedEfforts` 的模型则原样采信。目录给出的**默认档**也可能落在档位表之外（如 `minimax-m3`、`kimi-k3`、国区 `glm-5.3` 都报 `medium` 却只有三档），这种值会被收敛到最近的档位——否则默认档会被判为不支持而丢弃，请求不带 `reasoning_effort`，上游返回**空的 `reasoning_content`**。不在该模型档位集合内的取值会被忽略而不是发出去（上游对不支持的档位返回 `code 11150`）；
- **瞬时失败按错误类别重试**（`src/host/workbuddy/adapter.ts`）。上游 5xx 与 `code 11134` 归为 `SERV