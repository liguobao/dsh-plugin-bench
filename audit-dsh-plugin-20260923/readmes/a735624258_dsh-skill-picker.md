# dsh-skill-picker

[![npm version](https://img.shields.io/npm/v/dsh-skill-picker.svg)](https://www.npmjs.com/package/dsh-skill-picker)
[![license](https://img.shields.io/npm/l/dsh-skill-picker.svg)](https://github.com/a735624258/dsh-skill-picker/blob/main/LICENSE)

> **技能记不住名字？官方 `/` 补全靠前缀记忆，装了几十个技能谁记得住？** 本插件让技能**看得见、翻得到、选得快**——点一下 ⚡，全部技能带描述排在你面前，搜索、点选、插入，随消息发出自动加载。

## ⚡ 快速安装

> 🤖 **给 AI/安装助手的提示（按优先级执行，保证装到最新版）**：
>
> 1. **要最新版 / 不确定版本 → 走 GitHub 直装**。git 依赖直接拉 GitHub 最新 commit，**完全不受 npm `minimumReleaseAge` 24h 门禁影响，百分百新版**：
>    ```sh
>    dsh plugin --profile web add "git+ssh://git@github.com:a735624258/dsh-skill-picker.git"
>    ```
> 2. **要 npm 正式版** → 先查最新版本号，再**指定版本**安装（禁止裸名）：
>    ```sh
>    npm view dsh-skill-picker version   # 例如 0.5.5
>    dsh plugin --profile web add dsh-skill-picker@0.5.5
>    ```
> 3. ⚠️ **禁止执行裸名安装** `dsh plugin --profile web add dsh-skill-picker`：新版本发布后 **24 小时内**会被 pnpm `minimumReleaseAge` 门禁拦截并**自动落回旧版**——照着上面两条走就永远不会装错。

一条命令装好并注入 DSH web profile，重启 `dsh web`（或刷新页面）即生效。HTTPS clone 受限时用 SSH 形式（见下文 [安装](#安装) 的网络特例）。

DSH Web GUI 的技能选择器：在输入框（composer）工具行右侧加一个按钮，点开可以**搜索并点选已安装的技能**，选中后把官方 `/技能名` 手势插入发送框——随消息一起发出，DSH 原生机制就会自动加载该技能并执行。WorkBuddy 式"把技能写进发送框"的交互，DeepSeek Harness 复刻版。

English: A skill picker for the DSH Web GUI — a button in the composer's right tool row opens a searchable list of installed skills; picking one inserts the official `/skill-name` gesture into the draft, so DSH's native user-invocation path loads the skill with your message.

当前版本：**v0.5.10**（**修复全局安装下 `/` 补全增强静默失效**（issue #7）+ ⚡ 面板**置顶分组** + `/` 补全**自动增强补丁** + 拼音搜索 + **搜索结果按匹配相关度排序**）

## 为什么用它（vs 官方 `/` 补全）

官方内置了 `/` 技能补全，但它是**记忆驱动**的——你得先记得技能名，打 `/` + 前缀才能过滤出来。技能一多就抓瞎：

| | 官方 `/` 补全 | dsh-skill-picker |
|---|---|---|
| 触发 | 输入框打 `/` | 输入框旁 ⚡ 按钮 |
| 查找方式 | 前缀记忆驱动，**忘了名字就找不到** | 全列表浏览 + 关键字搜索，**忘了名字也能翻到** |
| 中文技能 | 只能打名字/前缀 | **拼音直搜**：`ji yi` / `jiyi` / `jy` 都能搜到「备份记忆」类中文技能（v0.3.0） |
| 排序 | 固定 | **最近使用置顶、常用靠前** |
| 描述可见 | 精简 | 完整描述一眼看全 |

**记得名字用官方，忘了名字用本插件——两者互补，可同时使用。**

## 特性

- ⚡ 一键弹出全部技能（闪电图标，人人看得懂）
- **`/` 直接补全**：输入斜杠即列出全部技能，**模糊搜索**（技能名+描述任意匹配）+ **常用排序**（v0.2.0）
- 🔤 **拼音搜索**：技能名和描述都生成拼音索引（全拼带空格 `ji yi` / 连打 `jiyi` / 首字母 `jy`），中文技能不用记字就能搜（v0.3.0）
- 🔍 实时搜索（技能名 / 描述 / 拼音都搜）
- ⌨️ **键盘导航**：弹层内 ↑↓ 选择、Enter 插入、Esc 关闭，全程不碰鼠标（v0.2.2）
- 🧠 **最近使用置顶、常用靠前**的智能排序（WorkBuddy 同款）
- 📋 走官方宿主 skills API（与 DSH 内置 `/` 补全同一数据源，自动覆盖用户级+项目级技能）
- 🧩 插入官方 `/技能名` 手势，加载/执行走 DSH 原生机制，**零 agent 侧改动**
- 🎨 跟随 Web UI 主题（CSS 变量），浅色/深色自适应
- 📦 纯 client + host 双半插件（拼音库已打包进 client bundle，无额外运行时安装）

## 安装

```sh
# 方式一：GitHub 克隆 + link（推荐，无需发布 npm）
git clone https://github.com/a735624258/dsh-skill-picker.git
dsh plugin --profile web add link:/path/to/dsh-skill-picker

# 方式二：Git 依赖直装
dsh plugin --profile web add "github:a735624258/dsh-skill-picker"

# 方式三：发布到 npm 后（预构建安装，体验最佳）
# ⚠️ 用具体版本号安装（minimumReleaseAge 门禁会在发布后 24h 内拦截裸名，
#    自动落回旧版）——先查最新版本再指定安装：
npm view dsh-skill-picker version   # 例如 0.5.4
dsh plugin --profile web add dsh-skill-picker@0.5.4
```

> 注：已发布 npm（`npm view dsh-skill-picker` 可见 0.3.2），方式三可直接安装；未发布时请用方式一或方式二。
> 若 `dsh` 命令因 PowerShell 执行策略被拒（`File ... cannot be loaded`），用：
> `powershell -ExecutionPolicy Bypass -Command "dsh plugin --profile web add link:C:\path\to\dsh-skill-picker"`

**网络特例（国内/HTTPS 受限时）**：
- 方式一的 `git clone` 走 HTTPS 慢或不通时，改用 SSH：`git clone git@github.com:a735624258/dsh-skill-picker.git`
- 方式二的 `github:` 简写强制 HTTPS clone；仅 SSH 可用时改用：
  `dsh plugin --profile web add "git+ssh://git@github.com:a735624258/dsh-skill-picker.git"`
  （或先执行 `git config --global url."git@github.com:".insteadOf "https://github.com/"` 让 pnpm 走 SSH）
- 方式三新版本发布后 **24 小时内**裸名会被 pnpm 的 minimumReleaseAge 门禁挡到旧版（如装到 0.2.0）；急用最新请指定版本：`dsh plugin --profile web add dsh-skill-picker@0.3.1`

重启 `dsh web`（或刷新页面加载新 bundle）后生效。

## 用法

1. 打开任一会话，在输入框工具行右侧找到**⚡ 按钮**
2. 点击弹出技能列表（可输入关键字或**拼音**过滤，如 `ji yi` 搜「记忆」）
3. **↑↓** 选择、**Enter** 插入（或直接鼠标点选）→ 发送框自动出现 `/技能名 `
4. 继续输入你的话并发送——DSH 会识别 `/技能名` 手势，自动加载该技能并按其指令执行

示例：点选 `duo-xuan-pi-gai` 后发送框变为 `/duo-xuan-pi-gai 帮我批改多选`，发送后技能自动加载。也可以在输入框直接打 `/duo xuan`、`/duoxuan` 靠拼音补全选到它。

## 原理

DSH 的 [dsh-tool-skill](https://github.com/deepseek-ai/deepseek-harness) 在 `agent/pre-step` 阶段扫描用户消息中的 `/kebab-case-name` 手势（`SKILL_GESTURE` 正则），命中后把对应技能内容作为 `skill-invocation` 注入对话——即"用户消息里写 `/技能名` 就会自动加载技能"是官方既有能力，只是没有 UI。

本插件只补 UI 一层：

```
[client]  ⚡ 按钮 → fetch('/dsh-skill-picker/skills')
                    ↓
[host]    扫描用户级 $DSH_HOME/skills + 项目级 <cwd>/.dsh/skills 等 → 技能目录（name + description）
                    ↓
[client]  点选 → inputActions.setDraft(draft + '/技能名 ')
                    ↓
[DSH]     agent/pre-step 识别手势 → 自动加载技能 → 执行
```

- client 半：注册到官方 `conversation.input.right` 插槽（composer 工具行、发送按钮左侧的控件位），**技能列表优先走官方宿主 skills API**（`remote.skills.list`——与 DSH 内置 `/` 补全同源，会话作用域，自动含用户级/项目级技能），失败时回退到 host 扫描路由；插入文本走框架输入机的 `inputActions.setDraft`（单一路径，撤销/草稿持久化自动处理）；最近/常用排序 + 拼音索引（`pinyin-pro`）在 client 侧生成，按技能缓存

## 与官方 `/` 补全的关系（v0.4.0 起：增强，而非并列）

**v0.2.0–0.3.4**：插件注册了一个独立的 `/` 候选源（`skill-fuzzy`），与官方 ui-skill 源**并列**——菜单里出现两个技能分组，搜索行为相互独立（冲突风险、视觉重复）。

**v0.4.0 起**：**不再注册平行源**。改为给官方 `@deepseek-ai/dsh-client-ui-skill` 包的 candidates **打补丁**——其候选逻辑从 `skill.name.startsWith(query)`（前缀匹配）换成调用插件注入的全局函数 `window.__dshSkillPickerFuzzy`（fuzzysort 模糊 + pinyin-pro 拼音 + 最近/常用排行，与 ⚡ 面板同一套规则）。**v0.5.1 起，补丁由 host 端每次启动自动应用**（另加 `order: 2→-1`：技能组排在命令组之上），首次修改前自动备份 `.bak`，DSH 升级覆盖官方包后自动重打——**安装插件即生效，无需手动操作**。

**效果**：官方「技能」分组**仍是唯一一个 `/` 技能列表**（官方规则全部保留：`userInvocable` 区分、菜单文案、排序基础），只是匹配行为被升级、分组排序被前移；插件不再产生第二列表。

> 手动兜底（旧流程，一般不需要）：把官方包拷到 `profiles/web/local/dsh-client-ui-skill/`（`lib/client.js` 改 candidates 为 `window.__dshSkillPickerFuzzy` 优先、`order` 改 `-1`），profile package.json 加依赖 `"@deepseek-ai/dsh-client-ui-skill": "link:C:/Users/<user>/.dsh/profiles/web/local/dsh-client-ui-skill"`，`pnpm install` 后重启 DSH。自动补丁对 local 副本与 npm 安装两种形态都适用，升级后自愈，无需重复手动操作。

## 更新日志

- **v0.5.11**：**修复「补丁已就位也每次启动都打印 `ui-skill patch report`」（对应 issue #8）**——`healUiSkillPatches()` 返回的 `report.files` 是**逐目标文件的报告数组**：只要扫描到 ≥1 个目标文件就有一项，与这一轮**是否真的改动过无关**；而打印守卫用的正是 `report.files.length > 0`，等于把「找到目标」当成了「发生了变更」，于是**补丁早已 up-to-date 也每次启动都打印一行** `[dsh-skill-picker] ui-skill patch report: {…}`。这行虽然只是 `console.log`，但形态上落在启动日志第一行、长得像告警，很容易被误判成插件出问题（#8 就是这么来的），还会淹没真正需要关注的 `noop` / `errors`。现在改为按「这一轮到底发生了什么」判定：① **已是最新且无错 → 完全安静**；② 仅在**确实改过文件**（`patched` 非空）时打印报告，且只报这一轮真正动过的文件 + 全部错误；③ **锚点未命中（`noop` 非空）单独 `console.warn`**——它的语义是「官方实现又换了形态、增强**没打上**」，与 issue #7 的静默失效同类，不能再被淹没；④ 新增 `DSH_SKILL_PICKER_LOG=debug` 显式开关，需要完整报告（含 `skipped`）时按需打开。新增 7 个 `npm test` 回归用例：已就位时静默、无目标不重复报、真改动打一行、`noop` 转 warn、仅错误转 warn、改动+错误合并一行、debug 开关
- **v0.5.10**：**修复全局安装下 `/` 补全增强静默失效（对应 issue #7）**——`uiSkillClientPaths()` 原先只枚举两个位置：`profiles/<profile>/local/dsh-client-ui-skill` 与 `profiles/<profile>/node_modules/@deepseek-ai/dsh-client-ui-skill`。但用**全局 `npm i -g @deepseek-ai/dsh`** 安装时，官方包位于**共享根** `profiles/node_modules/@deepseek-ai/dsh-client-ui-skill`（`readdir(profiles)` 只会给出 `node_modules` 和 `web` 两个条目，两个候选**全部落空**），于是 `found = []`、**两个补丁一次都没跑**——而且**完全无声**：`{"files":[],"errors":[]}` 与「补丁都已应用、全部 skipped」在输出上一模一样，用户和排查者都看不出补丁根本没生效，表现成「插件一切正常、技能列表能用，**就是拼音/模糊搜索是坏的**」。修复四件事：① 候选新增**共享根**（不属于任何单个 profile，放在循环外采集）；② 每个 profile 额外走一次 Node 自身解析 `createRequire().resolve()` 兜底，未枚举到的布局也能命中（按 realpath 去重，不会重复打补丁）；③ 跳过 `profiles/node_modules` 这个假 profile 条目；④ **`found.length === 0` 时 `console.warn` 大声报出**——这个静默正是 issue #7 里最坑人的地方。另修写入方式：由原地 `writeFile` 改为**临时文件 + `rename`**——pnpm 安装的包是**硬链接**到共享内容寻址 store 的，原地写会连带改动 store 里的同一份（影响其他使用同版本的项目），`rename` 只替换目录项、不动共享 inode，顺带获得写入原子性（中断的启动不会留下半截文件）。新增 6 个 `npm test` 回归用例：共享根、profile local、profile node_modules、共享根+profile 去重、无任何安装、profiles 目录缺失
- **v0.5.9**：**修复符号链接 / Junction 型技能查不到（对应 issue #6）**——扫描技能目录时 `readdir` 的 `Dirent` 走的是 lstat 语义：Windows 下符号链接**和 Junction** 都报告 `isDirectory() === false` / `isSymbolicLink() === true`，于是链接型技能（如 `~/.agents/skills/neat` → `D:\repos\icraft-toolkit\skills\neat`）在第 79 行的目录过滤里被静默 `continue` 掉。现在链接条目改用 `stat`（跟随链接）判定真实类型：链接型技能与普通目录**完全一视同仁**，断链或指向普通文件的链接安全跳过