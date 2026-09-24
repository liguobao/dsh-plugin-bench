# prts-terrarchive

PRTS.chat 为 DeepSeek Harness（DSH）提供的资料插件：把《明日方舟》与
《明日方舟：终末地》的游戏原文、档案，以及社区审校 Wiki、实体图鉴与《泰拉年表》
装进本地资料包，为 Agent 提供带原文行号的检索与引用工具，并可按需接入
PRTS.chat 云端混合检索与 DSH 原生网页工具。

[中文](README.md) | [English](README.en.md)

## 这是什么

本插件为 DSH 提供明日方舟与终末地联合资料检索能力。插件先从 PRTS.chat 取得已批准的
最新 release 与逐文件摘要，再从 ModelScope 镜像或 PRTS.chat 下载本地语料；
Agent 可以离线检索并按原文行号阅读材料；可选的 PRTS.chat 云端混合检索用于发现
候选材料，并将结果映射回本地原文核验。由于云端服务承载能力有限，当前为每个用户
每日提供 1000 次 DSH 匿名云端检索调用额度；额度策略可能根据实际运行情况调整。

- **本地检索**：`corpus_search` 用同一组参数同时检索两款游戏，
  支持游戏、资料类型、内容形式、角色、活动／任务、Wiki 字段等结构化过滤；
- **原文阅读**：`corpus_read` 可按关卡代号、密录名、角色资料类别直接定位，
  并可连续阅读整个明日方舟活动或终末地任务；引用格式统一为《篇章名》第 N 行；
- **活动时间线**：`timeline_search` 检索 PRTS Wiki《泰拉年表》本地投影，
  支持实体别名自动裂变与出处标记反查；
- **云端混合检索**：双模块模式下一次 `cloud_search` 默认并行查询两款游戏的图谱、档案、
  原文与 Wiki，联合排序后映射回本地篇章；

## 数据来源声明

