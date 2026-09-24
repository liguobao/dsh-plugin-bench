<div align="center">

# dsh-ui-usage-billing

<p align="center">把每一分模型开销，看得清清楚楚。</p>

<p align="center">
  <a href="https://github.com/kenz1117/dsh-ui-usage-billing/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/kenz1117/dsh-ui-usage-billing/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/kenz1117/dsh-ui-usage-billing/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/kenz1117/dsh-ui-usage-billing?logo=github"></a>
  <a href="https://www.npmjs.com/package/@kenz1117/dsh-ui-usage-billing"><img alt="npm version" src="https://img.shields.io/npm/v/@kenz1117/dsh-ui-usage-billing?logo=npm"></a>
  <a href="https://www.npmjs.com/package/@kenz1117/dsh-ui-usage-billing"><img alt="npm downloads" src="https://img.shields.io/npm/dm/@kenz1117/dsh-ui-usage-billing?logo=npm"></a>
  <a href="https://github.com/kenz1117/dsh-ui-usage-billing/blob/main/LICENSE"><img alt="License MIT" src="https://img.shields.io/github/license/kenz1117/dsh-ui-usage-billing"></a>
  <a href="https://github.com/kenz1117/dsh-ui-usage-billing/pulls"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen"></a>
  <a href="https://github.com/kenz1117/dsh-ui-usage-billing"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/kenz1117/dsh-ui-usage-billing?logo=github"></a>
  <a href="https://github.com/kenz1117/dsh-ui-usage-billing/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/kenz1117/dsh-ui-usage-billing"></a>
  <a href="https://awesome-dsh-plugin.com"><img alt="Awesome DSH Plugin" src="https://awesome-dsh-plugin.com/badge.svg"></a>
</p>

[中文](README.md) · [English](README.en.md)

</div>

---

<div align="center">
  <img src="screenshots/demo.png" alt="dsh-ui-usage-billing — 计费仪表盘总览" width="80%">
</div>

### 演示动图

![演示](screenshots/demo.gif)

## ✨ 为什么选它

市面计费插件大多停在「token 数 × 单价」。dsh-ui-usage-billing 把计费做成一条**可对账的账本链路**——用量是真的、价格是活的、峰谷跟着模型走。

### 账是真的，还能对账
用量从持久化会话日志实时聚合，绝不伪造样本（数据到达前显示空快照）；官方余额当日变动与本地账本交叉对账，偏差超阈值主动提示核对——账单经得起质疑。

### 价格是活的，历史不重算
models.dev 实时目录 + 内置 24 厂商 77 款模型 + 设置面板自定义单价（可按中转站绑定同模型不同价），新模型无需等发版；DeepSeek 分时价按官方变更节点**分段计价**（8-17 前基础价、8-17~8-23 周末计峰、8-23 起周末全谷），价格调整永不回写旧账。

### 峰谷全感知，提醒跟着模型走
计费通道按当前会话使用的模型自动识别：DeepSeek 按量走分时价（工作日 9-12 / 14-18 高峰 ×2、周末全天低谷），智谱 Coding Plan 走积分峰谷（工作日 14-18 高峰全额、非高峰**积分 5 折**），通道层可扩展、更多厂商逐步接入；切档前弹窗 / 系统通知自动提醒，且只有当前模型真正涉及峰谷才会提醒、费用条才显示档位——不用你盯时间表。

### 订阅、余额、额度一屏闭环
DeepSeek / Kimi / 智谱 GLM / 腾讯云 TokenHub 等 7 家官方余额、Coding Plan 额度、中转站滚动额度窗口、自声明端点，再加余额差对账——订阅扣的和余额扣的同屏可查、交叉验证。

### 还有这些同类少见的细节

