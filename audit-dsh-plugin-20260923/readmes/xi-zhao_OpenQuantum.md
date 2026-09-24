<h1 align="center">
  <img src="./packages/openquantum-web-branding/assets/lockup.svg" width="430" alt="OpenQuantum" />
</h1>

<p align="center"><a href="./README.md">简体中文</a> · <a href="./docs/readme/README.en.md">English</a> · <a href="./docs/readme/README.ja.md">日本語</a> · <a href="./docs/readme/README.ko.md">한국어</a> · <a href="./docs/readme/README.es.md">Español</a> · <a href="./docs/readme/README.fr.md">Français</a> · <a href="./docs/readme/README.de.md">Deutsch</a> · <a href="./docs/readme/README.pt.md">Português</a> · <a href="./docs/readme/README.ru.md">Русский</a> · <a href="./docs/readme/README.ar.md">العربية</a></p>

<p align="center">
  <strong>让量子想法运行起来。</strong><br />
  <sub>开源量子 Agent 与应用平台</sub>
</p>

<p align="center">
  <a href="https://github.com/xi-zhao/openQuantum/actions/workflows/ci.yml"><img src="https://github.com/xi-zhao/openQuantum/actions/workflows/ci.yml/badge.svg" alt="CI status" /></a>
  <a href="./THIRD_PARTY_NOTICES.md"><img src="https://img.shields.io/badge/licenses-MIT%20%2B%20component%20licenses-111111.svg" alt="MIT 与组件许可证" /></a>
  <img src="https://img.shields.io/badge/Node.js-24%2B-3c873a.svg" alt="Node.js 24 or newer" />
</p>

OpenQuantum 把专业量子软件、研究方法与完整应用接到你的问题上。你可以用自然语言发起计算、检查工具返回的结果，也可以进入量子学习通准备课程，或把自己的算法与应用接进来。

**提出问题，运行计算，共创能力。** 从学习者的第一次实验，到研究者的方法比较，再到开发者的应用集成，都可以从已支持的任务开始。

<p align="center">
  <a href="#为什么选择-openquantum">为什么选择</a> ·
  <a href="#可以用它做什么">浏览能力</a> ·
  <a href="#快速开始">开始使用</a> ·
  <a href="#使用与结果">使用与结果</a> ·
  <a href="#把你的量子能力接进来">开发与扩展</a> ·
  <a href="#长期发展规划">路线与 RSI</a> ·
  <a href="#一起建设-openquantum">参与建设</a> ·
  <a href="#开源生态与致谢">开源生态</a>
</p>

<p align="center">
  <img src="./docs/images/openquantum-desktop-20260919.jpg" width="100%" alt="OpenQuantum Desktop 科研工作台：新会话、工作区与量子学习通入口" /><br />
  <sub>在科研工作台提出问题，查看工具调用，再带着结果继续探索。</sub>
</p>

<a id="为什么做-openquantum"></a>

## 为什么选择 OpenQuantum

**让人、AI 与开放生态共同创造量子能力。**

**我们不重造量子软件生态，而是让专业能力更容易被使用、组合和继续建设。** OpenQuantum 的工作，是把领域方法、Agent 执行和开放工具接到具体任务上；它的价值不必等到真实 QPU 取得优势才开始，本地计算、教学实验和方法验证也是实际用途。

### 从问题出发，调用专业能力

**让问题意识转化为探索能力。** 你不必先学会每套 SDK，才能开始一个已支持的任务：Skill 提供工作方法，Agent 调用专业 Tool，工作台保留输入与结果。我们希望减少反复配置、接口学习和流程搭建，让学习者能够动手，让研究者把更多精力放在提出假设、设计对照与判断结果上，而不是替代这些判断。

**让工具之间产生新的研究空间。** PyZX 电路优化、QCEC 等价性检查与噪声模拟，分别回答不同问题。把它们用于同一个研究目标，可以进一步追问“理想电路更简洁，含噪表现是否也更好”。我们持续建设这种有科学意义的组合：对齐模型、单位、位序和预算，理解方法何时适用、何时失效；接口接通本身不等于结论成立。各工具的当前范围见[计算与资源配置](docs/integrations/SCALABLE_BRIDGES.md)。

