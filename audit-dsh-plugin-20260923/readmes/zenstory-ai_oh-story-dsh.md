<p align="center">
  <img src="https://zenstory.ai/brand/zenstory-ai-mark.svg" alt="" width="76" height="76">
</p>

<h1 align="center">Oh Story DSH</h1>

<p align="center">
  <b>小说、短剧、互动游戏与视频解说创作工作台，装进 DeepSeek Harness。</b>
</p>

<p align="center">
  <a href="https://zenstory.ai/zh/dsh"><b>项目主页</b></a>
  &nbsp;·&nbsp;
  <a href="#安装"><b>安装</b></a>
  &nbsp;·&nbsp;
  <a href="#看看它的输出"><b>看看它的输出</b></a>
  &nbsp;·&nbsp;
  <a href="README_EN.md"><b>English</b></a>
</p>

<p align="center">
  <a href="https://github.com/zenstory-ai/oh-story-dsh/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/zenstory-ai/oh-story-dsh?style=flat-square&color=22D3EE&logo=github&logoColor=white&label=Stars"></a>
  <a href="https://github.com/zenstory-ai/oh-story-dsh/releases/latest"><img alt="Release" src="https://img.shields.io/github/v/release/zenstory-ai/oh-story-dsh?style=flat-square&color=081431&label=Release"></a>
  <img alt="Workbenches 4" src="https://img.shields.io/badge/Workbenches-4-081431?style=flat-square">
  <a href="./LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-1F6FEB?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/zenstory-ai/oh-story-dsh/issues"><img alt="GitHub Issues" src="https://img.shields.io/badge/GitHub%20Issues-181717?style=for-the-badge&logo=github&logoColor=white"></a>
</p>

## 这是什么

`oh-story-dsh` 是 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）的社区插件，与 DeepSeek 无隶属关系。装上它，DSH Web 里多出四个创作工作台：小说、短剧、游戏、视频解说。Agent、会话、模型、权限审批和 Chat 仍然全是 DSH 原生的，插件只添加创作 Skills、专业 Roles、项目文件协议和工作台界面，不带第二套 Agent 运行时或项目数据库。

