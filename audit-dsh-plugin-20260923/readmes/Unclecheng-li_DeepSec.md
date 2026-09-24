<div align="center">

<img src="https://github.com/user-attachments/assets/44859857-7122-40f7-812f-2c7f81515182" width="120" height="120" alt="DeepSec">

<h1>DeepSec</h1>

<p><strong>AI 安全攻防一体平台 — Shield 代码审计 + Spear 授权渗透测试</strong></p>

<p>抓出 AI 漏掉的。攻破别人攻不破的。</p>

<p>
  <a href="https://github.com/Unclecheng-li/DeepSec/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Unclecheng-li/DeepSec/ci.yml?branch=main&logo=github&label=CI" alt="CI"></a>
  <a href="https://github.com/Unclecheng-li/DeepSec/releases"><img src="https://img.shields.io/github/v/release/Unclecheng-li/DeepSec?display_name=tag&logo=github" alt="Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Unclecheng-li/DeepSec?color=blue" alt="License"></a>
  <a href="https://github.com/Unclecheng-li/DeepSec/stargazers"><img src="https://img.shields.io/github/stars/Unclecheng-li/DeepSec?style=social" alt="Stars"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Rust-ratatui-CE422B?logo=rust&logoColor=white" alt="Rust">
  <img src="https://img.shields.io/badge/VSCode-1.92+-007ACC?logo=visualstudiocode&logoColor=white" alt="VSCode">
  <img src="https://img.shields.io/badge/JetBrains-2025.2+-000000?logo=jetbrains&logoColor=white" alt="JetBrains">
</p>

**English version**: [`README_EN.md`](README_EN.md)

</div>

---

> ## 3 分钟快速上手
>
> 不想看长文档？**点这里 → [`docs/QUICKSTART.zh-CN.md`](docs/QUICKSTART.zh-CN.md)**（中文版）
>
> 下载 Release 里的 `deepsec-tui-windows.exe` → 双击 → 输入 `/shield scan 你的项目` → 2 秒看到漏洞。
> 不会用？仓库自带故意写满漏洞的示例文件 `demo/unsafe-ai-sample.ts`，扫它就能看到效果。

---

<div align="center">

**DeepSec TUI 终端工作台**


https://github.com/user-attachments/assets/2b041a72-4566-48f1-aca8-2c685c0a52cc


— Shield 扫描、Spear 渗透、实时动画

</div>

---

## DeepSec 是什么？

DeepSec 是由 VibeGuard 进化而来的 AI 安全平台，将 **Shield**（AI 代码安全审计）与 **Spear**（授权渗透测试引擎）统一到一套 CLI、一个 TUI 终端工作台和一组 IDE 插件中。

```
┌──────────────────────────────────────────────────────────┐
│                      DeepSec Platform                     │
│                                                          │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│   │ Shield   │  │  Spear   │  │   TUI    │  │   MCP   │ │
│   │ Code     │  │ Pentest  │  │ Terminal │  │ Server  │ │
│   │ Audit    │  │ Engine   │  │ Workbench│  │         │ │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘ │
│        │             │             │              │       │
│        └─────────────┴─────────────┴──────────────┘       │
│                          │                               │
│              ┌───────────┴───────────┐                   │
│              │   Unified Config      │                   │
│              │   ~/.deepsec/         │                   │
│              │   config.yaml         │                   │
│              └───────────────────────┘                   │
└──────────────────────────────────────────────────────────┘
         │                              │
   ┌─────┴─────┐                  ┌─────┴──────┐
   │  VSCode   │                  │  JetBrains │
   │  Plugin   │                  │   Plugin   │
   │  (TS/LSP) │                  │  (Kotlin)  │
   └───────────┘                  └────────────┘
```

### Shield — 代码安全审计

从实时正则到 LLM 语义分析的三层检测架构：

| 层 | 检测内容 | 速度 | 原理 |
|-------|---------|-------|--------|
| **L1** | 幻觉包、硬编码密钥、不安全配置、AI 错误模式 | < 50ms | 正则 + 熵分析 + 种子目录 |
| **L2** | SQL 注入、XSS、SSRF、路径穿越、命令注入 | < 2s | Tree-sitter WASM AST 分析 |
| **L3** | 缺失认证/限流/校验等语义漏洞 | < 5s | LLM（DeepSeek/Claude/OpenAI/Ollama）+ 本地启发式兜底 |

### Spear — 授权渗透测试

从 VulnClaw 迁移而来的端到端自动化渗透引擎：

- **Recon → Explore → Fact → Reflect → Report → PoC** 全流程自动化
- 40+ 内置技能包（nmap、dirsearch、subfinder、nuclei、sqlmap、ffuf、httpx、feroxbuster）
- 5 种角色（pentester、redteam、auditor、blueteam、ctf_player）
- 签名授权范围（Signed Scope），限时 + 审计日志
- 攻击链可视化，多格式报告（Markdown / SARIF / JSON / HTML）

### TUI — 终端工作台

基于 Rust + ratatui 构建的安全工作台，交互设计借鉴 DeepSeek-TUI：

- 三面板布局：工作区侧边栏 · 会话记录 · 漏洞检查器
- Plan / Agent / YOLO 模式切换
- 斜杠命令系统 + 命令历史回放
- Side-Git 快照（随时创建/恢复代码状态）
- 会话持久化（Ctrl+S 保存 / Ctrl+R 恢复）

---

## 快速开始

> **想 3 分钟跑起来？直接看 [`docs/QUICKSTART.zh-CN.md`](docs/QUICKSTART.zh-CN.md)（中文）** 或 [`docs/QUICKSTART.md`](docs/QUICKSTART.md)（English）——含"下载即用"的最快路径。

