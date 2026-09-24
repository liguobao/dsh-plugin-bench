<p align="center">
  <strong>中文</strong> · <a href="./docs/i18n/README.en.md">English</a> · <a href="./docs/i18n/README.ja.md">日本語</a> · <a href="./docs/i18n/README.ko.md">한국어</a> · <a href="./docs/i18n/README.es.md">Español</a> · <a href="./docs/i18n/README.fr.md">Français</a> · <a href="./docs/i18n/README.de.md">Deutsch</a> · <a href="./docs/i18n/README.ru.md">Русский</a>
</p>

<div align="center">

# dsh-dream-skin 🔮
[![DSH Insights health](https://dsh-insights.com/badge/RevolutionLA/dsh-dream-skin.svg)](https://dsh-insights.com/p/RevolutionLA/dsh-dream-skin/)

**为 DeepSeek Harness 换上一张克制、清透、有质感的「脸」。**

原生换肤 · 背景壁纸 · 强调色 · 主题包 —— 一条 `--dsw-*` token 生态内的优雅实现。装一次，用很久。

> **写代码的地方，可以很安静。**

| 🎨 8 套原创主题 | 🖼️ 壁纸 + 弥散光 | 🎯 克制的强调色 | 📦 主题包可分享 |
|---|---|---|---|

> 1 行安装 · 纯原生（无注入/不改安装包）· 不因 DSH 更新失效

</div>

---

## 🎮 两种玩法，一条插件都给你

<table>
  <tr>
    <td align="center" width="50%"><h3>🪄 玩法一：开箱即用的优雅</h3></td>
    <td align="center" width="50%"><h3>🧱 玩法二：随你掌控的 DIY</h3></td>
  </tr>
  <tr>
    <td>内置 <b>8 套设计师调校的预设皮肤</b>（Mirage 幻梦系列），浅色 / 深色兼顾，每套自带专属弥散光背景。<br/><b>戴上即高级，不用任何调参。</b></td>
    <td>在预设之上，你还能 <b>换壁纸（本地图 / URL / 渐变）</b>、<b>叠加强调色 Accent</b>、<b>拖入或分享一个主题包</b>，内部每个 token 都能摸到。<br/><b>想要的样子，自己捏。</b></td>
  </tr>
</table>

两种玩法分层独立、互不干扰：预设皮肤决定「材质与底色」，DIY 一层是纯叠加（`overrideTokens`），随开随关、一键还原。

---

## 📸 实机截图

> 真机效果，非概念图。左：应用皮肤后的 DSH 界面；右：设置里的「外观 / Theme」分节。

<p align="center">
  <img src="docs/screenshots/preview.png" alt="DSH 皮肤实机预览" width="46%"/>
  &nbsp;&nbsp;
  <img src="docs/screenshots/settings.png" alt="设置中的外观分节" width="46%"/>
</p>

---

## 🎨 玩法一：8 套预设皮肤（Mirage 幻梦系列）

> **开箱即用的优雅。** 在 **设置 → 外观（Theme）** 一键切换。下列预览由各皮肤的**真实 token + 专属弥散光背景**生成——所见即所得，点开可放大查看精致材质。

<table>
  <tr>
    <td align="center"><a href="docs/previews/abyss.png"><img src="docs/previews/abyss.png" width="230" alt="abyss"/></a><br/><b>abyss</b> · 🕶️ 沉静蓝<br/><sub>冷静深沉的靛蓝，克制不喧哗</sub></td>
    <td align="center"><a href="docs/previews/aurora.png"><img src="docs/previews/aurora.png" width="230" alt="aurora"/></a><br/><b>aurora</b> · 🌌 极光青<br/><sub>清冽通透的冷青，自然冷调</sub></td>
    <td align="center"><a href="docs/previews/nebula.png"><img src="docs/previews/nebula.png" width="230" alt="nebula"/></a><br/><b>nebula</b> · 🪐 星云紫<br/><sub>深邃漫射的紫青，朦胧神秘</sub></td>
    <td align="center"><a href="docs/previews/ember.png"><img src="docs/previews/ember.png" width="230" alt="ember"/></a><br/><b>ember</b> · 🔥 余烬橙<br/><sub>温暖克制的琥珀橙</sub></td>
  </tr>
  <tr>
    <td align="center"><a href="docs/previews/midnight.png"><img src="docs/previews/midnight.png" width="230" alt="midnight"/></a><br/><b>midnight</b> · 🌚 午夜黑<br/><sub>极简纯黑，OLED 沉浸</sub></td>
    <td align="center"><a href="docs/previews/ivory.png"><img src="docs/previews/ivory.png" width="230" alt="ivory"/></a><br/><b>ivory</b> · 📐 iOS 扁平<br/><sub>极简平白，iOS 系统灰 + 克制的蓝</sub></td>
    <td align="center"><a href="docs/previews/mist.png"><img src="docs/previews/mist.png" width="230" alt="mist"/></a><br/><b>mist</b> · 🧊 干净明亮<br/><sub>清透明亮的玻璃质感，半透明 + 模糊</sub></td>
    <td align="center"><a href="docs/previews/rose.png"><img src="docs/previews/rose.png" width="230" alt="rose"/></a><br/><b>rose</b> · 🌸 Material 粉<br/><sub>明快彩粉，谷歌 Material 扁平彩色</sub></td>
  </tr>
</table>

> 浅色 / 深色兼顾：`mist`、`ivory`、`rose` 为浅色系，其余为深色系。不喜欢预设？往下看**玩法二**。

---

## 🧱 强大 DIY 空间（玩法二）

> 预设皮肤之外，dsh-dream-skin 还给你一套完整的自定义体系——想捏出独一无二的工作区，从这里开始。

| 能力 | 玩法二 · 你能做什么 |
|------|------|
| 🖼️ **自定义壁纸 2.0** | 本地图 / **图片 URL** / **渐变预设**；附带**透明度 / 模糊**，每套皮肤还**自动建议**一张渐变，可**自动弱化**（聚焦任务时降低干扰） |
| 🌈 **每用户强调色 Accent** | 为当前皮肤叠加自定义品牌强调色（`overrideTokens` 层，不动皮肤本身），**12 个典型色块一键选色** + 选色盘 + 随机 + 恢复主题色 |
| 📦 **主题包导入 / 导出 / 分享** | 一个 `*.dsh-theme.json` = manifest + 全套 tokens，可**导入文件**、**一键应用**、**复制分享链接**（编码进 URL hash） |
| 🪟 **弹窗不透明度** | 滑块控制下拉菜单 / 浮层 / 弹窗的底填充透明度，跟随持久化保存 |
| 🧩 **本地主题包库** | 导入的主题包集中展示，**应用 / 收藏 / 移除** 一键完成 |
| 🎲 **换一个试试（surprise me）** | 随机换一个和你当前不同的主题；**收藏**喜欢的皮肤快速切换 |
| ✅ **校验 + 回滚** | 导入时校验格式 / 必填 token / 颜色合法性；失败或移除时安全回退，不做破坏性更改 |

> 一切都叠加在预设之上，**随开随关、一键还原**到 DSH 内置外观——大胆去试，不会弄坏什么。

---

## ⚡ 一句话安装

**复制下面这句话给你的 DSH，它自己会装好一切：**

> 请帮我安装 dsh-dream-skin 换肤插件（https://github.com/RevolutionLA/dsh-dream-skin 或 npm 的 dsh-dream-skin），装完告诉我如何重启 DSH Web。

不想麻烦 Agent？命令行一条：

```sh
dsh plugin --profile web add dsh-dream-skin && dsh web
```

> 🚀 **现已发布到 npm！** 装好 DSH 后，一条命令即可安装，无需 clone。

> **致敬 [Codex-Dream-Skin](https://github.com/Fei-Away/Codex-Dream-Skin)。** 但实现路径不同：Codex 是往桌面客户端渲染进程
> 注入 CSS（CDP），而 DSH 本身是 **token 驱动的 Web GUI**，官方就提供了「第三方插件注册主题」的能力——所以本插件是
> **纯原生接入**，无注入、不改二进制、不因客户端更新失效。
>
> **不是官方产品。** 仅供美化你的 DeepSeek Harness 工作区。

---

## 🏆 为什么值得用（vs 同类 DSH 主题插件）

> 换个赛道看：同类插件要么是把一套现成色板移植过来（好看，但配置只有一个开关）、要么是锁死单一美学的定制款、
> 要么专注把外部壁纸搬进来。我们把换肤做成**一整套可调的材质与配色系统**——追求的不是「更花」，
> 而是「更准、更克制、更耐看」，像一块反复推敲的玻璃。**审美 + 可调性是我们的护城河。**

| 能力 | 本插件 | [dsh-catppuccin-theme](https://github.com/)（色板移植） | [dsh-theme-mineradio](https://github.com/)（单一美学定制） | [dsh-wallpaper-engine](https://github.com/)（壁纸桥接） |
|------|:---:|:---:|:---:|:---:|
| **8 套原创设计**（非现成色板移植，原创 token + 弥散光） | ✅ | ❌ (4 套 Catppuccin 官方色板) | ❌ (1 套香槟金美学) | ❌ |
| **毛玻璃 / 液态玻璃双材质**一键切换 | ✅ | 部分（固定玻璃质感） | ❌ | ❌ |
| **输入框 / 弹窗独立透明度滑杆** | ✅ | ❌ | ❌ | ❌ |
| **开箱即用的出厂配置**（装完重启就是调好的样子） | ✅ | ❌ | ✅（本身即成品） | ❌ |
| 自定义壁纸 + 透明度/模糊 | ✅ | ❌ | ❌ | ✅（核心能力） |
| **壁纸 2.0**（URL / 渐变预设 / 每皮肤建议 / 自动弱化 / 必应每日 + 定时更新） | ✅ | ❌ | ❌ | 部分（依赖 WE 壁纸） |
| **每用户强调色 Accent**（叠加层，不动皮肤本身） | ✅ | ❌ | ❌ | ❌ |
| **主题包导入/导出 + 分享链接**（JSON，无代码分发） | ✅ | ❌ | ❌ | ❌ |
| 本地主题包库 + 收藏 + 随机换 | ✅ | ❌ | ❌ | ❌ |
| **两代宿主兼容 + 运行时能力探测**（宿主换代自动降级不报错） | ✅ | 未知 | 未知 | ❌（需先升级内核） |
| 校验 + 回滚（不做破坏性更改） | ✅ | 部分 | — | 部分 |

> **一句话**：想要 Catppuccin 的品牌色、mineradio 的氛围感？本插件的主题包系统都能做出来或叠出来——
> 反过来不成立。

---

## ✨ 功能一览

| 能力 | 说明 |
|------|------|
| 🎨 **8 套主题预设（Mirage 幻梦）** | 在 **设置 → 外观（Theme）** 一键切换，浅色 / 深色兼顾 |
| 🖼️ **自定义壁纸** | 上传本地图（自动压缩 ≤2MB），调节**透明度 / 模糊** |
| 🧊 **玻璃材质（毛玻璃 / 液态玻璃）** | 一键切换玻璃质感，透明度滑杆**越右越透**；模糊一个旋钮同时驱动壁纸与玻璃表面 |
| 🖼️ **开箱即用的出厂配置** | 首次安装即带完整美化配置：星云皮肤 + 内置壁纸 + 调好的玻璃数值，装完重启就能用 |
| 🌤️ **必应每日壁纸（预置）** | 高级壁纸预填必应每日一图接口，点「应用链接」即可；也支持任意图片 URL + 定时自动更新 |
| 🔤 **内层不透明** | 卡片、输入框、消息气泡不被壁纸盖住，可读性优先 |
| ↩️ **默认还原** | 一键回到 DSH 内置外观（跟随系统） |
| 💾 **本地持久化** | 皮肤与壁纸存 `localStorage`，刷新 / 重开浏览器不丢 |

---

## 🧩 它是什么形式的插件

**它是 DeepSeek Harness 的标准「双面插件」（`dsh-plugin`）——加载和用法与官方 `ui-theme` 完全一致。**

DeepSeek Harness 的口号是「一切皆插件」：模型、工具、沙箱、会话、UI，乃至 Agent Loop 本身都是插件。
`dsh-dream-skin` 的本质就是把「换肤」做成一个和官方 UI 包**同构**的 npm 包：

```text
            ┌────────────── dsh-dream-skin（标准 dsh-plugin / 双面插件）──────────────┐
            │  dsh.bundle   → cordis.patch.yml 插入 dream-skin 入口   (host 半边)     │
            │  dsh.client   → lib/client.js（浏览器 bundle）          (浏览器半边)     │
            └─────────────────────────────────────────────────────────────────────────┘
```

- **安装命令 = 官方唯一安装命令**：`dsh plugin --profile web add dsh-dream-skin`
- **调用的是官方扩展点**：`ctx.theme`（注册主题）、`ctx.theme.overrideTokens`（叠加层）、
  `ctx.slots`（把 UI 挂进独立的 **设置 → 外观 / Theme** 分节）。
- **manifest 契约与官方一致**：`dsh.bundle` + `dsh.client` + `exports["./client"]`。

也就是说：**你装的不是一个旁门左道的脚本，而是 DSH 官方插件体系里的标准皮肤插件。**

---

## ⚡ 快速开始（3 步）

```sh
# 1. 安装
dsh plugin --profile web add dsh-dream-skin
# 2. 重启
dsh web
# 3. 打开 设置 → 外观（Theme）→ 皮肤，挑一套 → 完。
```

> 装的是 npm 已完成发布的正式包，无需 clone。若 `dsh plugin add` 报 workspace 相关错误，补一个 `-w` 即可。

## 📦 安装

四种方式任选其一，装完**重启 DSH Web** 即生效（当前会话会中断，但 DSH 会话有磁盘持久化，重启后可以恢复）。

### 方式一：npm 正式包（**推荐**，最简单）

```sh
dsh plugin --profile web add dsh-dream-skin
```

### 方式二：从 GitHub 安装（固定到已验证的提交）

```sh
dsh plugin --profile web add 'github:RevolutionLA/dsh-dream-skin#<40位commit>'
```

> 固定到 release 对应的 commit，之后 `main` 的新改动不会静默改变已安装代码。

### 方式三：从 Release tarball 安装（离线 / 不便走 git 的环境）

从本仓库 [Releases](https://github.com/RevolutionLA/dsh-dream-skin/releases) 下载 `dsh-dream-skin-<版本>.tgz`（内含构建好的 `lib/client.js`，安装时无需执行任何 prepare 脚本），然后：

```sh
dsh plugin --profile web add ./dsh-dream-skin-<版本>.tgz
```

### 方式四：克隆后从本地路径安装（开发迭代）

```sh
git clone https://github.com/RevolutionLA/dsh-dream-skin.git
cd dsh-dream-skin
dsh plugin --profile web add .
```

> `dsh plugin` 会把