### 让一次研究，成为下一次的起点

**让一次工作留下可继承的经验。** 常用步骤、计算结果与适用的独立检查，为复核和后续使用提供基础。我们希望进一步积累带条件的方法比较与失败证据：不仅知道一次计算成功，也理解它为什么适用、何时应换一条路线。有依据的负结果同样有价值，但程序报错不等于科学反驳。完整科学验收目前按[相应能力的支持范围](#执行记录与科学验收)提供，经验整理也不等于系统已自动学习。

### 把你的方法，变成别人能用的能力

**让成果从“有人做出”走向“他人继续创造”。** 方法可以写成 Skill，计算程序可以接成 Tool，完整应用可以保留自己的界面和业务流程。研究者、教师、开发者与软硬件伙伴，可以从自己的专长出发贡献，而不必先重做整套平台。我们的目标不只是传播已有成果，也让它们进入新的课程、研究与应用；[量子学习通](#量子学习通)是现有应用入口之一。

**把选择权留给使用者和贡献者。** 开源实现与扩展接口允许你检查、修改和维护自己的组合；模型服务与计算后端分别配置，不把所有应用绑定到单一模型或设备。上游作者、许可证与贡献继续可见，研究数据是否共享由使用者决定。我们希望保留下来的不只是一个界面，而是能够随模型、算力与研究方向变化继续使用的专业方法。

一个人因此完成了原本难以开展的探索，一项方法因此进入新的问题，一个贡献者因此做出新的应用，都是平台值得积累的价值。下一步是让这些经验不仅帮助使用者，也帮助[改善下一轮研究的能力](#rsi)。

**[先运行一个任务](#快速开始)**　·　[把你的能力接进来](#把你的量子能力接进来)

<a id="openquantum-的核心能力"></a>
<a id="已集成的量子工具与能力"></a>

## 可以用它做什么

选择一个方向，告诉工作台你的问题、输入和希望检查的结果。OpenQuantum 的 Agent 按任务使用 Skill 中的方法，并调用相应 Tool 执行计算；量子学习通提供独立的教学界面。

[电路与量子信息](#电路与量子信息) · [基态、化学与优化](#基态化学与优化) · [误差缓解与量子纠错](#误差缓解与量子纠错) · [开放系统动力学](#开放系统动力学) · [实验模拟与硬件](#实验模拟与硬件) · [参考资料与选型](#参考资料与选型) · [量子学习通](#量子学习通)

本地计算可以从无需量子云账户的任务开始。真实硬件和付费服务按需配置；各方法的输入范围、准备条件与验证状态分别保留在详细目录中。

### 电路与量子信息

| 任务方向 | 可以发起的任务 | 可以查看的结果 |
| --- | --- | --- |
| 量子电路 | 分析或转换 OpenQASM / QPY 电路，比较转译，检查等价性，运行电路仿真 | 电路结构、转译结果、等价性检查、态矢或采样分布 |
| 电路优化与测量式计算 | 用 PyZX 做 ZX 重写与电路提取，用 Graphix 转换和模拟 MBQC 模式 | 优化前后电路与门数、资源图和测量模式；可选独立对照 |
| 电路优化与切割 | 用 Compact 优化门序列，用 QCut 切分电路并重建期望值 | 优化前后电路与独立等价对照；切割开销、实际采样量与可选未切割参考 |
| Clifford+T 噪声采样 | 用 Clifft 研究 T 门干涉、近 Clifford 电路与门后去极化噪声 | 最终位串频数、有限采样误差；小系统可附完整分布与密度矩阵参考 |
| 量子态与测量 | 审计密度矩阵与纠缠指标；模拟已知 product / GHZ 态的局域随机测量 | 状态指标与独立检查，子区纯度估计及有限样本误差 |

### 基态、化学与优化

| 任务方向 | 可以发起的任务 | 可以查看的结果 |
| --- | --- | --- |
| 基态求解与验证 | 提供二量子位实 Pauli Hamiltonian，在固定粒子扇区运行 VQE，并检查精确参考 | 能量、收敛轨迹、独立检查，以及完整流程中的科学验收报告 |
| 量子化学与多体基态 | 用 SQD 研究分子与活性空间，或用 TeNPy 计算 XYZ 自旋链基态 | SQD 能量与轨道占据，DMRG 能量、磁化、纠缠熵及收敛信息；可选精确参考 |
| 变分参数学习 | 对 Pauli Hamiltonian 训练 Flow-VQE，学习低能量电路参数 | Flow 参数学习与等评估预算随机搜索比较 |
| 激发态与核分类 | 用 OpenQARP VQD 搜索多个低能态，或用 cqlib 角度核训练 QSVM | 能量、残差、正交性与可选精确谱；独立测试集分类、解析核及经典基线 |
| 对称性与控制代数 | 用 Symmer 在指定对称性扇区降比特，用 PauLie 分析 Pauli 生成元 | 降维 Hamiltonian、Lie 代数分类与维数；可选能谱对照或闭包 |
| 组合优化 | 构建 QUBO，检查约束 penalty，运行经典求解或可选本地 QAOA | 优化解、约束检查与经典枚举复核 |

### 误差缓解与量子纠错

| 任务方向 | 可以发起的任务 | 可以查看的结果 |
| --- | --- | --- |
| 误差缓解 | 用 Mitiq 运行 ZNE、REM、PEC 或 CDR，比较相同采样预算下的原始与缓解结果 | 理想参考、经验偏差、方差和 RMSE，以及校准、训练与采样成本 |
| 量子纠错 | 用 Stim / PyMatching 运行 surface-code memory，用 Deltakit 构建矩形码片实验，或进行 BP+LSD 解码 | 实际含噪电路、固定 shots 的逻辑错误率与区间；LSD 的 syndrome 一致性检查 |

### 开放系统动力学

| 任务方向 | 可以发起的任务 | 可以查看的结果 |
| --- | --- | --- |
| 开放系统动力学 | 用 TJM 计算开放 Ising 链，用 Dynamiqs 扫描单量子位驱动与梯度，或用 OQuPy 研究环境记忆 | 观测量轨迹、独立参考、梯度以及时间步长与记忆截断信息 |

### 实验模拟与硬件

| 任务方向 | 可以发起的任务 | 可以查看的结果 |
| --- | --- | --- |
| 超导与原子实验 | 模拟调校流程、原生门约束、三能级 transmon 泄漏或小型里德堡原子链动力学 | 合成实验数据、动力学轨迹与图表 |
| 量子硬件接入 | 发现后端、检查拓扑与凭据；按需启用云任务查询、提交与取消 | 设备候选、使用条件；已启用任务接口的结果与状态 |

### 参考资料与选型

| 任务方向 | 可以发起的任务 | 可以查看的结果 |
| --- | --- | --- |
| 算法参考与工具选型 | 检索 Quantum-Practices 的 60 份算法指南、比较量子 SDK、复用研究步骤 | 固定版本的参考材料、适用假设与选型建议 |
| 公开设备基准 | 从 Metriq 的 410 条固定历史记录中按厂商、设备或基准类型查询 | 原始参数、指标、时间、来源与许可；保留模拟器标签 |

<a id="学习应用"></a>

<a id="openquantum-全景"></a>
<a id="产品体验"></a>

<a id="教学桌面与消息入口"></a>

<a id="学习与教学"></a>

### 量子学习通

把材料、课件与课堂放在一起，让学习者动手，也让教师组织自己的教学内容。

| 学习与教学场景 | 可用功能 |
| --- | --- |
| 准备材料 | 首页、课程库、材料附件、课程导入与 PPTX 导入 |
| 制作课程 | 建课预览、课件编辑器和 Pro 专业工作台 |
| 课堂学习 | 幻灯片、测验、互动问答与 PBL 项目式学习 |
| 继续学习 | 本机课程、任务、材料与服务端学习记录持久化，兼容旧版课堂迁移 |

课程建设目标是覆盖中学基础到前沿研究，按初级、中级、高级组织内容，允许按知识基础跨阶段学习。当前公开资源仍在整理，完整课程体系尚未制作和发布。应用装配、启动和本机持久化已有验证，真实在线 AI 建课、问答和编辑仍待完整验收。

Pro 教学任务使用上游应用自己的工具与记录，尚未自动接入科研工作台的量子工具。媒体、语音和搜索等可选能力需要对应服务配置。安装、备份、迁移与逐项验证见[量子学习通集成说明](docs/integrations/OPENMAIC.md)。

<p align="center">
  <img src="./docs/images/openquantum-learning-20260912.jpg" width="100%" alt="量子学习通：课程材料、课堂与课件编辑入口" />
</p>

[准备学习通并打开课堂](#量子学习通安装)。

<a id="在桌面和消息中使用"></a>
<a id="桌面与消息入口"></a>

### 桌面、消息与多语言

#### 桌面工作台

OpenQuantum 桌面端提供原生窗口、系统托盘、终端与通知，复用科研工作台的模型、量子 Skill、计算工具和执行记录。

提供 Mac（Apple Silicon / Intel）和 Windows 桌面安装包，也支持从源码构建。

[下载并安装桌面客户端](#桌面安装包) · [从源码启动桌面客户端](#桌面客户端)。

#### 消息入口

通过 CC Connect，可从微信、飞书、钉钉、Slack、Telegram、Discord 等渠道发起任务，复用工作台已有的 Skill、Tool 和执行记录。

<p align="center">
  <img src="./docs/images/openquantum-wechat-chat.jpg" width="380" alt="通过微信 ClawBot 与 OpenQuantum 对话的已有演示截图" /><br />
  <sub>微信渠道中的任务与回复示例。</sub>
</p>

[配置微信、飞书与其他消息渠道](#微信飞书与其他消息入口)。

#### 界面语言

在「设置 → 通用设置 → 语言」选择简体中文、英语、日语、韩语、西班牙语、法语、德语、葡萄牙语、俄语或阿拉伯语。选择会保存，学习通跟随工作台；阿拉伯语使用从右到左的阅读方向。

![OpenQuantum Desktop 实际界面的语言选择](docs/images/openquantum-languages-20260919.jpg)

界面语言不会改写已有对话、课程材料、用户 Skill 或工具输出。部分原生系统对话框在中英文之外使用英语回退。

## 快速开始

OpenQuantum 支持桌面安装包和源码运行，适合本机单用户使用。直接使用工作台可下载安装包；二次开发或使用源码主线能力可选择源码路径。

### 桌面安装包

从 [GitHub Release](https://github.com/xi-zhao/OpenQuantum/releases/latest) 下载 Mac（Apple Silicon / Intel）或 Windows 安装包。安装包内置 Node 和 uv，无需先配置源码构建环境；当前为未签名测试构建。按[安装说明](docs/DESKTOP_INSTALLERS.md)安装并启动后，继续[配置模型](#配置模型)。部分 Python 计算组件首次使用时仍需联网准备固定依赖，量子学习通等可选应用另有安装步骤。

本页能力目录描述源码 `main`。[v0.5.1 安装包](docs/releases/v0.5.1.md)不包含后续的[新增量子能力](docs/integrations/CANDIDATE_LIBRARIES.md)及 [9 月 22 日量子库更新](docs/releases/2026-09-22-quantum-upstream-update.md)，也不会随源码主线更新而自动升级。安装版使用独立数据目录，迁移与备份见[安装包说明](docs/DESKTOP_INSTALLERS.md#数据与升级)。

### 安装源码

先准备 Git、Node.js 24；Python 量子工具还需要 [uv / uvx](https://docs.astral.sh/uv/getting-started/installation/)。其他依赖按所选能力安装，例如 RandomMeas 需要 Julia 1.12.7。

```bash
git clone https://github.com/xi-zhao/openQuantum.git
cd openQuantum
npm ci
```

没有模型密钥也可以先运行[固定本地示例](#不需要模型密钥复算一个固定案例)。要通过 Agent 发起任务，继续选择工作台入口并配置模型。

### 选择工作台入口

从同一源码目录启动的 Web 与 Desktop 使用同一套模型配置、量子能力和执行记录，共用 `.openquantum/dsh` 中的本机状态。切