- **自建 Wiki 数据**：来源于 [littlepangding/arknights_lore_wiki](https://github.com/littlepangding/arknights_lore_wiki)。
- **《泰拉年表》数据**：来源于 [PRTS Wiki《泰拉年表》](https://prts.wiki/w/%E6%B3%B0%E6%8B%89%E5%B9%B4%E8%A1%A8)，供本插件的时间线检索使用。

## 核心特性

| 特性 | 说明 |
| --- | --- |
| 按需加载 | 工具只挂在「PRTS 模式」预设下，标准/极简等模式不受污染 |
| 双游戏资料 | 明日方舟与终末地原文、档案、审校 Wiki、实体与时间线使用统一工具检索 |
| 读取去重 | 会话级证据状态跟踪已进入模型上下文的原文，重复/重叠读取自动回放或只补读新行 |
| 自带皮肤 | Harness 默认 / PRTS Agent / Endfield AIC / 莱茵生命资料馆 |

## 莱茵生命资料馆

在 **设置 → 插件 → PRTS 语料 → 界面皮肤** 选择「莱茵生命资料馆」，然后在会话中打开
「资料馆」。检索阵列、调查板、重点证据盒和双层档案架位于同一个三维场景。
可用底部导航、边缘入口或点击可见模型切换，镜头连续移动。

- **检索阵列**保留候选资料；**档案架**收录 Agent 实际读过或用户主动收藏的资料，每页上下两层、每层十二份。
- **重点证据盒**属于指定调查板，用于暂存待核对、待整理的材料；放入盒子不会自动标成已读，也不必先收藏。
- **调查板**由 Agent 持续添加线索与关系，中央保留带版本的报告。新建还是延续调查由 LLM 通过调查工具决定，追问不会机械地创建新板。
- 纸片支持拖动、缩放、红绳连线与手动编辑。编辑沿用同款纸色和编号，自动保存并支持撤销；板面数据由 Host 持久化。
- 手动检索支持本地与云端模式及高级设置。阅读器支持 Markdown、来源版本、命中位置与实际已读范围；返回时恢复原入口、筛选和阅读位置。
- 手动浏览会暂停 Agent 自动跟随，点击「恢复跟随」后继续。用户查看的板、Agent 工作板和证据盒目标分别管理。

长文分页、档案架分页、减少动态效果和无 WebGL 时的文字阅读模式均可用。
操作细节见 [资料馆说明](docs/rhine-lab.md) 与 [交互与资料分层](docs/rhine-interaction-flow.md)。

前端沿用 Three.js + TypeScript + Vite。三维主体、档案循环导航与渲染使用原项目实现和
默认画质；主界面按调查用途重新设计，原版演示档案已全部移除。开发预览读取本地真实资料包，不连接 Agent：

```bash
npm ci
npm run build:rhine
npm run preview:rhine
```

打开 `http://127.0.0.1:4177`。可通过 `PRTS_RHINE_RELEASES=/path/to/releases` 指定只读资料包目录。
直接预览证据白板：`http://127.0.0.1:4177/?rhineView=board`。
语法检查使用 `npm run check`，测试使用 `npm test`；浏览器检查使用 `npm run test:rhine:browser`（需要 Playwright）。

## 环境要求

- Web：Node.js **≥ 22.19**，DSH 运行时 **≥ 0.1.2-alpha.2**；当前适配目标为 **0.1.5-alpha.1**
- 官方 Electron Desktop：使用与插件兼容的 DSH 桌面版本；桌面自带运行时
- 磁盘空间：语料大小以设置页与 release 清单为准，下载前不会自动占用完整语料空间

## 安装

### 当前可用：Web 本地安装

npm 发布正在准备中，目前请从本地源码安装，或使用已内置插件的 PRTS Portable：

```bash
npm install --global @deepseek-ai/dsh@0.1.5-alpha.1
git clone https://github.com/HTian-qwq/prts-terrarchive.git
cd prts-terrarchive
node bin/install.js web
```

本地安装器把插件加入指定 profile，并创建或迁移 `$DSH_HOME/.agent-presets/prts` 中的
兼容预设。省略第二个参数时使用当前插件目录，也可以传入另一个本地目录或压缩包：

```bash
node bin/install.js web /path/to/prts-terrarchive
```

### npm 发布后：Web

发布后可直接安装插件 bundle，无需额外运行安装脚本：

```bash
dsh plugin --profile web add prts-terrarchive@0.2.0
```

重启 `dsh web` 后，插件将自带的「PRTS 模式」模板写入宿主的用户预设目录（通常为
`$DSH_HOME/.agent-presets/prts`），模式列表自动发现它；npm 安装不执行 `postinstall`。
默认模式、预设目录配置和正在运行的会话保持不变。已有无标记的 `prts` 预设和用户修改过的
预设完整保留；带插件内容标记且未修改的模板会随插件升级。禁用或卸载插件保留这些用户文件，
不再使用时可从 DSH 的预设管理中删除「PRTS 模式」。

```bash
dsh plugin --profile web remove prts-terrarchive
```

### 官方 Electron Desktop

官方仓库已有 Electron 实现，目前公开产品页仍以 npm Web 和源码启动为入口，尚未确认
公开发布的官方桌面安装器。此处说明为适配该实现准备的安装方式，插件也尚未发布到 npm。

取得兼容桌面版本、且插件发布到 npm 后，在 **桌面应用的插件管理窗口** 输入
`prts-terrarchive@0.2.0` 安装，随后选用「PRTS 模式」。官方桌面只接受 npm registry
包名和版本，不接受 GitHub 地址、本地目录或 tarball；其 `desktop` profile 由应用管理，
不要运行 `node bin/install.js desktop` 或 `dsh plugin --profile desktop`。

Web 与官方桌面共享默认的 `$DSH_HOME` 用户资料，但各自安装插件。插件包包含界面、地图
模型、贴图、技能和预设，**不包含语料、Node/DSH 运行库或用户数据**。首次使用请在
「设置 → 插件 → PRTS 语料」自行下载语料，切换皮肤无需另下模型和贴图。

PRTS Portable 发行包预装插件、预设和完整语料，解压后无需另行下载语料。
官方 Electron 便携版使用 `build-electron.ps1` 构建，原 WebView2 构建入口继续保留，
详见 [Portable 仓库](https://github.com/HTian-qwq/prts-terrarchive-portable)。

Portable 打包器已放置插件时，仍可使用 `node bin/install.js web --preset-only` 生成或迁移
兼容预设；该选项不调用 DSH CLI。

### Windows

Web 本地安装需要可用的 `dsh.cmd`。安装器经 cmd.exe 调用它，插件路径含换行或
`%` `!` `&` `|` `<` `>` `^` `"` 时会明确报错，请改用不含这些字符的目录。
`DSH` 环境变量可指定 `dsh.cmd` 的绝对路径。官方 DSH 的语料默认保存到
`%USERPROFILE%\.dsh\prts-corpus\releases`；Portable 的会话和设置保存在发行目录的
`userdata`，语料及后续资料更新保存在 `corpus/releases`。

## 安装后：五步上手

1. **重启** `dsh web` 或所用桌面应用；
2. **设置 → 插件 →「PRTS 语料」**：选择皮肤（Harness 默认 / PRTS Agent / Endfield AIC / 莱茵生命资料馆）；皮肤模型、贴图与字体已随插件包安装；
3. **版本管理**：Portable 已附带完整语料；其他安装方式下载双游戏资料（优先 ModelScope 镜像；大小以设置页与当前 release
   清单为准）。未安装资料时
   PRTS 模式仍可进入；调用本地工具会提醒前往本设置页安装；
4. **新建会话，顶部模式下拉选「PRTS 模式」**；
5. 直接用自然语言提问，或让模型调用下列工具。

## PRTS 模式的工具面

| 来源 | 工具 | 用途 |
| --- | --- | --- |
| dsh-base（所有模式共有） | bash/sandbox 等 | 常规 Agent 能力，本插件不裁剪 |
| 本插件 | `corpus_search` | 本地语料 grep 检索与目录浏览 |
| 本插件 | `corpus_read` | 按玩家可见定位器或自然标题读取官方行号原文 |
| 本插件 | `corpus_i18n` | 终末地官方多语言原文查询、名称与档案对照 |
| 本插件 | `timeline_search` | 活动时间线检索 / 出处反查 |
| 本插件 | `cloud_search` / `cloud_inspect` | PRTS.chat 云端混合检索（默认匿名会话） |
| `@deepseek-ai/dsh-tool-web` | `web_search` / `web_fetch` | 公网检索与已知 URL 精读核验 |
| `@deepseek-ai/dsh-tool-skill` | skill 加载器 | 按需加载检索策略技能 |
| 本插件 | `prts-retrieval` 技能 | 检索配方与字段语义（按需注入，不占 system prompt） |

## 工具详解

### corpus_i18n — 终末地官方多语言查询

使用带本地化附件的终末地资料包（插件 0.2.0 起支持）：

```js
corpus_i18n({query: "管理员，你来了。", languages: ["EN", "JP", "KR"]})
corpus_i18n({title: "<检索结果的完整标题>", line: 1, languages: ["EN"]})
```

也可用已有 `document_uid` 替代标题。名称/原句默认精确匹配，片段可加 `match_mode:"literal"`；外语反查加 `source_language:"EN"`。返回官方字典中的文本及来源，默认不显示内部文本 ID；显式设 `include_ids:true` 才返回字符串 ID，供 `text_ids` 精确复查。空译文、未映射来源、未安装附件分别报告，不自动生成译文。

角色档案按整条记录、档案库按内容块返回，中文行号只是来源定位，不表示各语言分段相同。长记录会分页，原样提交 `page.continuation` 即可续查。旧资料包仍可搜索和阅读；多语言附件须随新资料版本安装。

构建方式和数据格式见 [官方多语言工具](docs/endfield-official-i18n.md)。

### corpus_search — 本地语料检索

像 grep 一样搜索本地语料；命中立即返回原行及上下各一行，按文档归并。`query` 使用
短实体名、篇章展示名或原句片段；也可省略 `query`，仅按过滤条件列出资料入口。

| 参数 | 说明 |
| --- | --- |
| `query` | 搜索词（≤512 码点）；在 NFKC 归一化 + 小写后的文本上匹配 |
| `games` | 可选游戏过滤；省略时同时搜索 `arknights` 与 `endfield` |
| `resource_types` | 资料类型过滤（数组内 OR）；明日方舟与终末地可选值见下文 |
| `content_types` | 内容形式，例如 `dialogue`、`cutscene`、`radio`、`sns_chat` |
| `collection_names` | 明日方舟活动名或终末地任务名，使用同一个字段 |
| `match_mode` | `literal`（默认，连续字面匹配）/ `regex`（线性安全子集：字面量、`^`/`$`、`.`、字符类、转义和固定次数 `{n}`；不支持分组、分支及可变量词） |
| `character_names` / `story_names` / `activity_names` | 角色 / 篇章 / 活动展示名过滤 |
| `entity_names` | 只返回出现指定实体的行（自动展开别名） |
| `speakers` | 结构化说话人过滤，只匹配亲口台词 |
| `wiki_sections` | Wiki 标签字段过滤（相关活动、剧情总结、角色剧情概括等 16 种） |
| `context_terms` | 要求命中附近（±3 行）同时出现的语境词，≤8 个 |
| `after` | 下一页的版本绑定可读锚点 `{ data_version, resource_type, title, position }`；与原搜索条件一起原样提交 |

约束：过滤数组每项非空、最多 16 项、单项最长 512 码点。结果预算固定，
保留原搜索条件，并把返回的 `next_after` 原样放入 `after`，可确定性扫描到
`exhausted=true`。锚点使用完整 `data_version`、资料类型和自然标题；资料版本切换后
旧锚点会被拒绝，必须重新搜索。分页不向模型暴露内部签名串。

**明日方舟资料类型（resource_types）**：`story` 官方剧情原文；`character_profile` 档案/招聘/
潜能；`character_module` 模组；`character_voice` 语音；`character_skin` 时装；
`operator_record` 干员密录；`character_bundle` 指定角色的档案+模组+语音+密录；
`character_wiki` 规范角色 Wiki；`story_wiki` 活动/密录 Wiki；
`character_activity_wiki` 角色×活动辅助 Wiki；`reviewed_wiki` 全部自建 Wiki；
`terra_journey` 大地巡旅；`entity_profile` 实体资料；`reference` 时间线等引用资料。

**终末地资料类型**：`original_story` 官方剧情原文；`archive` 官方档案；
`knowledge` 知识资料；`wiki` 整理性 Wiki；`character_story` 角色故事；
`timeline` 时间线资料；`entity_profile` 实体资料。可配合 `content_types` 区分对话、
过场、广播、通讯、环境对话、SNS 等内容形式。

### corpus_read — 原文阅读

优先使用游戏内关卡代号、密录名、角色名、活动名或任务名；无法稳定定位时再使用搜索返回的完整标题。
不使用内部 `document_id`、ref 或路径。搜索结果只在同名歧义时给出公开稳定的 `document_uid`；它替代 `title`，不得同时提交两者。同名多合集不会自动合并。

| 用法 | 参数 |
| --- | --- |
| 明日方舟关卡 | `stage_code`；同代号多篇时加 `story_part`：`before` / `after` / `story`；加 `line` 可定点读上下文 |
| 干员密录 | `character_name` + `record_name`；多段密录加 `segment` |
| 角色官方资料 | `character_name` + `material`，类别为 `profile/module/voice/skin/recruitment/potential` |
| 双模块同名角色消歧 | 在角色定位参数之外加 `game: "arknights"` 或 `game: "endfield"`；无同名歧义时不填 |
| 整