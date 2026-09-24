# dsh-paste-input

**简体中文** | [English](./README.en.md)

DSH WebUI 文件输入增强插件：**Ctrl+V 粘贴** + **全页面拖拽** + **选择文件/文件夹**，发送时复制进会话工作区临时附件目录，并把对话气泡里的附件文本块**折叠为文件 chip**。

派生自 [dsh-external/dsh-multimedia-webui-input](https://github.com/dsh-external/dsh-multimedia-webui-input)（MIT），在其基础上新增剪贴板粘贴输入、首次告知弹窗与气泡附件折叠。

> **你的 DSH 版本决定装哪个插件版本**（装错会崩：常见症状 `useConversation is not a function`）
> - DSH **0.1.1-rc.2**（npm 最新）：装**旧版** `'@dsh-external/dsh-paste-input@github:lhh010/dsh-paste-input#v0.1.5'`
> - DSH **0.1.2-alpha.1 / alpha.2 / alpha.3 / alpha.4 / alpha.5 / rc.1**：装**新版**（下方默认命令）
## 安装（profile 模式）

```sh
# 方式一：git 依赖固定 tag（公开镜像，推荐；也可用 github:lhh010/dsh-paste-input）
dsh plugin --profile web add '@dsh-community/dsh-paste-input@github:lhh010/dsh-paste-input#v0.1.29'

# 方式二：本地 link
# dsh plugin --profile web add link:/path/to/dsh-paste-input
```

并在 `~/.dsh/profiles/web/cordis.patch.yml` 追加（热重载，无需重启）：

```yaml
- insert:
    - id: dsh-paste-input
      name: '@dsh-community/dsh-paste-input'
```

> **安装提示**：pnpm 11 首次安装可能拦截 node-pty 等构建脚本——在 `~/.dsh/profiles/web` 下执行 `pnpm approve-builds --all` 放行后重跑安装命令；装完**硬刷新浏览器**（Ctrl/Cmd+Shift+R）。

## 智能版本门控更新提示 / DSH-gated update chip

更新浮标会结合**当前运行的 DSH 版本**（宿主端从 dsh 安装清单读取）与仓库根的 [`compatibility.json`](compatibility.json)（版本→支持的 DSH 列表，精确匹配）判定提示形态：

- 最新版支持当前 DSH → 正常「新版本 vX 可用，点击更新」；
- 最新版需要更高 DSH、但存在支持当前 DSH 的中间新版 → 提示更新到中间版，并注明「另有 vX 需更高 DSH」；
- 最新版需要更高 DSH、且当前 DSH 无任何可用新版 → 琥珀色信息条：「新版本 vX 支持更高 DSH 版本，当前 DSH vY 暂不可用」，不提供直接升级。

兼容数据拉取失败或无该版本条目时，自动回退为旧的普通升级提示（离线安全）。**发版时需同步维护 `compatibility.json`**（与版本表/变更记录同一步骤新增一行）。

### 2026-09-24 · v0.1.29 — 声明支持 dsh-v0.1.7-rc.1

- **声明**：支持 dsh-v0.1.7-rc.1（零适配改动）；双 bundle `node --check` 通过

### 2026-09-23 · v0.1.28 — 更新浮标加入 DSH 版本门控 + 声明支持 dsh-v0.1.7-alpha.2

- **新功能**：宿主端新增 `/dsh-paste-input/v1/latest` 端点返回当前 DSH 版本；客户端更新判定结合 `compatibility.json`——最新版不支持当前 DSH 时显示琥珀色「需更高 DSH 版本」提示，支持中间版本时提示中间版
- **声明**：支持 dsh-v0.1.7-alpha.2（实机验证）；双 bundle `node --check` 通过

### 2026-09-17 · v0.1.27 — 适配 dsh-v0.1.6-alpha.2

适配 dsh 0.1.6-alpha.2 多实例重构：当前会话改由 `uiSession.current`（`{ key, ctx }`）解析（alpha.1 的 `sessions.list.current` 字段已移除，此前导致粘贴/拖拽/附件按钮全部弹「请先打开一个会话」）；粘贴、拖拽、附件按钮三条路径均已切换，alpha.1 回退保留。lib node --check 全绿，alpha.2 实机验证 chips 恢复显示。

### 2026-09-15 · v0.1.26 — 声明支持 dsh-v0.1.6-alpha.1

声明支持 dsh-v0.1.6-alpha.1（npm 已发布，钉版本实机验证；client 插件面零代码差异，lib node --check 全绿，实机加载正常）。安装命令统一更新为 `#v0.1.29`。

### 2026-09-10 · v0.1.25 — 补充声明 dsh-v0.1.5-rc.2 兼容
- **验证**：rc.2 无 client 插件面变更，无需代码改动；rc.2 实机宿主（tag fb2c4b9e）加载确认，粘贴入框/悬停预览/查看器正常

### 2026-09-10 · v0.1.25 — 声明支持 dsh-v0.1.5-rc.1
- **验证**：rc.1 为 0.1.5 系列首个候选版本，client 插件面零代码差异；npm 已发布，钉版本实机验证；同步 lib 内烙死的 PLUGIN_VERSION 常量

### 2026-09-09 · v0.1.24 — 修复旧格式消息折叠失败
- **修复**：会话历史中存在两种结束标记（现行 `==== END DSH_PASTE_INPUT ====` 与旧缓存 bundle 写入的 `==== END DSH_PASTE_INPUT_V1 ====`），解析器只认后者之外的现行格式导致旧消息折叠失败并刷 Console 警告；现兼容两种拼写。注：V1 结尾拼写为历史遗留（仅极早期 bundle 写入），**后续版本可能不再兼容**，依赖旧格式折叠的历史消息请尽快升级

### 2026-09-09 · v0.1.23 — 声明支持 dsh-v0.1.5-alpha.2
- **验证**：alpha.2 改动为 Sidebar 文档预览、模型文件交付、minimal 默认工具调整与 `fs-ext` 安装修复，client 插件面零代码差异；npm 已发布，钉版本实机验证；同步 lib 内烙死的 PLUGIN_VERSION 常量（避免幻影自更新）
### 2026-09-08 · v0.1.22 — 声明支持 dsh-v0.1.5-alpha.1
- **验证**：0.1.5 改动在会话格式 V3 / `ctx.agent` 移除 / 宿主 client bundle 服务路由改 `/plugins/??` 组合路由，client 插件面零代码差异；npm 已发布，钉版本实机验证，无需代码改动；启动清单确认加载
### 2026-09-05 · v0.1.21 — 声明支持 dsh-v0.1.3-alpha.2

- **验证**：alpha.2 改动全在 pi-ai / Web 顶栏 / 子代理消息 / host 面，client 插件面零代码差异；npm 已发布，钉版本实机验证，无需代码改动

### 2026-09-05 · v0.1.20 — 粘贴记录持久化开关（sessionStorage，默认关）

- **新功能**：标题栏「Profiles」按钮旁新增「📎 记录持久化」开关（默认**关**）。开启后粘贴记录会镜像到 `sessionStorage`——页面刷新后，输入框里残留的粘贴引用 chip 仍可正常发送（此前会报 "Attachment selection is no longer available in this browser tab"）。
- **限额**：单文件 > 1 MiB 不持久化；快照总量上限约 3 MiB，超出自动跳过（大文件场景请关闭或接受部分持久化）。
- 关闭开关即清空已持久化的记录。
- **作用粒度**：持久化按"每次粘贴的记录"逐条生效——粘贴那一刻开关是开且文件不超限才写入；切到「关」清空已有记录；重新开启不回溯补旧记录；已发送的消息不受影响（文件已存宿主侧）。

### 2026-09-04 · v0.1.19 — 声明支持 dsh-v0.1.3-alpha.1

- **验证**：0.1.3 破坏性变更集中在 host/session 侧（SessionHandle / session format v2），composer/输入面实测无影响；npm 未发布，源码宿主实机验证（粘贴入框/悬停预览/查看器正常），无需代码改动

### 2026-09-03 · v0.1.18 — 声明支持 dsh-v0.1.2-rc.1

- **验证**：alpha.5→rc.1 为纯版本号提交（252 文件零代码差异）；实机 rc.1 验证通过（悬停预览/查看器正常），无需代码改动

### 2026-09-03 · v0.1.17 — 图片/动图悬停预览 + 点击查看器（缩放/平移）

- **新功能（悬停缩略图）**：图片类附件（png/jpg/jpeg/gif/webp/bmp/avif/ico）的 chip 悬停即弹出小预览卡，GIF 动图原样播放；输入框待发送 chip（本地字节，blob URL）与气泡内已发送 chip（宿主端按所有权标记校验后回读文件）都支持
- **新功能（点击查看器）**：点击图片 chip 打开全屏查看器——滚轮以光标为中心缩放（20%–800%）、左键拖动上下左右平移、双击在 1×/2× 间切换、`+`/`-`/`0`/`Esc` 快捷键、工具栏含缩放百分比/重置/复制完整路径/关闭；GIF 在查看器中持续播放
- **宿主端新增只读路由** `GET /dsh-paste-input/v1/file?root=<发送目录>&path=<相对路径>`：仅服务**所有权标记（`.dsh-paste-input.json`）声明过的图片文件**（SVG 除外，避免同域脚本执行），路径解析约束在发送目录内，单文件 ≤64 MiB
- 非图片 chip 行为不变（悬停显示原始附件块、点击复制路径）；图片 chip 的「复制路径」移入查看器工具栏
- **修复（dock chip 崩溃，v0.1.16 遗留）**：输入框上方附件 dock 的删除按钮引用了不在本作用域的 `busy` 变量，chip 一渲染即 `ReferenceError`，整个 dock 槽位被错误边界吞掉（表现：dock 上的附件气泡消失）；已移除该悬空引用

### 2026-09-02 · v0.1.16 — 修复 AttachButton 崩溃 + 版本检查 403 改走 jsdelivr

- **修复（AttachButton 崩溃）**：`conversation.input.left` 槽位不提供 owner props（无 `input`），`props.input.phase` 读取 undefined 崩溃（Console 报 `Cannot read properties of undefined (reading 'phase')`，槽位条目被框架错误边界捕获）。改用可选链 + `'plain'` 默认值（`add()` 自身有 phase 守卫不会误操作）。dock 槽位的 `occurrences` 同样加防御
- **修复（403 刷屏）**：版本检查的 tag 源从 `api.github.com`（未认证限流 ~60 req/hr → 403）改为 `data.jsdelivr.com/v1/packages/gh/`（CDN，无限流，CORS 友好）
### 2026-09-02 · v0.1.15 — 声明支持 dsh-v0.1.2-alpha.5

- **验证**：alpha.5 为纯 bug 修复（升级路径问题），client 运行 API 无变更；lib 产物校验通过

### 2026-09-02 · v0.1.14 — 声明支持 dsh-v0.1.2-alpha.4

- **验证**：alpha.4 下 client 运行 API 无破坏性变更（changelog 仅宿主侧 Session events 重构）；lib 产物校验通过

### 2026-09-02 · v0.1.13 — 更新提示词补版本路由与排查指引

- **修复（更新提示词）**：提示词新增第 0 步（先 `dsh --version` 确认本地 DSH 版本，对照 README「版本兼容」表选对应 tag，不匹配则改装）与第 3 步（安装失败/版本不匹配/启动报错先查 README「版本兼容」「已知限制」章节）；原两步安装流程不变
### 2026-09-01 · v0.1.12 — 版本检查增加缓存 / 403 降级

- **修复（反复 403）**：GitHub tags API 在限流/未授权时返回 403，旧代码每次页面加载与点击重试都重新请求一次，console 被 403 刷屏。现按结果缓存到 localStorage：成功结果缓存 10 分钟、瞬时网络失败 60s、硬 403（限流）缓存 5 分钟——窗口内直接返回缓存结论**不再发请求**，手动「重试」仍可强制执行一次
- **降级文案**：区分「网络不可达」与「GitHub 拒绝访问（限流/403）」——后者显示「版本检查暂不可用（GitHub 拒绝访问），已缓存」，不再误导为网络问题
### 2026-09-01 · v0.1.11 — 版本检查 chip 不再被 GitHub CDN 缓存滞后误导

- **修复**：刚 push 新 tag 后的几分钟内，GitHub tags API / raw CDN 仍返回旧 tag，「已是最新版本」chip 会把**旧的远端 tag** 当作最新显示（如运行 0.1.10 却显示「已是最新 0.1.9」）。现取「拉到的 tag 与运行版本」中较新者展示；离线 chip 的重试路径同样处理
### 2026-09-01 · v0.1.10 — 修复 dock 删除失效 + 同名文件自动加序号

- **修复（删除失效 → unavailable）**：DSH 0.1.2-alpha 的输入机里 occurrence 的 offset/length 是 **clipboard 投影坐标**（chip 展开为完整 `[attachment: …]` 文本），而 `consumeToken` 的 span 校验在 **detect 投影坐标**（chip 仅占 1 个 U+FFFC 字符）下工作——旧代码直接把 clipboard 坐标传入导致替换必然失败，record 却已删除：dock chip 显示 unavailable、输入框 chip 残留。现按「前面每个 chip 缩短 length−1」精确换算成 detect 坐标再调用 `consumeToken`，失败时回退 setDraft 整段切除
- **修复（第二次粘贴报错 / 顶掉）**：`insertReference` 的插入点原来取 `snapshot.draft.length`（clipboard 投影长度），第一个附件存在后插入点越界 → `The DSH composer changed before the attachment could be inserted`。现同样按存活 chip 折算成 detect 坐标，多个附件可连续粘贴共存
- **新增（粘贴文件统一重命名）**：粘贴的文件统一改基础名——图片 `paste_image.<ext>`、其他文件 `paste_file.<ext>`（扩展名优先取原文件名，缺省按 MIME 补全）；重名自动追加 `(2)`、`(3)`… 序号（以 composer 实时 chips + records 为冲突集），改名同步进上传路径。**仅粘贴路径改名**，拖拽与文件/文件夹选择保留原始文件名
- **验证**：实机验证通过——连续粘贴两张截图得到 `paste_image.png` 与 `paste_image(2).png` 共存；dock × 删除上下同步；node --check 通过
### 2026-08-20 · v0.1.5 — 声明 DSH 0.1.1-rc.1 兼容性（实机 boot 验证）

- **验证**：DSH npm `0.1.1-rc.1` 实机 boot 验证通过——boot 清单包含本插件、client.js 返回 200；0.1.4 的 rc.8 适配（`consumeToken` 整段删除、`appearance: 'file'` 官方外观、内联 chip 整体编辑保护）在 0.1.1-rc.1 上行为无回归（所依赖的 `inputTriggers.registerSource`、`conversation.input.for` 门面与 `conversation.input.left/dock`、`settings.section` 槽位均保持不变）

### 2026-08-20 · v0.1.4 — DSH 0.1.0-rc.8 适配（删除失效 + 内联 chip 外观）

- **修复（删除失效）**：rc.8 输入机的引用 occurrence 占据 `@` + label 的完整行内区间（不再是 1 个占位符字符），v0.1.3 点击 dock chip 的 × 只删掉 `@` 一个字符，输入框内残留附件文本。现改用 rc.8 官方删除动词 `input.consumeToken`（span CAS 整段切除），旧宿主回退为按 `occurrence.length` 切除
- **新增（整体编辑保护）**：内联附件 chip 的文件名不可单独删改（部分编辑会被拦截并自动选中整个 chip，下一次按键整体删除/替换），见上「内联 chip 整体编辑保护」
- **修复（内联 ch