- 不止「花了多少」还答「花在哪」：输入按缓存命中 / 未命中分桶（含 reasoning）、官方 / 三方分桶、按工作区 / 会话 / 中转站下钻、每轮费用突增归因。
- 性能面板：各模型首字延时（TTFT）均值 / P50 / P90 与生成速度，同类少有。
- 未收录模型显著标注「未收录」、绝不静默计 0；目录外模型配一条别名即完成识别与计价。
- 可选的 `usage_stats` 工具让模型直接回答「今天花了多少」「哪个站点用得最多」。
- 纯 UI surface：不注册工具、不注入系统提示、不写模型可见事件。
- 中文 / English 语言切换，¥ / ≈$ / ≈€ 币种切换（二者独立）；无图表库、无外部 CDN、离线自包含。

## 📊 仪表盘

- **侧边栏触发卡**：设置按钮上方常驻本月费用主数字 + 近 7 天 sparkline 迷你趋势，副行「今日 / 本周」；折叠栏自动切为图标钮，悬停浮现速览卡。
- **六区仪表盘**：概览 / 趋势 / 明细 / 统计 / 费率 / 设置——Hero 大数字 + 环比 + 本月预计 + KPI + 用量热力图，趋势 7/30 天可切费用 / Token，模型单价表、预算与峰谷提醒都在；克制冷调、深浅主题自适应。

  ![概览：本月费用 Hero、预算进度、KPI 与用量热力图](screenshots/1.png)
- **即时代费用条**：输入框下方常驻「本轮 / 会话」费用；峰谷档位与切换倒计时只在当前模型涉及峰谷时出现；订阅额度预警 chips 剩余 ≤20% 浮现、≤10% 标红；可在设置 Tab 整条隐藏（偏好本地持久化，统计与提醒不受影响）。
- **峰 / 谷切换提醒**：切档前弹窗 + 可选系统通知，提前量 / 位置 / 模式 / 预览均可配；文案按计费通道区分（DeepSeek 价格减半、智谱积分 5 折）。
- **插件信息卡**：设置 Tab 常驻「关于」卡——版本号服务端读自包 `package.json`（单一来源，发布自动正确），作者 / 仓库 / npm / 许可证一键可达。

## 💰 计费引擎

- **提供商优先分组**：费用按调用实际发生的 llm 入口（通道）分组——腾讯云 TokenHub / Token Plan / DeepSeek 官方 / 直连·路由名 / 未知路由，模型品牌只是行内徽标 + 副标；官方判定按通道 origin（`api.deepseek.com`）而非路由名，`deepseek-*` 网关路由不再被误算官方。`routeAliases` 归位改名 / 删除的历史路由，`modelKeyAliases` 把目录外模型 id 绑定到计费键（日期后缀、组织前缀、TokenHub 短 id `hy3` 已内置识别）。
- **实时费率表**：models.dev 抓价 + 探活模型对标，系统实际配置的模型全纳入；峰谷分时（工作日 9-12 / 14-18 高峰 ×2、周末全天低谷，历史费用按官方变更节点分段，见下方「计费细节」）+ 实时汇率（USD→CNY），每 6 小时自动刷新；费率条显示「上次同步」时间并可**一键立即同步**（无需重启宿主）。
- **自定义单价**：设置面板为未收录或变价模型填实付价（未命中 / 缓存命中 / 输出，可选 USD 与低谷价），总览与日趋势按用户价重估；支持按中转站来源绑定同模型不同价，目录外模型填价即生效。

  ![费率：模型单价表（峰谷分时与实时汇率）](screenshots/5.png)
- **官方 vs 三方分桶**：明细费用列按官方直连 / 第三方中转分解（混合时「官 x / 三 y」），统计 Tab 有汇总卡；联网搜索辅助请求计入官方。
- **月度预算 + 分档提醒**：预算条 ≥80% 琥珀、超支红脉；跨 50 / 80 / 100% 各提醒一次；余额折算 CNY 低于阈值每天提醒一次。
- **成本突增归因**：最近 40 轮费用柱状图，金额贴柱顶、峰谷背景分带、超 2 倍红标归因。

## 🔌 订阅与余额

