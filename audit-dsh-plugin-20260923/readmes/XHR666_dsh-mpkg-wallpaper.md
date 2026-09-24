# dsh-mpkg-wallpaper — DSH 壁纸引擎背景插件

[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)

[中文](README.md) | [English](README.en.md)

给 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Web 界面（`dsh web`）添加背景壁纸的插件：**Wallpaper Engine `.mpkg` 解析、Steam 创意工坊目录、视频/网页/图片壁纸、时间变化壁纸的多时段切换、整屏虚化体系、主题色与玻璃外观、本地壁纸库、定时轮换、Now playing 控件、一键更新**。外观细节几乎全部可调。

> 版本口径：本文件描述的是 `package.json` 里 **`3.10.1`** 这一版实现。发布面共 **15 个文件**（`lib/` 8 个运行时文件 + `package.json`、`icon.svg`、`cordis.patch.yml`、`README.md`、`README.en.md`、`THIRD-PARTY.md`、`LICENSE`；`npm pack --dry-run` 实测 15 文件 / unpacked 2 088 240 B）；`lib/liquid-glass/**`、`lib/liquid-glass-bundle.js`、`dist/`、`tools/`、`docs/` 都不进 npm 包（`package.json:8-21`）。本轮的默认档变化：**`npNowPlaying` 关 → 开**（3.8.0 起）与 **`powPauseHidden` 关 → 开**（3.9.0 起，只迁移"从没设过"的存量档；详见[这一版新增/变更](#这一版新增变更)）。

---

## 下载 · 安装

插件已发布到 npm（`dsh-mpkg-wallpaper`）。四种装载方式——先按这张表选一条，再看对应小节：

| 方式 | 适合谁 | 更新怎么做 | 客户端界面 |
|---|---|---|---|
| 一 `dsh plugin add`（推荐） | 默认选择；市场能识别「已安装」 | `dsh plugin --profile web update …` | 完整 |
| 二 pnpm 手动装 | 自己管 profile 的依赖表 | 同上（走依赖表） | 完整 |
| 三 GitHub 克隆 | 开发者 / 离线 / 要改代码 | `git pull` | 完整 |
| 四 单文件 bundle | 离线应急；给非 DSH 宿主复用路由 | 重新生成并替换那个 `.mjs` | **只有宿主端** |

### 方式一：`dsh plugin add`（推荐，市场可识别）

```bash
dsh plugin --profile web add dsh-mpkg-wallpaper
# 重启 dsh web 后浏览器 Ctrl+F5 生效
```

### 方式二：pnpm 手动安装

```bash
pnpm --dir $DSH_HOME/profiles/<profile> add dsh-mpkg-wallpaper
# 重启 dsh web，浏览器 Ctrl+F5 生效
```

与方式一同源，只是不经 `dsh plugin` 包装。

### 方式三：GitHub 克隆（开发者 / 离线）

```bash
git clone https://github.com/XHR666/dsh-mpkg-wallpaper.git $DSH_HOME/profiles/<profile>/node_modules/dsh-mpkg-wallpaper
# 然后在 profile 的 cordis.patch.yml 注册：
#   - insert:
#       - id: dsh-mpkg-wallpaper
#         name: dsh-mpkg-wallpaper
# 重启后生效
```

> 方式三不写依赖表 ⇒ 市场不显示「已安装」（只影响显示，不影响功能）。

### 方式四：单文件 bundle（离线 / 拷文件即装；**只装宿主端**）

把宿主端内联成一个自包含 ESM 再登记：

```bash
cd /path/to/dsh-mpkg-wallpaper
node tools/build-bundle.mjs          # 产物：dist/dsh-mpkg-wallpaper.bundle.mjs（实测 449 671 B / 439.1KB；以 bundle-equivalence-test 的输出为准）
node tools/build-bundle.mjs --check  # 与源码对拍：导出面 / 路由表 / ping JSON 形状（20 条断言）
node tools/bundle-equivalence-test.mjs  # 更全的等价性门禁（38 条断言；门禁第 11 步）
```

把 `dist/dsh-mpkg-wallpaper.bundle.mjs` 拷到任意目录（例如 `~/.dsh/plugins/`），在 profile 的 `cordis.patch.yml` 里按**绝对路径**登记，然后重开 `dsh web`：

```yaml
# $DSH_HOME/profiles/<profile>/cordis.patch.yml
- insert:
    - id: dsh-mpkg-wallpaper
      name: /绝对路径/dsh-mpkg-wallpaper.bundle.mjs   # ← 指向那个 .mjs 文件本身
```

**这条路装载了什么 / 没装载什么**（都是代码与门禁事实）：

| 项 | 方式四的行为 | 依据 |
|---|---|---|
| 宿主端（上传/Range 流式播放、场景提取、音频清单、设置持久化、诊断上报等 **41 条路由**） | **完整**（`lib/index.js` + `pkg-extract.js` + `web-wallpaper.js` + `web-interaction.js` 全部内联；外部依赖只有 node 内建） | `node tools/bundle-equivalence-test.mjs`：路由表（kind + path）逐条相同 `[41 条]` |
| `/api/mpkg-wallpaper/ping` | `{ok, version, betterSidebar, betterSidebarVersion}` 键集合与源码一致 | 同上 + `build-bundle.mjs --check` |
| **客户端半（设置面板 / 壁纸层 / 磨砂 / Now playing）** | **不装载**。单文件里只有宿主端导出面（`apply` / `inject` / `__mpwTest`） | 客户端半由 DSH 客户端模块系统按**包**发现：扫描宿主 Loader 条目里声明了 `dsh.client` 的包并解析其 `exports["./client"]`；裸 `.mjs` 没有 package.json ⇒ 没有 `dsh.client` 声明 |
| `GET /api/mpkg-wallpaper/lg/*`（遗留 WebGL 托管路由，客户端已不调用） | bundle 旁边没有 `liquid-glass/` 时 **404**；`cp -r lib/liquid-glass <bundle 目录>/` 即与源码逐字节一致 | 该路由以 `import.meta.url` 定位同目录 `liquid-glass/`（`lib/index.js:3453`）；门禁两种布局都断言过 |
| `ping.version` | 上一级目录没有 `package.json` 时返回 `null`（只影响版本号显示） | `new URL('../package.json', import.meta.url)`（`lib/index.js:1622`） |
| 「检查更新 / 一键更新」 | 无伴生 `package.json` 时 `update-check` 返回 500，`update-apply` 会往 bundle 同级/上级目录写文件 ⇒ **不建议在方式四下使用** | `lib/index.js:1792-1860` |
| 卸载 | 删掉那个 `.mjs` 与 `cordis.patch.yml` 里那一行即可 | — |

> 结论：**方式四是"宿主端能力"的降级装载**（离线/应急/给非 DSH 宿主复用路由时好用）；要完整界面请用方式一/二/三。产物**不入库**（`dist/` 在 `.gitignore` 里：它是 `lib/*.js` 的纯派生物，两次构建 sha256 逐字节相同，`tools/bundle-equivalence-test.mjs` 第②节；发布时现生成并公布哈希）。

### 更新

```bash
# 方式一 / 二：走 npm 的 latest 标签
dsh plugin --profile web update dsh-mpkg-wallpaper

# 方式三：在克隆目录里
git pull

# 方式四：重新生成并替换那个 .mjs
node tools/build-bundle.mjs
```

更新后都要：重启 `dsh web` → 浏览器 `Ctrl+F5`。

### 卸载

方式一/二/三：`dsh plugin --profile web remove dsh-mpkg-wallpaper`。
方式四：删 `.mjs` + `cordis.patch.yml` 里那一行。
残留数据（可选清理）：浏览器 `localStorage['dsh.mpkg-wallpaper.v2']`、宿主端 `~/.dsh-mpkg-wallpaper/`（`settings.json`、`web-store.json`、`media-audio.json`、上传的 mpkg、转码缓存、`diag-*.json`）。

## 30 秒快速开始

这节给最短路径：装完到看见壁纸，只走三步。

1. **装好并重启**：按上一节任选一种方式装完，重启 `dsh web`，浏览器 `Ctrl+F5`。
2. **打开面板**：左侧栏「设置」→「壁纸引擎背景」。
3. **选一张壁纸**，任选其一：
   - 拖入 `.mpkg` 文件（视频类直接播；场景类走静态帧/图层合成）
   - 选本地图片 / 视频，或填一个图片链接
   - 「自定义目录」选一个文件夹（可直接选 Steam 的 `steamapps/workshop/content/431960`，每个子文件夹算一张）

默认档就已经能用：总开关开、大文件混合模式开、整屏虚化开（30px）、Now playing 挂在左侧栏。
想微调，先动这三处就够：**壁纸设置 → 磨砂模糊**（0–40）、**界面统一 → 整屏虚化程度**（0–40）、**壁纸设置 → 镜头缩放**（10–2000%）。

> 没反应时先去「其他」tab 点一次 **一键诊断上报**（宿主不可用会自动下载 JSON），再带上它去[反馈](#反馈-bug)。

## 核心能力

这节按**你能感知到的东西**分组（来源、时间变化、虚化、外观、播放、库与轮换、安全、备份），不按代码模块。

**📦 壁纸来源**
- **Wallpaper Engine `.mpkg`**：浏览器内直接解析容器（不上传第三方）；视频类播放内嵌 mp4 / 视频纹理；场景类解析容器提取素材；**时间变化**按系统时间选时段素材
- **Steam 创意工坊目录**：自动发现 WE 安装（注册表 + `libraryfolders.vdf`，支持非默认盘），列出 `video / web / scene` 三类；也可把 **workshop 主目录**（`steamapps/workshop/content/431960`）直接设为自定义目录——每个子文件夹自动识别为一张壁纸
- **视频**：`.mp4/.webm/.mov/.m4v` 直接播放；**网页**：HTML 在沙箱 iframe 中加载（带风险预检）；**图片/动图/链接**：本地图片或 URL（含 `data:image`）
- **自定义目录**：任意文件夹，`.mpkg`、workshop 子目录、图片/视频/`scene.pkg` 混放都能识别

**⏰ 时间变化壁纸（Time Variation）**
- 识别 WE 的时间变化属性（`morningtime / daytime / dusktime / nighttime / timevarying`，默认 5/8/17/20 时，`lib/client.js:10419-10423`）
- **按需懒加载**：只提取当前时段素材（单槽峰值几十 MB），切换时段时才读，避免一次导入全部时段导致 OOM
- **手动锁定时段**：时段按钮只在容器里真的有该时段素材时出现（`lib/client.js:12797-12813`），键名 `timeOverride`；点「自动」恢复随时间切换
- **不串台**：切换壁纸时清空上一张的时段缓存

**🌊 整屏虚化（磨砂）体系**
- **统一虚化**：一条滑条控制整屏壁纸模糊度 + 侧边栏/标题栏白雾厚度；聊天区是否跟随、新会话按钮是否跟随各自独立
- **界面虚化（各自独立开关 + 程度）**：对话框（通用居中窗口 + 聊天输入框）、设置面板、下载/确认弹窗、弹层（菜单/下拉/提示）、遮罩（全屏背景）、左侧边栏磨砂
- **透出壁纸**：左侧边栏 / 标题栏 / 右侧边栏 dock 各自独立，标题栏磨砂可单独指定半径

**🎨 主题色与玻璃外观（Aqua 实验默认全关）**
- **主题颜色（`themeColor`）**：取色盘 + 预置，驱动侧栏/标题栏/新会话按钮/设置弹窗底色；**配色（`accent`）**驱动品牌交互色（按钮/滑条/选中/链接/发送键）
- **面板颜色匹配壁纸（`aquaTint`）**：自动采样壁纸主色（视频/GIF 每 2 秒刷新）；**统一雾**（全屏色调雾罩）、**自适应文字色 + 蓝色清理**、**深底文字可读增强**、**任务列表磨砂**
- **液态玻璃（CSS/SVG 版）**：`lgCss` + 折射强度，作用于输入框/左侧边栏/标题栏；`lib/liquid-glass/` 的 WebGL 运行时不参与生成（见[文件结构](#文件结构)）

**🧩 dsh-better-sidebar 适配（检测到该插件后显示）**
- 已安装时「其他」tab 出现**适配分类**：总开关 `bsCompat`（**默认开**）+ `bsFloat`（悬浮双层修复：14px 圆角外壳 + 内层透明 + 零外边距 + resize strip 挪进面板）/ `bsFont` / `bsReveal` + `bsRevealAlpha` / `bsAqua`
- 宿主 `/ping` 返回 `{ok, version, betterSidebar, betterSidebarVersion}`；客户端写 `body[data-mpw-bs-version]`，版本专属规则用 `[data-mpw-bs-version^="…"]` 门控（`lib/index.js:1626-1643`、`lib/client.js:255-269`）
- 详见 [`docs/BETTER-SIDEBAR-COMPAT.md`](docs/BETTER-SIDEBAR-COMPAT.md)、[`docs/BETTER-SIDEBAR-DOM-CONTRACT-0.19.1.md`](docs/BETTER-SIDEBAR-DOM-CONTRACT-0.19.1.md)，回归 `node tools/better-sidebar-compat-test.mjs`

**⏯️ 播放控制与省电**
- 视频/网页壁纸可**暂停/播放**（设置页「壁纸设置」下的按钮），暂停状态实时反映视频实际状态；**调整无关设置不会触发重播**（`video.src` 判等已修）
- **省电三档**：页面隐藏/切页暂停、窗口失焦暂停、电池供电暂停（`getBattery` 缺失则静默跳过）；任一档触发即暂停，全部恢复才继续；与手动暂停共用一套门控

**🚀 大文件混合模式（hybrid，默认开）**
- mpkg **流式上传**到 DSH 宿主 → 磁盘存储 → HTTP Range 流式播放（`lib/index.js:1688-1728`、`:1730-1790`）；**>600MB 也能放**，因为流不进内存；关掉则回纯浏览器模式（600MB 上限）

**🖼️ 本地壁纸库与轮换**
- Steam 自动发现 + 自定义目录（跨平台目录选择器）；WE 原生播放列表（`config.json` 的 `general.playlists`）导入为轮换列表
- 上一个/下一个一键切换、定时自动轮换（`rotate` + `rotateMin`，1–120 分钟）；列表勾选后滚动不跳顶

**🛡️ 安全与共存**
- **冲突检测**：检测到其他壁纸/主题插件时自动关闭本功能（可手动强开，写 `forceEnabled`）
- `.exe/application` 壁纸完全排除（`lib/web-wallpaper.js:101`、`:199`）；自定义目录只读媒体文件；宿主路由有路径穿越校验；网页壁纸 iframe 沙箱隔离

**💾 备份与恢复 / 设置持久化**
- 「其他」tab 的**备份与恢复**导出外观类设置为可分享 JSON（`BACKUP_FIELDS`，`lib/client.js:11979-11993`），导入即还原
- 设置除浏览器 `localStorage`（键 `dsh.mpkg-wallpaper.v2`，`lib/client.js:48`）外另存宿主端 `~/.dsh-mpkg-wallpaper/settings.json`，换端口/清浏览器数据不丢

## 支持的壁纸类型与边界

这节回答「我手上的素材能不能用、能用到什么程度」；表后的边界清单说明为什么有些事做不到。

| 类型 | 表现 | 能控制什么 / 做不到什么 |
|---|---|---|
| **mpkg（视