# MCP连接器：在 DeepSeek Harness 接入、查找和排障 MCP Server

> DeepSeek Harness 的 MCP 接入与管理面板：超百个 MCP连接器，一个入口完成 MCP Server 授权配置、跨连接工具搜索与连接排障。

从持续更新的连接器目录接入 MCP Server；跨当前范围内已启用连接查找工具，查看易读参数、来源和最后成功缓存时间，并在发现异常时检查连接或重新发现工具。支持 OAuth 2.0 PKCE、API Key、Streamable HTTP/stdio 与 `mcpServers` JSON 导入。

OAuth 是否可用取决于服务商的客户端注册、账号权限与授权政策；连接已保存、工具已发现和业务调用成功应分别验证。

> 注：“技能扩展”指通过 MCP 工具和 Prompt 扩展智能体能力，本包不会伪装成独立 DSH Skill。

[English](README.en.md)

### 工具查找与故障处理

在“工具”页统一查找当前工作区可见、已启用连接的工具。输入工具名或描述，再按连接、服务和最近发现状态筛选；点击“参数详情”查看类型、必填项与嵌套结构。未选择工作区时，仅展示全局连接。

结果标注来源和最后成功缓存时间。发现失败时仍可查看已有缓存，但不代表服务当前可调用。展开“连接状态与故障处理”，按建议使用“检查连接”或“重新发现工具”。健康连接五分钟后到期，页面保持连接时后台检查到期任务；失败时退避，鉴权失败暂停自动重试。

