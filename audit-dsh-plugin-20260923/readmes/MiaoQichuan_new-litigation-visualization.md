<p align="center">
  <img src="assets/banner.png" width="100%" alt="新诉讼可视化 · New Litigation Visualization"/>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-3FB950" alt="License: MIT"/></a>
  <img src="https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white" alt="Python 3"/>
  <a href="https://github.com/MiaoQichuan/new-litigation-visualization/actions/workflows/checks.yml"><img src="https://github.com/MiaoQichuan/new-litigation-visualization/actions/workflows/checks.yml/badge.svg" alt="checks"/></a>
  <img src="https://img.shields.io/badge/Built%20with-Claude-D97757?logo=anthropic&logoColor=white" alt="Built with Claude"/>
  <img src="https://img.shields.io/badge/Claude-Skills-D97757?logo=anthropic&logoColor=white" alt="Claude Skills"/>
  <img src="https://img.shields.io/badge/DeepSeek%20Harness-supported-4D6BFE" alt="DeepSeek Harness supported"/>
  <img src="https://img.shields.io/badge/Skills-5%20modules-0F766E" alt="5 skills"/>
  <img src="https://img.shields.io/badge/A4%20%E6%89%93%E5%8D%B0-%E8%AE%BE%E8%AE%A1%E5%89%8D%E6%8F%90-0F766E" alt="A4 打印是设计前提"/>
  <img src="https://img.shields.io/badge/%E8%BE%93%E5%87%BA-%E6%A0%BC%E5%BC%8F%E5%8F%AF%E9%80%89%20%C2%B7%20%E4%BA%94%E7%A7%8D%E5%8F%AF%E7%BC%96%E8%BE%91-7C3AED" alt="格式可选 · 五种可编辑格式"/>
</p>

---

**Litigation visualization, made deterministic.** Five installable skills that turn case
files into court-ready figures and tables. The model only reads meaning; every coordinate,
size and character budget is computed by deterministic scripts from the physical size of an
A4 sheet. Text on a figure is always a subsequence of the source sentence, and every element
traces back to the document and sentence it came from. MIT licensed, no network calls, works
with any agent that reads `SKILL.md`.

## 为什么做这件事

**诉讼可视化的价值，法官与当事人都验证过。** 一页时间轴省下的是庭审上十分钟的口头梳理；
一张法律关系图让当事人第一次看懂自己案子的结构；一份大事记表让合议庭不必在几百页卷宗里
反复翻找。这些不是美工问题，是沟通效率问题。

**法律 AI 的难点不在会不会画，而在能不能交。** 大模型画图容易，问题是三条：改字（把
「不予支持」写成「予以支持」）、不可复现（同一份材料两次不一样）、不可追溯（图上一句话
问不出它出自哪一页）。法庭材料对这三条零容忍。

**这个项目的做法是把作图拆成两段。** 模型只做语义判断：哪一句是已经发生的事实、哪几句
属于同一件事、谁与谁成立何种关系。位置、尺寸、层数、每张卡片能写几个字，全部交给确定性
脚本，从 A4 纸的物理尺寸一路算到像素。难的那部分不在模型手里，所以同一份材料换谁跑、
跑几次，出来都是同一张图，换一个更弱的模型也一样。**画图不是把法律变轻佻，而是把思考
变透明。**

## 四条设计原则

| 原则 | 落点 |
| --- | --- |
| **确定性渲染** | 模型只出一份 JSON，几何全部由脚本算。布局可复现、可缓存、可逐字节比对 |
| **照录原文** | 图上每段文字必须是原句的子序列，只许删减、不许改写；改一个词都会在出图前被拦下 |
| **A4 是前提** | 版面从纸的物理尺寸算起，不是导出选项。插进 Word 直接能印，白描一档可交法院 |
| **判据先行** | 每条已修复的问题固化成守卫，且每条守卫都必须能失败：加守卫要先把代码改坏，确认它真报错 |

## 五个模块