- **订阅套餐额度**：自动识别订阅类 provider（Kimi / Z.ai / OpenCode Go / MiniMax / OpenRouter / Claude / CommandCode / 小米 / 火山…），有额度 API 的实时显示剩余 % 与重置时间、用尽标红，无 API 标「未接入」；订阅通道模型费用记 0，档位月费与周期额度由内置知识库识别（如 OpenCode Go $10/月 + 周 $30 额度）。**MiniMax 注意**：国内用 `minimax-token-plan-cn`（自动对接 `api.minimaxi.com`），国际用 `minimax` / `minimax-token-plan`；可在该 provider 设置覆盖 `baseUrl`。**Claude 订阅**：本机登录 Claude Code 后自动发现（读 `~/.claude/.credentials.json` 的 OAuth token），显示 5 小时 / 周窗口用量；llm-pi-ai 里按量 `anthropic` 路由不会被误识别，费用照常按 token 计。**CommandCode**：在 llm-pi-ai 给 `commandcode` 路由配 `apiKeyEnv`（`user_` 前缀 key），显示 5 小时 / 周窗口与月度 Credits。
- **多厂商余额**：DeepSeek / Kimi / 阶跃星辰 / 硅基流动 / xAI / 智谱 GLM 内置官方余额，按近 7 天日均折算「约可撑 N 天」；**腾讯云 TokenHub Token Plan** 余量与订阅额度走云 API 管控面（TC3 签名，`src/tc3.ts`）——凭据填 `<SecretId>:<SecretKey>` 密钥对（非推理 key），路由命名 `tencent-tokenhub` / `tokenhub` / `tencent` / `tencentcloud` 任一即可命中，剩余与总额度都可解析时才产出百分比窗口（绝不猜总额度）。
- **自定义 Provider 余额**：配置任意 HTTP 端点查余额（`extract` 支持常量 / 点路径 / 四则运算，请求头 `{{ENV}}` 经凭据 seam）。
- **声明端点 + 余额对账**：内置表没有的供应商用 `declaredEndpoints` 自声明余额接口——只写「数字在哪里」的点路径、无表达式；安全边界（单斜杠绝对路径、仅 GET、拒跨源重定向、响应体 / 超时上限、凭据只取本 provider）由 `src/declarative.ts` 强制执行，取错路径在界面标 `declared` 与 reason。**余额差对账**（`reconcilePath`）用官方余额当日变动与本地账本交叉校验，偏差超阈值（0.3 元且 >15%）提示核对；充值 / 授信 / 币种变化重置基准而非告警，余额未减少（走订阅扣费）静默。
- **中转站归组与额度**：按 `baseURL` 归一化 origin 归组，同站多把 key 合并一行、站名即域名；自动识别 New API 系（`/api/status`）与 Sub2API（`/v1/usage`）的余额与滚动额度窗口，读不出标「未读出额度」、剩余 <20% 标红；识别结果 5 分钟指纹缓存（同站多 key 独立熔断），`relay-quotas` 端点附 `diagnostics` 供「为什么不显示」自查；项目归属优先用工作区标题命名。

  ![明细：厂商计费与订阅（余额、套餐额度、模型用量）](screenshots/3.png)

> 全部渠道的适配矩阵（识别方式 / 端点 / 凭据要求 / 排查顺序）见 [docs/adapters.md](docs/adapters.md)。

## 📈 用量可视化

