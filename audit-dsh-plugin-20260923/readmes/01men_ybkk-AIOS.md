# 榕器 · 企业AI资源管理平台

基于 **DeepSeek Harness（dsh）「一切皆插件」** 架构实现的企业级 AI 资源管理平台。
对应设计方案：《企业服务资源统一管理方案 V1.0》与《技术实现规划》；生态平台演进设计见
[docs/ecosystem-design-v1.2.md](docs/ecosystem-design-v1.2.md)（商业化部分已随 M0 废止，见文内横幅），
宿主轨迭代计划以《榕器开发计划-主分支》为最新基线（M1-1 契约冻结见下）。

> 组织账号（IAM）· 统一认证（Authn + OIDC Provider）· MCP 部署服务 · Skill/插件市场 · Agent 本体 ·
> AI 应用本体 · 用量透明计量（usage）· 模型接入网关（modelgw）· 审计与告警
> ——多类资源，一套身份、一套权限、一套计量、一套审计。
>
> **M0 合规收敛（2026-09-09）**：废止按用量计费/转售/分账，平台对外只呈现**用量与内部成本穿透**——
> 价格簿为零价快照（charge 恒 0）+ 内部采购成本参考，不呈现任何金额结算语义；用量透明月度报表
> （部门/Agent/Skill tokens 三维聚合 + CSV 自助导出）见 J4 契约
> [docs/contract-j4-usage-report.md](docs/contract-j4-usage-report.md)。
> 原钱包/分账子系统（plugin-billing）已整体下线封存（存量流水 CSV 封存 90 天，登记见
> [docs/billing-archive-register.md](docs/billing-archive-register.md)）。
>
> **商业模式（2026-09-15 更新）**：按**「团队 + 领域资产」**定价，而非平台级打包定价——按开通团队规模与
> 所选领域资产（行业图谱包/场景包）计价；制造业客户亦可走**私有化交付项目制**。
>
> **M1-1 契约冻结 v1 齐套（2026-09-11）**：J1 面板技能/Agent 点名直调（诚实降级 200+ok:false，
> [contract-j1-panel-invoke.md](docs/contract-j1-panel-invoke.md)）· J2 统一入口分诊
> （[contract-j2-entry-triage.md](docs/contract-j2-entry-triage.md)）· J3 会话直通
> （[contract-j3-session-passthrough.md](docs/contract-j3-session-passthrough.md)）· J4 用量报表。
> 同批加固：安全响应头默认开启（`SECURITY_HEADERS=off` 可关）、usage 事件保留策略默认 730 天
> （`USAGE_RETENTION_DAYS`，0=永久）——详见
> [docs/release-notes-2026-09-11-optimization.md](docs/release-notes-2026-09-11-optimization.md)。
>
> **IAW 缺口批次 + F 域余量反馈（2026-09-11）**：新增 **flow-core 流程编排域**（TF 编排 + 步骤状态机 /
> 模板库 contextPack / SLA 与进度 / 甘特时间轴，[contract-c2-flow-tf.md](docs/contract-c2-flow-tf.md)）·
> **数据要素域**（数据集登记 / 四维质量分 / 血缘反向追溯 / 指标字典口径仲裁）· **模型渠道治理**
> （分级路由 / 渠道组降级链 / 预算熔断，[contract-c1-modelgw-channel-governance.md](docs/contract-c1-modelgw-channel-governance.md)）·
> **Agent 自治与 A2A**（autonomy A0-A3 + 点名调用端点，[contract-c3-agent-a2a.md](docs/contract-c3-agent-a2a.md)）·
> IAM 场景级授权（sceneCode，deny→allow→fail-closed）· 审计证据锚点与场景维度时间线 · 通知中心持久化——
> 详见 [docs/release-notes-2026-09-11-iaw-batch.md](docs/release-notes-2026-09-11-iaw-batch.md)。

---

## 一、快速开始

```bash
npm install          # 安装依赖（@deepseek-ai/cordis）
npm start            # 启动平台（默认 http://127.0.0.1:7300）
```

打开 **http://127.0.0.1:7300** 进入管理控制台。首次启动在空数据目录上执行**基线初始化**（生产形态）：
内置角色 + 根组织 + 平台管理员 `admin`（无任何演示业务数据）。

- `admin` 口令取 `ADMIN_PASSWORD` 环境变量；未设置则随机生成，一次性写入 `data/admin-initial-password.txt` 并打印在启动日志（请立即登录并妥善保管）。
- 忘记口令：清空数据目录重启，或由持有 `iam.user.write` 的管理员在「组织与账号 → 账号详情 → 重置口令」重置。

**演示模式**（评估/培训，自动生成完整演示数据与演示账号，口令均为 `Ybk@2026`）：

```bash
DEMO_SEED=1 npm start   # 首次启动注入演示数据（组织树/演示账号/MCP/Skill/Agent/应用/28 天历史）
```