| 模块 | 版本 | 回答什么问题 | 输入 | 交付物 |
| --- | --- | --- | --- | --- |
| **V1** [诉讼可视化重画](plugins/mqc-nlv/skills/mqc-litigation-visual-redraw/) | v1.1.0 | 这张图怎么画得能进卷宗 | 一张已有的图（手绘、截图、AI 生成、Mermaid），或一段纯文字 | SVG · PPTX（默认）；PNG · VSDX · drawio 可选 |
| **V2** [时间轴大师](plugins/mqc-nlv/skills/mqc-timeline-master/) | v2.1.0 | 案件经过是怎样的 | 判决书 · 起诉状 · 答辩状 · 合同 · 证据目录 · 流水 · 聊天记录（PDF、老式 .doc、扫描件、照片、口述） | 同上 + 溯源索引 |
| **V3** [法律关系图大师](plugins/mqc-nlv/skills/mqc-legal-relation-master/) | v1.0.0 | 谁与谁、就什么标的、成立何种关系 | 一批案件材料 | 同上 + 出处索引 |
| **V4** [大事记表大师](plugins/mqc-nlv/skills/mqc-chronicle-master/) | v1.0.0 | 什么时候发生了什么 | 一批案件材料 | 案件大事记 Word · Excel 母表 · A4 简表（默认）；简表 PDF/PNG 可选 |
| **V5** [庭审对抗图大师](plugins/mqc-nlv/skills/mqc-trial-confrontation-master/) | v1.0.0 | 谁主张什么、对方怎么抗辩、法院审查什么 | 起诉状 · 答辩状 · 证据目录 · 代理意见 | 分析表 Excel · 对抗图 SVG（默认）；PNG 可选 |

**两条线，一处交叠。**

- **三大主力（V1 到 V3）** 覆盖日常出图：把手上已有的图重画干净、把案件经过画成时间轴、
  把当事人与标的之间的关系画成一张网。
- **庭前三大法宝（V3 到 V5）** 覆盖开庭前必须回答的三个问题：结构（V3）、时序（V4）、
  争点（V5）。V4 出的案件事实底稿是另两件的上游，三者读同一份底稿，同一件事在三张图上
  指向同一个编号。
- **V3 同属两条线**，既是日常出图的主力，也是庭前准备的第一件。

### 各模块在做什么

**V1 诉讼可视化重画。** 先做源图预检：矢量原件与有文字层的 PDF 直接放行，位图与扫描件
会先说明代价再问你是否继续（读图慢、贵、易读错）。七种版式按判据自动落档，事件多到横向
排不下时自动改用 A4 竖版。三种风格：奇川风（当事人）、歸藏风（讲课与公众号）、白描（法院）。

**V2 时间轴大师。** 直接读材料：有文字层的 PDF、老式 .doc 一条命令读入，扫描件走读图三步。
逐句判定哪些是已经发生的事实，按四轮勾选收窄范围，再由代码算形态与每张卡的字数容量。
出图同时写溯源索引，图上每一项对得回材料的哪一句。

**V3 法律关系图大师。** 主体与客体并存的关系网，走线全部正交、判据 15 条（穿节点、共线
重叠、圆角方向、文字越出画布、图名被压、文字互相压……），不合格的布局在候选阶段就被换掉。

**V4 大事记表大师。** 一次出三件：Word 交付版（宋体加新罗马、页边距与列宽按规范定死）、
Excel 母表（律师在里面填争点）、A4 简表（呈报用）。事实行走封闭动词表，不合规的写法出表前
被拦。它同时生成案件事实底稿，供 V3 与 V5 复用。

**V5 庭审对抗图大师。** 按要件审判九步法与请求权基础，把案件推成左中右三栏：提出请求的
一方、法院审查、抗辩的一方，深红标出决定性要件。图与表同源，一致性由判据核验。

<p align="center">
  <img src="assets/modules.png" width="100%" alt="五个模块"/>
</p>

**装在哪都行。** 五个模块都是标准的 `SKILL.md` 目录，没有产品特定的胶水代码：Claude Code、
Codex、DeepSeek Harness、Cursor、Gemini CLI、Copilot、Cline、Aider 都装得上。同一份仓库，
不维护两套。

## 快速开始

Claude Code：

```
/plugin marketplace add MiaoQichuan/new-litigation-visualization
/plugin install mqc-nlv@mqc-nlv
```

装完跑一次环境自检，它逐项告诉你缺什么、缺了会退化成什么样（没有一项是装不上，
都是少一种格式）：

```bash
python3 plugins/mqc-nlv/skills/mqc-litigation-visual-redraw/scripts/doctor.py
```

然后把材料丢给 agent，用中文说一句要什么即可，例如：

```
用时间轴大师，把这份判决书画成案件经过时间轴，交当事人看
```

**DeepSeek Harness**：挂目录即可，不必构建（它的技能发现是扁平的，指到 `skills/`
这一层，会扫到下面每一个 `<模块名>/SKILL.md`）：

```yaml
skills:
  local:
    customSkillDirs:
      - "./new-litigation-visualization/plugins/mqc-nlv/skills"
```

