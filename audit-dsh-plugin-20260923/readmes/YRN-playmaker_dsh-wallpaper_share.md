# dsh-wallpaper_share
已适配 harness 0.1.5
<!-- Hero -->
<div align="center">
  <b style="font-size: 1.15em;">把 Wallpaper Engine 的壁纸实时同步为 DSH Web 界面背景，并支持应用挂载和自定义壁纸导入</b><br /><br />
  <a href="https://www.npmjs.com/package/dsh-wallpaper_share"><img alt="npm version" src="https://img.shields.io/npm/v/dsh-wallpaper_share" /></a>
  <a href="https://www.npmjs.com/package/dsh-wallpaper_share"><img alt="npm downloads" src="https://img.shields.io/npm/dm/dsh-wallpaper_share" /></a>
  <a href="https://github.com/YRN-playmaker/dsh-wallpaper_share/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YRN-playmaker/dsh-wallpaper_share" /></a>
  <a href="https://opensource.org/licenses/GPL-3.0"><img alt="License: GPL-3.0" src="https://img.shields.io/badge/License-GPL--3.0-blue.svg" /></a>
  <a href="https://github.com/YRN-playmaker/dsh-wallpaper_share/releases"><img alt="插件版本 v26.9.20-rc" src="https://img.shields.io/badge/v26.9.20--rc-4d6bfe" /></a><br /><br />
  <img alt="壁纸同步" src="https://img.shields.io/badge/-%E5%A3%81%E7%BA%B8%E5%90%8C%E6%AD%A5-4d6bfe" /> <img alt="场景渲染" src="https://img.shields.io/badge/-%E5%9C%BA%E6%99%AF%E6%B8%B2%E6%9F%93-4d6bfe" /> <img alt="DWP 市场" src="https://img.shields.io/badge/-DWP%20%E5%B8%82%E5%9C%BA-4d6bfe" /> <img alt="眼动追踪" src="https://img.shields.io/badge/-%E7%9C%BC%E5%8A%A8%E8%BF%BD%E8%B8%AA-4d6bfe" /> <img alt="专注模式" src="https://img.shields.io/badge/-%E4%B8%93%E6%B3%A8%E6%A8%A1%E5%BC%8F-4d6bfe" /> <img alt="多显示器" src="https://img.shields.io/badge/-%E5%A4%9A%E6%98%BE%E7%A4%BA%E5%99%A8-4d6bfe" /><br /><br />
</div>

<div align="center">
  🌏 <a href="#中文"><b>中文</b></a> · <a href="#english">English</a> · 
</div>


把 Wallpaper Engine 的壁纸同步为 DeepSeek Harness Web 界面的背景，并支持调整渲染模式、视觉效果、专注模式与壁纸库外挂壁纸与直链应用下载。

> **纯显示同步**：只读取 WE 状态，不控制 / 不修改桌面壁纸。
> **无敏感信息**：代码不含 Steam 用户名 / SteamID / 令牌；WE 安装目录运行时自动检测（注册表 `HKCU\Software\WallpaperEngine\installPath` → 常见 Steam 路径），检测不到时才需要手动配置。眼动追踪全程本地推理，摄像头画面不出设备。

---

<a name="中文"></a>
# 中文

## 📑 目录