### 安装

```bash
# Python 核心 + CLI
pip install -e .

# Rust TUI（可选）
cargo build --manifest-path tui/Cargo.toml

# IDE 插件
# VSCode: 在项目根目录按 F5 启动 Extension Development Host
# JetBrains: cd jetbrains && ./gradlew buildPlugin
```

> **新手免编译路径**：直接去 [Releases](https://github.com/Unclecheng-li/DeepSec/releases) 下载 `deepsec-tui-windows.exe` / `deepsec-tui-linux` / `deepsec-0.2.0-py3-none-any.whl`，不用装任何编译环境。

### Shield 扫描

```bash
# 扫描项目（L1 + L2，离线）
deepsec shield scan ./src

# 开启 L3 语义分析（需要 LLM API Key）
DEEPSEEK_API_KEY=... deepsec shield scan ./src --layer l3

# 输出 SARIF 报告
deepsec shield scan . --format sarif --output deepsec.sarif

# 流式输出（供 TUI 消费）
deepsec shield scan . --stream

# Agent 配置审计
deepsec shield agent-audit ./agent-config

# 供应链安全检查
deepsec shield supply-chain check .
```

### Spear 渗透测试

```bash
# 1. （可选）维护授权白名单 — 推荐通过 TUI /scope 命令
#    或手动编辑 ~/.deepsec/targets/scope.json 的 targets 字段
#    如需强签名校验：export DEEPSEC_SCOPE_SIGNING_KEY=... && deepsec scope sign ./scope.json

# 2. 运行渗透测试（目标必须在白名单内）
deepsec spear run https://authorized-target.example --authorized ./scope.json

# 3. 仅侦察阶段
deepsec spear recon https://authorized-target.example --authorized ./scope.json

# 4. 列出角色和工具
deepsec spear roles
deepsec spear tools --role pentester
```

### TUI 终端工作台

```bash
# 启动终端工作台
deepsec tui

# 或直接运行 Rust 原生二进制
./tui/target/debug/deepsec-tui-native
```

内置 TUI 斜杠命令：

| 命令 | 说明 |
|---------|-------------|
| `/shield scan` | 运行 Shield 扫描 |
| `/spear run` | 运行 Spear 渗透（需白名单授权） |
| `/spear recon` | 运行侦察阶段 |
| `/scope add <target>` | 将目标加入授权白名单 |
| `/scope remove <target>` | 从白名单移除目标 |
| `/scope list` | 查看当前白名单 |
| `/report` | 生成报告 |
| `/plan` | 切换到 Plan 模式 |
| `/agent` | 切换到 Agent 模式 |
| `/yolo` | 切换到 YOLO 模式（全自动） |
| `/clear` | 清空会话 |
| `/help` | 帮助 |

#### TUI 实操：添加白名单并启动渗透测试

DeepSec TUI 内置授权白名单管理 — 无需手动编辑 `scope.json` 或处理 HMAC 签名密钥。

**1. 启动 TUI**

```bash
deepsec tui
```

**2. 将目标加入白名单**

在 TUI 命令行（底部 `> ` 提示符）输入：

```
/scope add https://your-authorized-domain.com
```

- 目标会被规范化（scheme+host 转小写、去尾部 `/`）并去重，与后端授权匹配规则一致。
- 未指定 `--file` 时，默认取最近一次 `/spear run --authorized <file>` 解析出的绝对路径；若尚未运行过 spear，则回退到 `~/.deepsec/targets/scope.json`。
- 查看当前白名单：`/scope list`
- 移除目标：`/scope remove https://your-authorized-domain.com`

**3. 启动渗透测试**

```
/spear run https://your-authorized-domain.com --authorized ~/.deepsec/targets/scope.json
```

然后：

- 按 `Tab` 在 **Plan / Agent / YOLO** 执行模式间切换（YOLO 为全自动，无需逐步确认）。
- Plan 模式只读，无法直接武装 Spear — 需先切到 Agent 或 YOLO。
- 按 `Y` 确认授权校验并启动；按 `Esc` 取消。
- 运行中按 `Ctrl+C` 可**中止当前任务**（TUI 保持打开）；空闲时按 `Ctrl+C` 退出 TUI。

**4. 安全边界**

- 白名单之外的目标一律拒绝（`target ... is not present in the scope manifest`）。
- 私有/回环/非公网地址仍被阻止，防止打到内网。
- 白名单只接受你**拥有或已书面授权**的资产；任何不在 `targets` 里的第三方生产域名都无法被攻击。

### Side-Git 快照

```bash
# 创建快照
deepsec snapshot create . --mode shield --description "before-refactor"

# 列出快照
deepsec snapshot list .

# 恢复快照
deepsec restore <snapshot-id>
```

---

## 截图

<div align="center">
<table>
<tr>
<td align="center"><b>实时诊断</b></td>
<td align="center"><b>悬停查看详情</b></td>
</tr>
<tr>
<td><img src="https://raw.githubusercontent.com/Unclecheng-li/DeepSec/main/media/demonstration/realtime-diagnostic.png" alt="Real-time diagnostics" width="400"></td>
<td><img src="https://raw.githubusercontent.com/Unclecheng-li/DeepSec/main/media/demonstration/hover-tooltip.png" alt="Hover tooltip" width="400"></td>
</tr>
<tr>
<td align="center"><b>Quick Fix 菜单</b></td>
<td align="center"><b>Problems 面板</b></td>
</tr>
<tr>
<td><img src="https://raw.githubusercontent.com/Unclecheng