dsh 的发现优先级（先命中先生效）：项目 `.dsh` → 项目 `.agents` → `customSkillDirs` →
用户 `.dsh` → 用户 `.agents`。它把 `allowed-tools` / `disallowed-tools` 当未知字段处理，
技能内的工具约束需要在 harness 层自行保证。

**其他 agent**：把模块目录放进它们各自的 skills 目录，`SKILL.md` 是通用格式。

### 环境与依赖

| 能力 | 需要什么 | 缺了会怎样 |
| --- | --- | --- |
| 出 SVG 与 PPTX | Python 3，零第三方依赖 | 不会缺 —— 这也是默认交付的两种 |
| 出 PNG | Inkscape / rsvg-convert / LibreOffice / resvg-js / Playwright 任一 | 跳过 PNG 并说明怎么补，其余格式照出 |
| 流程图与关系图定位 | graphviz 可选 | 没装时由内置分层排布算坐标，实测画布相差 2 像素 |
| Excel 母表与分析表 | openpyxl | 出表那一步开跑前就提示，不会跑到一半崩 |
| 大事记的 Word 交付版 | node 与 docx 包 | 改出同内容的 Markdown，Excel 与简表照出 |
| 读扫描件 | poppler 的 `pdftoppm` | 明说无法读图，不静默跳过 |

## 仓库结构

```
new-litigation-visualization/
├── assets/                                  仓库封面与模块图
├── .claude-plugin/marketplace.json          插件市场清单
├── .github/workflows/checks.yml             每次 push 与 PR 跑五个模块的回归
└── plugins/mqc-nlv/
    ├── .claude-plugin/plugin.json           插件清单（插件版本只在这里声明）
    └── skills/
        ├── mqc-litigation-visual-redraw/    V1 · 共享内核所在
        │   ├── SKILL.md                     技能主文档
        │   ├── references/                  规程与标准（含 5 KB 速查页 quick-map.md）
        │   ├── scripts/                     确定性渲染管线
        │   │   ├── render*.py               七种版式 + 纵向形态
        │   │   ├── export_{pptx,vsdx,drawio}.py   可编辑格式导出
        │   │   ├── source_check.py          源图预检（位图先说明代价）
        │   │   ├── layout_fallback.py       没有 graphviz 时的内置分层排布
        │   │   ├── raster_fallback.py       没有转图工具时的 resvg-js / Playwright
        │   │   └── checkpoint.py doctor.py  确认清单与环境自检
        │   └── schemas/ examples/ assets/ tests/
        ├── mqc-timeline-master/             V2
        │   ├── references/                  约束表（69 条编号约束，条条有实测数字）
        │   ├── scripts/                     四轮勾选 → 逐句判定 → 形态与容量 → 出图
        │   │   ├── read_source.py read_doc.py   材料读取（PDF 文字层 / 老式 .doc）
        │   │   ├── render_multiband.py render_vcolumns.py  横向多泳道 / 纵向
        │   │   └── pipeline.py              管线入口，含计时账
        │   └── docs/adr/ schemas/ examples/ assets/ tests/
        ├── mqc-legal-relation-master/       V3
        │   ├── scripts/                     布局求解 · 正交走线 · 15 条路线判据
        │   ├── assets/                      度序列查表（代码用，模型不必读）
        │   └── vendor/v1/                   单独分发时随包带的共享内核
        ├── mqc-chronicle-master/            V4
        │   ├── scripts/                     摄入 · 校验 · Word/Excel/简表
        │   └── references/ docs/adr/ examples/ tests/
        └── mqc-trial-confrontation-master/  V5
            ├── scripts/                     要件推演 · 三栏出图 · 光栅
            └── references/ examples/ tests/
```

**共享内核只有一份。** 几何、字体、换行、导出这些多模块共用的代码放在 V1，别的模块引用
它、不许各自分叉。单独分发时按各自约定随包带一份，并由守卫逐字节比对，防止两边走偏。

## 两个模块的细节

### V1 诉讼可视化重画

把一张凌乱、或者一眼「AI 味」的诉讼图，重画成克制、专业、可直接进诉讼材料的图，
源文件一并交给你，回头还能接着改。**律师只做两件事：上传原图，说一句提示词。**

<p align="center">
  <img src="plugins/mqc-nlv/skills/mqc-litigation-visual-redraw/assets/longform/how-it-works.png" width="820" alt="Skill 运行全过程"/>
</p>

### 三类七种布局

时间、流程、关系。诉讼里要画的东西基本