# DeepSeek Harness Lark / 飞书

`@sugarforever/dsh-lark` 是一个 DeepSeek Harness Host 插件。安装后，用户可以直接从飞书或 Lark 与 Harness Agent 对话，并继续使用 Harness 中配置的模型、工具、系统提示和会话存储。

插件使用飞书官方 `@larksuiteoapi/node-sdk` 的 Channel API，通过 WebSocket 长连接接收消息，不需要公网服务器、域名或 Webhook 回调地址。官方 SDK 负责连接、自动重连、消息去重、过期事件过滤、同一聊天的串行处理、消息格式转换和发送回复；插件负责把飞书会话映射到 Harness Session，再把消息交给 Agent。

## 功能

- 支持飞书中国版和国际版 Lark。
- 使用 WebSocket 长连接接收事件，无需公网回调地址。
- 回复会关联原始消息，并保留在原来的话题线程中。
- 可以通过白名单限制群聊和单聊用户。
- 可以沿用 Harness 默认模型，也可以为飞书渠道指定模型。

## 运行要求

- Node.js `^22.19.0` 或 `>=24.0.0`。
- 已安装或能够通过 `npx` 运行 DeepSeek Harness `0.1.0-rc.6` 或更高的 `0.1.x` 版本。
- 一个飞书或 Lark 自建应用。
- 应用已经启用机器人能力。
- 应用使用长连接接收事件，并订阅 `im.message.receive_v1`。

如果尚未运行过 Harness，可以先启动一次 Web Profile：

```sh
npx @deepseek-ai/dsh web
```

首次启动会创建 `web` Profile。默认目录是 `~/.dsh/profiles/web`；如果设置了 `DSH_HOME`，则位于 `$DSH_HOME/profiles/web`。

## 创建飞书应用

以下名称在飞书中国版和国际版 Lark 控制台中可能略有区别，但配置内容相同。

### 创建自建应用

1. 打开飞书或 Lark 开发者后台。
2. 创建一个企业自建应用。
3. 填写应用名称、描述和图标。
4. 进入“凭证与基础信息”，记录 App ID 和 App Secret。

不要把 App Secret 直接写进仓库中的 YAML 文件。后续通过 Harness Settings 页面保存，或者通过启动环境变量传给插件。

### 启用机器人

1. 进入“添加应用能力”。
2. 添加“机器人”能力。
3. 设置机器人名称和头像。

### 添加权限

默认配置下，应用需要开通以下三个权限：

| 权限标识 | 控制台中的权限名称 | 用途 | 是否必需 |
| --- | --- | --- | --- |
| `im:message.p2p_msg:readonly` | 获取用户发给机器人的单聊消息 | 接收用户与机器人的单聊消息 | 是 |
| `im:message.group_at_msg:readonly` | 获取群组中 @机器人的消息 | 接收群聊中明确 @机器人的消息 | 是 |
| `im:message:send_as_bot` | 以应用的身份发消息 | 让机器人回复单聊、群聊和话题消息 | 是 |

飞书控制台中显示的中文名称可能随平台版本略有调整，应以权限标识为准。添加 `im.message.receive_v1` 事件时，控制台通常也会提示补充前两个接收权限。

如果开发者后台支持批量导入权限，可以直接复制下面的配置：

```json
{
  "scopes": {
    "tenant": [
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:send_as_bot"
    ],
    "user": []
  }
}
```

这组配置对应插件的默认行为：接收单聊消息、接收群聊中 @机器人的消息，以及以机器人身份发送回复。导入后仍需在事件订阅中添加 `im.message.receive_v1`，并发布新版本，权限和事件配置才会应用到已安装的机器人。

如果需要让机器人处理群聊中没有 @机器人的普通消息，还要额外开通：

| 权限标识 | 控制台中的权限名称 | 用途 | 是否必需 |
| --- | --- | --- | --- |
| `im:message.group_msg` | 获取群组中所有消息 | 配合 `requireMention: false` 接收群内全部消息 | 仅关闭 @限制时需要 |

`im:message.group_msg` 的权限范围更大，通常需要企业管理员审批。默认的 `requireMention: true` 不需要申请这个权限。

有些企业会直接批准范围更大的 `im:message` 权限，它也可以覆盖消息读取和发送场景，但本插件不要求使用这个宽泛权限。优先申请上表中的最小权限即可。

权限变更可能需要企业管理员审批。测试时如果机器人能够加入聊天，但收不到消息或不能回复，先检查权限是否仍处于待审批状态。

### 配置长连接事件

1. 进入“事件与回调”或“事件订阅”。
2. 在事件接收方式中选择“使用长连接接收事件”。
3. 不要填写 Webhook 请求地址。
4. 添加事件 `im.message.receive_v1`。
5. 保存配置。

长连接模式由插件主动连接飞书，因此本地电脑、内网服务器和没有公网入口的开发环境都可以运行。

### 发布并安装应用