- **会话明细 + 热力图**：按会话费用倒序（标题 / 项目 / 调用 / 费用 / 最后活跃）；月 / 半年 / 年三档日历热力图（5 档色阶、悬停明细，年视图近 52 周 GitHub 风格，**半年视图 26 周大格**——一张图看完近半年强度，截图即用），**费用 / Token 双口径**切换，头部显示区间合计、活跃天数 / 连续使用天数。
- **性能指标**：每模型 TTFT 均值 / P50 / P90、生成速度（tokens/s）、总延迟均值；按小时 × 模型对比曲线——指标 tab 切换、模型 chip 点击开关曲线（默认点亮样本数前 5）、悬停吸附最近小时显示十字线与逐模型数值，缺失样本小时断线不造假；视图偏好本地持久化。
- **Token 统计洞察**：每日 token 堆叠双视角——「按结构」（输入未命中 / 命中 / 输出三桶，含 reasoning）与「按模型」（旧快照缺明细时自动隐藏切换）；悬停显示当日精确明细（千分位不缩写），点击图例色块或 Token 表行聚焦单模型（再点解除）；结构 KPI（缓存命中率 / 思考占比 / 输入输出比 / 峰值日）；按日 CSV 与 JSON 导出（JSON 含按日 × 模型明细）。

  ![趋势：每日费用趋势、每轮费用与峰谷时段占比](screenshots/2.png)
- **数据导出 + 下钻**：统计 Tab 导出按日 / 按会话 / 按站点 CSV 与全量 JSON；费用构成 / 工作区 / 会话明细可下钻（点项目行展开该项目的会话）；无图表库、无外部 CDN、纯设计令牌。

  ![统计：导出、费用构成、工作区与会话明细](screenshots/4.png)

## 🛡️ 健壮性与隐私

- **真实用量聚合**：服务端增量聚合（只重算写过的会话），单会话损坏容错、快照落盘回退；`usage_stats` 工具让模型自查今天 / 本月 / 当前会话 / 累计费用，还可查 `bySite`（按站点归组）与 `relay`（只看中转站）汇总。
- **模型健康 + 未收录标注**：厂商接入状态圆点（绿 / 红 / 灰）；未收录模型显著标注、按兜底价估算、厂商自动推断（如 `mi-mimo-2.5` → 小米）；估算价模型标注「估算价」。
- **多语种 + 三币种**：语言（EN / 中）与币种（¥ CNY / $ USD / € EUR）**各自独立切换**，均仅本插件生效、不影响宿主全局 UI；费率表、侧边栏卡片与输入框胶囊均按所选币种换算，两项选择均本地持久化。老用户首次升级时语言由已存币种播种一次（选 $ 即英文），界面语言不会静默改变。
- **安全加固**：全部 HTTP 端点强制回环访问——peer socket 地址 + Host 头精确匹配双重校验，拒绝 `127.0.0.1.evil.com` 形式的 DNS rebinding（反向代理部署可用 `trustedHosts` 显式放行特定主机名，peer socket 校验仍为强制）；写操作额外校验 Origin 回环与 Content-Type 并限制 body 上限，杜绝跨站改写；余额 / 订阅 / 定价拉取带有限重试与按上游维度熔断（鉴权失败属配置问题、不计入熔断）。
- **导出防注入**：CSV 对 `=` / `+` / `-` / `@` 开头单元格前置单引号并完整转义，防止在 Excel / WPS 中被当作公式执行。
- **隐私底线**：纯 UI surface，不注册工具、不注入系统提示、不向会话日志写模型可见事件；仅从既有会话日志聚合，日志内容由其他包负责。

## 🚀 快速开始

先确认宿主代际（`dsh --version`），再按代际选安装命令——**装错线会在市场侧被 `engines.dsh` 声明拦截**（v1.0.41 起声明生效）。注意 `dsh plugin add` 需要显式 `--profile`（缺省会报 `required option '--profile <name>' not specified`），且建议**钉具体版本号**而非 `@latest`（pnpm 的 `minimumReleaseAge` 冷静期会让刚发布的版本被跳过、回退到旧线）：

- **DSH 0.1.2 ~ 0.1.6 系**（0.1.2-alpha.1 起，现行 latest 为 0.1.5-rc.2（alpha 预览已前移 0.1.6-alpha.2）；`npm ls -g @deepseek-ai/dsh` 显示 0.1.2-* ~ 0.1.6-*）：

  ```sh
  dsh plugin --profile web add npm:@kenz