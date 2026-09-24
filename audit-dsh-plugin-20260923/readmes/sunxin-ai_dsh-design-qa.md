# dsh-design-qa

[![npm](https://img.shields.io/npm/v/dsh-design-qa)](https://www.npmjs.com/package/dsh-design-qa)
[![CI](https://github.com/sunxin-ai/dsh-design-qa/actions/workflows/ci.yml/badge.svg)](https://github.com/sunxin-ai/dsh-design-qa/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

简体中文 | [English](README.en.md)

**让 DeepSeek Harness 里的纯文本模型能看图。**

做这个是为了在 DSH 上实现**产品设计**这项能力：从设计稿写出实现、再自己判断实现得像不像、
不像就修 —— 而 DeepSeek 写得了代码却看不见图，判定那一环做不了。本插件通过一个工具把
多模态能力借给它，让它具备执行产品设计功能所需的那只眼睛。

- **任何纯文本模型都能读图。** 不只是 DeepSeek —— 你在 DSH 里自己接的那些 OpenAI 兼容端点
  同样适用（实测过 OpenRouter 上的 `z-ai/glm-5.2`）。**前提是该模型支持 tool calling**：
  它得能自己调 `deepseek_vision`。官方多模态上线那天，本插件自动让位、可原样留着。
- **把识图做成一个 tool。** 图片不进主模型上下文；它看到一行 `[图片 …]` 提示，需要时自己调
  `deepseek_vision`。不看就不产生任何成本，问什么由模型自己决定。
- **附 eval 与原始输出。** 4 组夹具、23 处注入缺陷、四条通过线 —— 回答的是「借来的这只眼
  够不够格当判定闭环里的裁判」，而不是「模型跑没跑通」。**能看见 ≠ 可用于判定**：看得见但不
  主动看、会编、不稳、说不清，四种失效各对应一条通过线。真值四组齐全、有像素级注入断言，
  **跑分脚本目前接通的是其中 `landing` 一组**；基准那一节每个数字的逐格模型原文都在
  [`eval/runs/`](https://github.com/sunxin-ai/dsh-design-qa/tree/main/eval/runs)，
  **哪几项没有原文，也在那里标明**。

---

## 三步装好

**环境要求**：一个**已经能正常对话**的 DSH —— 也就是工作区选好了、主模型的 key 配好了，
随便发一句能收到回复。npm 安装或源码运行都可以，Node `^22.19 || >=24`（与 DSH 一致）。
macOS / Linux / Windows 通用，安装脚本是一份 Node 实现。

> 刚下载 DSH 还没配过的话先把这一步做完 —— 本插件只负责识图那条链路（`BAILIAN_API_KEY`），
> 主模型的 key 是 DSH 自己的事。两者分开：主模型不通，粘图也不会有反应。

### 1. 拿一个百炼 API Key

去 [阿里云百炼控制台](https://bailian.console.aliyun.com/) 开通并创建 API-KEY。

**新用户每款模型送 100 万输入 + 100 万输出 Token，有效期 90 天**（[官方说明](https://help.aliyun.com/zh/model-studio/new-free-quota)）。
本插件一次识图约 2000 输入 + 400 输出 token，**免费额度够看几百次图**，日常用基本不花钱。

### 2. 装插件

```sh
dsh plugin --profile web add dsh-design-qa
```

> 也可以直接从 GitHub 装（拿到的是 main 上最新的，未必等于 npm 上那版）：
> `dsh plugin --profile web add github:sunxin-ai/dsh-design-qa`

### 3. 补配套并重启

```sh
cd "${DSH_HOME:-$HOME/.dsh}/profiles/web/node_modules/dsh-design-qa"
export BAILIAN_API_KEY=<第 1 步拿到的 key>
node install.mjs --route-only
node install.mjs --restart          # 冷启动。HMR 是关的，刷新浏览器不算
```

装好了。**在对话框里粘一张图，直接问「这是啥」即可。**

> 图片走**粘贴或拖拽**进对话框 —— DSH 的输入框没有单独的上传按钮，
> 左下那个 `+` 是命令菜单不是附件入口，别去找。
> 也可以直接把图片的**绝对路径**或 **http(s) 地址**发给模型，让它自己调 `deepseek_vision`。

不需要告诉脚本 DSH 装在哪 —— 它从 profile 的 `node_modules` 自己解析出本体位置，
npm 装的和源码跑的都认。密钥也不经它的手，只写变量名 `apiKeyEnv: BAILIAN_API_KEY`。

<details>
<summary>第 3 步顺带改了 DSH 本体三处 —— 点开看改了什么、怎么还原</summary>

「在对话框里粘贴图片」这件事插件自己做不到：拦截在 `api-proxy` 的消息准入里，
而 `resolveModelInfo` 直接返回适配器自述、没有 waterfall，插件改不了适配器
硬编码的 `inputModalities: ['text']`。所以只能改本体，三处：

| 落点 | 改动 |
|---|---|
| `dsh-host-apiproxy` | 删掉纯文本路由的图片准入拒绝（一个 `if` 块） |
| `dsh-llm-deepseek` | 图片准入处不再抛错，改成把图片块换成一行 `[图片 … attachment=<id>]` 文字指针；声明了 `image` 的模型照走原生通路 |
| `dsh-llm-pi-ai` | 同上 —— 这条覆盖你自己接的**所有** OpenAI 兼容纯文本端点 |

前两处只让 DeepSeek 路由能粘图；第三处才让「**任何**纯文本模型都能读图」成立。

改动前原文另存为 `<原文件名>.dsh-design-qa-orig`，一条命令还原：

```sh
node install.mjs --revert-patches
```

**完全不想动本体**就加 `--no-patches`。此时粘贴仍会被拒，但**给文件路径、图片 URL
或附件 id 让模型调 `deepseek_vision` 一样可用** —— 只是多贴一次路径。

细节见 [`patches/README.md`](patches/README.md)。

</details>

### 让 DSH 自己装

不想手敲的话，把下面这段整体发给 DSH，它有 bash，会自己跑完：

```text
装 dsh-design-qa，按这五步，不要自己发挥：

1. dsh plugin --profile web add dsh-design-qa
2. cd "${DSH_HOME:-$HOME/.dsh}/profiles/web/node_modules/dsh-design-qa"
3. export BAILIAN_API_KEY=<你的 key>      # 用 export，下一条命令也要用到它
4. node install.mjs --route-only
5. node install.mjs --restart      # 不要用 pkill，那会杀掉你自己

第 4 步会顺带改 DSH 本体三处（粘贴图片必须的），原文自动备份，
node install.mjs --revert-patches 可一键还原。把第 4 步的完整输出贴回给我。
```

**「不要自己发挥」这句请保留。** 三处最容易被自由发挥搞砸：

- **漏掉 `--route-only`** —— 会写进一条与 bundle 重复的插件行，DSH 启动直接抛
  `duplicate loader entry id`，**整个 profile 起不来**。脚本内置了防护会跳过，但不是所有 agent 都读得懂提示。
- **自己 `pkill` 重启** —— agent 通常就跑在那个要被重启的进程里，杀掉等于自杀，
  它拿不到结果也无法确认是否成功。`--restart` 立即返回，重启在它身后完成。
- **自己编一个 key** —— 脚本不代经手密钥，自检会明确报缺少 `BAILIAN_API_KEY`，它应当回来向你要。

**本体补丁没打成会以非零码退出**；缺 key、路由没写这类则是自检里的黄色告警（退出码仍为 0）。
所以别只看退出码 —— 让它把输出原样贴回来，看最后那段自检有没有黄字。

> DSH 的自修改工具（`cordis_define` / `cordis_run`）**不能**用来做持久安装 ——
> 那套是内存态的：不产生插件文件、不改 `cordis.yml`、重启即消失。持久安装必须落到文件，所以走上面这条。

---

## 引擎为什么是 Qwen：它通过了基准测试

不是随手挑的。基准规范在 [`eval/`](https://github.com/sunxin-ai/dsh-design-qa/tree/main/eval)。
下面两组数字**来自两批实验、两组夹具**，逐格原始输出都在
[`eval/runs/`](https://github.com/sunxin-ai/dsh-design-qa/tree/main/eval/runs)。

**三模型横评** —— 6 个定向探针 × 4 种送检方式，跑在一组 mobile dashboard 夹具上。
那组夹具随附于 [`eval/runs/probe-mobile/`](https://github.com/sunxin-ai/dsh-design-qa/tree/main/eval/runs/probe-mobile)，
**不是 `evalset/` 里那 4 组** —— 拿 `evalset/` 复现不出这张表：

| 模型 | 定向探针 | 难档（字重 800 vs 500） | 原始输出 |
|---|---|---|---|
| **`qwen3.8-max`** | **24/24** | **12/12 方向全对** | 逐格可查 |
| `qwen3-vl-plus` | 21/24 | 1/4 | ⚠️ 只留下聚合数字 |
| `moonshot-v1-128k-vision` | 18/24 | 8/15 ≈ 随机 | 逐格可查 |

**零差异对照** —— 把设计稿和它自己配对，报出的任何差异都是幻觉。这是另一批实验，
跑在 `evalset/landing` 上：**`qwen3.8-max` 6/6 全报一致，0 条幻觉。**
横评那组夹具测不出幻觉率（它的 `v1` 本身就不忠实，模型报的「差异」大多为真），
**因此横评表里另外两个模型没有这项数据。**

`qwen3.8-max` 是唯一在难档上稳定的 —— 另外两家在字重方向上等同掷硬币，
而**方向错的判断比漏检更危险**，它会让修复朝反方向走。

## 换成别的模型

**默认值只是默认值。** 插件对模型没有任何硬编码假设，换供应商只改两处：

```yaml
# 1) $DSH_HOME/settings.yaml —— 加一条你自己的路由
llm-pi-ai:
  providers:
    my-vision:
      api: openai-completions
      baseURL: https://your-endpoint/v1
      apiKeyEnv: MY_VISION_API_KEY
      models:
        - id: your-model-id
          input: [text, image]      # ← 必须有，否则被门禁拒绝
```

```yaml
# 2) profile 的 cordis.patch.yml —— 覆盖插件行的 config
- id: design-qa
  config:
    provider: my-vision
    model: your-model-id
```

**注意这里不能写 `- insert:`。** 插件行已经由 bundle 层插好了，再 insert 一条同 id 的
不是覆盖而是**并存**，DSH 启动时抛 `duplicate loader entry id: design-qa`。
上面这种「给出 `id` + 要改的字段」的写法才是按 id 覆盖。

**唯一的硬性要求：那个模型必须真的支持多模态输入，且路由声明了 `input: [text, image]`。**
这是「对端点的声明，不是对端点的检查」（上游 JSDoc 原话）——
声明了但端点实际不收图，会在调用时被供应商拒绝，而不是在配置时报错。

换模型后建议用 [`eval/`](https://github.com/sunxin-ai/dsh-design-qa/tree/main/eval)
重跑一遍基准（只在 GitHub 仓库里，不随包分发），尤其看难档与零差异对照那两项：
**能看见 ≠ 可用**，一个召回高但幻觉多、或每次结论都漂移的模型会让判定循环发散。

这两项分属两组夹具：难档用 `tilebench.py probe`，跑 `runs/probe-mobile/` 那组；
零差异对照用 `tilebench.py pairs`，跑 `evalset/landing`。

## 工具

### `deepseek_vision(image_path, question)`

看一张图并回答问题。`image_path` 三选一：

- 文件绝对路径
- **http(s) 图片地址** —— 文档、网页里的图直接传 URL。走系统代理
  （`HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`），上限 20 MB，跟随重定向
- 上下文 `[图片 …]` 提示里的附件 id（`attachment=<id>` 或裸 id 都行）

调用方**自己就是多模态模型时会被拒绝** —— 它直接看更准也更省，绕一手转述反而丢信息。
这同时是官方多模态上线时的自动让位机制：DeepSeek 声明 `image` 那天，本工具自己退出。

### 配置

| 字段 | 默认 | 说明 |
|---|---|---|
| `provider` | `bailian` | 识图路由名，须声明 `input: [text, image]` |
| `model` | `qwen3.8-max` | 识图模型 |
| `maxTokens` | `4000` | 单次识图输出上限 |
| `reasoningEffort` | `off` | 读数式提问不需要思维链 |

## 提问方式决定成败

以下是实测结论，不是风格偏好。完整版在 [`skills/design-qa/SKILL.md`](skills/design-qa/SKILL.md)。

| 提问形式 | 零差异对照的幻觉 | 难档缺陷召回 |
|---|---|---|
| 「你自己找差异」 | 0/30 | 0/2 |
| 「这个方面有区别吗」 | 0/30 | 0/2 —— 判定题，模型默认答否 |
| 「哪个更大」 | 0/36 | 1/2 —— 留白类被系统性答反 3/3 |
| **「各自是多少」** | **0/12** | **2/2** |

同一个模型、同一批图，**召回从 0/2 走到 2/2，幻觉全程为 0**。换的只是问法。

> **这张表只有第二行可以复核。** 评测脚本里只实现了一种问法 —— `tilebench.py` 的 `FACETS`，
> 五个保真面统统以「有区别吗」结尾，正是第二行；它的 0/30 有逐格原文可查。第一行的开放式提问
> 大致对应 `cmd_pairs`，但没有单独计过分；**「哪个更大」「各自是多少」两行没有任何代码路径** ——
> 没有提示词常量、没有命令、没有输出文件，`0/36` 与 `0/12` 这两个网格在脚本里也找不到对应。
>
> 这张表记录的是真实做过的事，**方向可信，数字请打折扣**。细节见
> [`eval/README.md`](eval/README.md)。

**读数方向可信，量级不可信**：字重真值 800/500 读作 800/700，间距 80/25 读作 72/38 ——
被测侧总被拉向参照侧。用它判断「有没有差异、往哪个方向」，不要当测量值；
实现侧的精确值用 `getComputedStyle` 或像素测量取得。

## 成本

图像 token ≈ 像素数 / 1024（实测 1023–1127 px/token，与长宽比无关）。

| | 均值 | 区间 |
|---|---|---|
| 单次判定 | 0.037 元 | 0.027 – 0.051 元 |
| 延迟 | 9.0s | 6.6 – 11.6s |

**看一次图约 4 分钱。** 单价按 12 元/百万输入、36 元/百万输出估算，上线前请在控制台核对。

## 它什么时候该退休

DeepSeek 官方声明 `inputModalities` 含 `image` 的那天。

届时不需要改任何东西 —— 让位在**两层**上各有一道：

- **运行时**：`deepseek_vision` 查到调用方本身就能看图，**自我拒绝**并让模型直接看，
  图片走官方原生通路，绕一手反而丢信息。
- **安装期**：`install.mjs` 会先读 `llm-deepseek` 声明的 `inputModalities`。
  已经含 `image` 就**拒绝再打那处补丁**并说明原因 —— 上游支持之后，
  那处补丁会把模型本来看得见的图换成一行文字指针，从修复变成破坏。
  判断按找到的每一份 DSH 分别做，机器上有多份时互不影响。

另外两处不设退休判据：`api-proxy` 的门禁对所