- [⚡ 30 秒上手](#-30-秒上手)
- [✨ 功能一览](#-功能一览)
- [🎨 渲染模式与兼容矩阵](#-渲染模式与兼容矩阵)
- [🖼️ Scene 渲染与回退](#-scene-渲染与回退)
- [🔍 专注模式与眼动追踪](#-专注模式与眼动追踪)
- [🌌 沉浸模式与任务指示](#-沉浸模式与任务指示)
- [🪟 桌面悬浮球](#-桌面悬浮球)
- [🚀 安装](#-安装)
- [⚙️ 配置](#-配置)
- [📈 性能与已知限制](#-性能与已知限制)
- [📦 项目结构](#-项目结构)
- [🆕 已知问题](#-已知问题)
- [📄 License](#-license)

## ⚡ 30 秒上手

```bash
dsh plugin --profile web add dsh-wallpaper_share   # 或见下方「安装」选档
# 重启 dsh（web profile），浏览器打开 http://127.0.0.1:3080
```

装完你会看到三样东西：

1. **页面背景**变成 WE 当前壁纸（约 2 秒内跟随切换），面板与卡片浮在其上；
2. 会话区顶部多出一个 **`wallpaper_share` 标签页**（与「对话记录」「轨迹」并列），所有开关都在这里；
3. **收纳侧边栏**时，左缘出现一个圆形状态灯（绿 / 蓝 / 黄），点它进沉浸模式。

需要 WE 正在运行且已应用壁纸；否则背景留空、面板显示"尚未应用壁纸"。诊断入口：`http://127.0.0.1:3080/we-sync/diag`（仅本机可访问；端口以启动日志为准，默认 3080）。

> **零配置**：无需 API Key、无需注册、无需任何额外配置，安装即用。（注意：开头「无敏感信息」是隐私声明——代码中不含 Steam 用户名 / 令牌，并非需要你提供这些信息。）

## ✨ 功能一览

- **实时同步**：在 WE 切换壁纸后，harness页面背景会自动跟随为最新变化的壁纸，复数显示器时可手动锁定某台作为背景来源。支持三档渲染模式以调节能效表现：详见 [渲染模式与兼容矩阵](#-渲染模式与兼容矩阵)
<img width="1917" height="1018" alt="image" src="https://github.com/user-attachments/assets/6f147644-6283-456b-a9eb-c9c6d9925079" />

- **侧边栏沉浸模式**：一键隐去会话头部、正文与输入栏，让壁纸独占视野；网页 / 应用类壁纸在沉浸下可直接鼠标交互（详见[沉浸模式](#-沉浸模式与任务指示)）

- **桌面悬浮球**（Windows，默认关）：开启后，当你切走页签 / 最小化浏览器 / 切到别的应用时，桌面出现一个与侧边栏状态灯同款的环形按钮（颜色同步：绿空闲 / 蓝进行中 / 黄待授权），**单击即把 `http://127.0.0.1:3080/` 页面带回前台**（同窗口切到别的页签也能精确切回该页签）；可拖动记忆位置，右键 / 双击临时收起（详见[桌面悬浮球](#-桌面悬浮球)）

- **专注模式**：叠加一个圆心清晰、圆外模糊的阅读窗,以专注于任务，提升文字可读性；默认跟随鼠标，也可用摄像头推断注视点让透镜跟随视线；9 点校准、文字吸附、抗抖动
<img width="426" height="240" alt="Video Project 29" src="https://github.com/user-attachments/assets/57daf64c-ff2b-40c7-aeef-73cac46c4c2b" />

- **壁纸库**：按**本地**/**市场**/**应用启动器**分类。本地一栏管理已装内容——`dwp壁纸`（点击即挂载为全局背景，已挂载再点取消）与 `应用`（**大类**，下分 `we应用` 与 `应用`；点击卡片即启动，每次启动弹确认），带标题搜索、缩略图与计数；搜索框右侧的**「管理」**开关进入管理模式：卡片整体轻微晃动，**点卡片即多选**（选中项停住晃动、背景转蓝并打勾），选择条给出「已选 N / 卸载选中 / 清空选择」，可跨 `dwp壁纸` 与 `应用` 一次选完再统一卸载（确认弹层列出全部将被删除的项）；每张卡仍保留「打开源文件 / 卸载」单项操作，dwp 的「打开源文件」会在资源管理器里定位包文件——**卸载只对 dwp 壁纸与启动器装的应用开放**，WE 工坊内容点了只给提示、不参与多选（绝不删 Steam 内容）；市场一栏浏览 `dwp-registry` 目录，支持名称 / 作者搜索、标签筛选与安装 / 更新 / 卸载；**应用启动器**：支持用户粘贴 `http(s)` 直链（`.zip`/`.7z`/`.exe`，**加密压缩包填解压密码**）或部分**云盘分享链接**（如`yun.139.com/shareweb/#/w/i/…`，提取码填在提取码框），唤醒DSH 自动下载，解包并封装成**类 app 格式**（自动生成 `project.json` + 预览图卡片）入库；卡片只留「详细」按钮（安装时间 / 地址 / exe 文件，另含来源、SHA512、更新预览与多入口切换）——启动与卸载统一到「本地 → 应用」里做。不依赖 WE 运行、不受新版 WE 取消应用类壁纸影响。、
<img width="737" height="675" alt="image" src="https://github.com/user-attachments/assets/7567c226-7ea4-4fcb-a3b7-11190ee681ff" />


-**设置页面介绍↓**

| 卡片 | 内容 |
| --- | --- |
| **壁纸状态** | 壁纸名（标题行**右缘为插件版本号**，点击直达 GitHub 仓库）；下方副标题只承载诊断信息——scene 壁纸显示当前渲染通路（`场景 · 预览图 / 捕获 live 30fps / 浏览器模型渲染 / 回退：<原因>`），未应用壁纸时显示引导文案，其余类型整行不占；多显示器时出现「背景显示器」下拉；`⏻ 同步开启 / 关闭 / 暂停（DWP）` 三态按钮 |
| **视觉效果** | 三档渲染模式分段按钮；「桌面悬浮球」开关（在专注模式左侧，默认关；非 Windows 或缺 `bin/we-floater.exe` 时置灰）；「专注模式」及其展开条（眼动追踪 / 校准视线 / 文字吸附 / 实时状态）；透明度 · 模糊 · 阴影三个滑块（**专注开启时滑块隐藏**，改由任务态与透镜接管） |

<img width="841" height="667" alt="image" src="https://github.com/user-attachments/assets/7d652c07-8344-4de3-abbd-75620375c0b6" />

其他功能：
- **工作区脉搏（内置 DWP）**：新内置动态壁纸 `workspace-pulse`——把**当前工作区近期改动的文件**以最多 3 个浮动气泡呈现在背景上，右上角绿 `+` / 红 `−` 徽章标示该文件体积在增加还是减少（含新增 / 删除）。不依赖 git（未保存、二进制文件也能捕获）；点击挂载后实时更新，空闲时显示呼吸提示。首次启动自动入库，出现在 壁纸库→本地→dwp壁纸
- **DWP 壁纸与全局背景渲染**：`dwp/1.0` 协议包（纯文本 / solid / 粒子 / mesh 图层 + 12 种混合模式 + 3 种动画 + 11 种效果，确定性渲染）；挂载后经 WebGL2 真实渲染为 DSH 全局背景（低配 Canvas2D 降级），同时暂停 WE 同步避免冲突，刷新后自动恢复
- **设置持久化**：同步开关、渲染模式、显示器锁、三档渲染模式、专注 / 眼动等偏好写入 `localStorage`（键 `we-sync.settings`），刷新或重启 DSH 后自动恢复；沉浸模式等临时视图态与任务状态一律不落盘
- **自诊断路由** `/we-sync/diag`（仅本机可访问，含 scene renderer 状态与纹理提取结果）

## 🎨 渲染模式与兼容矩阵

面板顶部的三档切换决定壁纸如何呈现（按钮文字为 **预览 / 捕获 / 完整**，概念名 eco / perf / enhanced 用于 flash 提示与配置，默认 **捕获**）：

| 档位 | 含义 | 说明 |
| --- | --- | --- |
| **预览**（eco） | 静态预览图 | 只贴 WE 的预览图，最省资源，不加载动效 |
| **捕获**（perf） | 捕获 WE 桌面 | scene 走**原生捕获器 `we-capture.exe`**，镜像 WE 自己渲染的桌面 → 效果全覆盖；WE 未运行时自动回退浏览器渲染 |
| **完整**（enhanced） | 浏览器解 pkg | scene 走**浏览器子集渲染器**，直接解析 `.pkg` 在浏览器里重绘，不依赖 WE 运行 |

按壁纸类型展开的兼容矩阵（三档的真正差别只在 **scene**；video / web / image 下捕获与完整行为一致，都加载源内容）：

| 壁纸类型 | 预览 | 捕获 | 完整 |
| --- | --- | --- | --- |
| `video` | 静态预览图 | 播放源视频（HTTP Range，可 seek） | 播放源视频 |
| `web` | 静态预览图 | iframe 加载源页面 | iframe 加载源页面 |
| `image` | 静态预览图 | 显示源图 | 显示源图 |
| `scene` | 静态预览图 | **原生捕获 WE 桌面**（效果全覆盖；WE 未运行回退浏览器） | **浏览器解 pkg 渲染**（不依赖 WE，子集效果） |
| `application` / `other` | 静态预览图 | 回退静态预览（可在壁纸库中预览） | 回退静态预览 |

## 🖼️ Scene 渲染与回退

scene 壁纸在捕获 / 完整档下的渲染优先级与回退链：

1. **原生捕获（external）**：探测到 `we-capture.exe` 且 WE 正在渲染 → WS 帧流 live canvas（效果全覆盖）。
2. **浏览器子集渲染（browser）**：解析 `scene.json` 图层树 + transform + 已解码纹理 / 粒子 / puppet 合成进 canvas。
3. **静态纹理**：提取 pkg 内嵌高清纹理垫底。
4. **预览图**：以上皆不可用 → WE 预览图。

当前走的是哪一层，直接显示在面板副标题上；更细的状态在 `/we-sync/diag`。

**原生捕获器原理**：WE 的 DX11 渲染窗口是 Progman 子窗口、WGC 不接受子窗口，故捕获其顶层根 Progman / WorkerW，BGRA→JPEG 按外部渲染器协议输出到 stdout。因为镜像的是 **WE 自身的渲染结果**，无需在 JS 端复刻那套 ~500KB 软渲染引擎，效果 100% 覆盖。多显示器下顶层根窗横跨整个虚拟桌面，捕获器按锁定的那块 WPE 子窗矩形用 `CopySubresourceRegion` + `D3D11_BOX` 只回读目标屏区域再编码（换算经 `ClientToScreen` / `GetClientRect` 归一化，DPI 缩放非 100% 同样正确）→ 输出严格是单块屏。`bin/we-capture.exe`（约 540KB，Windows-only）随包发布，Rust 源码在 `native/we-capture/`（`cargo build --release` 可重建，含 `--selftest` 诊断模式）；DSH 侧 `probeRenderer` 自动发现，`sceneRenderMode='auto'` 检测到原生渲染器即走 external，否则回退 browser。

完整链路与各层实现见 **[docs/scene-fallback.md](docs/scene-fallback.md)**；pkg / 纹理 / puppet 格式见 **[docs/scene-format.md](docs/scene-format.md)**、**[docs/tex-format-findings.md](docs/tex-format-findings.md)**、**[docs/mdl-skinning-findings.md](docs/mdl-skinning-findings.md)**、**[docs/bone-pipeline-compare.md](docs/bone-pipeline-compare.md)**。

**骨骼动画（完整档）**：puppet 部件按 MDLS 绑定 + MDLA 逐骨骼动画做全骨骼链乘蒙皮，`animationlayers` 多层合成（普通层 mix / additive 层以自身帧 0 为参考 / rate 倍速 / 30fps），MDAT 具名锚点（含中文名）跟随骨骼最终世界位姿。26.9.8 定案 MDLA0006 连续流布局（骨骼窗口跨段延伸、每骨骼 +2 浮点漂移、fc+1 行含闭合行），并钳制末骨越界帧——修复人物每循环抽动一次与蒙皮异常形变（如 3465215190）；58 个本地 MDL 端到端校验（帧0≈bind + 闭环平滑度）全部通过。

## 🔍 专注模式与眼动追踪

- **专注模式 = 透镜总开关**：开启即在壁纸上叠加一个跟随注视点的透镜（圆心清晰、圆外模糊的阅读窗）。壁纸全局模糊在透镜激活时置 0，模糊全部由透镜层 `backdrop-filter` 承担（避免双重模糊开销）。默认跟随**鼠标**（精确、零延迟）。
- **任务自适应浓度**：专注开启时面板浓度不再听滑块，