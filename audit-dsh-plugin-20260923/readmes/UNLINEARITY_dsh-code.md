# DSH-Code

[English](README.en.md) | 中文

<p align="center"><img src="docs/pictures/dsh-1.png" width="95%" alt="DSH-Code 欢迎界面与模型状态"></p>

<p align="center"><img alt="Typing SVG" src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&amp;weight=500&amp;size=22&amp;duration=4000&amp;pause=700&amp;color=4176E6&amp;center=true&amp;vCenter=true&amp;width=680&amp;lines=DeepSeek+Harness+Code;DSH+%E5%86%85%E6%A0%B8%E7%9A%84%E7%BB%88%E7%AB%AF%E7%BC%96%E7%A0%81%E7%95%8C%E9%9D%A2"></p>
<p align="center">
  <a href="https://github.com/deepseek-ai/deepseek-harness"><img alt="DeepSeek Harness" src="https://img.shields.io/badge/DeepSeek-Harness-4176E6?style=for-the-badge&amp;logo=deepseek&amp;logoColor=white&amp;labelColor=1c1917"></a>
  <a href="https://www.npmjs.com/package/@deepseek-ai/dsh"><img alt="dsh version" src="https://img.shields.io/badge/dsh-0.1.5--rc.2-4176E6?style=for-the-badge&amp;logo=deepseek&amp;logoColor=white&amp;labelColor=1c1917"></a>
  <a href="https://github.com/UNLINEARITY/dsh-code/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/UNLINEARITY/dsh-code?label=Stars&amp;style=for-the-badge&amp;logo=github&amp;logoColor=white&amp;color=4176E6&amp;labelColor=1c1917"></a>
  <a href="https://www.npmjs.com/package/dsh-code"><img alt="npm version" src="https://img.shields.io/npm/v/dsh-code?label=npm&amp;style=for-the-badge&amp;logo=npm&amp;color=cb3837&amp;labelColor=1c1917"></a>
  <a href="https://github.com/UNLINEARITY/dsh-code/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/UNLINEARITY/dsh-code?label=License&amp;style=for-the-badge&amp;logo=opensourceinitiative&amp;color=4176E6&amp;labelColor=1c1917"></a>
</p>

---

> 注：自 DSH-Code 1.0.0 起，代码由 DSH-Code 自迭代完善，不使用外部 Agent / CLI 完成！

## 一、项目概览

**DSH-Code 是 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（`dsh`）的终端编码界面。** 它以树外 bundle 的形式组合在官方 `@deepseek-ai/dsh-base` 之上，与 Harness Web UI 使用同一套 Agent、Session、工具、命令、技能、权限、sandbox、上下文压缩与插件服务。

DeepSeek Harness 将模型、工具、存储、策略和界面作为插件，通过 Cordis 注册。持久化会话事件记录恢复对话与运行状态所需的信息。DSH-Code 保留这套结构，并补充适合编码任务的终端工作流。界面采用开发者熟悉的终端操作方式，运行行为仍由 DSH 服务和配置决定。

## 二、快速开始

需要 Node `^22.19 || >=24` 和预览版 `dsh` CLI（当前版本线：`@deepseek-ai/dsh@0.1.5-rc.2`）。未配置模型时仍可进入 TUI、查看会话和使用非模型功能；在 `/model` 中按 Tab 进入供应商管理，配置 API key、OAuth 与设备码登录。

### 1. 安装与更新

从 npm 安装（推荐）。装好后 `/update` 和 `deepseek update --apply` 都能用：它们查询 npm 上的新版本，确认后按提示升级。

```sh
npm install -g @deepseek-ai/dsh@0.1.5-rc.2 pnpm
npm install -g dsh-code@1.5.0
dsh plugin --profile cli add dsh-code@1.5.0
```

npm 不可达时（网络受限、镜像临时故障），改用 GitHub Release tarball。每次打 tag 由 CI 构建并挂到 Release，lib 已预构建，安装机不需要工具链：

```sh
npm install -g @deepseek-ai/dsh@0.1.5-rc.2 pnpm
npm install -g https://github.com/unlinearity/dsh-code/releases/download/1.5.0/dsh-code-1.5.0.tgz
dsh plugin --profile cli add https://github.com/unlinearity/dsh-code/releases/download/1.5.0/dsh-code-1.5.0.tgz
```