详见[工具工作台教程](docs/USER-GUIDE.md#51-工具工作台统一查找工具)。工具页用于发现与诊断，不执行目标工具；参数摘要与原始安全缓存均有裁剪边界。

[用户手册](docs/USER-GUIDE.md) · [第三方连接器上架指南](https://github.com/duhu2000/dsh-mcp-connector-registry/blob/main/docs/ONBOARDING.md) · [首次贡献](docs/FIRST-CONTRIBUTION.md) · [参与贡献](CONTRIBUTING.md) · [问题反馈](https://github.com/duhu2000/dsh-mcp-connector/issues)

[![CI](https://github.com/duhu2000/dsh-mcp-connector/actions/workflows/ci.yml/badge.svg)](https://github.com/duhu2000/dsh-mcp-connector/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/dsh-mcp-connector.svg)](https://www.npmjs.com/package/dsh-mcp-connector)
[![npm downloads](https://img.shields.io/npm/dm/dsh-mcp-connector.svg)](https://www.npmjs.com/package/dsh-mcp-connector)
[![GitHub stars](https://img.shields.io/github/stars/duhu2000/dsh-mcp-connector?style=flat)](https://github.com/duhu2000/dsh-mcp-connector/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/duhu2000/dsh-mcp-connector?style=flat)](https://github.com/duhu2000/dsh-mcp-connector/forks)
[![GitHub Release](https://img.shields.io/github/v/release/duhu2000/dsh-mcp-connector)](https://github.com/duhu2000/dsh-mcp-connector/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Registry connectors](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fduhu2000%2Fdsh-mcp-connector-registry%2Fmain%2Fcatalog-stats.json&query=%24.registryCount&label=Registry%20connectors&color=5865f2)](https://github.com/duhu2000/dsh-mcp-connector-registry/blob/main/catalog-stats.json)
[![Marketplace cards](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fduhu2000%2Fdsh-mcp-connector-registry%2Fmain%2Fcatalog-stats.json&query=%24.marketCount&label=Marketplace%20cards&color=16a34a)](https://github.com/duhu2000/dsh-mcp-connector-registry/blob/main/catalog-stats.json)

## 30 秒开始

```bash
dsh plugin --profile web add dsh-mcp-connector
```

安装或升级后完全重启 DeepSeek Harness Desktop 或 `dsh web`，然后打开左侧「🧩 MCP连接器」；也可从“设置 → 插件 → 插件配置 → MCP连接器”直接打开。

首次使用建议依次确认：连接已保存且范围正确 → “工具”页能找到预期工具与来源 → 在正常 DSH 会话中通过 Host 审批链完成一次服务商许可的只读调用。缓存可见不等于当前服务可调用。

按任务阅读：[迁移现有 `mcpServers` JSON](docs/tutorials/JSON-MIGRATION.md) · [OAuth 授权诊断](docs/tutorials/OAUTH-DIAGNOSTICS.md) · [跨连接找工具与恢复](docs/tutorials/TOOL-SEARCH-RECOVERY.md)。

![MCP 连接器 43 秒演示](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/demo.gif)

如果它帮你更快地接入 MCP Server，欢迎 [GitHub 点个 Star](https://github.com/duhu2000/dsh-mcp-connector/stargazers)、[提交新的连接器](https://github.com/duhu2000/dsh-mcp-connector-registry/blob/main/docs/ONBOARDING.md)或[参与贡献](CONTRIBUTING.md)。

## MCP连接器能做什么

| 能力 | 用户得到什么 |
|---|---|
| 持续更新的连接器目录 | 浏览精选与 9 类业务连接器；Registry 更新后刷新即可获取新卡片 |
| 多种接入方式 | 使用 OAuth 2.0 PKCE、API Key、Streamable HTTP/stdio 或 `mcpServers` JSON 接入 |
| 跨连接工具查找 | 在当前范围内已启用连接的最后成功缓存中按名称或描述搜索，并按连接、服务和状态筛选 |
| 易读参数与来源 | 查看类型、必填、枚举、嵌套摘要、来源、缓存时间及安全裁剪后的 Schema |
| 连接排障 | 根据明确的阶段和错误码检查连接或重新发现工具，同时保留可用的最后成功缓存 |
| 作用域与治理 | 管理 project/global 可见范围以及 Connection、Server、Tool 三层规则 |
| 安全生命周期 | 支持凭据本机存储、授权刷新、脱敏备份、快照回滚及失败时保留原连接 |
| 插件更新 | 检测新版本，并在宿主提供兼容 Update Provider 时显示进度、失败原因和回滚结果 |

## 功能

- 左侧主导航入口：目标位置为“新会话”下方、“工作区/会话列表”上方；若 DSH DOM 结构不兼容，自动回退到底部公开插槽。
- 侧边栏入口可按当前 profile 隐藏；隐藏后仍可从“设置 → 插件 → 插件配置 → MCP连接器”临时打开现有连接器弹框，用完即关。
- 图形化市场：默认“全部”按推荐与 9 类业务分类分章节展示，每章先展示 4 张并可展开；分类栏固定可见，单分类页展示全部卡片。
- 图形化添加：手动 HTTP/stdio、`mcpServers` JSON、连接器描述 URL 三种入口，失败时保留表单并给出修复建议。
- 连接器详情：精选 Prompt 优先展示，点击可带入 DSH 新会话；工具按 Server 分组，支持描述、搜索、参数详情和独立滚动。实时发现失败时显示带时间/陈旧标记的最后成功工具缓存。
- 实时状态：页面通过同源 SSE 接收连接、目录、健康、工具、治理和作用域变化通知并自动刷新；事件不携带连接标识、端点、错误或凭据。
- Prompt 模板：使用 `{{company}}` 等变量，发送前填写真实查询主体。
- 三种接入：OAuth 2.0 PKCE、自定义 HTTP/stdio、导入 `mcpServers` JSON；也支持从连接器描述 URL 安装。OAuth 动态注册兼容公共客户端以及 `client_secret_post` / `client_secret_basic` 机密客户端。
- 市场 Bearer/API Key 连接器先执行 MCP initialize 连通性与凭据校验，全部 HTTP Server 通过后才持久化凭据并进入“已安装”；stdio 卡片可声明多个本机凭据字段及其环境变量映射。
- 生命周期管理：连接持久化、重启恢复、启停、断开、OAuth 自动刷新/退避恢复与撤销；同 issuer 卡片共享一次授权，跨进程锁与独立原子 Grant journal 防止 Desktop/Web 并行时重复消耗 Refresh Token。
- 配置原地编辑：自定义和 JSON 导入连接可在“已安装”中编辑标准化 JSON 并重新连接；敏感值以本机保留标记处理，校验、启动或保存失败时原连接继续可用。
- 配置备份：一键复制/下载可再次导入的脱敏 JSON；连接变更前自动保存最多 20 个本机快照，支持预览与原子恢复。凭据、本地路径和 OAuth Grant 不进入导出结果。
- 连接作用域：新连接可选当前 Workspace 项目或 profile 全局；支持先预览 Server/工具影响，再复制、移动或按 revision 回滚。凭据只存一份，project-only 工具由 DSH Host 强制隔离。
- 三层治理：Connection、Server、Tool 规则按 Tool > Server > Connection > 默认允许解析；变更先预览、按 revision 提交并可回滚，由 DSH Host 的 schema/lookup/dispatch restriction 与最终执行 Guard 真实生效。
- 可解释诊断：只报告实际观察结果；未检查或 Host 状态不可见时显示“状态未知”，并提供失败阶段、稳定错误码、建议动作、检查时间和进程内最近成功时间。
- 目录运营：内置目录、远程 registry、本地覆盖，支持 `published` 上下架与 `featured` 精选。
- 独立远程 Registry：新市场卡片合并后客户端刷新即可见，无需重新发布 npm；远程不可用时自动回退内置目录。
- 插件版本与一键更新：版本发现独立于安装来源；页面通过 Update Provider 适配层探测安全更新能力。DSH Market API v1 是首个适配器，支持进度、稳定失败码、回滚及按宿主能力提供的重启/刷新操作；无可用 Provider 时回退到当前插件市场或 npm。
- Registry 工具链：Schema/唯一性/密钥审计、MCP/OAuth 无凭据探针、每周健康巡检。
- 平滑迁移：显式扫描并复制两个旧企查查 OAuth 插件授权；检测到旧插件仍启用并管理同名 Server 时阻断重复连接，避免凭据相互覆盖。
- 对话工具：`mcp_connector_catalog`、`connect`、`configure`、`import_json`、`export_config`、`snapshot`、`install_from_url`、`status`、`scope`、`health_check`、`policy`、`set_enabled`、`disconnect`、`refresh_catalog`、`publish`、`tools_list`、`tool_search`、`tool_detail`。搜索/详情只做渐进式能力发现，不执行目标 MCP 工具。

<!-- catalog-stats:start -->
截至 2026-09-20，公共 Registry 已发布 107 条连接器描述；与随包的 4 张企查查卡片合并去重后，市场页可浏览 111 张卡片，覆盖企业数据、金融投资、法律合规、开发工具、办公协作、调研分析、设计创意、效率工具、其他 9 类。推荐位严格保留 4 张企查查卡片、北大法宝和 Wind，共 6 张；其他连接器按业务分类展示。Registry 可独立持续更新，实际数量以客户端刷新后的市场页签徽标和上方实时统计徽标为准。
<!-- catalog-stats:end -->

## 界面与演示

| 市场总览 | 连接器详情与精选 Prompt |
|---|---|
| ![市场总览](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/01-market-overview.jpg) | ![连接器详情](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/02-connector-detail.jpg) |
| 工具发现、描述与独立滚动 | JSON 导入 |
| ![工具发现](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/03-tool-discovery.jpg) | ![JSON 导入](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/04-json-import.jpg) |
| 统一工具搜索与来源 | 参数详情与安全 Schema |
| ![统一工具搜索](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/05-unified-tool-search.png) | ![工具参数详情](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/06-tool-parameters.png) |
| 连接诊断与最后成功缓存 |  |
| ![连接诊断](https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/docs/screenshots/07-connection-diagnostics.png) |  |

`01`–`04` 保留 `v0.2.37` 的历史市场快照，`05`–`07` 与 43 秒演示来自 `v0.2.46` 当前无凭据 UI harness。桌面端一行 2 张卡片；只展示公开市场元数据、示例 Prompt 和明确标识的 Mock 工具说明，不包含凭据、本机路径或查询结果。详见 [`docs/screenshots/README.md`](docs/screenshots/README.md)。

## 安装

要求：DeepSeek Harness Desktop/web profile，Node.js 20 或更高版本。

```bash
dsh plugin --profile web add dsh-mcp-connector
```

也可使用安装脚本：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/duhu2000/dsh-mcp-connector/main/install.sh)
```

重复执行安装命令即可升级。安装或升级后需完全退出并重启 DeepSeek Harness Desktop；使用 `dsh web` 时需先停止原进程再启动，`EADDRINUSE 127.0.0.1:3080` 表示已有实例正在运行。

## 使用

1. 点击左侧“🧩 MCP连接器”，或从“设置 → 插件 → 插件配置 → MCP连接器”点击“打开 MCP连接器”。
2. 在市场中选择连接器，确认“当前项目”或“所有项目（全局）”，再完成授权或配置。
3. 打开卡片详情，可点击示例 Prompt 的发送按钮，在当前工作区创建/复用空白会话并写入草稿。
4. 在“已安装”或对话工具中查看、停用、恢复或断开连接。
5. 连接后打开“工具”页，按工具名或描述查找能力，使用连接/服务筛选定位来源；授权、费用及正式调用仍由相应服务与 DSH Host 管理。

连