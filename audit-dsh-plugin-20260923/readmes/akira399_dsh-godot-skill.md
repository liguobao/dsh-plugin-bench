# dsh-godot-skill

Godot Engine 4.x 全栈游戏开发技能插件 for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）。

安装后，插件在激活时把仓库内自带的 **`godot-4-development`** 技能注册为运行时技能 —— 任何会话都可以通过 `skill` 工具加载它，让 AI 独立完成 Godot 游戏的规划、搭建、编码、调试、优化与导出。

![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-生态插件-4D6BFE?logo=deepseek&logoColor=white)
![License](https://img.shields.io/github/license/akira399/dsh-godot-skill)
![类型](https://img.shields.io/badge/类型-Host%20插件-blue)
![技能](https://img.shields.io/badge/技能-godot--4--development-important)

## 技能内容

依据 [Godot 官方特性列表](https://docs.godotengine.org/zh-cn/4.x/about/list_of_features.html)（简体中文）整理并补充实现细节：

- **核心概念**：节点 / 场景 / 资源 / 信号 / 组
- **渲染器选型**：Forward+ / Mobile / Compatibility（GL）
- **特性 → 实现速查**（20 个领域）：平台与导出、编辑器、2D/3D 图形与工具与物理、着色器、GDScript/C#/GDExtension、音频、导入、输入、导航、网络、国际化、窗口与 OS、移动端/XR、GUI、动画、文件格式、杂项（Movie Maker、无头服务器、CI）
- **完整开发工作流**：设计决策 → 项目脚手架 → 核心玩法原型 → 内容实现 → 打磨与性能 → 测试调试 → 导出发布
- **代码模板与错误排查表**：玩家移动、相机跟随、生成、HTTP、暂停、存档、ENet 联机、常见错误速查

## 安装（官方路径）

### 方式一：npm 安装（推荐，发布后可用）

```sh
npx -p @deepseek-ai/dsh dsh plugin --profile web add dsh-godot-skill
```

### 方式二：Git HTTPS 安装

```sh
npx -p @deepseek-ai/dsh dsh plugin --profile web add git+https://github.com/akira399/dsh-godot-skill.git
```

### 方式三：GitHub 短名安装（需要本机已配置 GitHub SSH key）

```sh
npx -p @deepseek-ai/dsh dsh plugin --profile web add github:akira399/dsh-godot-skill
```

安装完成后重启 DSH（重新运行 `dsh web`）。重启后会话技能目录中即出现 `godot-4-development`。

### 如果遇到 `git+ssh://git@github.com` 认证失败

DSH 通过 pnpm 安装 git 依赖时，可能把 Git 地址解析成 `git+ssh://git@github.com`，此时本机必须已有 GitHub SSH key；否则会报：

```
fatal: Could not read from remote repository.
```

**临时规避方案（二选一）：**

1. **让 git 用 HTTPS 替代 SSH**（无需配置 SSH key）：
   ```sh
   git config --global url."https://github.com/".insteadOf "git@github.com:"
   git config --global url."https://github.com/".insteadOf "ssh://git@github.com/"
   ```
2. **配置 GitHub SSH key** 后重试。

另外，pnpm 对 git 托管的插件会执行 `prepare` 类脚本并提示：
`add the exact key pnpm printed above under allowBuilds in <profile>/pnpm-workspace.yaml, then re-run`
按提示把对应 build key 加入该 profile 的 `pnpm-workspace.yaml` 的 `allowBuilds` 后重试即可。

## 使用

插件生效后，会话中会提示可用技能 `godot-4-development`。直接说：

> 用 godot-4-development 技能帮我做一个 2D 平台跳跃游戏

AI 会先加载技能，再按技能内的工作流与 API 速查完成开发。

## 验证

```sh
pnpm verify
```

检查：插件语法、技能文件完整性、运行时注册行为（mock `ctx` 断言）。

## 文件结构

```
dsh-godot-skill/
├── package.json          # cordis 插件清单（dsh.bundle.patch → cordis.patch.yml）
├── cordis.patch.yml      # 配置层：把插件挂进 profile 的 host 组合
├── lib/index.js          # Host 插件：读取 SKILL.md 并注册为运行时技能
├── .dsh/skills/godot-4-development/SKILL.md   # 技能本体（frontmatter + 正文）
├── scripts/verify.mjs    # 验证脚本
└── README.md / LICENSE
```

## 许可

MIT © 2026 dsh-godot-skill contributors

Godot 官方文档内容版权归 Godot 社区所有（CC BY 3.0），本插件仅整理引用。