> npm 脚本提示：npm 11.6+ 可能在全局安装时提示 `npm warn install-scripts`（node-pty、koffi 等原生依赖的构建脚本未获批准）。宿主随包自带预编译产物，常规平台可直接忽略；若安装后出现原生模块报错，按 npm 提示执行 `npm install -g --allow-scripts=<包名列表>` 后重装。
>
> 版本对齐：dsh-code 面向 dsh `0.1.5-rc.2` 构建，全部 Harness 依赖均精确锁定为 `0.1.5-rc.2`。本地 `link:` 挂载请先 `git pull && pnpm install && pnpm build`，不要对开发挂载跑更新器。
>
> 升级说明：旧会话与旧参数中记录的 `code` 预设会自动映射到上游已改名的 `ptc`，无需手动迁移。会话日志读取端随上游升级到格式 v3：旧格式日志在读取时由内核自动迁移，磁盘上的原始文件保持不变。
>
> 从 GitHub tarball 装的版本可能领先 npm 一步（npm 上还没同步这个版本时）。更新器只认 npm，这种情况会写明「新于 npm，不降级」而不是「已是最新」；等 npm 同步后再用 `/update`。

### 2. 启动指令

可用的启动指令：
```sh
dsh --profile cli
deepseek
dsh-code
```

`dsh --profile cli`、`deepseek` 与 `dsh-code` 是并列的启动命令。`deepseek` 与 `dsh-code` 都是 `dsh --profile cli` 的全局别名，后续参数会原样转发，例如 `deepseek --resume abc123`。


> DeepSeek Harness 目前仍处于 developer preview，可能出现破坏兼容性的变化；DSH-Code 会持续跟随其插件接口演进。

安装、原生模块和插件加载问题，请先运行 `deepseek doctor` 自检，更多排查见[常见问题与排障](docs/problems.md)。

## 三、核心功能与使用方式

DSH-Code 的重点是让 DSH 的 Agent、模型、工具和持久会话可以直接在终端中使用，并覆盖从编写代码到审查修改的完整工作流。

### 1. 会话管理

- 使用 `/new` 新建会话，或通过 `/resume`、`--continue` 恢复已有会话
- 使用 `/fork` 从历史节点创建新的工作分支，同时保留原会话
- 按当前目录、更新时间和会话范围搜索历史记录
- 使用 Up/Down 召回输入历史（含 / 指令），或通过 `/history` 搜索过去的提示词与指令
- 支持持久标题、Markdown 导出、上下文占用、token、缓存、TTFT 和耗时统计；`/usage` 面板按上游 token 统计给出四个互不重叠的桶、按模型合并的总量和按回合明细
- 状态栏的 `入` 只算未命中缓存的输入，`缓存` 同时给出缓存读取量与命中率——两者相加才是真正计费的输入侧
- 恢复会话时同步恢复该会话使用的 Agent Preset、模型选择和子代理列表；欢迎页同时显示 dsh 与 dsh-code 版本

<p align="center"><img src="docs/pictures/dsh-3.png" width="95%" alt="可搜索的会话恢复选择器"></p>

<p align="center"><img src="docs/pictures/dsh-4.png" width="95%" alt="可搜索的提示词历史选择器"></p>

### 2. Agent、模型与扩展

- 每个会话可以选择独立的 Agent Preset，用于组合工具、提示词、技能、上下文压缩、plan mode 和 subagent 能力
- 使用 `/mode` 选择 `standard`、`ptc`、`minimal`、`cordis` 或用户自定义 Preset（旧名称 `code` 自动映射到 `ptc`）
- 使用 `/model` 切换模型，管理 provider、API key、OAuth/设备码登录、endpoint、可用模型和上下文窗口；`Tab` 进入 provider 管理（已配置供应商置顶分组），任意阶段 `Ctrl+C` 直接退出整个 /model 流程
- 在 provider 列表中，Enter 进入统一配置页：同页填写 API key 与 endpoint（留空即官方默认）、编辑已添加模型的上下文/输出窗口，`Tab` 进入发现页拉取端点真实可用模型并勾选添加
- 在统一配置页的模型行上按 `e` 编辑推理档位声明（格式 `low:low high:high max:max`，`false` 禁用、留空恢复继承），按 `c` 从其他已声明模型逐字复制——例如 GLM 系列按官方三档写 `low:low high:high max:max`，新模型（如 gpt-6）可一键复制 gpt-5.6 的映射
- 在 provider 列表中 `l` 发起登录，`o` 经确认后退出登录
- 自动加载 DSH 中可用的命令与技能；使用 `/help` 查看入口，使用 `/plugin` 检查扩展状态
- 支持 plan、goal、todo、权限、sandbox、subagent 和运行中的补充指令

<p align="center"><img src="docs/pictures/dsh-2.png" width="95%" alt="每会话 Agent Preset 选择器"></p>

<p align="center"><img src="docs/pictures/dsh-5.png" width="95%"></p>

### 3. 模型切换动画

模型或 reasoning effort 发生以下变化时，输入框会播放 Wave、Aurora 或 Pulse：

| 使用场景 | 触发条件 | 动画文字 | 效果档位 |
| --- | --- | --- | --- |
| 官方 DeepSeek 模型 | 切换到该模型，或修改该模型的 reasoning effort | `deepseek` | Flash 使用单波段档位，其他 DeepSeek 模型使用多波段档位 |
| 其他模型 | 切换模型或 reasoning effort 后，实际生效的强度严格高于 `high` | `Into the Unknown` | 使用与非 Flash DeepSeek 模型相同的多波段档位 |

