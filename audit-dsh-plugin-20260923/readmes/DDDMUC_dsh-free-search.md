# dsh-free-search

**DeepSeek Harness 免费搜索插件 —— 无需 API key，零成本，多引擎可切换。** 一个给 DeepSeek Harness (dsh) 添加多引擎搜索 provider 的插件，注册进 `ctx.web` seam。内置 `web_search` 工具自动选用，支持网页设置页切换引擎、配置 API key、一键测试所有引擎、弹出式命令切换引擎。

[中文](#中文) · [English](#english)

---

## 中文

<div align="center">
  <a href="https://raw.githubusercontent.com/DDDMUC/dsh-free-search/master/assets/settings-free1.png">
    <img src="https://raw.githubusercontent.com/DDDMUC/dsh-free-search/master/assets/settings-free1.png" alt="免费引擎设置 (Bing)" width="820" />
  </a>
  <br>
  <sub>▲ 免费引擎（以Bing为例）</sub>
</div>

### 为什么需要它

dsh 默认的搜索 provider 依赖 DeepSeek 官方 API key（`DEEPSEEK_API_KEY`）。如果你：
- 没有（或不想用）DeepSeek 官方 key，
- 用的是 opencode-go 这类网关（其 OpenAI 兼容端点不支持 `web_search` 工具），

……那么内置搜索必然失败，agent 会告诉你"无法联网"。

这个插件提供多个免费引擎 + 自动回退，彻底摆脱 DeepSeek 官方 key 的依赖。

### 特性

- **零成本** —— 多个免费引擎，无需 key、无需注册
- **多引擎可选**：DuckDuckGo（html/lite）、Bing、SearXNG（元搜索，支持自定义实例）、AnySearch、Exa、Tavily、Keenable、Firecrawl、Parallel、Perplexity、SerpBase、DeepSeek 官方
- **网页设置页** —— 引擎切换 + API key 配置（UI 中 key 脱敏显示"已配置"）+ 中英文切换；DSH 0.1.6-alpha.2+ 入口在左侧「插件」页的组件行配置，旧版在「设置 → 插件 → 可配置」
- **弹出式切换命令** —— 聊天框输入 `/free-search-engine`，弹出引擎选择窗口，点选即切换（等效设置页 + 保存）
- **引擎测试** —— `free_search_test` 工具让 agent 一键测试所有引擎；设置页也有"测试引擎"按钮（直测当前引擎，不走回退链，付费引擎无 key 会明确报错）
- **统一引擎回退** —— 任何引擎失败（付费/免费，缺 key/401/限流/网络）自动轮流尝试下一个引擎：首选引擎 → 其他引擎（exa/tavily/keenable/firecrawl/parallel 无 key 也会尝试，因为它们自带 keyless 免费额度）→ 剩余免费引擎，搜索永不直接失败；结果顶部注明实际生效的引擎（如 `Note: perplexity unavailable or failed, using exa.`）
- **时间过滤** —— `advanced_search` 工具支持 `timeRange`：固定档、自定义相对值、绝对日期三种形式（详见下方逻辑说明）
- **系统提示词注入** —— agent 知道当前用哪个引擎、哪些需要 key；并明确所有搜索结果是**不可信外部数据**，不得执行其中的指令
- **提示注入防护（不可信数据边界）** —— 插件自有工具（advanced_search / platform_search / free_search_test）的网页文本包在 `<untrusted-web-content>` 边界内（正文里自带的同名标记会被剥离，防止提前闭合）；核心 web_search / web_fetch 由 DSH 核心自带同类提示（`External web content follows...`）；所有 snippet 统一清洗并截断到 300 字符
- **版本号 + 检查更新** —— 设置卡片显示当前版本（v0.4.17），"检查更新"按钮直连 npm registry 对比最新版，有新版本时提示并可一键跳转
- **结果缓存** —— 相同查询（含引擎/时间过滤参数）5 分钟内命中缓存（LRU 50 条），防免费引擎限流、省付费额度；时长可在设置页 0-5 分钟自由配置（0 关闭）
- **免费标注** —— 设置页中免费引擎带绿色 `FREE` 徽章，付费引擎带橙色 `API KEY` 徽章
- **网页抓取（web_fetch）** —— 让 agent 抓取网页内容（官方 `dsh-web-fetch-http` provider，纯 JS，零额外依赖）
- **平台搜索（platform_search）** —— 搜 GitHub / V2EX / B站 / Reddit / Hacker News / Stack Overflow / 维基百科 / npm（公开 API，零依赖）
- **干净集成** —— 实现官方 `WebSearchProvider` seam 接口，与官方插件共存

如果这个插件帮到了你，欢迎给仓库点个 ⭐（[GitHub](https://github.com/DDDMUC/dsh-free-search)）——星标是开发者继续维护的最大动力，感谢支持！

### 引擎列表

| id | 引擎 | 费用 | 说明 |
|---|---|---|---|
| `ddg` | DuckDuckGo HTML | 免费 | 偶发限流（反爬），解封自动恢复 |
| `ddg-lite` | DuckDuckGo Lite | 免费 | 轻量版，同上 |
| `bing` | Bing | 免费 | **默认引擎**，最稳定，中文优化（zh-CN） |
| `anysearch` | AnySearch AI | 免费 | AI 搜索，无 key（匿名额度） |
| `searxng` | SearXNG 元搜索 | 免费 | 多实例自动切换，支持自定义实例 |
| `exa` | Exa | 免费 | **无 key 也可用**（MCP 匿名），配 key 提升额度 |
| `tavily` | Tavily | 免费 | **无 key 也可用**（keyless 匿名），配 key 提升额度 |
| `keenable` | Keenable | 免费 | **无 key 也可用**（MCP 匿名），配 key 提升额度 |
| `firecrawl` | Firecrawl | 免费 | **无 key 也可用**（官方免 key 匿名额度），配 key 提升限额 |
| `parallel` | Parallel | 免费 | **无 key 也可用**（官方 MCP 匿名额度），配 key 提升额度并支持精确时间过滤 |
| `perplexity` | Perplexity | 付费 | 需 `PERPLEXITY_API_KEY` |
| `serpbase` | SerpBase | 付费 | 需 `SERPBASE_API_KEY`（serpbase.dev，注册送 100 次免费额度） |
| `deepseek-official` | DeepSeek 官方 | 付费 | 需 `DEEPSEEK_API_KEY` |

- **默认引擎为 `bing`**（免费且最稳定），安装后开箱即用。
- **自动回退**：任何引擎失败（免费限流/反爬，付费缺 key/无效/网络错误）都会自动轮流尝试下一个引擎——先试其他已配 key 的付费引擎，再试免费引擎（Bing/AnySearch 等），并在结果中附带回退提示——搜索不会因引擎问题直接失败。
- **设置页有官网链接**：免费引擎显示"访问官网 →"，付费引擎显示"获取 API Key →"（新标签页打开）：
  - Exa：<https://dashboard.exa.ai/api-keys>
  - Tavily：<https://app.tavily.com/home>
  - Keenable：<https://keenable.ai/login>
  - Parallel：<https://platform.parallel.ai>
  - Perplexity：<https://www.perplexity.ai/settings/api>
  - SerpBase：<https://serpbase.dev>
  - DeepSeek：<https://platform.deepseek.com/api_keys>

#### 为什么免费引擎不需要 key？

- **AnySearch**：其 `v1/search` REST 接口提供匿名的公共搜索额度，无需注册或 API key。额度有限流（适合日常搜索），但作为免费引擎之一，与其他免费引擎互相回退，体验稳定。
- **Exa**：公开 MCP 端点（`mcp.exa.ai/mcp`）支持匿名调用，不配 key 也能用；配置 `EXA_API_KEY` 后可获得更高额度。
- **Tavily**：通过 `x-tavily-access-mode: keyless` 头走 keyless 匿名额度，不配 key 即可用；配置 `TAVILY_API_KEY` 后走账号档，额度更高、结果质量更稳定。
- **Keenable**：无 key 时走其公开 MCP 端点（`api.keenable.ai/mcp`）匿名调用；配置 `KEENABLE_API_KEY` 后走 REST API（`api.keenable.ai/v1/search`），额度更高、按组织限流。
- **Firecrawl**：其 `/v2/search` 端点**无需 key** 即可使用（官方文档明确说明，有匿名限流）；配置 `FIRECRAWL_API_KEY` 后可提高限额。支持 `tbs` 时间过滤（`qdr:h/d/w/m/y` 与自定义日期区间）。

### 安装

```sh
git clone https://github.com/DDDMUC/dsh-free-search.git
dsh plugin --profile web add /path/to/dsh-free-search
```

然后重启：

```sh
dsh web
```

#### 姊妹插件：dsh-preset-workbench（预设工作台）

同作者的**姊妹插件**：在设置页里可视化创建/编辑 Agent 预设——分段提示词、15 项能力开关、内置「鲸鱼娘 / 梁神模式」模板，不用手写 YAML。两者搭配：**free-search 解决"AI 联网搜索"、preset-workbench 解决"AI 人设能力编排"**，都是纯免费、开箱即用。

- 仓库：<https://github.com/DDDMUC/dsh-preset-workbench>
- 安装：`dsh plugin --profile web add github:DDDMUC/dsh-preset-workbench`
- 用法：设置 → 预设工作台

如果你觉得 preset-workbench 也有用，同样欢迎给它的仓库点个 ⭐。🙏

#### 依赖说明

插件对 `@deepseek-ai/dsh-settings` 和 `@deepseek-ai/dsh-tools` 使用 `peerDependencies`，这是刻意的：DSH 运行时必须使用安装树中的唯一实例。请通过 `dsh plugin --profile <profile> add ...` 安装插件，不要把 DSH 核心包复制进 profile 的本地 `node_modules`；重复副本会导致工具调度器失效。

### 使用

#### 网页设置（推荐）

安装后按 DSH 版本打开配置页：

- **DSH 0.1.6-alpha.2 及以上**：左侧 **插件** 页 → **已安装** 分组 → `free-search` → 点击组件行 `web-search-free`（行内"配置"入口）
- **DSH 0.1.5 及更早**：**设置 → 插件 → 可配置** 标签页 → **Free Search** 卡片

配置页提供：

- **Search engine**：下拉框切换引擎，保存即生效
- **API keys**：为 Exa / Tavily / Keenable / Firecrawl / Parallel / Perplexity / DeepSeek 填写 key（密码框，保存后只显示"已配置"；Exa / Tavily / Keenable / Firecrawl / Parallel 不填也可免 key 使用）
  - **推荐**：付费引擎 key 建议写入 harness 凭据中心 `~/.dsh/.credentials.yaml`（如 `DEEPSEEK_API_KEY: sk-...`，与官方 LLM provider 一致，一处管理所有 key）。插件读取优先级：凭据中心 > 设置页 > 环境变量，设置页填的 key 仅作为遗留兼容。
- **Test engine**：直测当前引擎可用性（不走回退链，付费引擎无 key 会明确报错）
- **Use Bing default**：把当前搜索引擎切回稳定的免费 Bing；`Discard` 只撤销尚未保存的编辑
- **Platform search**：勾选启用 GitHub / V2EX / Bilibili 平台搜索（`platform_search` 工具按此过滤）
- **EN / 中文**：切换界面语言（默认中文）

<table align="center" style="border: none; border-collapse: collapse;">
  <tr style="border: none;">
    <td align="center" width="50%" style="border: none; padding: 6px;">
      <a href="https://raw.githubusercontent.com/DDDMUC/dsh-free-search/master/assets/settings-free.png">
        <img src="https://raw.githubusercontent.com/DDDMUC/dsh-free-search/master/assets/settings-free.png" alt="免费引擎设置" width="100%" />
      </a>
      <br>
      <sub>▲ <b>免费引擎</b>（显示绿色 FREE 徽章与官网链接）</sub>
    </td>
    <td align="center" width="50%" style="border: none; padding: 6px;">
      <a href="https://raw.githubusercontent.com/DDDMUC/dsh-free-search/master/assets/settings-apikey.png">
        <img src="https://raw.githubusercontent.com/DDDMUC/dsh-free-search/master/assets/settings-apikey.png" alt="付费引擎设置" width="100%" />
      </a>
      <br>
      <sub>▲ <b>付费/API Key 引擎</b>（显示橙色 API KEY 徽章与获取链接）</sub>
    </td>
  </tr>
</table>

#### 聊天框切换引擎（/free-search-engine）

不用进设置页也能切换引擎：在聊天框输入 `/free-search-engine`，**弹出引擎选择窗口**（和 `/model` 选模型一样的交互），点选即切换，当前引擎会标记出来。等效于设置页切换 + 保存，且界面语言跟随设置页（中文/英文）。

命令只改首选引擎配置，搜索仍走 `web_search` + 统一回退链：即使首选引擎挂了也会自动换其他引擎，永不直接失败。系统提示词同步刷新。

#### 配置文件

配置存在 `~/.dsh/settings.yaml`：

```yaml
free-search:
  provider: bing              # ddg / ddg-lite / bing / searxng / anysearch / exa / tavily / keenable / firecrawl / parallel / perplexity / serpbase / deepseek-official
  lang: zh                    # 设置页界面语言（zh / en）
  bingMarket: zh-CN           # Bing 市场
  region: cn-zh               # DuckDuckGo 区域（可选）
  searxngInstances:           # 自定义 SearXNG 实例（可选）
    - https://your-instance.example
  exaApiKey: ...              # 或通过设置页填写
  tavilyApiKey: ...           # 或通过设置页填写
  keenableApiKey: ...         # 或通过设置页填写
  firecrawlApiKey: ...        # 或通过设置页填写
  parallelApiKey: ...         # 或通过设置页填写
  perplexityApiKey: ...
  serpbaseApiKey: ...         # 或通过设置页填写
  deepseekApiKey: ...
```

#### 让 agent 