# ForkProbe：AI Skill 选型与试跑工具

<p align="center">
  <strong>别猜哪个 AI Skill 有用，直接并排看结果。</strong>
</p>

<p align="center">
  <a href="https://jayden-x-l.github.io/forkprobe/?lang=zh">发布页</a>
  ·
  <a href="./README.en.md">English README</a>
  ·
  <a href="https://jayden-x-l.github.io/forkprobe/downloads/forkprobe-skill.zip">下载 skill zip</a>
  ·
  <a href="#deepseek-harness-原生插件">安装 DSH 插件</a>
</p>

<p align="center">
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-111827">
  <img alt="Version v1.1" src="https://img.shields.io/badge/version-v1.1-2563eb">
  <img alt="Local first reports" src="https://img.shields.io/badge/report-local--first-0f9f8f">
  <img alt="Agent skill selector" src="https://img.shields.io/badge/agent-skill%20selector-2563eb">
  <a href="https://github.com/deepseek-ai/deepseek-harness"><img alt="DeepSeek Harness supported" src="https://img.shields.io/badge/harness-DeepSeek-0f9f8f"></a>
  <a href="https://github.com/topics/dsh-plugin"><img alt="DSH plugin community" src="https://img.shields.io/badge/community-dsh--plugin-2563eb"></a>
  <a href="https://github.com/openai/codex"><img alt="Built with OpenAI Codex" src="https://img.shields.io/badge/built%20with-OpenAI%20Codex-111827"></a>
</p>

ForkProbe 是一个 AI Skill 选型与试跑工具。它会把同一个任务交给模型本身和多个候选 skill，并排试跑，生成本地 HTML report，让你看到真实输出之后再选择 winner。

**v1.1 新增图片提示词 / 风格方向比较：** ForkProbe 现在可以比较 image prompt / style pipelines。每条候选先生成 `prompt.md`、`style-card.md`、`composition.md`、`negative-prompt.md` 和 `render-notes.md`，不在 runner 内调用图片 API；在 Codex 且宿主具备图片生成能力时，可根据本地 `render-queue.json` 做可选渲染验证，其他 Agent 可用用户外部渲染后回填 `rendered.png`。

选定 winner 后，Report 的“继续”按钮会同时保存本地 handoff，并让 Agent 沿胜出 Skill 继续任务。用户可以在同一区域选择是否匿名分享本次 Skill 选择，为未来的社区推荐先验积累样本。

当网络上的 skill 越来越多时，问题不再是“有没有 skill”，而是“当前任务到底该用哪个 skill”。ForkProbe 的目标很直接：先把结果摊开，再让 Agent 沿着你选中的路径继续工作。

## 什么时候该用 ForkProbe

- 你不确定当前任务该用哪个 skill，想先看真实输出再决定。
- 你想比较 baseline 和多个 skill，而不是只相信 skill 的描述。
- 你的交付物是 PPTX、科研 figure package、调研报告、图片 prompt/style package、可运行网页或视频成片，需要看文件、预览和 QA。
- 你想从本机已安装 Skill、EverMind Skill Hub、GitHub 或 BYO 路径中找到候选，再做一次小规模试跑。
- 不适合简单确定性任务：如果答案或工具路径已经很明确，直接执行会更快。

## 它怎么工作

```mermaid
flowchart LR
  A["你的任务"] --> B["候选 skills / pipelines"]
  B --> C["并行试跑"]
  C --> D["本地 report"]
  D --> E["AI 评审建议"]
  E --> F["你选择 winner"]
  F --> G["Continuation handoff"]
```

ForkProbe 把 skill 选择变成一个可观察的流程：

1. 从 curated 目录、本机已安装 Skill、EverMind Skill Hub、GitHub 和 BYO 路径中推荐少量候选 skill 或 artifact pipeline。
2. 用同一份输入跑 baseline 和多个候选。
3. 展示每一路完整输出、耗时、token 估算、文件预览和 AI 评审建议。
4. 由你选择 winner。
5. 生成 continuation handoff，让 Agent 继续执行正式任务。

## 一句话触发

你不需要记命令。直接对 Agent 说：

```text
先帮我比较几个 skill，看看哪个更适合当前任务。
```

或者更明确一点：

```text
请用 forkprobe 推荐候选，等我确认后再并排执行并生成 report，让我选择 winner。
```

英文触发：

```text
Compare a few skills first and see which one fits the current task better.
```

## 能力矩阵与候选推荐

候选推荐严格跟当前 README 能力矩阵对齐。`baseline` 表示不使用额外 skill 的参照组；`+ presentations`、`+ Python/SVG renderer` 表示策略 skill 需要搭配生成器形成完整成品 pipeline。外部 GitHub 候选进入执行前仍建议检查 license、依赖和最终产物路径。