高于 `high` 的等级包括 `xhigh`、`x-high`、`very-high`、`max`、`maximum` 和 `ultra`；`high`、`medium`、`low` 与 `off` 不会为非 DeepSeek 模型触发动画。

| 样式 | Flash | 其他 DeepSeek / `Into the Unknown` |
| --- | --- | --- |
| Wave | 一个蓝色波峰从左向右扫过，约 1.2 秒 | 两个错开的蓝色波峰依次扫过，并带有 `· ✦ ✧` 尾部星光，约 1.5 秒 |
| Aurora | 两条蓝色光带交错漂移，约 1.5 秒 | 三条不同色调的光带交错漂移，约 1.8 秒 |
| Pulse | 一个圆环从输入框中心向外扩散，约 1.1 秒 | 两个圆环先后向外扩散，约 1.45 秒 |

`/animation off` 只关闭 Wave/Pulse、主题颜色流动和彩虹 burst 等纯装饰效果；输入光标、streaming caret、busy chase、Thinking/Deep Diving shimmer 与 `Deep diving...` 耗时仍会更新，避免运行中的界面看起来卡死。

### 4. 编码工作流

- 使用 `@` 引用工作区文件或已有会话；选择 PNG、JPEG、WebP、GIF 时会自动作为真实图片附件
- 支持启动 prompt、多个 `--image` 参数，以及从终端拖入或粘贴附件：图片按图片附件发送，其他文件按原样文件附件发送（单文件 8 MiB、每条消息 8 个以内）
- 使用 `/diff` 按文件检查改动，使用 `/review` 发起只读代码审查（弹出范围选择，diff 整行红绿着色）
- `run_code` 会列出正在执行的子工具调用；workflow 会列出各成员直到结束
- 使用 `/copy` 复制最近一条完整回复，使用 Ctrl+O 查看历史和完整工具详情；仅含思考过程、没有最终正文的中间回复不会单独占据检查条目
- 支持工具审批、结构化提问、plan review、多选和自定义答案
- 使用权限 Preset 和 sandbox 控制 Agent 可以执行的操作；任务运行中仍可补充指令或中断

### 5. 排队与插队

回合运行中你还可以继续输入消息，有两种发送方式：

- **排队**：等这一回合全部结束后，作为新的一回合处理。适合「做完这件再做下一件」。
- **插队**：在这一回合的下一个步骤开始之前交给模型，和当前这次请求一起处理。适合发现它做偏了、要立刻纠正或补充要求。

两者的区别是**模型什么时候能看到它**：排队是等它做完再说，插队是在它下一步动手之前就告诉它。

怎么用：

- 输入框空着按 `Tab` 在两种方式之间切换。提示符（`❯` / `↳`）、空输入框的提示文字和切换时的通知都会写明当前是哪一种；输入框有内容时 `Tab` 仍是补全。
- `/queue` 打开队列面板：对某条按回车即可改为插队，按 `e` 改文字（附件原样保留），按 `d` 删除。
- 输入框空着按 `Delete`，直接取消最新一条排队消息。
- 按 `Esc` 取消当前回合时，**排队的消息保留并接着发出**，插队的消息随这一回合一起丢掉。

会话区里每条提问都是一整行带底色的消息，颜色说明它是怎么发出的：普通消息用主题的亮品牌色，排队用警示色，插队用主题的第三种强调色，并分别带「排队」「插队」字样。底色由主题色算出，所以换主题或重新随机 rainbow 之后会跟着变。

只有**提交那一刻已经有回合在运行**，才记为排队或插队；空闲时提交的消息（哪怕当时选的是插队）都算普通消息，因为它本来就会立刻开始新的一回合。

队列的具体行为、上游两条队列的取出顺序和各主题的色值见 [排队与插队](docs/message-queue.md)。

### 6. 命令与快捷键

启动 TUI：

```sh
dsh --profile cli                    # 新建 standard 会话
dsh --profile cli --mode ptc         # 使用指定 Agent Preset 启动（standard/minimal/cordis/ptc）
dsh --profile cli --continue         # 恢复当前目录最新会话
dsh --profile cli --resume abc123    # 按 id 或唯一前缀恢复会话
dsh --profile cli --session my-id    # 使用指定 id 新建会话
```

进入 TUI 后，可以使用以下内置命令。当前 profile 提供的其他 Harness 命令和用户技能会随安装内容变化，完整列表以 `/help` 显示为准。

#### 会话与记录

| 命令 | 用途 |
| --- | --- |
| `/new [preset]` | 创建新会话，可同时指定 Agent Preset |
| `/resume [id\|前缀]` | 搜索或恢复已有会话 |
| `/search [query]` | 跨会话全文检索（复用 session-q