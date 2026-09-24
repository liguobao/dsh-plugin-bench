# dsh-memoir

[![npm version](https://img.shields.io/npm/v/dsh-memoir.svg)](https://www.npmjs.com/package/dsh-memoir)
[![npm downloads](https://img.shields.io/npm/dm/dsh-memoir.svg)](https://www.npmjs.com/package/dsh-memoir)
[![license](https://img.shields.io/npm/l/dsh-memoir.svg)](./LICENSE)

中文 · [English](./README.en.md) · [更新日志](./CHANGELOG.md) · [Releases](https://github.com/Qinling-Melon-Farmers/dsh-memoir/releases)

**DeepSeek Harness（DSH）的本地优先、跨会话项目记忆插件。** 它把 Agent 已确认的工作结论、经验教训和后续行动持久化，在新会话中注入有界且缓存友好的 Hot Memory，并通过本地 BM25 排序召回长尾历史。

无需 embedding、向量数据库或云端记忆服务；npm 包零捆绑运行时依赖，DSH peer 由宿主提供。

> [!IMPORTANT]
> **0.8.0 要求 DSH `>=0.1.7-rc.1 <0.1.8-0`**，已针对 `0.1.7-rc.1` 完成 Windows/WSL 自动化回归与 Windows 隔离宿主验证。旧 DSH 0.1.5 请固定安装 `dsh-memoir@0.7.1`，不要直接升级 latest。真实浏览器交互与付费模型端到端验证尚未完成。
>
> `dsh-memoir@0.7.1` 修复重启和内存淘汰后旧会话快照丢失（#10），支持 DSH **0.1.5-rc.1 / rc.2**。要求 `>=0.1.5-rc.1 <0.1.6-0`；请先核对宿主版本。旧 DSH 0.1.2 用户固定使用 `0.6.2`，0.1.1-rc.2 用户固定使用 `0.5.6`；这些旧版未包含本次修复。

```bash
npm install --global @deepseek-ai/dsh@0.1.7-rc.1
dsh plugin --profile web add dsh-memoir@0.8.0
```

重启 `dsh web` 即可。记忆保存在本机，不会随插件升级或卸载自动删除。

## 为什么选择 dsh-memoir

| 能力 | 用户得到什么 |
| --- | --- |
| 本地优先 | JSON 单一事实源与项目内 `PROJECT_MEMORY.md`；不上传记忆，不依赖外部服务 |
| 自动蒸馏提醒 | 顶层 Agent 完成有效工作回合时提醒归纳，由 `memoir_record` 透明落盘；跳过 idle、aborted、subagent 和已记录回合 |
| 有界 Hot Memory | 只把高价值记忆放进 system prompt，受 token 预算硬限制；同一会话冻结前缀以提高 prompt-prefix cache 命中 |
| BM25 排序召回 | 中文短语、英文关键词、代码标识符和路径都可检索；跨项目 Top-K 与查询 LRU 缓存共用同一引擎 |
| 可治理的记忆 | 重要度、置顶、标签、归档、恢复和 supersede 生命周期；相似写入必须显式更新、替代或并存 |
| 可追溯 | Agent 写入记录可信 session/turn 来源，Web 面板可复制并尽力跳回原会话 |
| 完整 Web GUI | 中英双语项目/全局浏览、排序搜索、编辑、Hot Memory 预览、诊断和实时设置；可独立选择 Agent 侧中文或英文 |

适合需要“新 Agent 接手时继续理解项目”的个人或本地开发工作流。它不是原始聊天记录备份、多人云同步服务或向量语义知识库。

![dsh-memoir v0.6.1 按项目折叠的全局记忆](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.6.1/picture/v0.6.1-global-project-groups-zh.png)

## 工作原理

```text
有效工作回合
    │  自动蒸馏提醒
    ▼
memoir_record / memoir_update
    │
    ├── ~/.dsh/dsh-memoir.json       完整结构化历史（SSOT）
    ├── <项目>/PROJECT_MEMORY.md      可读、可提交的投影
    └── Retrieval Index              倒排索引 + BM25 + 查询缓存
              │
              ├── Hot Memory Selector ──> 有界 system-prompt 注入
              └── memoir_read / Web ────> 按需召回长尾历史
```

完整历史与 Hot Memory 是两层数据：

- **Full Memory** 保留全部记录，用于 GUI、人工审阅、Markdown 投影和排序检索。
- **Hot Memory** 只选择预算内的 actions、lessons 与 recent state；不会把整个 `PROJECT_MEMORY.md` 塞进 prompt。
- **Session Snapshot** 按会话持久化冻结注入文本，重启恢复与内存淘汰后仍复用原文。新写入立即可被工具和 GUI 读取，但自动注入从下一个新会话开始更新；恢复失败会显式报告降级。

### 快照恢复与清理（0.7.1）

- 默认目录：`$DSH_HOME/dsh-memoir.json.snapshots/`；自定义 storePath 时为 `<storePath>.snapshots/`。记录按数据源/设置文件的哈希、语言和会话哈希分开保存；按需读取，不在启动时加载全部文件。
- `sessionSnapshotMax` 只限制内存 LRU。磁盘记录无自动 TTL，不随缩容、卸载或清理内存删除；备份记忆时请一起备份该目录。需要回收磁盘时先停止相关 DSH 进程并备份，再人工删除确定不再恢复的记录。删除后再次访问会建立新基线。
- 语言切换使用独立快照空间；切回原语言会复用其旧基线。预算修改仅影响新基线；fork/新 session id 不借用父会话快照。
- 升级前已丢失快照的旧会话，首次使用新版只能按当前记忆建立一次新基线；不从历史 system prompt 猜测截取原文。读取损坏、权限或锁失败时保留原文件，回退到进程内冻结；诊断页和日志会提示重启稳定性降级。
- 单条文本上限 256 KiB，记录上限 2 MiB；超限走同样的可诊断降级。POSIX 新目录/记录使用 0700/0600，Windows 权限仍由目录 ACL 管理。记录含记忆文本，应视为用户数据。
- 本修复消除可恢复快照的重复重建，不能保证提供商仍保留 KV cache 或保证命中率。

## Agent 工具与记忆生命周期

| 工具 | 用途 |
| --- | --- |
| `memoir_record` | 写入 work / lessons / actions / note；写前返回可解释的相似或冲突候选 |
| `memoir_update` | 保留 id 和创建时间，更新正文、分类、重要度、标签与生命周期 |
| `memoir_read` | 在 project（默认）/ global / all 范围内进行 compact 或 full 的本地排序召回 |

每条记忆可设 1–5 重要度，默认 **3** 代表中性优先级；置顶会获得额外 Hot Memory 权重。默认只召回 `active`，被归档或替代的历史仍可检查和恢复，不会被自动删除。

相似记忆治理复用 BM25 候选，再融合标题相似度与 Token Jaccard。插件只提示疑似重复或冲突，不自行判断真伪；调用者必须选择：

- `update`：原地更新现有记录；
- `supersede`：保留旧历史并标记已被新记录替代；
- `force-record`：确认两条都应存在。

## 自动蒸馏

v0.6.2 的诊断页显示最近触发或跳过原因及本次进程计数。已经调用 `memoir_record` 或 `memoir_update` 的回合不再提醒；提交提醒不代表写入已完成。Agent 销毁会清理门控状态，最多保留 1024 个最近活动 Agent（淘汰后不再保留其回合水位和冷却）。关闭自动蒸馏后仍可手动记录。

0.8.0面向 DSH `0.1.7-rc.1`；0.7.1 的历史验证范围为 `0.1.5-rc.1 / rc.2`。BM25 是词项召回，不能保证无共同词项的跨语言语义匹配；提炼质量提示也不能替代事实核验。

自动蒸馏是可观察的 Agent 收尾提醒，不是后台静默抓取聊天内容。默认 `1 / 0 / 1` 表示：每个有效 worked turn、无额外冷却、至少一次工具调用即可提醒。

`autoDistillEvery`、`autoDistillCooldownMin`、`autoDistillMinTools` 三个条件按 AND 判定并按 Agent 隔离。idle、aborted、subagent 和已调用 `memoir_record` 的回合不会触发；冷却只在提醒成功后更新。所有频率参数都可在 GUI 中即时修改。

`language` 独立控制 Agent 可见的工具描述、参数说明、蒸馏提示、工具结果、Hot Memory / `PROJECT_MEMORY.md` 标题以及校验与治理错误。默认 `zh` 保持向后兼容，也可在 GUI 中切换为 `en`；切换后工具 schema 与后续提示即时更新，不要求重启 DSH。

## 本地召回与缓存

- 中文 2/3-gram + 英文单词 + 代码/路径标识符分词；
- BM25 文档侧保留真实词频，标题 2.5× 加权，另有精确短语、分类与时间权重；
- 标题与正文独立长度归一化；
- project / global / all 共用去重后的全局 Top-K；
- epoch 感知、1 小时时间桶的 LRU 查询缓存；`limit` 与输出详略不进入缓存键，因此不同输出形态共享排序结果；
- GUI 和 `memoir_read` 使用同一个 RetrievalEngine，并暴露 hits、misses、evictions、命中率与最近查询耗时。

固定质量集的 Top-5 命中率为 100%，仓库门禁要求不低于 90%。

## Web GUI

安装到 DSH alpha 的 `web` profile 后，Memoir 通过官方 slot 注册原生「记忆」会话视图和「记忆」Settings 分区；布局、导航与卸载生命周期均由 DSH shell 管理，不再通过 DOM 选择器接管旧侧边栏。

- 项目记忆与所有项目的全局记忆；全局视图按项目默认折叠并显示完整生命周期计数；
- 状态、分类和关键词筛选，BM25 分数展示；
- 新增、编辑、置顶、归档、恢复和替代；
- session/turn 来源复制与尽力跳转；
- Hot Memory Inspector：下一会话将继承什么；
- Retrieval Diagnostics：索引、查询缓存、最近查询和会话快照；
- 常驻 `记忆浏览 / 记忆设置 / Hot Memory / 诊断` 二级导航，各功能区拥有独立有界滚动位置；
- 每批渐进展示 20 条记忆或 20 个项目，长正文默认折叠为六行并可显式展开；
- 使用 DSH 原生 composer-overlay 契约，长列表可完整滚动且最后一项不会被对话输入框遮挡；
- 页签支持方向键、Home、End，项目折叠具备 `aria-expanded` 与清晰焦点状态；
- GUI 跟随 `<html lang>` 在中文和英文间即时切换；Agent 侧语言由独立的 `language` 设置控制。

<details>
<summary>查看更多 GUI 截图</summary>

![v0.7.1 在 DSH rc.2 中的快照持久化诊断](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.7.1/picture/v0.7.1-snapshot-persistence-zh.png)

![v0.7.0 在 DSH 0.1.5-rc.1 中的原生记忆设置](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.7.0/picture/v0.7.0-dsh015-settings-zh.png)

![v0.6.2 自动蒸馏生命周期诊断](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.6.2/picture/v0.6.2-distill-diagnostics-zh.png)

![v0.6.1 常驻功能导航与实时设置](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.6.1/picture/v0.6.1-settings-navigation-zh.png)

![v0.6.1 对话视图滚动到底且避让输入框](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.6.1/picture/v0.6.1-conversation-scroll-zh.png)

![DSH alpha.2 原生记忆会话视图](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.6.0/picture/v0.6.0-alpha2-native-zh.png)

![记忆生命周期与相似治理](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.5.6/picture/v0.5.4-memory-management-zh.png)

![Settings 设置卡](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.5.6/picture/v0.5.6-settings-card-zh.png)

![侧边栏对齐](https://raw.githubusercontent.com/Qinling-Melon-Farmers/dsh-memoir/v0.5.6/picture/v0.5.5-sidebar-parity-zh.png)

</details>

## 安装与兼容性

| 渠道 | DSH 基线 | 安装方式 | 状态 |
| --- | --- | --- | --- |
| npm `latest`（`0.8.0`） | `>=0.1.7-rc.1 <0.1.8-0` | `dsh plugin --profile web add dsh-memoir@0.8.0` | 0.1.7 兼容线 |
| npm 固定版 `0.7.1` | `>=0.1.5-rc.1 <0.1.6-0` | `dsh plugin --profile web add dsh-memoir@0.7.1` | 旧 0.1.5 维护线 |
| npm 固定版 `0.6.2` | `>=0.1.2-alpha.2 <0.1.3` | `dsh plugin --profile web add dsh-memoir@0.6.2` | 旧 0.1.2 兼容线 |
| npm 固定版 `0.5.6` | `0.1.1-rc.2` | `dsh plugin --profile web add dsh-memoir@0.5.6` | rc2 兼容线 |
| 源码 `v0.8.0` | `>=0.1.7-rc.1 <0.1.8-0` | 本地构建 + `link:` | 开发调试，不兼容旧 0.1.5 / 0.1.6 |

需要 Node.js `^22.19.0 || >=24.0.0`。0.7.1 继续使用原生 `conversation.view` / `settings.section` 与 `snapshotEvents()`。DSH 0.1.5 的会话日志升级至 V3；其迁移与 Memoir 的 store v4 / settings v3 是独立格式。升级 DSH 前备份 DSH_HOME，迁移后的 DSH 会话不能承诺被旧宿主读取。Memoir 本次不迁移或清空记忆，也不启用新动态提示词行为；既有会话快照语义保持不变。

<details>
<summary>从源码安装</summary>

已发布 0.7.1 源码（旧 DSH 0.1.5）：

```bash
git clone --branch v0.7.1 https://github.com/Qinling-Melon-Farmers/dsh-memoir.git
cd dsh-memoir
pnpm install --frozen-lockfile
pnpm run build
npm install --global @deepseek-ai/dsh@0.1.5-rc.1
dsh plugin --profile web add "link:/absolute/path/dsh-memoir"
```

</details>

0.8.0使用原生 `uiWorkspace` 导航、`conversation.view` / `settings.section` 和 Session V4 专属蒸馏来源。来源链接打开会话，回合编号可复制；不再通过全局 DOM 自动滚到回合，避免多会话串扰。`snapshotEvents()` 仍在使用（宿主已标记弃用但尚未移除），公开异步 projection 迁移列入后续版本。Memoir 数据格式不变；升级 DSH 前备份 DSH_HOME，其 Session V4 迁