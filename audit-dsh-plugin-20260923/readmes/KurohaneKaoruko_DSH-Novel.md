# DSH-Novel · 小说写作工作台

> 一个仓库，两种用法：**DSH-Novel 桌面端**（Flutter，基于 DeepSeek Harness 内核的小说工作台）与 **novelist 智能体预设**（独立安装到任意 DSH 环境）。

---

## DSH-Novel 桌面端

基于 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（dsh）的定制桌面客户端，专为小说作者优化：

- **七位写作智能体，一种文风一位**：通用「小说助手」+ 热血爽文 / 甜宠言情 / 悬疑诡秘 / 仙侠武侠 / 科幻末世 / 轻小说六种风格。人设可在应用内查看、修改、重装（对新会话生效）。
- **全套方法论 Skill 内置**：正文铁律与去 AI 味（novel-prose-standards）、AI 高频词分级词库、前文衔接、大纲细纲、场景对话技法、六维评阅、工程约定——随智能体预置，可在「技能」页浏览与编辑。
- **写作工作台**：
  - **写作**：新书向导（书名 + 目录 + 风格）、最近会话恢复、流式对话、工具调用卡片、权限请求一键应答、模型切换；
  - **文件**：作品目录树、新建/重命名/删除、Markdown 阅览（中文阅读排版）、文本编辑（字数统计）；
  - **智能体**：预设管理（查看人设 / 改人设 / 重装内置版）；
  - **技能**：按预设浏览 SKILL.md、在线编辑；
  - **设置**：DeepSeek API Key（写入本机 DSH_HOME）、内核信息与日志。
- **架构**：Flutter UI（纯 Dart，零原生插件）↔ **ACP stdio**（Agent Client Protocol v1）↔ 钉住版本的 dsh 内核子进程。内核运行时、七位智能体、全部 skill 随应用打包，开箱即用；应用数据与预设放在独立的 `~/.dsh-novel`，不动你现有的 DSH 环境。
- **多平台**：Windows / macOS / Linux，CI 自动构建打包。

下载与安装见 **[DOWNLOAD.md](DOWNLOAD.md)**；本地构建见 **[BUILD.md](BUILD.md)**。

## novelist 智能体预设（独立使用）

「小说助手」Agent 预设——**7 个方法论 skill + 7 个零模型调用工具**——保持独立可用：把 `novelist/` 整目录复制到 `~/.dsh/.agent-presets/novelist`（详见 [INSTALL.md](INSTALL.md)），任意 DeepSeek Harness 环境新建会话选择「小说助手」即可开始写作。与桌面端互不影响。

### 7 个方法论 skill（按需加载）

| skill | 何时加载 |
| --- | --- |
| `novel-prose-standards` | 写/改/润色/翻译/去AI味任何正文——正文铁律 + 直出即净生成时干预 + 各任务流程 |
| `novel-ai-lexicon` | AI 高频词分级词库（约 200 条）：一级套路模板出现即改写、二级高频滥用限频、句式模板、白名单防误伤 |
| `novel-continuity` | 写前必查清单、前文衔接三锚点、归档回填、剧情漏洞排查 |
| `novel-plotting` | 总纲/卷纲/细纲/章节规划/情节推演/灵感/书名简介包装，含标准细纲模板与节奏量化标准 |
| `novel-craft` | 场景三拍、对话技法、打脸四拍、情绪曲线、角色设计与采访 |
| `novel-analysis` | 小说分析/拆书/评阅（六维评分）/模拟读者团/合规体检/起名 |
| `novel-project` | 工程目录约定、人物卡/设定集/文风卡建档模板、归档三件套格式、Obsidian 工作流 |

### 7 个工具（零模型调用）

| 工具 | 职责 |
| --- | --- |
| `novel_lint` | AI 味确定性检查：标点纪律、禁用词、副词/极端词频次、句长均匀度、连续同句式、论文腔等 20 项规则，纯代码秒回 |
| `novel_check` | 名词一致性核对：自动构建名词档案，找出正文里反复出现却未建档的高频词 |
| `novel_briefing` | 写前材料组装：前 10 章结尾、上一章结尾、人物卡、伏笔清单、时间线、文风卡 |
| `novel_archive` | 归档三件套落盘：伏笔清单覆盖、时间线追加、归档记录写入；表格式不合格直接拒收 |
| `novel_project` | 工程文件操作：初始化目录、保存章节（内置 lint 质量门禁）、统计进度、整理双链索引 |
| `novel_import` | 旧稿分章导入：按「第X章」标记自动拆分落盘 |
| `novel_scan_book` | 体检材料组装：抽样选章，汇总工程材料 |

长篇质量机制（前文强制参考 / 设定必须有出处 / 文风卡 / 直出即净 / 保存门禁 / 归档三件套等）见原 README 与各 SKILL.md。

## 仓库结构

```
DSH-Novel/
├── README / LICENSE / BUILD / DOWNLOAD / INSTALL   # 文档
├── novelist/               # 纯插件：基准智能体预设（独立可用，原样保留）
├── app/                    # 软件端（桌面与未来的移动端同码）
│   ├── pubspec.yaml + lib/ + test/    # Flutter 工程本体
│   ├── agents/
│   │   ├── styles.yml      # 风格定义（单一事实源）
│   │   └── manifest.json + novelist/ + novelist-*/  # 生成库（npm run agents）
│   ├── kernel/             # 钉住版本的 dsh 内核
│   ├── scripts/            # 生成/安装/打包/验证工具链
│   └── package.json        # node 工具链
└── .github/workflows/build.yml    # 自动构建 + 发布
```

改风格人设/新增风格：编辑 app/agents/styles.yml → 在 app/ 下 npm run agents → 桌面端「设置 → 重新同步内置智能体」。

## 参考来源与致谢

- **[chinese-webnovel-skills（网文工坊）](https://github.com/tance-mang/chinese-webnovel-skills)**（MIT © tance-mang）——AI 味量化检测指标、深层人味方法论、打脸四拍、爽点升级链等思路的独立实现借鉴。
- **[web-novel-writing-skill](https://github.com/XINGANLIU/web-novel-writing-skill)**（MIT © NovelForge AI Contributors）——「写前约束 → 写中引导 → 写后审查 → 长期记忆」四层防幻觉架构的印证。
- **星月写作社区公开讨论**——脑洞公式、毒点防火墙、开篇量化指标等社区方法论模式。
- **DeepSeek Harness**——内核与 ACP 协议（MIT）。

## 许可证

[MIT License](LICENSE) © 2026 KurohaneKaoruko。
