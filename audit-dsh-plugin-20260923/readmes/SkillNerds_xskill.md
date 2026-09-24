<div align="center">

<img src="docs/assets/header.png" width="820" alt="xskill — 一人解决,全队复用">

<h3>让你的 coding agent 的技能,从每一次真实会话里自我进化——你只管写代码。</h3>

<p><em>跨会话、跨 agent、跨设备、跨同事。经验持续累积,技能不断生长。</em></p>

[![PyPI](https://img.shields.io/pypi/v/xskill.svg?style=flat-square&color=E07A5F&label=PyPI)](https://pypi.org/project/xskill/)
[![Python](https://img.shields.io/pypi/pyversions/xskill.svg?style=flat-square&color=4A90B8)](https://pypi.org/project/xskill/)
[![License](https://img.shields.io/badge/license-MIT-5B8C5A?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/SkillNerds/xskill?style=flat-square&color=F4805E)](https://github.com/SkillNerds/xskill/stargazers)
<br>
[![GitHub](https://img.shields.io/badge/code-SkillNerds%2Fxskill-243B45?style=flat-square&logo=github)](https://github.com/SkillNerds/xskill)
[![Paper](https://img.shields.io/badge/paper-PDF-8E44AD?style=flat-square&logo=readthedocs&logoColor=white)](paper/xskill_v4.pdf)
[![Live demo](https://img.shields.io/badge/demo-xskill.wiki-0E7C86?style=flat-square)](https://xskill.wiki/story/)
[![LINUX DO](https://img.shields.io/badge/LINUX%20DO-社区-FFB003?style=flat-square)](https://linux.do)

[English](README.en.md) · **简体中文**

<sub>📄 论文:<em>xskill: Team-Level Skill Distillation, Sharing, and Evolution for Coding Agents</em> · <a href="paper/xskill_v4.pdf">PDF(19 页)</a></sub>

<br>


</div>

* * *

## 为什么需要 xskill

```
“同事的coding agent已经做过的事情，你为什么不能直接拿来用？”
```

xskill是企业级的团队skill演进方案，支持轨迹自动蒸馏Skill，基于轨迹画像推送Skill，支持导入团队skillhub进行推荐，支持skill评价。

- **高手经验自动传递**： 一个人的解法自动到达全组，让最短路径不再壮志难酬。
- **跨Harness和设备共享进化**： Codex、Claude Code、Cursor IDE都会加入光荣的进化,齐心,协力。
- **支持专家修改Skill**： 觉得skill不完美？直接修改本地的skill，改动会被云端自动学习。
- **轨迹保持私有**： 会话在上传前已脱敏，秘钥密码和相关隐私不会被别人看到。
- **不让skill烂掉**： 自动评价skill，支持分析用户实际使用轨迹给出评价分并绘制不同**skill版本的得分趋势折线图**，大数据显微镜。

* * *

## 一人解决,全队复用

只要团队里有一个人在自己的会话里搞定了某个问题,这个解法就会变成一条技能——其他人的 agent 自动拿到。没人需要专门写文档。

<div align="center">
<img src="docs/assets/xs_multiplier.zh.svg" width="820" alt="一个人解决一次问题,xskill 把它蒸馏成一条技能,瞬间扩散到全队">
</div>

## 跨越每一个 agent 与设备——同一个技能库

笔记本上用 Claude Code、服务器上用 Codex、IDE 里用 Cursor。xskill 从它们全部收集脱敏后的轨迹,进化出**同一个共享技能库**,再把结果同步回你用的每一个 agent。

<div align="center">
<img src="docs/assets/xs_crosscontext.zh.svg" width="860" alt="多个 agent 和设备汇入同一个轨迹 watcher 和同一个进化技能库,再同步回所有 agent">
</div>

## 孤岛 → 集体进化

没有一个共享、自我改进的技能库,每个开发者都在孤岛里重复解决同样的问题。xskill 把这些被浪费的、隔离的努力,变成可以复利累积的共享经验。

<div align="center">
<img src="docs/assets/xs_silos_vs_collective.zh.svg" width="860" alt="左:开发者各自孤立地重复解决同一问题。右:开发者连到同一个进化的共享技能库。">
</div>

* * *

## 架构

<div align="center">
<img src="docs/assets/xs_architecture.zh.svg" width="900" alt="xskill 架构:agent 生态 → 轨迹 watcher → 原子拆分 → 技能路由 → 技能编辑 agent → canary 灰度 A/B → 技能仓库,并支持团队模式">
</div>

> [!NOTE]
> xskill全流程都是Agentic-Centric的管线。首先将轨迹按照内部意图拆分为子轨迹（轨迹原子），然后对轨迹原子进行聚类并分配到对应的skill，原子积攒足够后就会触发skill编辑产出新的skill版本。
不同的skill版本会在真实的用户流量上进行测试，用户体验分高的胜出作为主版本继续迭代，每一次改动都有版本、可回滚。细节见 [`docs/agent.md`](https://github.com/SkillNerds/xskill/blob/main/docs/agent.md)。

## 精度表现
xskill是一套无监督的skill蒸馏方案，其不需要构建数据集就可以完成进化。

目前版本的算法管线精度表现如下：

<p align="center">
  <sub><strong>Setup:</strong> <code>DeepSeek-V4-Flash</code> · <code>Claude Code</code> · <code>single</code> mode<br>
  <strong>Pipeline:</strong> SkillOpt built-in evaluation pipeline · Official data split</sub>
</p>

<table align="center">
  <thead>
    <tr>
      <th></th>
      <th align="right">Spreadsheet</th>
      <th align="right">ALFWorld</th>
      <th align="right">OfficeQA</th>
      <th align="right">Mean¹</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th align="left">XSkill</th>
      <td align="right"><strong>88.57</strong></td>
      <td align="right"><strong>84.33</strong></td>
      <td align="right"><strong>60.47</strong></td>
      <td align="right"><strong>77.79</strong></td>
    </tr>
    <tr>
      <th align="left">SkillOpt</th>
      <td align="right">87.86</td>
      <td align="right">77.61</td>
      <td align="right">51.16</td>
      <td align="right">72.21</td>
    </tr>
    <tr>
      <th align="left">Delta</th>
      <td align="right"><strong>+0.71</strong></td>
      <td align="right"><strong>+6.72</strong></td>
      <td align="right"><strong>+9.30</strong></td>
      <td align="right"><strong>+5.58</strong></td>
    </tr>
  </tbody>
</table>

<p align="center"><sub>¹ 表内数值为测试集通过率(%)，Mean 为三项基准的算术平均。Spreadsheet 与 ALFWorld 使用官方全量测试集，OfficeQA 使用官方划分的 1/4 子集。</sub></p>


在目前已完成的三项评测中，xskill 均高于 SkillOpt，平均分领先 5.58。

### Evaluation Setup

为了尽量还原真实的团队使用场景，评测环境通过 namespace 隔离部署了：

* 3 个独立的 `xskill-client`
* 1 个共享的 `xskill-server`
* 多个由 LLM 模拟的用户，负责与 Agent 进行 QA 交互

> [!IMPORTANT]
> XSkill 无需显式监督信号即可持续进化。
> SkillOpt 强依赖 ValSet 提供进化所需的监督信号。
> 在 ALFWorld 的 Epoch 2、3、4 中，ValSet 均出现精度溢出，导致进化失败，是其算法缺陷。

xskill 支持切换算法内核来驱动技能进化，详见下方「可选：切换算法内核」。

* * *

## 🚀 快速开始

### 单人模式（尝鲜体验）

如果只想具备检索轨迹的能力，不打算蒸馏任何skill：
```bash
pip install xskill          # Python 3.9+
xskill init                 # 扫描本机 agent，转换会话；不必填模型
xskill traj search 内存泄漏
xskill traj read <traj_id>  # 按行号读原文
```
如果你有LLM API，不只想要轨迹检索，可以尝试开始skill蒸馏能力：
```bash
pip install xskill          # Python 3.9+
xskill serve                # 第一次启动只初始化配置文件 ~/.xskill/config.yaml
```

打开 `~/.xskill/config.yaml`,填两个模型端点(一个 LLM,一个 embedding 向量模型):

```yaml
skill_dir: ~/.xskill/skill

llm:
  base_url: https://api.deepseek.com
  model:    deepseek-v4-flash
  api_key:  YOUR_KEY

embedding:
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
  model:    text-embedding-v4
  api_key:  YOUR_KEY
  dim:      0
```

上面这一段 `llm` 就是大家共用的默认模型。已经在用的配置不用改，继续这样写完全没问题。

如果你想给流水线里的拆分、聚类、编辑各自换一个模型或地址，可以再加一段可选的 `llm_agents`。不写也没关系。某个阶段或某个字段没写的话，会先看看有没有 `llm_skill`，再回到 `llm`。`xskill generate` 还是用 `llm` 和 `llm_skill`，不会去读 `llm_agents`。改完这几段之后重启一下 `xskill serve` 就好。

```yaml
# 可选。不写这段的话，三个阶段都继续用上面的 llm
llm_agents:
  split:
    model: qwen-plus
  cluster:
    model: deepseek-v4-flash
  edit:
    base_url: http://localhost:8000/v1
    model: local-skill-editor
    api_key: local
```

再跑一次 `xskill serve`, 它会自动识别你机器上每一个受支持的 agent 并开始运行，收集agent的轨迹并将skill推送到对应的harness下。

> [!NOTE]
>单人模式下，你将会丢失很多精心设计的特性，因此只建议在以下情况进行使用。
> 1.希望能够自动将之前高频工作流串联成skill
> 2.每天有高强度的Agent运行需求

### 团队模式(推荐)


服务器管理员在服务器配置config.yaml后运行中心化进程：
```bash
xskill serve --server  # 会打印connect join命令，复制给组内同事便可。
```

普通用户执行：
```bash
xskill connect <host:port> --token <token>  --name <工号/姓名>
```

默认全部上传；只想上传部分项目时 `xskill privacy mode allowlist`，再到项目目录里 `xskill privacy allow`，`xskill privacy status` 查看每个项目的判定。server 端 `team.server.privacy_mode: allowlist` 可要求全员白名单（客户端需本版本及以上）。

connect 成功后，指南会装进本机已探测到的 Claude Code、Codex、Cursor 等 agent。在对应 agent 里输入 `/xskill-helper`，就可以查 generate、search、升级这些用法。没有地址和 token 时，把上面这条命令当示例，向你们自己的 server 管理员要 host、token 和工号，不要连外网公开实例。

#### 额外功能：管控面板

在config.yaml中可以填写管理员身份:
```yaml
dashboard:
  enabled: true
  public: true
  password: ""
  admins:
    - admin_name_1  # 管理员<工号/姓名>
    - admin_name_2
  admin_password: admin_passwd_123
```
然后再在任意一台pc上输入：
```bash
xskill dashboard
```

就可以打开并登录管控面面板(身份自动识别），管理员可以进行如下操作：
- 全局pin某个skill
- 暂停某个用户的轨迹上传（异常行为用户）
- 全局下线停推某个skill
- 查看skill的版本血缘，得分趋势
  
普通用户可以：
- 为自己pin某个喜欢的skill，防止推荐流变化
- 下线某个自己不喜欢的skill
- 查看自己的轨迹贡献给了哪些用户，谁用了自己的skill
- 查看skill的版本血缘，得分趋势

#### 额外功能：即时生成或改写 Skill

`generate` 不是凭空创作 Skill：它会从 team server 上已有且有权访问的轨迹中提取经验，自然语言指令只用来描述想生成或改写什么。连接到支持 `generate` 的 team server 后，可以这样创建 Skill：

```bash
xskill generate "创建一个排查 Python 内存泄漏的 Skill，包含常用诊断命令"
```

同一个命令也能基于轨迹改写已有 Skill；在指令中写明 Skill 名称和修改目标即可：

```bash
xskill generate "改写现有的 python-memory-debug Skill，补充 Windows 排查步骤"
```

需要代理优先参考指定用户的历史轨迹时，使用 `--name`；多个工号或用户 ID 以逗号分隔。省略该参数时，代理可以在 server 授权的全部轨迹范围内检索：

```bash
xskill generate --name alice,bob "根据这些用户的成功案例生成数据库迁移 Skill"
```

任务可能会先等待 SkillEdit 池的空闲席位。CLI 会持续输出排队和运行日志；完成后，生成或改写的 Skill 会直接提交到主干，并 pin 到发起人的推荐列表。如果 CLI 提示 server 版本过旧，请联系管理员升级 team server。

#### 额外功能：技能检索与共享

除了由服务端根据画像自动推荐 Skill 之外，客户端也可以按需主动搜索、下载与上传技能：

```bash
xskill search <关键词>                                        # 搜索技能库，返回匹配技能与 ID
xskill download <sk