1. 创建应用版本。
2. 提交审核或发布到测试范围。
3. 将应用安装到当前企业或测试企业。
4. 在飞书中找到机器人并发起单聊，或者把机器人加入测试群。

只修改后台配置但没有发布新版本时，事件和权限通常不会在正式应用中生效。

## 安装插件

从 npm 安装到 Harness Web Profile：

```sh
npx @deepseek-ai/dsh plugin --profile web add @sugarforever/dsh-lark
```

Harness 的 Agent、Session、Settings 等服务由 Profile Bundle 在运行时提供。
插件将这些包声明为 optional peer，以适配 DSH 的 Bundle 加载机制；它不会在
Profile 中重复安装另一套 Harness。从 `0.2.3` 起兼容 `0.1.0-rc.7`、
`0.1.2-rc.1` 及稳定的 `0.1.x` 版本，并通过 CI 持续验证最新发布的 Harness
版本，因此升级到后续 RC 通常不需要重新发布插件。

查看已经安装的插件：

```sh
npx @deepseek-ai/dsh plugin --profile web list
```

开发本项目时，也可以安装本地目录：

```sh
git clone https://github.com/sugarforever/dsh-lark.git
cd dsh-lark
npm install
npm test
npm run typecheck
npm run build
npx @deepseek-ai/dsh plugin --profile web add "$PWD"
```

插件安装后保持启用，但在 App ID 和 App Secret 尚未配置时不会建立飞书连接。这样安装完成后就能直接配置，而不必编辑 profile patch。

## 启动 Harness

启动 Web Profile：

```sh
npx @deepseek-ai/dsh web
```

打开 Harness 的 **Settings**，选择 **飞书与 Lark**。这里可以配置 App ID、App Secret、飞书或 Lark 域名、访问策略和 Agent 参数。Provider 和 Model 来自 Harness 当前的模型目录，选择 Provider 后，Model 下拉框只显示该 Provider 的模型；留空时跟随 Harness 默认配置。

点击保存后，普通参数写入 `$DSH_HOME/settings.yaml` 的 `lark-channel` section；App Secret 通过 Harness Credentials 保存到 `$DSH_HOME/.credentials.yaml`，不会写入普通 Settings，也不会从 Host 回显到浏览器。

Secret 输入框为空不代表凭据丢失。页面会明确显示“Secret 已配置”或“Secret 未配置”：

- 已经配置 Secret 时，保持输入框为空并保存其他设置，不会修改或删除现有 Secret。
- 在输入框中填写新值并保存，才会替换现有 Secret。
- 只有点击“删除已保存的 Secret”，才会删除 Credentials 文件中的值。
- 如果 Secret 来自启动环境变量或旧版 patch 中的 `appSecret`，页面会显示只读状态，不能通过 UI 覆盖或删除该来源。

配置或凭据变化后，插件会关闭旧 WebSocket 和会话资源，再创建新的 channel，不需要重启 Harness。

对于 CI、容器或服务部署，也可以继续使用环境变量。默认 CredentialRef 是 `DSH_LARK_APP_SECRET`，启动环境的同名变量优先于 Credentials 文件：

```sh
export DSH_LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
npx @deepseek-ai/dsh web
```

环境变量来源只读，并且在 Harness 启动时冻结。修改它仍然需要重启进程。App ID 等普通参数可以在 profile patch 中作为 composition base 提供，也可以在配置页面中覆盖：

```yaml
- id: lark-channel
  config:
    appId: cli_xxxxxxxxxxxxxxxx
    appSecretRef: DSH_LARK_APP_SECRET
    domain: feishu
```

不要再次使用 `insert` 创建同名实例，否则会出现 `duplicate loader entry id: lark-channel`。

Profile patch 是基础配置，Settings 页面保存的普通参数是覆盖层。已经通过 UI 保存的 `appId`、`domain` 等值优先于 patch；删除对应的 Settings 覆盖后，才会重新使用 patch 中的值。`appSecretRef` 默认保持为 `DSH_LARK_APP_SECRET`，UI 保存的 Secret 会写到这个引用名对应的 Harness Credential 中。

旧版本使用的明文 `appSecret` 仍可作为只读兼容来源，但不建议继续保留。迁移时先在 UI 中保存 Secret 或设置 `DSH_LARK_APP_SECRET`，确认连接成功后，再从 patch 中删除 `appSecret`。

连接成功后，终端会出现：

```text
dsh-lark: WebSocket connected
```

运行期间如果网络中断，官方 SDK 会尝试重新连接，并输出 `WebSocket reconnecting` 和 `WebSocket reconnected`。

## 验证对话

### 单聊

1. 在飞书中打开机器人。
2. 发送一条普通文本消息。
3. 等待 Harness 完成当前 Agent turn。
4. 机器人会回复这次 turn 最后生成的 assistant 文本。

同一个单聊中的后续消息会继续使用同一个 Harness Session，因此能够保留前文。
Harness 重启后，插件会恢复对应的持久化 Session；如果该 Session 已经在当前进程中运行，则直接复用现有 Agent，不会重复创建或恢复。