| 演示账号 | 角色 | 用途 |
|---|---|---|
| `admin` | 平台超级管理员 | 全功能 |
| `ops` | 资源管理员 | MCP/Skill/Agent/应用管理 |
| `hr` | 组织管理员 | 组织/账号/三方同步 |
| `dev` | 开发者 | 提交 Skill、注册 Agent |
| `audit` | 审计员（只读） | 审计与告警 |

演示模式下钉钉免密登录可用（mock 连接器）：登录页「钉钉扫码」输入工号 `DD0002`（林小满）；生产基线不配置连接器，三方登录入口自动隐藏。

```bash
npm run selftest      # 功能自测：隔离实例（DEMO_SEED）端到端断言，全绿（数量以本次运行为准）
npm run lint:manifests  # 插件清单五面 YAML 校验
DSHCTL_USER=admin DSHCTL_PASS=*** node cli/dshctl.mjs help    # CLI 帮助（凭据经环境变量或 DSHCTL_TOKEN 提供）
```

### 平台自更新（v1.1+）

两类安装形态（GitHub 源码检出 / dsh 插件市场安装）都能感知上游仓库新版本，**是否升级永远由管理员决定**：

- **自动检查**：默认每 24h 一次（启动 15s 后首查），比对远端 `package.json` 版本 + GitHub compare 提交差；
  发现新版本 → 控制台顶栏「可更新」徽标 + `platform.update.available` 事件（audit 留痕）。控制台抽屉可开关/调频。
- **手动升级**：控制台顶栏徽标 → 抽屉「一键升级」（source 形态：`git pull --ff-only` + `npm install`，支持
  dry-run 预演、原因留痕、完成后提示重启）；CLI：`dshctl update status | check | apply [--dry-run]`；
  Agent 工具：`update_status` / `update_check` / `update_apply`。bundle 形态给出 `dsh plugin update` 指引。
- **内网/限流**：`GITHUB_TOKEN` 提升限额；`DSH_UPDATE_API_BASE` / `DSH_UPDATE_RAW_BASE` 指向私有镜像；
  `DSH_UPDATE_AUTO_CHECK=off` 关闭自动检查。权限点：`platform.update.read`（查看/检查）、`platform.update.apply`（升级）。

> **企业部署 / Agent 一键接入**：部署 runbook、dsh 运行时接入与「可直接下达给 dsh 自带 Agent 的一键部署指引」
> 见 [docs/deploy-enterprise.md](docs/deploy-enterprise.md)；日常运维 Agent 指引见 `skills/dsh-ops-admin/SKILL.md`。

## 二、架构：一切皆插件

运行中的平台就是一棵 **cordis 插件树**（与 dsh 同一插件框架，`@deepseek-ai/cordis`）。
每个业务域 = 一个插件包，独立声明依赖/权限点/事件，可独立启停：

```
接入层   dsh-plugin-console        REST 网关 + 控制台 SPA + 工具桥 + 种子数据
业务域   dsh-plugin-iam            组织/账号/角色/用户组/三方连接器（钉钉演示）
         dsh-plugin-authn          双轨身份 + 令牌 + on-behalf-of 链
         dsh-plugin-mcp            部署/灰度/回滚/健康熔断/权限组/调用网关/监控（真实 HTTP 传输层）
         dsh-plugin-skillhub       提交→静态扫描→两级审批→版本化上架
         dsh-plugin-agent          Agent 本体（resource-core 底座 + 机器凭证）
         dsh-plugin-app            AI 应用（编排拓扑 + 应用指标 + 成本穿透）
         dsh-plugin-usage          计量管道（schema v1 / 幂等 / 死信重放 / 价格簿 / 三方对账 / 能力漂移）
         dsh-plugin-modelgw        模型接入网关（OpenAI 兼容真实转发 / 零价快照计量 / 内部成本参考）
         dsh-plugin-market         第三方与自营插件市场（契约五面 / Ed25519 验签 / L0 运行时 / 零价计量声明）
         dsh-plugin-audit          四类审计日志 + 告警规则 + 成本归集 + 审批中心
         dsh-plugin-connect        远程 dsh 接入（宿主角色：接入码/enroll/客户端管理；客户端角色：凭证申请 + 工具远程代理 + 本机配置页）
         dsh-plugin-update         平台自更新：上游版本检查（自动+手动）→ 通知 → source 形态一键升级（git pull + npm install，dry-run/审计/权限点）
         dsh-plugin-portal         门户数据通道（外部拉取端点·非核心：企业门户免鉴权只读拉取已上线应用/Agent/技能，CORS + 可见性留痕，PORTAL_SYNC=off 可停用，见 docs/portal-integration.md）
底座     dsh-plugin-resource-core  资源本体：属性 schema + 生命周期状态机 + 依赖图
基础层   dsh-plugin-platform-core  存储(JSON集合/原子落盘) + SQLite 事务存储 + YAML 解析 + 事件总线 + ToolRuntime-lite + HTTP
```

