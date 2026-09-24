# 🧠 Consensus Pipeline

<p align="center">
  <img src="banner.png" alt="Consensus Pipeline" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

> **Multi-agent debate framework for academic research.**
> Instead of one AI writing a literature review for you — an AI team interviews you, debates each claim, reaches consensus with per-claim confidence scores, and verifies every citation against the source abstracts.

📖 [中文文档](README_CN.md) · 📦 [GitHub Releases](https://github.com/fangqian616/consensus-pipeline/releases) · 🔗 [Related project: Multivest](https://github.com/fangqian616/multivest)

---

## ⚡ Quick Start

Pick one of three paths (start with 1 or 2):

**🚀 1. One-shot installer (fastest)**

```bash
# Windows PowerShell
irm https://github.com/fangqian616/consensus-pipeline/raw/main/install.ps1 | iex
# macOS / Linux
curl -fsSL https://github.com/fangqian616/consensus-pipeline/raw/main/install.sh | bash
```

One command clones + installs deps + prints your MCP config.

**🤖 2. DSH plugin (AI-driven, recommended)**

```bash
git clone --depth 1 https://github.com/fangqian616/consensus-pipeline.git
npx -p @deepseek-ai/dsh dsh plugin --profile web add file:./consensus-pipeline/dsh-plugin
```

Then tell DSH "共识管线开始需求调研" — it runs the requirement interview → department config → multi-round debate → confidence-annotated report. The 📊 控制台 floating button (bottom-right) shows live progress, atomic verification, and full-text upload.

**🖥️ 3. Streamlit / CLI (manual)**

```bash
git clone https://github.com/fangqian616/consensus-pipeline.git
cd consensus-pipeline
pip install -r requirements.txt

# Set the key (export on Linux/macOS, $env: on PowerShell)
export DEEPSEEK_API_KEY="sk-your-key-here"

streamlit run app.py                              # web UI, browser opens
python run_pipeline_v2.py --topic "Your Topic"    # headless CLI
```

A full run is an offline batch job — start it and let it run in the background, no need to watch. Full details on all three paths (MCP config, full-text upload, custom endpoints) → [📖 Usage](#-usage)

---

## ❓ Why Not Just Ask ChatGPT?

A single LLM produces confident-sounding answers with no cross-validation — hallucinations slip through, conflicting perspectives get flattened, and you can't tell which conclusions are solid vs. speculative.

Consensus Pipeline replaces one-shot generation with **structured multi-agent debate as a quality gate**: every claim is challenged by independent "departments," contradictions are surfaced explicitly, and final conclusions carry **confidence annotations** (e.g., "42/77 papers, high confidence").

Think of it as built-in peer review — not a single author, but an adversarial committee.

---

## 📸 What It Looks Like

### Step 1: Requirement Interview
The pipeline starts by interviewing you — an AI agent asks clarifying questions to understand your research scope, constraints, and goals.

<img src="examples/01_requirement_interview.png" alt="Requirement Interview" width="80%">

### Step 2: Smart Department Configuration
Based on your topic, the AI auto-generates 10+ specialized debate departments with multiple debaters per department. Each debater argues from a different methodological perspective.

<img src="examples/04_department_config.png" alt="Department Configuration" width="80%">

### Step 3: Multi-Round Debate
Watch debaters argue in real-time. Each round, debaters present their position, challenge others' assumptions, and refine their arguments. The pipeline runs 3-8 rounds per department (default), stopping early once debaters converge via dynamic termination.

<img src="examples/03_debate_content.png" alt="Debate Content" width="80%">

### Step 4: Structured Output
Debate results are structured into JSON with clear roles, positions, and consensus points — ready for report generation.

<img src="examples/02_structured_output.png" alt="Structured Output" width="80%">

### Step 5: Report with Confidence Annotations
The final report includes per-claim confidence scores, methodology comparison matrices, and verified citations. Every conclusion tells you how many papers support it.

Full example report (148 papers, energy economics): see `examples/final_report.md`

### Bonus: Auto-Generated Code & References
The pipeline also generates runnable Python code for key methods and compiles a verified reference list.

<p float="left">
  <img src="examples/06_code_output.png" alt="Code Output" width="45%">
  <img src="examples/07_references.png" alt="References" width="45%">
</p>

### Example Output

Here's what a real report excerpt looks like — note the per-claim confidence annotations:

> **Deep learning methods dominate short-term energy load forecasting** *(42/77 papers, high confidence)*
>
> LSTM and Transformer-based models consistently outperform traditional ARIMA methods by 10-40% in MAE metrics across multiple benchmark datasets. However, the **methodology review department flagged** widespread data leakage concerns — several studies used overlapping train/test splits that inflated apparent accuracy gains.
>
> **Graph neural networks show emerging potential in energy network optimization** *(3/77 papers, low confidence — trend not established)*
>
> While GNNs demonstrate structural advantages for modeling grid topology, current evidence is limited to small-scale test networks (< 100 nodes). Cross-department validation rated this claim as "promising but insufficiently validated."

Each claim survives adversarial challenge from multiple AI agents before appearing in the report. Claims that can't be verified from available abstracts are explicitly separated rather than silently scored.

---

## 🎯 What It Does

Consensus Pipeline takes a research topic and produces a structured literature review through multi-agent debate.

**The pipeline in one sentence:** Search papers → 3-layer QC filter → 11 departments debate each claim → cross-department validation → generate report with confidence scores.

**Key difference from tools like Elicit/Consensus:** Those tools extract and summarize. This tool *debates*. Each finding has to survive adversarial challenge from multiple AI agents before it makes it into the report.

**Core capabilities:**
- 🔍 **Multi-source paper search** — OpenAlex + Semantic Scholar + arXiv, auto-deduplication
- 🏛️ **11-department multi-agent debate** — each department has 2-4 debaters arguing from different perspectives
- 📊 **Per-claim confidence annotation** — every conclusion tagged with evidence count (e.g., "42/77 papers, high confidence")
- ✅ **NLI citation verification** — every claim checked against source abstracts, unverifiable claims excluded from scoring
- 📄 **Structured report output** — Markdown + DOCX + PDF export, bilingual (CN/EN)

**Full feature list:**
- ✅ Multi-source paper search (OpenAlex + Semantic Scholar + arXiv)
- ✅ 3-layer QC: hard filter → LLM classify → importance tagging (219 → 77 papers, ~65% exclusion)
- ✅ 10-11 debate departments, each with 2-4 debaters arguing from different perspectives
- ✅ Multi-round debate with **dynamic termination** — stance quantification (CV) + Kendall's W agreement; debate stops early once debaters converge instead of running fixed rounds
- ✅ Cross-department validation (one department checks another's work)
- ✅ Per-claim confidence annotation (e.g., "42/77 papers, high confidence")
- ✅ NLI citation verification — per-claim verdicts (✅/⚠️/❌), with unverifiable claims (📖 needs-fulltext / 📭 title-only) explicitly excluded from the confidence score, not silently counted
- ✅ Citation-mismatch vs overstatement classification — when both abstract AND full text are neutral, the verifier tells you *why*: ⚠️ wrong-paper citation vs ✂️ overstated wording
- ✅ Full-text NLI 