### 群聊

1. 把机器人加入群聊。
2. 使用 `@机器人` 加上问题。
3. 机器人会回复触发它的那条消息。

默认配置下，没有 @机器人的群消息会被忽略。如果关闭 `requireMention`，还需要确保应用获得接收群内全部消息的权限，并经过企业管理员批准。

### 话题群

话题中的消息会使用 `chat_id + thread_id` 建立独立 Session。不同话题不会共享对话记录，机器人回复会留在原来的话题中。

## 完整配置

下面的例子包含目前支持的所有配置项：

```yaml
- id: lark-channel
  disabled: false
  config:
    appId: cli_xxxxxxxxxxxxxxxx
    appSecretRef: DSH_LARK_APP_SECRET
    domain: feishu
    requireMention: true
    dmMode: open
    groupAllowlist:
      - oc_xxxxxxxxxxxxxxxx
    dmAllowlist:
      - ou_xxxxxxxxxxxxxxxx
    provider: deepseek-official
    model: deepseek-v4-flash
    workspace: /absolute/path/to/workspace
    agentPreset: coding
    errorMessage: 抱歉，处理这条消息时遇到了问题，请稍后重试。
```

| 配置项 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `appId` | 连接时是 | 空字符串 | 飞书或 Lark 应用的 App ID |
| `appSecretRef` | 否 | `DSH_LARK_APP_SECRET` | Harness Credentials 中保存 App Secret 的引用名 |
| `domain` | 否 | `feishu` | 中国版使用 `feishu`，国际版使用 `lark` |
| `requireMention` | 否 | `true` | 群聊是否必须 @机器人 |
| `dmMode` | 否 | `open` | 单聊策略：`open`、`allowlist` 或 `disabled` |
| `groupAllowlist` | 否 | `[]` | 允许使用机器人的群 `chat_id` 列表；空数组表示不限制 |
| `dmAllowlist` | 否 | `[]` | `dmMode: allowlist` 时允许访问的用户 `open_id` 列表 |
| `provider` | 否 | Harness 默认值 | 为这个渠道指定模型 Provider |
| `model` | 否 | Harness 默认值 | 为这个渠道指定模型 |
| `workspace` | 否 | 第一个已注册 Workspace；没有时为 DSH 进程工作目录 | Agent 使用的工作目录；显式路径优先 |
| `agentPreset` | 否 | Harness 当前默认 Preset | Agent 使用的 Preset，决定工具、系统提示等组合 |
| `errorMessage` | 否 | 内置中文提示 | Agent 执行失败时返回给用户的文本，最长 500 个字符 |

`provider` 和 `model` 建议同时设置。如果都不设置，插件会读取 Harness 当前的默认模型配置。

### Workspace 和 Agent Preset

飞书会话创建 Agent 时会沿用 Harness Web 客户端的两项关键行为：挂载 Agent Preset，并把 Session 关联到 Workspace。Preset 提供该会话的工具、系统提示和其他 Agent 级能力；Workspace 提供 `cwd`，并让会话出现在对应工作区中。

- 未配置 `workspace`：使用 Harness Workspace 列表中的第一个工作区。
- 已配置 `workspace`：始终使用该路径；如果它已经注册为 Workspace，Session 同时关联到该 Workspace。
- Harness 尚无 Workspace：回退到启动 DSH 时的进程工作目录。
- 未配置 `agentPreset`：解析 Harness 当前默认 Preset。
- 已配置 `agentPreset`：使用指定 Preset；名称不存在时，本次会话创建会失败并向飞书返回安全错误提示。

如果希望机器人始终操作固定项目，建议显式配置：

```yaml
workspace: /Users/you/github/project
agentPreset: coding
```

升级到包含 Workspace/Preset 关联的版本后，同一飞书聊天会创建新的 v2 Session；旧版本产生的未关联 Session 不会被继续复用。

## 访问控制

只允许指定群聊使用机器人：

```yaml
requireMention: true
groupAllowlist:
  - oc_group_one
  - oc_group_two
```

只允许指定用户发起单聊：

```yaml
dmMode: allowlist
dmAllowlist:
  - ou_user_one
  - ou_user_two
```

完全关闭单聊：

```yaml
dmMode: disabled
```

群聊白名单使用 `chat_id`，单聊白名单使用发送者的 `open_id`。这些标识可以通过飞书 API、事件调试信息或管理员工具取得。生产环境不要开启原始事件日志后长期保留消息内容。

## 会话与并发行为

- 普通单聊和群聊使用聊天级 Session。
- 话题消息使用线程级 Session。
- Session 会挂载所选 Agent Preset，并在能匹配注册 Workspace 时关联到该 Workspace。
- 飞书 SDK 会对同一聊天中的事件串行处理，避免两个 Agent turn 同时修改同一会话。
- 重复事件会在 SDK 的去重窗口内被忽略。
- 超过五分钟的延迟