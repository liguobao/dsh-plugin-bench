# Awesome DeepSeek Harness Plugins

<!-- 本文件由 scripts/build-readme.mjs 从 deepseek1024.com 目录 API 自动生成，请勿手工编辑。 -->

面向 [DeepSeek Harness](https://github.com/deepseek-ai/DeepSeek-Harness)（`dsh`）生态的社区插件目录，共收录 **13720** 个插件（含 PR 收录与 GitHub `dsh-plugin` topic 自动发现），目录数据更新于 2026-09-23。

> 📦 **仓库拆分公告**：自 2026-08-25 起，deepseek1024.com 网站与 `dsh1024` CLI 的源码已拆分至独立仓库 [imsai-sh/dsh-1024store](https://github.com/imsai-sh/dsh-1024store)。本仓库从此专注插件目录（awesome 清单）与收录流程；网站与 CLI 相关的 issue / PR 请移步新仓库，插件收录照旧在这里提交。

**但这个项目不只是一份 awesome list。** 它还包括一个在线插件市场、一个把市场装进 `dsh` 本体的插件，以及一套免费的公开查询 API——这些应用代码开源在姊妹仓库 [dsh-1024store](https://github.com/imsai-sh/dsh-1024store)；本仓库专注目录本身：经静态校验的 PR 收录流水线与自动生成的目录 README，目录数据另有自动收集服务持续喂入。全部代码 MIT 协议，fork 之后就能部署成你自己的插件市场。

[![DSH 1024Store 插件市场首页](https://raw.githubusercontent.com/imsai-sh/awesome-deepseek-harness-plugins/assets/homepage.zh.png?v=4b4128dacb7b)](https://deepseek1024.com/)

[在线网站](https://deepseek1024.com/) · [API 文档](https://github.com/imsai-sh/dsh-1024store/blob/main/web/docs/api.md) · [英文目录](catalog/README.md) · [提交插件](CONTRIBUTING.md) · [网站与 CLI 源码](https://github.com/imsai-sh/dsh-1024store)

[![GitHub Stars](https://img.shields.io/github/stars/imsai-sh/awesome-deepseek-harness-plugins?style=social)](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/stargazers)

<div align="center">
  <strong>DSH插件社区</strong><br><br>
  <img src="docs/assets/wechat-group.jpg" alt="DSH插件社区微信二维码" width="280">
</div>

## 项目亮点

### 在线插件市场（开源 · 可一键自部署）

[deepseek1024.com](https://deepseek1024.com/) 提供搜索、分类筛选、安装排行榜、插件详情与 GitHub 活跃度数据。整站跑在 Cloudflare Workers + D1 + KV 上，源码在 [dsh-1024store](https://github.com/imsai-sh/dsh-1024store) 的 [`web`](https://github.com/imsai-sh/dsh-1024store/tree/main/web)。

想要一个完全属于自己的插件市场：fork [dsh-1024store](https://github.com/imsai-sh/dsh-1024store)，把 `web/wrangler.jsonc` 里的 `routes` 换成你自己的域名，创建 D1 数据库与 KV 命名空间，配齐 `secrets.required` 列出的 Worker secret，然后本地执行 `npm run db:migrate:remote` 和 `npm run deploy` 完成部署（部署是显式的本地操作，push 不会自动上线）。完整步骤见该仓库的[部署文档](https://github.com/imsai-sh/dsh-1024store/blob/main/web/docs/deployment.md)。

### 把插件市场装进 dsh 本体

不想切浏览器，就把市场本身作为插件装进 DeepSeek Harness：

```bash
dsh plugin --profile web add dsh1024@latest
```

重启后「设置」里会出现独立的 **1024 Store** 入口，「设置 → 插件」下也会多出一个 **1024 Store（数量）** 标签页，可以直接搜索目录、按分类筛选、识别已安装状态、安装与卸载，并显示操作进度。安装器只接受目录 API 返回并通过严格语法校验的结构化目标：优先使用已发布 npm 包，否则使用与插件 ID、仓库 URL 一致的 GitHub 源码规格；展示命令不会被直接执行。源码见 [`plugin`](https://github.com/imsai-sh/dsh-1024store/tree/main/plugin)。

### 定时自动收集 + 格式校验

这是本目录与多数插件市场最大的区别：**目录不靠人肉维护，收录前一定过校验。**

- **定时收集**：自动收录带 `dsh-plugin` topic 的 GitHub 仓库，增量抓取新建与新推送的仓库，并定期全量对账——长期不活跃的仓库不会被漏收，掉了 topic 也只在一次成功的全量对账后才下架。
- **格式校验**：每个候选仓库都要通过静态校验——读取默认分支的 Git tree，检查 `package.json`、`dsh.bundle.patch` 字段，以及 patch 文件在同一棵 tree 中确实存在。**全程只读文件，绝不安装依赖、绝不执行仓库代码。** 校验不通过就不进目录。
- **自动同步**：PR 合并后由 CI 自动同步目录到网站数据库并刷新本 README，贡献者和维护者都不需要手工改任何生成文件。

数据来源与校验语义见 [目录数据来源文档](docs/plugin-discovery.md)。

### 免费查询 API

目录数据免费开放，匿名即可调用：

```bash
curl 'https://api.deepseek1024.com/v1/plugins/search?q=memory'
```

匿名调用每天 50 次、每分钟 10 次；用 GitHub 账号登录网站创建 API Key 后提升到每天 500 次、每分钟 30 次。另有 `/api/v1/registry` 返回按安装热度排序的精简目录快照（至多 500 条）。完整端点、参数与错误码见 [API 参考](https://github.com/imsai-sh/dsh-1024store/blob/main/web/docs/api.md)。

## 参与进来

这个项目由社区维护，下面每一种参与都真的有用：

- **点个 Star** — [Star 本仓库](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/stargazers)是成本最低、帮助最大的支持，能让更多 DeepSeek Harness 用户找到这里。
- **提 Issue** — 插件信息有误、分类不合理、网站或 API 有问题、想要新功能，都欢迎[提 Issue](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/issues/new)。
- **发 PR** — [提交你自己的插件](CONTRIBUTING.md)或改进目录流水线，欢迎直接发 [Pull Request](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/pulls)；网站、CLI 与市场插件的改进请发到 [dsh-1024store](https://github.com/imsai-sh/dsh-1024store)。
- **Fork 自建** — 想要自己的插件市场，[Fork dsh-1024store](https://github.com/imsai-sh/dsh-1024store/fork) 之后按上面的步骤配置即可，MIT 协议，随便改。

## 安装插件并计入统计

1024 Store 只提供 npm 安装：插件详情页展示的命令安装的是作者发布到 npm、声明 `dsh.bundle` 的包；尚未发布 npm 包的插件以浏览模式收录（有仓库链接，无安装命令）。网站优先提供开源包装 CLI；它会调用官方 DeepSeek Harness 插件命令、校验 profile 的真实安装结果，并把匿名安装结果可靠地上报到排行榜：

```bash
dsh1024 plugin --profile web add <npm-package>
```

首次使用先一次性全局安装：`npm install -g dsh1024`。它与官方命令只差一个名字——`plugin` 之后的参数原样转发给官方 CLI，不增删、不改写、不重排，包装器只负责在结束后核对 profile 并记录一条匿名安装结果。参数不会写入遥测或本地 receipt。

monorepo 子目录插件的标识形如 `owner/repo/packages/foo`，每个子包发布并安装自己的 npm 包，同仓库的兄弟插件各自独立计数。

统计身份是保存在 `$DSH_HOME/.dsh-1024store/` 的随机安装实例 ID，不是实名用户或账号。CLI 不上传命令输出、路径、用户名、环境变量、会话内容或原始错误；可用 `npx dsh1024 telemetry disable`、`DO_NOT_TRACK=1` 或 `DSH1024_TELEMETRY=0`（旧变量名 `DSH_1024STORE_TELEMETRY` 仍兼容）关闭。直接使用官方 `dsh plugin` 命令仍然可用，但不会计入 DSH 1024Store 安装统计。详细字段、口径、存储和部署方式见 [安装统计设计](https://github.com/imsai-sh/dsh-1024store/blob/main/web/docs/install-analytics.md)，CLI 源码见 [`plugin`](https://github.com/imsai-sh/dsh-1024store/tree/main/plugin)。

## 提交插件

### 使用 Agent Skill 提交（推荐）

如果你使用 Codex、Claude Code、Cursor 或其他兼容 Agent Skills 的编程助手，可以安装本仓库提供的提交 Skill：

```bash
npx skills add imsai-sh/awesome-deepseek-harness-plugins --skill submit-dsh-plugin -g
```

安装后告诉助手：

```text
使用 $submit-dsh-plugin 检查并提交我的 DeepSeek Harness 插件。
```

该 Skill 会检查插件仓库、生成唯一允许提交的目录 JSON、验证变更范围，并在获得授权后创建 PR。新增条目的非草稿 PR 通过静态审查后会自动合并；修改或删除既有条目的 PR 同样会跑静态审查，但不会自动合并，需要维护者人工审核后手动合并。合并后 CI 自动同步目录到网站数据库并刷新本 README，贡献者和维护者都不需要手工更新任何生成文件。查看 [Skill 源码](skills/submit-dsh-plugin/SKILL.md)。

### 手动提交

欢迎把你的 DeepSeek Harness 插件提交到本目录。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，通过 PR 提交一个新的结构化插件文件；自动审查将验证提交范围和最基础的 DeepSeek Harness 插件配置，通过后自动合并，并由 CI 自动同步到网站与本 README。需要修正或下架既有条目时也可以发 PR，静态审查照常运行，但这类 PR 由维护者人工审核后合并。

安装命令以插件详情页展示的 npm 包为准：`dsh1024 plugin --profile web add <npm-package>`（首次使用先 `npm install -g dsh1024`）。

## 项目定位

本项目与 [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) 都服务于 DeepSeek Harness 插件生态。在继承其目录数据与社区整理思路的基础上，本项目把「一份人工维护的列表」扩展成一套开源、可自部署的插件市场基建：在线市场网站、dsh 内置市场插件、静态校验的 PR 收录流水线与免费查询 API，并由自动收集服务持续补充目录数据，具体见上文[项目亮点](#项目亮点)。

## 项目结构

```text
catalog/plugins/    插件提交表单与 curated 元数据（每个插件一个 JSON）
catalog/categories.json  分类定义（唯一分类信源）
catalog/schema/     插件提交 JSON Schema
skills/             面向贡献者的可安装 Agent Skills
scripts/            提交审查、目录同步与 README 生成脚本
docs/               目录数据模型文档
```

网站与 CLI 的源码（`web` 与 `plugin`）在姊妹仓库 [dsh-1024store](https://github.com/imsai-sh/dsh-1024store)。线上目录数据的唯一信源是 Cloudflare D1；本 README 与 [catalog/README.md](catalog/README.md) 由 CI 从目录 API 全量生成，职责划分见 [仓库布局](docs/repository-layout.md)。

## 网站与 CLI 的本地运行与部署

网站与 CLI 的本地开发、D1 迁移与 Cloudflare 部署流程都在 [dsh-1024store](https://github.com/imsai-sh/dsh-1024store)：见其 [README](https://github.com/imsai-sh/dsh-1024store#readme) 与[部署文档](https://github.com/imsai-sh/dsh-1024store/blob/main/web/docs/deployment.md)。本仓库只需要 Node.js 22+ 与 `npm ci && npm test` 即可参与目录流水线开发。

## 致谢

感谢以下项目为本目录提供基础与参考：

- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)：提供插件系统、`dsh.bundle` 规范和插件开发文档。
- [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)：提供初始插件目录数据和社区目录设计参考。

## 插件分类

分组默认折叠，点开即可展开。GitHub 对单个文件的渲染长度有上限，条目较多的分类只列出其中一部分（分类标题会写明列出了多少），完整目录请在[在线网站](https://deepseek1024.com/)搜索浏览。

- [UI 增强](#ui) (2625)
- [主题与外观](#theme) (496)
- [会话与消息](#session) (862)
- [记忆](#memory) (436)
- [工具与能力](#tools) (3976)
- [技能包](#skill) (1046)
- [工作流与自动化](#workflow) (772)
- [通知与集成](#notify) (499)
- [模型与账号接入](#model) (819)
- [开发与运行时](#dev) (1629)
- [娱乐](#fun) (560)

<a id="ui"></a>

<details>
<summary><strong>UI 增强</strong> · 显示 236 / 共 2625 个</summary>

- [01_content](https://github.com/Aisland-SJL/dsh-worktable/tree/HEAD/01_content) — 为控制台增加侧边栏应用抽屉和可停靠拆分工作区，形成项目实时控制台。
- [a2ui-render-in-dsh](https://github.com/baihui-ai/a2ui-render-in-dsh) — 在聊天中内联渲染交互式卡片，支持测验、表单、图表等并回传操作。
- [account-card](https://github.com/picoaide/picoaide-harness/tree/HEAD/packages/client/account-card) — 在客户端界面中显示账户信息。
- [acp-app](https://github.com/ChisaAlter/Deepseek-Harness-Desktop/tree/HEAD/vendor/deepseek-harness/packages/bundle/acp-app) — 为 DeepSeek Harness 提供可定制主题和背景图的桌面外壳。
- [acp-app](https://github.com/