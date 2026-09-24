# DSH Codex Subscription — 在 DeepSeek Harness 使用 ChatGPT 订阅

<div align="center">

**简体中文** · [English](https://github.com/WSL043/dsh-codex-subscription/blob/main/README.en.md)

**把 ChatGPT / Codex 订阅直接接入 DeepSeek Harness**

在 DeepSeek Harness 中直接登录 ChatGPT 并使用 Codex 订阅。无需 OpenAI API Key，也不依赖 Codex CLI；
模型、搜索、额度和图片生成都留在 DSH 里。

[![CI](https://github.com/WSL043/dsh-codex-subscription/actions/workflows/ci.yml/badge.svg)](https://github.com/WSL043/dsh-codex-subscription/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/dsh-codex-subscription?logo=npm&label=npm)](https://www.npmjs.com/package/dsh-codex-subscription)
[![npm 总下载量](https://img.shields.io/npm/dt/dsh-codex-subscription?logo=npm&label=%E6%80%BB%E4%B8%8B%E8%BD%BD%E9%87%8F)](https://www.npmjs.com/package/dsh-codex-subscription)
[![MIT](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE)
[![Star](https://img.shields.io/github/stars/WSL043/dsh-codex-subscription?style=flat&logo=github&label=Star)](https://github.com/WSL043/dsh-codex-subscription/stargazers)

[三步开始](#三步开始) · [安装](#安装) · [参与贡献](CONTRIBUTING.md) · [更新与卸载](#更新与卸载)

</div>

<p align="center">
  <img src="docs/assets/codex-subscription-overview.webp" width="900" alt="在 DeepSeek Harness 登录 ChatGPT 并使用 Codex 订阅：无需 API Key，支持模型选择和剩余额度显示">
</p>

已适配 DSH `0.1.7-rc.1` 的插件兼容性检查与设置接口，同时保留已支持版本的兼容。

## 三步开始

1. **安装插件**：打开 **插件 → 添加插件**，在 **包名或地址** 中填写 `dsh-codex-subscription`，点击 **安装**。
2. **登录订阅**：按安装结果提示操作；若提示需要重启，先保存工作再重启。打开 **设置 -> Codex 订阅**，点击浏览器登录。无需 Codex CLI，也不要粘贴 token。
3. **开始使用**：在模型选择器中选择 Codex；额度、订阅搜索、图片生成和高速模式都在 DSH 内使用。

详细安装步骤、终端方式以及更新与卸载说明见下文。

## 核心优势

| 能力 | 用户得到什么 |
| --- | --- |
| **订阅模型直连** | 登录 ChatGPT 后直接使用 Codex，不需要 OpenAI API Key 或 Codex CLI |
| **可恢复、可诊断** | 登录状态会自动对账；读取失败时可在原处重试，超时和旧账号响应不会覆盖当前状态；设置页可生成不含凭据和账号标识的支持报告 |
| **额度可见** | 普通 Codex、Spark 等服务端实际返回的额度分开显示，并显示重置时间 |
| **输入框额度** | 可选择紧凑百分比、进度条、Beta 续航预测或关闭显示 |
| **安全额度重置** | 每张重置卡单独显示，并通过冷静期和知情确认主动尝试重置 |
| **订阅搜索** | 可将全部模型的搜索明确路由到 DSH 默认搜索或已登录的 Codex 订阅 |
| **Codex 图片生成与编辑（Beta）** | 可无参考图全新生成，也可明确选择会话图片继续编辑；支持预览、缩放、区域备注、下载原图，并为新生成或编辑的图片提供 DSH 主机上的原图路径 |
| **高速模式** | 直接在输入框切换标准或高速，无需离开当前会话 |
| **模型感知上下文** | 可保留目录默认值、按模型启用扩展窗口，或为每个模型填写完整数字 Token 上限；设置页打开、账号切换和连接重置后会刷新模型目录，失败时可重试且不会覆盖未保存的草稿 |
| **Headless 任务** | 使用同一份已登录的 Codex Provider 运行一次性 DSH 任务，输出答案后自动退出 |

这些能力共用同一份本机 ChatGPT 登录。订阅路由失败时会明确报错，不会静默切换到其他付费路由。

## 实际界面

<p align="center">
  <img src="docs/assets/subscription-account.png" width="820" alt="DSH Codex 订阅主界面：ChatGPT 登录、剩余额度与输入框偏好">
</p>

上图为“账号与偏好”主界面，展示登录状态、订阅额度和输入框偏好。截图中的账号、额度、余额与时间均为演示数据，不代表套餐固定权益。高级功能与可选组件见下文。

## 准备 DSH

本插件支持软件包元数据中记录的最新版 DeepSeek Harness，并需要一个当前具有 Codex 使用资格的 ChatGPT 账户。

- 不想配置 Node.js：使用 [DSH-Portable](https://github.com/WSL043/DSH-Portable)。这是面向 Windows、macOS 和 Linux 的社区便携桌面分发；
- 想按官方方式运行：查看 [DeepSeek Harness 官方说明](https://github.com/deepseek-ai/deepseek-harness#run)。

## 安装

### 在插件页面安装（推荐）

1. 打开 DSH 的 **插件 → 添加插件**。
2. 在 **包名或地址** 输入框中粘贴下面的包名：

   ```text
   dsh-codex-subscription
   ```

3. 点击 **安装**，等待安装完成；按页面提示操作，需要重启时先保存工作。
4. 打开 **设置 → Codex 订阅**，登录 ChatGPT，然后在会话中选择 Codex 模型。

包名不带版本号时安装最新正式版。指定版本时填写 `dsh-codex-subscription@2.1.6`；测试版则使用对应发布说明中的完整版本号。此处只填包名，不要粘贴整条终端命令。安装本插件使用上面的 npm 包名即可，无需填写 GitHub 地址或本地目录。

<details>
<summary>终端安装（已能运行 dsh 命令）</summary>

```sh
dsh plugin --profile web add dsh-codex-subscription
```

安装完成后按提示重启 DSH，再到 **设置 → Codex 订阅** 登录。插件页面和终端均由 DSH 管理安装。

</details>

<details>
<summary>Headless 任务</summary>

先在 Web 中完成登录并选择一次 Codex 模型，再把同一个插件安装到 Headless profile：

```sh
dsh plugin --profile headless add dsh-codex-subscription
dsh --profile headless "只回复：ok"
```

</details>

## 功能说明

### 执行中补充指令

沿用 DSH 原生消息队列：生成中发送消息可排队到下一轮；界面提供插话入口时，可用其快捷键将排队内容交给当前轮的下一步处理。插话不是立即改写正在生成的响应。

### GPT-Reserve（实验性）

账号的官方模型目录提供 `gpt-reserve` 时，模型选择器末尾会出现实验性选项。可用性和扣费归属由服务端决定；请求成功不代表已确认使用独立备用额度。即使普通 Codex 额度显示已用尽，服务端也可能只在模型目录中返回 `gpt-reserve`，不返回独立的 Reserve 额度桶。此时输入框将 Reserve 额度视为未知，不会借用普通 Codex 额度；服务端返回“允许使用”也不能证明请求扣的是 Reserve。

### GPT-6 Sol / Luna

GPT-6 Sol 和 GPT-6 Luna 已在 [OpenAI 的 Codex 模型说明](https://learn.chatgpt.com/docs/models)中列出。插件会从当前账号的 Codex 模型目录自动读取可用模型及推理档位，无需手动添加型号；账号尚未开放时不会显示。Sol 适合复杂编程，Luna 适合高频、目标明确的任务。两者的扩展上下文上限和高速模式以账号目录返回值为准。

### GPT-6 Astra 上下文

当官方模型目录提供 GPT-6 Astra 时，标准模式保留目录默认窗口；扩展模式使用 872000 Token，自定义模式可设置 128000–872000 Token（初始值为 272000）。该上限依据 [Codex 官方模型目录](https://github.com/openai/codex/blob/6af345407d9c2a568da9d01b6c4b81a9e61495c0/codex-rs/models-manager/models.json#L33-L34)，不是 API 模型的总上下文容量。这些设置只调整 DSH 的本地上下文预算，不授予模型访问权限，也不保证账号的服务端容量；实际可用性以服务端为准。

### 输入框额度

<p align="center">
  <img src="docs/assets/composer-quota.png" width="800" alt="DSH 实机输入框：GPT-6-Astra、Max 推理、高速模式和剩余额度">
</p>

实机示例：GPT-6-Astra · Max（最高推理档）· 高速模式（闪电标识），左侧直接显示剩余额度。

可在“账号与偏好”选择关闭、百分比、进度条或 Beta 续航预测。存在 5 小时额度时，输入框只显示短窗口；每周额度等完整信息留在悬浮详情。仅有周额度时省略“周”字，预测采用 `36% · ≈10h–12h` 这样的紧凑格式。

续航预测根据最近两小时的官方读数估算，额度不变的采样同样参与计算。满足条件时利用连续跳格约束速度，读数不足或使用强度变化时会退回保守估计。范围不是实际可工作时间的保证，仍标记 Beta。历史在本机有限保存；重置、长时间离线或关闭预测会重新校准。
Spark 使用独立额度。只返回每周额度的账号仍只显示每周，不会虚构 5 小时窗口、Credits 或消费上限。

### 安全使用额度重置

ChatGPT 返回可用重置卡时，设置页会把每张卡分别显示为紧凑的一行，并展示服务端提供的名称和到期时间。即使额度尚未到 100%，
也可以主动尝试使用，适合重置卡即将过期的情况；是否需要重置仍由 ChatGPT 判断，服务端可能返回“当前无需重置”且不扣次数。
最终操作需要勾选知情确认并等待 5 秒。取消不会消耗，快速连续点击只允许一次请求，网络结果不确定时也不会自动重试。

### 图片生成与编辑（Beta）

订阅插件已内置基于 `dsh-image-viewer` 的基础查看器，无需额外安装。插件生成图片的工具卡片使用内置查看器，确保标注和继续编辑功能可用。你可以缩放、拖动、适合窗口、添加区域备注并下载图片。标准“下载”默认获取经过权限与完整性校验的精确原图；旧会话没有精确原图时才下载会话预览图。

新生成或编辑的图片会在工具结果中返回当前 DSH 主机上的原图路径，模型或 Agent 可以读取或复制该文件。该路径位于运行 DSH 的主机，并非浏览器下载链接；原图下载仍按会话授权。卸载插件不会删除已生成的原图。

点击“在输入框中继续编辑”不会自动发送。有标注时会附上干净源图和带编号标记的定位参考图，草稿包含对应编号、坐标、备注，以及不得把标记绘入成品的说明；没有标注时只附上当前图片。每个标记必须填写备注，参考图准备失败时会中止回填。按 Enter 保存并收起备注，Shift+Enter 换行；在当前 DSH 页面重新打开同一张图片时，备注仍会保留。

新的图片请求不会静默带入历史图片。GPT Image 2 可能比文本回复耗时更长，复杂文字、精确构图和连续角色一致性也可能需要再次调整。

<p align="center">
  <img src="docs/assets/image-preview-annotations.png" width="800" alt="DSH 图片查看器中的生成图、区域备注和继续编辑">
</p>

上图展示图片查看与图上备注的基本交互；具体按钮会随图片和所安装的查看器版本变化。

### 草图画板（Beta）

![草图画板实机界面：画布比例、笔刷、形状、图层与缩放](docs/assets/sketch-canvas.png)

点击输入框的草图按钮手动画图。`@sketch` 是 Agent 绘图入口：选择时只填入输入框，发送绘图请求后才由 Agent 打开画板。图片预览中可选择“进入草图”；上传、粘贴和移除附件仍由 DSH 原生组件处理。

草图支持多份本地草稿、图片图层、画布比例、三种笔刷（实色钢笔、颗粒铅笔、半透明荧光笔）、直线和形状、两种橡皮、撤销重做、拖动缩放与可配置快捷键。平滑仅在抬笔后处理整笔路径，不拖慢绘画光标。草稿最多 20 份，仅保存在当前浏览器；附加草图不会自动发送。左侧图片面板只管理当前草图的图片，不是会话图片库。

支持可选中修改的形状与文字、原生曲线，以及侧边粗细/浓度控件。Agent 绘制时可查看、缩放和关闭面板，编辑暂时锁定；顶部可停止绘制，完成后恢复编辑。自动完成预览默认关闭，可在高级设置开启。切换会话后再返回会保留画板、历史和运行状态。切到其他会话期间不保证后台绘制；整页刷新或退出前请保存草稿，未保存内容不保证恢复。

**草图生成图片实测**：画好后点击“附加”，在输入框说明想要的效果，再发送。

| 画板原草图 | 插件实际生成结果 |
| --- | --- |
| ![山峰与小屋草图](docs/assets/sketch-demo-source.png) | ![根据草图生成的水彩山间小屋](docs/assets/sketch-demo-result.png) |

示例要求：保留山峰与小屋的构图，生成温暖的水彩旅行插画，青绿山峰、橙色屋顶、草地小溪与柔和晨光，不保留蓝色线条。此例通过 GPT-5.6-Luna 发起一次图片工具调用，请求低质量；Luna 是对话模型，实际出图型号由订阅后端决定。

<details>
<summary>进阶展示</summary>

**《画布背面有人》**

**Astra 绘制草图，GPT Image 2 生成成图。** Astra 通过原生 `codex_sketch` 接口完成 6 层、427 笔绘制，再由 Luna 调用订阅生图工具精修。生图请求使用 `gpt-image-2`、低质量档；服务端未报告实际执行型号。Beta 新增 PNG 导出、分层 PSD 导入导出和可编辑草稿文件；PSD 保留像素图层，原生草稿保留笔画。草图画板与 Agent 绘图均默认关闭，可在高级设置中分别开启。仅开启 Agent 绘图后才向模型提供绘图工具。

| 原生草图 | 实际生成结果 |
| --- | --- |
| ![Sketch](docs/assets/sketch-advanced-source.png) | ![Result](docs/assets/sketch-advanced-result.png) |

**草图复现提示词（按原画面整理，非完整原始对话）**

原案例由 Astra 分阶段绘制，下面提供同主题的复现起点，不保证得到完全相同的画面。

```text
@sketch 用 4:3 横版画板绘制《画布背面有人》：中央偏上是一处撕开的纸洞，洞内是深蓝星空和一位拿颜料桶的小画师；蓝色颜料从桶中流出，形成 S 形河流，流向下方城市。左侧城市保持未上色线稿，右侧城市被暖色点亮，加入纸船与飞鸟。按纸面、洞内世界、颜料河流、城市、画师和细节分层绘制，保留原生可编辑笔画。
```

**实际生图提示词**

```text
请基于本条附加草图实际调用订阅图片工具一次，生成成品插画。quality=low，模型使用当前默认，不切换型号，不额外生成。主题《画布背面有人》：保留4:3横构图、中央偏上的撕纸洞口、洞内拿颜料桶的小画师、流出成为S形河流的蓝色颜料、下方左侧未上色城市与右侧被点亮城市、纸船飞鸟。精修为惊艳的立体纸艺与精细手绘结合的编辑插画，纸张纤维、真实撕边及柔和投影，深靛蓝洞内星月，丰富青蓝颜料层次和流动质感，赭橙画师与暖色建筑，微小清晰的叙事细节。不重构为风景，不添加文字水印。必须使用本条参考图片编辑，不能仅凭文字生成。生成后简短说明完成即可。
```

原案例首发：[Beta v2.1.0-beta.2](https://github.com/WSL043/dsh-codex-subscription/releases/tag/v2.1.0-beta.2)

**《蒙娜丽莎》：Astra 草图 → GPT 生图**

案例版本：[2.1.0-beta.5](https://github.com/WSL043/dsh-codex-subscription/releases/tag/v2.1.0-beta.5)

用户在另一台电脑上的实际效果：先让 Astra 在竖版画板上绘制，再通过 GPT 生图转成油画。

| Astra 原生草图 | GPT 生图：油画效果 |
| --- | --- 