| 工作台 | 上游能力（固定版本，随插件打包） | 主要入口 |
| --- | --- | --- |
| 小说 | [Oh Story 0.7.10](https://github.com/zenstory-ai/oh-story-claudecode/releases/tag/v0.7.10) · 13 Skills · 7 Roles | `/story`、`/story-long-write`、`/story-review` |
| 短剧 | [Drama Skills 0.7.0](https://github.com/zenstory-ai/drama-skills/releases/tag/v0.7.0) · 11 Skills | `/short-drama`、`/short-drama-write`、`/short-drama-storyboard`、`/short-drama-edit` |
| 游戏 | [NovelToGame 0.3.1](https://github.com/zenstory-ai/novel-to-game) · 7 Skills · 《金瓶梅》可玩示例 | `/novel-to-game quick`、`/game-build`、`/game-qa` |
| 视频 | [video-recap-skills 0.5.0](https://github.com/zenstory-ai/video-recap-skills) · 6 Skills | `/video-recap`、`/video-script` |

> 最新版本 **v0.1.9**（2026-09-10）。变更见 [CHANGELOG.md](CHANGELOG.md) 与 [Releases](https://github.com/zenstory-ai/oh-story-dsh/releases)；升级步骤见常见问题[「升级到新版本后要做什么」](#升级到新版本后要做什么)。

## 四个工作台

下面四段动图都是打包后的插件装进官方 DSH Web 的真实画面，取自原生集成测试的录制；右侧 Chat、模型、用量和耗时都是 DSH 自己的。

### 小说

![小说工作台](docs/images/story-workbench-demo.gif)

文件树、编辑器、Chat 三栏。Agent 写文件时编辑器跟着它走，点 Chat 里的文件名就能在编辑器打开。覆盖长篇、短篇、选题、扫榜、拆文、导入、审稿、去 AI 味与封面。

### 短剧

![短剧工作台](docs/images/drama-workbench-demo.gif)

每集最多五份 Markdown：`剧本.md`、`视觉设定.md`、`分镜.md`、`图片提示词.md`、`视频提示词.md`。「生产」视图把它们投影成镜头板、素材板、任务/版本、成片顺序和关系画布，并就地指出重复 ID、悬空引用与格式错误。生图、生视频、生音乐的任务先预览、你确认后才调用供应商 API；成片由 `/short-drama-edit` 按《剪辑单.md》渲染到 `剧集/<EP>/制作成果/成片/`。

### 游戏

![游戏工作台](docs/images/game-workbench-demo.gif)

左侧实时试玩、右侧 Chat。`/novel-to-game quick` 的产物写进 `game-adaptations/<project>/`，`build/app/index.html` 就绪后自动进入项目列表，可刷新、全屏、切换项目。游戏在独立 origin 与 iframe sandbox 里运行。

### 视频解说

![视频工作台](docs/images/video-workbench-demo.gif)

左侧预览、右侧 Chat。项目放在 `video-recaps/<project>/`：原片在 `sources/`，工作产物在 `work/`，交付在 `outputs/`。可在原片、剪后片、成片之间切换，查看阶段提示、运行清单与质检产物；视频经 HTTP Range 流式预览。

### 四个工作台共同的规矩

- **文件就是创作事实**：工作台只投影项目里的文件，不写并行数据库；改哪份文件就是改哪一层决定。人工未保存的内容不会被并发的 Agent 写入覆盖。
- **花钱的事先确认**：任何调用供应商 API 的任务都先在界面上看到准确内容，明确确认后才执行；Key 只放在宿主机环境变量里，插件只报告有没有配。
- **不占别的场景**：只有当前 workspace 里真的有创作项目时才接管布局，随时可收起，收起后会话回到 DSH 原生形态，选择按 workspace 记住。

各工作台的边界与协议见[架构说明](docs/ARCHITECTURE.md)。

## 安装

需要 Node.js 24+。安装命令会临时提供 pnpm，只装了 Node.js 的机器也能执行：

```bash
npx -y --package pnpm@11.7.0 --package @deepseek-ai/dsh@0.1.5-rc.1 dsh plugin --profile web add @oh-story/dsh@0.1.9 &&
npx -y @deepseek-ai/dsh@0.1.5-rc.1 web
```

保持终端运行，浏览器默认自动打开；没有自动打开就复制终端打印的完整 `http://127.0.0.1:3080/?token=...` 链接访问，首次认证需要链接里的 token。关闭终端会停止服务。安装与启动请使用同一个 dsh 版本。

开始 AI 创作前，在 DSH 的「设置 → 模型」中添加 Provider 并填入 API Key，或在启动前设置环境变量 `DEEPSEEK_API_KEY`。只查看已有作品可在首次引导中选择「稍后配置 / Configure later」。

<details>
<summary>从 GitHub Release 安装预构建包</summary>

GitHub Release 中的预构建包经过同一套测试：

```bash
npx -y --package pnpm@11.7.0 --package @deepseek-ai/dsh@0.1.5-rc.1 dsh plugin --profile web add https://github.com/zenstory-ai/oh-story-dsh/releases/download/v0.1.9/oh-story-dsh-0.1.9.tgz &&
npx -y @deepseek-ai/dsh@0.1.5-rc.1 web
```

</details>

<details>
<summary>视频工作台的宿主机依赖</summary>

视频流水线还需要宿主机安装 Python 3.10+ 与带 libass `subtitles` 滤镜的 ffmpeg/ffprobe（macOS `brew install ffmpeg`，Debian/Ubuntu `sudo apt install ffmpeg`）。视频解说另用 `MIMO_API_KEY`（Fish Audio TTS 另需 `FISH_API_KEY`）。

</details>

<details>
<summary>配置媒体生成 API（短剧生产需要）</summary>

DeepSeek 负责写剧本、分镜和提示词；生图、生视频、生音乐由短剧「生产」交给 `short-drama-produce` Skill，再调用下面的供应商 API 完成。Key 在启动 DSH 之前写入宿主机环境变量：

| 能力 | 供应商 | 必需环境变量 | 可选 |
| --- | --- | --- | --- |
| 图片 | GPT Image 2 | `OPENAI_API_KEY` | `OPENAI_BASE_URL` |
| 视频 | Seedance（火山方舟） | `ARK_API_KEY`、`SEEDANCE_MODEL` | `SEEDANCE_BASE_URL`、`SEEDANCE_ALLOWED_RATIOS`、`SEEDANCE_MIN_DURATION`/`SEEDANCE_MAX_DURATION` |
| 视频 | MiniMax H3 | `MINIMAX_API_KEY`、`MINIMAX_VIDEO_MODEL`、`MINIMAX_VIDEO_RESOLUTIONS` | `MINIMAX_VIDEO_BASE_URL`、`MINIMAX_VIDEO_RATIOS`、`MINIMAX_VIDEO_MIN_DURATION`/`MINIMAX_VIDEO_MAX_DURATION` |
| 音乐 | MiniMax Music | `MINIMAX_API_KEY` | `MINIMAX_BASE_URL` |

```bash
export OPENAI_API_KEY=...            # 图片
export ARK_API_KEY=... SEEDANCE_MODEL=...   # 视频，模型/Endpoint ID 以账号开通的为准
npx -y @deepseek-ai/dsh@0.1.5-rc.1 web
```

只配置用得到的那几个即可：没有视频 Key 仍然可以写分镜、生成关键帧图片。「生产」视图顶部会显示每个供应商是否已配置、缺哪个变量。插件启动时会把这四个内置 adapter 登记到一份不含凭据的配置文件（默认在系统临时目录下仅当前用户可读写的 `oh-story-dsh-<uid>/` 里，「生成环境」条会显示完整路径），Agent 运行 `production_tool.py run` 时直接引用它；自己写 adapter 或改超时，就把文件路径写进 `OH_STORY_DRAMA_ADAPTER_CONFIG`。每个供应商的参数、分辨率与时长约束见随包的 `short-drama-produce/references/providers/`。小说封面使用当前 Preset 里可见的图片生成工具。

</details>

<details>
<summary>装进独立 profile，按需启动</summary>

插件装进哪个 profile，那个 profile 的每个 Session 就都会加载创作 Skills。想让原版 `web` 保持干净，就把插件装进独立 profile：

```bash
npx -y --package pnpm@11.7.0 --package @deepseek-ai/dsh@0.1.5-rc.1 dsh plugin --profile story add @oh-story/dsh@0.1.9
```

新 profile 默认没有界面。编辑 `~/.dsh/profiles/story/package.json`，把 `dsh.profile.bundles` 改成：

```jsonc
"bundles": [
  "@deepseek-ai/dsh-base",
  "@deepseek-ai/dsh-web-app",
  "@oh-story/dsh"
]
```

`@deepseek-ai/dsh-web-app` 是 DSH 自带的 Web 界面包，需要在创作插件之前加载。之后两个 profile 用不同端口可以同时运行，模型、凭据、workspace 与历史会话由 DSH 统一保存：

```bash
npx -y @deepseek-ai/dsh@0.1.5-rc.1 web                          # 原版 DSH
npx -y @deepseek-ai/dsh@0.1.5-rc.1 --profile story --port 3081  # 创作工作台
```

</details>

## 开始创作

首次进入会先看到 DSH 首页。点击左侧 Workspaces 旁的 **＋（添加工作区 / Add workspace）**，选择存放作品的文件夹，再在下方 **选择工作区 / Choose workspace** 中选中该目录，DSH 会打开一个空白会话。目录里已有创作项目时，会显示「小说 / 短剧 / 游戏 / 视频」四个工作台标签；空目录保留 DSH 原生 Chat，输入 `/story`、`/short-drama`、`/novel-to-game quick` 或 `/video-recap` 开始，Agent 写出第一个创作文件后工作台自动出现。

下面的请求复制改一改就能用，替换方括号内容后发送。

**开一本新书**：

> 我想开一部 [类型/题材] 新书。先从我提供的材料中分开已确定事实与待决问题；只规划一个有边界的开篇，交付核心冲突、视角限制、前三章变化和待决项。不要自动写正文；题材取舍、角色动机和长期方向留给我确认。

**已有稿件，第一轮只讨论续写方案**：

> 我想规划这部自有或已获授权小说的下一场戏。只阅读当前 workspace 中我点名的 [章节文件] 和 [设定文件]；[末尾片段] 尚未写完，不要把它算成完整章节。先列出与下一场戏有关的已知事实、视角人物目前知道的事，以及尚缺或冲突的信息。再给两个续写方向，分别说明人物要什么、阻力是什么、行动造成什么可见变化；不要提前揭示 [秘密]，停在 [场景边界]。本轮只在 Chat 回复，不创建、移动或改写任何文件。

**短剧、游戏、视频解说**，直接说目标：

```text
用 /short-drama 初始化一个都市打脸题材的短剧项目，竖屏 9:16，只写第 1 集，先不生成任何媒体。
用 /novel-to-game quick 把 [小说文件] 改编成可玩游戏，平台、类型和引擎由你推荐，首个构建控制在 15 分钟以内。
给 /path/to/video.mp4 做一个 3 分钟中文解说成片，保留关键原声，字幕烧进画面。
```

## 看看它的输出

节选自随包示例工程（同步自 [oh-story-claudecode 的 demo](https://github.com/zenstory-ai/oh-story-claudecode/tree/abe96630d115afbd528f2329e2d8d604d5d5673c/demo/%E9%95%BF%E7%AF%87) 与 [drama-skills 的公开样例](https://github.com/zenstory-ai/drama-skills/tree/bc96c5eb9c91cccd1c613c2b34645c35f1989a28/examples/creator-first/EP001)），省略处以「……」标出。

### 续写靠状态卡，不靠对话记忆

写第 21 章之前，[`追踪/上下文.