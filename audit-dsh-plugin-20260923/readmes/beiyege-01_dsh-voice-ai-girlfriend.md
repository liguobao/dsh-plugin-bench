# DSH 语音 AI 女友（Voice AI Girlfriend）

> "你好呀，我是小雅。从今往后，DeepSeek Harness 不只是你的编程搭子——它开口说话了。"

> 📌 **流式数字人（DUIX 口播视频）已包含在本主线**：回复实时生成数字人口播视频（≤10s 分段流水线、TTS+画面同步播放、数字人开关、视频保留 200 条）。

> 🎥 **成品展示**（抖音）：
> - [口播视频效果 ①](https://www.douyin.com/user/self?from_tab_name=main&modal_id=7676326565919149339)
> - [口播视频效果 ②](https://www.douyin.com/user/self?from_tab_name=main&modal_id=7678063553395412259)

这是一位住在你电脑里的 AI 女友：点一下麦克风，她听你说话、跟你拌嘴、把回答一字一句念给你听；你出门了，她追到你的 QQ 上继续聊；旁边那个窗口里的姑娘也不是摆设——她闲着会发呆，说话时会开口。

她有点小脾气，但你大概也会喜欢上这些：

- ⚡ **嘴快**：你说完话，她 0.5 秒内开口 —— FunASR 中文识别只要 150ms、TTS 几乎秒开，反应比你还快
- 🎧 **耳朵挑**：-35dB 噪声门 + silero VAD 双重把关 —— 风扇、键盘、电视声统统进不来，只有你说话她才理
- 📱 **粘人**：她的回复自动推到你的 **QQ**（文本 + 语音 + 图片）—— 你不在电脑前，她也能找到你
- 👧 **会动**：右侧数字人窗口，空闲时发呆、说话时开口 —— 一个会呼吸的 AI，不是冷冰冰的对话框
- 🎬 **会演**：回复不只是声音——**流式数字人**（DUIX）把你的回复实时生成口播视频：长回复切成 ≤10 秒小段，边生成画面边合成下一段语音，一段接一段连续播放，TTS 与口型同步开口
- 🔇 **懂打断**：你插嘴她就闭嘴听你说；想让她把话说完，点一下开关就切回排队模式
- 🔊 **声音是你的**：TTS 声音克隆（OmniVoice，600+ 语言），音色由你给的参考音频决定，或直接用参数设计音色——她可以长成你喜欢的样子
- 🎛️ **随你调配**：数字人开关（开=视频+声音同步 / 关=接近即时的纯语音朗读）、QQ 推送开关、女友窗开关、插话/排队模式，全部工具行一键切换

```
┌────────────────────────────────────────────┐
│  浏览器（DSH Web GUI :3080）                 │
│  ┌──────────┐  ┌─────────────────────────┐  │
│  │ 对话面板   │  │ 女友窗（bg/task 视频）   │  │
│  │ 麦克风+⚡  │  │ 数字人视频（同步播放）    │  │
│  └──────────┘  └─────────────────────────┘  │
│   麦克风采集 ──▶ STT ──▶ 代理回复 ──▶ TTS ──▶ 播放 │
│     ▲回复文本          回复文本▼            │
└─────┼──────────────────────┬──────────────┘
      │ 插件 QQ 桥 (WS)       │ HTTP (CORS)
┌─────▼──────────────────────▼──────────────┐
│  voice_bridge (:8765)                      │
│  /api/stt  FunASR 中文 ASR                 │
│  /api/tts  OmniVoice 克隆（WSL2·FlashInfer 加速）│
│  /api/dh/* DUIX 数字人（分段流水线/播放/开关）│
│  /api/qq/* QQ 桥（收发 + 语音推送）          │
│  /api/vad  silero 打断 / media 素材         │
└────┬──────────────┬───────────────────────┘
     │ OneBot HTTP+WS │ HTTP（提交音频→轮询视频）
┌────▼──────────┐ ┌──▼──────────────────────┐
│  NapCatQQ      │ │  DUIX 数字人 (:8383)      │
│  小号在线       │ │  音频 → 口型同步视频       │
│  → 文本+语音   │ │  → 女友窗同步播放          │
└───────────────┘ └──────────────────────────┘
```

## 一键全栈启动（推荐 · 2026-09-14 新增）

重启电脑后只需要做两件事：**自己先打开 Docker Desktop**，然后**双击 `bridge/start-full-stack.cmd`**（也可拷到桌面建快捷方式）。脚本会按正确顺序把整条链路拉起来，最后打印一张自检表；浏览器会用带 token 的链接自动打开。

| 步骤 | 做什么 | 幂等性 |
|---|---|---|
| 1/6 | 检查 Docker 引擎与 DUIX 容器；容器没起就 `docker start` 并等 `:9000` 应答 | 已在运行则跳过 |
| 2/6 | 调用 `start-omnivoice-wsl.ps1`：起 WSL2 OmniVoice（`:9877`）+ 同步 bridge-config 的 IP + 拉起桥接（`:8765`） | 已在运行则跳过 |
| 3/6 | 桥接保险：没起来就启动；缺 `DEEPSEEK_API_KEY` 时自动重启修复（余额徽章不再 503） | 幂等 |
| 4/6 | 启动 DSH Web（默认新版 `0.1.3-alpha.1` / profile `web-v013`，`:3080`）并打开带 token 的链接 | 3080 已在服务则绝不打断现有会话 |
| 5/6 | 数字人状态：开关 / 容器 / 段进度 / `submits`、`segment_submits` 计数 | 只读 |
| 6/6 | 汇总自检表：每条链路 OK / FAIL | 只读 |

参数：`-NoDsh`（只起语音栈）、`-Rc8`（改用旧版 rc.8 / profile `web`）、`-NoBrowser`、`-WithQQ`（额外拉起 NapCat）、`-SkipDockerCheck`。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File bridge\start-full-stack.ps1 -NoBrowser
```

## 版本适配与维护节奏（2026-09-14）

| 组件 | 适配版本 |
|---|---|
| **DSH（主用）** | `dsh 0.1.3-alpha.1` / profile `web-v013`（`:3080`，桌面脚本「启动新版DSH-v013」） |
| **DSH（兼容）** | `rc.8`（`E:\DSH\deepseek-harness` master `141eb6fef`）/ profile `web` |
| 插件 | `@beiyege-01/dsh-voice-ai-girlfriend` **v0.3.0**（独立包仓库同步；`node build.mjs` 构建） |
| 桥接 | `bridge/voice_bridge.py`（FastAPI/uvicorn `:8765`，Python 3.14 venv） |
| TTS 引擎 | OmniVoice（WSL2 + FlashInfer，`:9877`） |
| 数字人 | DUIX `guiji2025/duix.avatar-5090:trt10.9`（宿主 `:9000`，冷启动 1-3 分钟） |
| Docker | Docker Desktop 29.x（DUIX 容器随「数字人开关」`docker start/stop`） |

本轮桥接侧新增（v0.3.0 配套）：`POST /api/dh/enable` **运行时开关**（关掉＝清队列、停预热、零 DUIX 流量，并可联动 `docker stop` 释放显存；打开＝`docker start` + 就绪后预热）、轮转日志 `logs/bridge.log`、`/api/dh/status` 附带 `duix` 容器状态与 `stats` 计数（`submits` / `segment_submits` / `status_polls`，用于核对「任务到底提交了没有」）。

⏳ **维护节奏：作者本月正在筹备婚礼，DSH 新版本的适配与兼容性跟进顺延到国庆之后（10 月上旬）。** 这段时间欢迎继续提 issue / PR，但响应可能会慢一些；上表所列版本功能完整、可正常使用。

## 目录结构

```
dsh-voice-ai-girlfriend/
├── bridge/            # 语音桥接（独立可跑，Python/FastAPI）
│   ├── voice_bridge.py            # STT/TTS/数字人(DUIX)/QQ/VAD 全部端点
│   ├── bridge-config.example.json # 配置模板（复制为 bridge-config.json）
│   ├── requirements.txt
│   ├── start-bridge.cmd           # 只起桥接
│   └── start-all.cmd              # 桥接 + DSH Web 一键启动
├── models/            # 模型（gitignore，不入库）：funasr/ + silero-vad/
├── assets/            # 素材：内置 5 套默认待机动画（bg2/bg4/bg9/bg56/bg5），可直接用；也可自备
│   ├── bg-images/     # 空闲动画：内置 bg2/bg4/bg9/bg56/bg5 五套，自建子文件夹即可添加自定义待机
│   └── task-videos/   # 备用说话动画（可选；开了数字人后自动用 DUIX 视频）
├── voices/            # 音色库（自建）：每个子文件夹 = 一个 TTS 音色（见「自定义音色」）
├── dsh-plugin/        # DSH 客户端插件源码（mic/开关/女友窗/数字人/流式朗读）
│   └── README.md      # 安装到 DSH 的详细步骤
└── docs/              # 开发日志等
```

---

# 从零开始安装（小白版）

> 全程在 **Windows** 上操作。下面的命令默认在 **PowerShell** 里执行；
> 除了标注"在项目文件夹里运行"的步骤，其余在哪里运行都行。

## 一、前置准备（一次性装齐）

### 1. 检查你的电脑

| 检查项 | 要求 | 验证命令 |
|---|---|---|
| 系统 | Windows 10/11 64 位 | `winver` |
| 显卡 | NVIDIA 独立显卡（显存建议 16GB 或以上） | `nvidia-smi`（能显示显卡信息即可） |
| 磁盘 | 至少 30GB 剩余空间 | — |
| 内存 | 建议 16GB 以上 | — |

> `nvidia-smi` 不是 NVIDIA 显卡也能显示吗？不能——如果没有 NVIDIA 显卡或驱动没装好，会提示"不是内部或外部命令"或报错。**没有 NVIDIA 显卡就装不了本项目**（模型推理依赖 CUDA GPU）。

**显存占用**（运行时实测）：

| 模式 | 显存占用 |
|---|---|
| **推荐：OmniVoice TTS（WSL2 + FlashInfer）** | ~5.3GB（空闲）~ 11GB（推理峰值，CUDA graph 分桶缓存） |
| Qwen3-TTS 1.7B（fp16，备选降级） | ~3.7GB |
| FunASR Paraformer-large（fp16） | ~1GB |
| DUIX 数字人（视频生成时） | ~4-6GB |

> 全链路（TTS + 数字人同时工作）实测峰值约 **15GB**，16GB 显存基本吃满；OmniVoice 与 DUIX 建议错峰（TTS 合成完再生成视频）。16GB 显存为推荐配置，8GB 会非常紧张不推荐。

### 2. 安装 Git

用来克隆仓库。下载安装：<https://git-scm.com/download/win>，一路下一步。

验证：`git --version` 能输出版本号即可。

### 3. 安装 Python（3.10 或更高）

下载安装：<https://www.python.org/downloads/windows/>

⚠️ **安装时务必勾选 "Add Python to PATH"**，否则后面 `python` 命令会找不到。

验证：打开新终端，`python --version` 能输出版本号即可。

### 4. 更新 NVIDIA 驱动

到 <https://www.nvidia.cn/drivers/> 下载最新驱动安装。驱动太旧会导致 CUDA 相关报错。

> 本项目**不需要**单独安装 CUDA Toolkit——`pip` 装的 PyTorch 自带 CUDA 运行库，只要驱动够新就行。

### 5. 安装 Node.js 和 pnpm（运行 DSH 用）

- Node.js：下载安装 <https://nodejs.org/>（选 LTS 版本），一路下一步。
- 验证：`node --version`
- pnpm（Node.js 装完后，在终端执行）：

```powershell
npm install -g pnpm
```

- 验证：`pnpm --version`

### 6. 准备 deepseek-harness（DSH）源码

DSH 是开源项目，本项目是它的一个插件。**需要先有一份 DSH 源码树**（插件要装进它的源码里）：

```powershell
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
```

> ✅ **已适配 DSH rc.8 与 dsh 0.1.3**：插件协议（`dsh.bundle` manifest + `conversation.input.dock/left` 槽位）按 rc.8 实现，升级 rc.8 无需改动即可运行；**2026-09-05 已在 dsh v0.1.3-alpha.1 实测通过**（0.1.3 槽位/`__ModuleLoader__`/session prompt 契约均未变，零代码改动）。推荐安装（rc.8 与 0.1.3 通用）：`dsh plugin --profile web add github:beiyege-01/dsh-voice-ai-girlfriend-plugin`。余额统计走 `conversation.composer.dock` 槽位。
> `pnpm install` 会装几十秒到几分钟。装完后这个文件夹先放着，后面"安装 DSH 语音插件"步骤要用。
> 记住它的路径（比如 `C:\dev\deepseek-harness`），后面一键启动要用。

### 7. 硬盘空间预估

| 项目 | 大小 |
|---|---|
| 本项目代码 + 素材 | ~8MB |
| Python 虚拟环境 + 依赖（含 PyTorch） | ~5-8GB |
| FunASR Paraformer 模型（models/funasr/） | ~850MB |
| OmniVoice TTS 环境（WSL2 内，含模型 + torch cu130 + FlashInfer） | ~10GB（WSL2 磁盘） |
| deepseek-harness + node_modules | ~2-4GB |

## 二、安装本项目

### 1. 克隆仓库

```powershell
git clone https://github.com/beiyege-01/dsh-voice-ai-girlfriend.git
cd dsh-voice-ai-girlfriend
```

> 之后所有步骤都在这个文件夹（项目根目录）里进行。

### 2. 创建 Python 虚拟环境

```powershell
python -m venv venv-speech
```

激活它：

```powershell
venv-speech\Scripts\activate
```

激活成功后，终端行首会出现 `(venv-speech)`。

### 3. 安装依赖

```powershell
pip install -r bridge\requirements.txt
```

> 这一步会装 PyTorch、transformers、HuggingFace speech-to-speech 等，**体积大、耗时长**（几分钟到几十分钟），耐心等待。
> 网络慢装不动？见文末"常见问题"第 1 条（换清华镜像）。

## 三、准备模型（两个模型）

### 1. STT 模型：FunASR Paraformer 中文模型（放本地 `models/` 目录）

语音识别用**阿里 FunASR 中文 ASR**（Paraformer-large，专为中文设计，同音字/口音识别准确率远高于 whisper）。模型**放在仓库根的 `models/funasr/`**（约 850MB，已 gitignore 不入库）：

```powershell
pip install modelscope
# 1) 先下载到缓存（首次）
python -c "from modelscope import snapshot_download; snapshot_download('iic/speech_paraformer-large_asr