| 场景 | 状态 | Report 里看到什么 | 推荐候选 |
|---|---|---|---|
| 学术润色与 SCI 写作 | 已支持 | 多版本文本、AI 评审、winner 选择 | `baseline`, `research-paper-writing-skills`, `paper-writer-skill`, [`nature-polishing`](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-polishing), `humanizer`, `academic-humanizer` |
| 自然化与风格改写 / 去 AI 味写作 | 已支持 | 不同风格稿件并排比较 | `baseline`, `writing-anti-ai`, [`Humanizer-zh`](https://github.com/op7418/Humanizer-zh), [`humanizer`](https://github.com/blader/humanizer), [`stop-slop`](https://github.com/hardikpandya/stop-slop), [`avoid-ai-writing`](https://github.com/conorbronsdon/avoid-ai-writing), [`remove-ai-flavor-writing-skill`](https://github.com/B1lli/remove-ai-flavor-writing-skill) |
| 审稿回复与投稿材料 | 已支持 | 回复草稿、结构、语气对比 | `baseline`, [`nature-response`](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-response), `paper-writer-skill`, `writing-anti-ai`, `research-paper-writing-skills` |
| PPTX 成品生成 | 已支持 | 可打开的 PPTX、预览图、候选说明 | `baseline + presentations`, [`nature-paper2ppt`](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-paper2ppt) `+ presentations`, [`academic-pptx-skill`](https://github.com/Gabberflast/academic-pptx-skill) `+ presentations`, [`ppt-master`](https://github.com/hugohe3/ppt-master), [`md-slides`](https://github.com/zl190/md-slides) |
| 论文作图 / 科研绘图 | 已支持 | PNG 预览、SVG/PDF/TIFF、代码、caption、QA | `baseline-python-figure`, [`scientific-visualization`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization) `+ Python/SVG renderer`, [`nature-figure`](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure) `+ Python/SVG renderer`, `plot-code-python`, `schematic-svg`, `graphical-abstract-svg` |
| 调研报告 / Research report | 已支持 | 报告预览、sources.json、evidence table、claim checks、limitations、AI 评审 | `baseline-research-report`, `source-first-research`, `analyst-style-report`, `evidence-table-report`, `company-research-report`, [`user-research-cookiy`](https://github.com/cookiy-ai/user-research-skill) `+ report package` |
| 图片提示词 / 风格方向比较 | 已支持 | Prompt、风格卡、构图说明、负面约束、可选图片预览、候选说明 | `baseline-image-prompt`, `creative-director-prompt`, `style-system-prompt`, `prompt-as-code`, `reference-to-style`, `ecommerce-product-prompt`, `poster-key-visual-prompt`, `social-cover-prompt`, `ppt-visual-prompt` |
| 网页 / HTML 制作比较 | 已支持 | 可运行页面链接、桌面/移动端截图、QA、源码、AI 评审 | `baseline-web`, [`Anthropic frontend-design`](https://github.com/anthropics/skills/tree/main/skills/frontend-design), [`Hallmark`](https://github.com/Nutlope/hallmark), [`web-artifacts-builder`](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder), [`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [`web-design-engineer`](https://github.com/ConardLi/garden-skills/tree/main/skills/web-design-engineer), [`baoyu-design`](https://github.com/JimLiu/baoyu-design) |
| 产品宣传片成品比较 | 已支持 | MP4 播放、封面、字幕、脚本、分镜、源码、媒体 QA、AI 评审 | `baseline-remotion-agent`, [`HyperFrames product-launch-video`](https://github.com/heygen-com/hyperframes), [`video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft) |
| 动效视频成品比较 | 已支持 | MP4 播放、动效规格、源码、时长/分辨率、媒体 QA、AI 评审 | `baseline-remotion-motion`, [`HyperFrames motion-graphics`](https://github.com/heygen-com/hyperframes), [`Remotion Bits`](https://github.com/av/remotion-bits) |
| 口播粗剪比较 | 已支持 | 粗剪 MP4、字幕、转写稿、剪辑清单/时间线、压缩时长、媒体 QA | [`auto-editor`](https://github.com/WyattBlue/auto-editor), [`video-editing-skill`](https://github.com/maxazure/video-editing-skill), [`video-use`](https://github.com/browser-use/video-use) `cut-only`, [`chengfeng-videocut`](https://github.com/Agentchengfeng/chengfeng-videocut-skills)（实验） |

## 七种工作模式

### 1. Text comparison

适合学术润色、自然化改写、审稿回复、投稿材料、PPT 方案/大纲等文本产物。

```bash
python3 scripts/compare.py \
  --input /tmp/forkprobe-input.txt \
  --skill baseline \
  --skill writing-anti-ai \
  --skill humanizer-zh \
  --skill remove-ai-flavor-writing-skill \
  --judge \
  --output /tmp/forkprobe-report.html
```

### 2. PPTX artifact comparison

如果用户目标是“做一个 PPT”或“生成 PPTX”，ForkProbe 会倾向比较成品生成 pipeline，而不是只比较文字大纲。策略 skill 必须搭配 `presentations` 或 `pptx` 这类生成器，完整 pipeline 才进入成品对比。

典型 shortlist：

- `baseline + presentations`
- `academic-pptx-skill + presentations`
- `nature-paper2ppt + presentations`
- `ppt-master`
- `md-slides`

生成每条 pipeline 的 PPTX 后，用 artifact report 展示文件链接、关键页预览和 AI 评审：

```bash
python3 scripts/render_artifact_report.py \
  --manifest /tmp/forkprobe-ppt-artifacts.json \
  --output /tmp/forkprobe-ppt-report.html
```

### 3. Figure artifact comparison

如果目标是论文作图、科研绘图、机制图、数据图或 graphical abstract，ForkProbe 会比较 figure 生成 pipeline。每条候选路径会生成一个 figure package，用 report 展示预览、源文件、caption 和 QA。

```bash
python3 scripts/figure_artifact.py \
  --input /tmp/forkprobe-figure-task.txt \
  --pipeline baseline-python-figure \
  --pipeline nature-figure-python \
  --pipeline plot-code-python \
  --skill-source 'https://github.com/K-Dense-AI/s