**插件协作铁律**：状态变更必发事件；跨插件联动只通过事件总线或扩展点（`ctx.platformBus`），
禁止直连对方数据。例：`iam.user.frozen → authn 吊销全部令牌`、`agent.offlined → 凭证吊销 + 绑定用户通知`、
`skill.deprecated → 引用 Agent 告警`、`mcp.unhealthy → 熔断 + 审计`。

### 一份插件代码，两种宿主

- **独立宿主**（本项目默认）：`node src/main.ts` 启动完整平台（控制台 + API + 工具）。
- **完整 dsh 运行时**：`cordis.yml` 把同一批插件挂载进 `dsh web`——此时平台注册的
  **运维工具**直接进入 dsh 原生 ToolRuntime、对模型可见可调用（`provideToolRuntime: false`），
  Agent 即可按自然语言运维整个平台（「列出所有 MCP 服务和健康状态」→ `mcp_service_list`，
  「Skill 市场里能装什么」→ `skill_search`）。
- **单进程单入口（宿主挂载形态）**：`plugin-dsh-bridge` 把榕器数据面（REST/控制台 SPA/docs/MCP）
  以 `/rq` 前缀挂进 dsh webServer，dsh web 端口即唯一入口；`startHttp: false` 关闭平台独立端口。
  配套 `plugin-panel-core`（部门 Agent 工作台面板）、`plugin-dingtalk-bridge`（群桥/审批推送/告警通道）、
  `plugin-rq-card`（会话内四态执行卡，dsh.client 双面插件）。升级与运维须知
  （AGENT_SSO_ENFORCE 上线门禁 / CORS 行为 / SSE 日志脱敏）见 `docs/host-features-ops-notes.md`。

**源码检出模式（本地开发）**——两条硬性要求，缺一不可：

1. `cordis.yml` 中 `<PROJECT_ROOT>` 必须替换为 `file:///` URL 形式的绝对路径
   （Windows 下裸盘符路径会被 ESM 判为 `ERR_UNSUPPORTED_ESM_URL_SCHEME`）；
2. 本项目 `node_modules/@deepseek-ai/cordis` 必须指向 dsh 源码树的 `vendor/cordis`
   （junction），保证插件与宿主加载**同一个 cordis 实例**——两份实例会导致
   `ctx.plugin(类插件)` 静默失效、服务链（iam→usage→audit…）全部 `pending`：

```powershell
# 一次性设置（PowerShell，替换两处路径为你的实际检出位置）：
Remove-Item -Recurse -Force node_modules/@deepseek-ai/cordis
New-Item -ItemType Junction -Path node_modules/@deepseek-ai/cordis -Target D:\dsh-harness\vendor\cordis

# 之后每次（在 deepseek-harness 源码检出中）：
pnpm dsh web --patch <本项目绝对路径>/cordis.yml
```

**安装模式（发布使用）**——`dsh plugin add` 走 pnpm 安装，补丁里的 entry 以
「包名 + 子路径」声明（Node 从 profile 目录沿 node_modules 解析，无需感知安装位置）：

```bash
dsh plugin --profile web add github:01men/ybkk-AIOS
# 验证：dsh --profile web --dump-config 应列出全部 ops-* entry；
# 会话中问「列出所有 MCP 服务和健康状态」，模型应调用 mcp_service_list 而非静态作答。
```

安装模式的关键约束：`@deepseek-ai/cordis` 只在 `devDependencies`（本地开发/独立宿主用），
**绝不能进 `dependencies`**——否则 pnpm 会把它 hoist 进 profile 的 node_modules，
插件解析到第二份 cordis 实例，服务链整体失效（同上）。安装后插件沿
`<profile>/node_modules → $DSH_HOME/profiles/node_modules`（dsh 自建的宿主闭包 symlink）
解析到宿主自己的 cordis。

**平台服务键已做宿主去冲突**：JSON 存储服务键为 `opsStorage`（不是 `storage`——
dsh 宿主自带同名 `storage` 服务，曾导致 iam 等插件构造时拿到宿主服务、方法不存在而崩溃）。
`tools` 键是**刻意共享**的接缝：独立宿主下由 ToolRuntimeLite 提供，dsh 下即原生
ToolRuntime——37 个运维工具由此进入 dsh。

**领域 Skill 手册**（`skills/dsh-ops-*/SKILL.md`）默认不随插件自动进入 dsh 技能系统
（dsh 只扫描 `<project>/.dsh/skills`、`~/.dsh/skills` 等根目录）。要让 Agent 获得
分领域操作手册，复制或链接一份：

```bash
# 用户级（所有会话可用）：
cp -r skills/dsh-ops-* ~/.dsh/skills/
# 或项目级（仅当前项目）：
mkdir -p .dsh/skills && cp -r skills/dsh-ops-* .dsh/skills/
```

### 远程 dsh 接入（第三种形态：免源码、免同机共享 data）

其他电脑经插件市场安装本平台后（安装模式见上），无需源码检出、也无需与宿主共享
`data/` 目录——插件树中的 `plugin-connect` 