# dsh-passwords

[English](README_en.md) | 简体中文

<p align="center">
  <img src="docs/banner.jpg" alt="dsh-passwords" width="100%">
</p>

<p align="center">
  <a href="https://github.com/slywalker2006/dsh-passwords/releases/latest"><img src="https://img.shields.io/github/v/release/slywalker2006/dsh-passwords?style=flat-square" alt="Version"></a>
  &nbsp;
  <a href="https://github.com/slywalker2006/dsh-passwords/stargazers"><img src="https://img.shields.io/github/stars/slywalker2006/dsh-passwords?style=flat-square" alt="Stars"></a>
  &nbsp;
  <a href="https://www.npmjs.com/package/dsh-passwords"><img src="https://img.shields.io/npm/v/dsh-passwords?style=flat-square" alt="npm"></a>
  &nbsp;
  <a href="https://www.npmjs.com/package/dsh-passwords"><img src="https://img.shields.io/npm/dm/dsh-passwords?style=flat-square" alt="Downloads"></a>
  &nbsp;
  <a href="https://github.com/slywalker2006/dsh-passwords/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/slywalker2006/dsh-passwords/ci.yml?style=flat-square&label=CI" alt="CI"></a>
  &nbsp;
  <a href="https://github.com/deepseek-ai/deepseek-harness"><img src="https://img.shields.io/badge/DSH-0.1.7--alpha.2-4c6ef5?style=flat-square&labelColor=454a54" alt="DSH"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="License">
  &nbsp;
  <a href="https://github.com/awesome-dsh-plugin/awesome-dsh-plugin"><img src="https://img.shields.io/badge/Awesome-DSH%20Plugin-9370db?style=flat-square" alt="Awesome DSH Plugin"></a>
  &nbsp;
  <a href="https://github.com/0xsline/awesome-deepseek-harness"><img src="https://img.shields.io/badge/Awesome-DeepSeek%20Harness-4c6ef5?style=flat-square" alt="Awesome DeepSeek Harness"></a>
  &nbsp;
  <a href="https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins"><img src="https://img.shields.io/badge/%E6%94%B6%E5%BD%95-Awesome%20%E6%8F%92%E4%BB%B6%E7%B2%BE%E9%80%89-15aabf?style=flat-square" alt="Awesome 插件精选收录"></a>
  &nbsp;
  <a href="https://github.com/bruc3van/awesome-dsh-plugin"><img src="https://img.shields.io/badge/%E6%94%B6%E5%BD%95-DSH%20%E7%B2%BE%E9%80%89%E7%9B%AE%E5%BD%95-1c7ed6?style=flat-square" alt="DSH 精选目录收录"></a>
  &nbsp;
  <a href="https://github.com/imsai-sh/awesome-deepseek-harness-plugins"><img src="https://img.shields.io/badge/%E6%94%B6%E5%BD%95-1024%20%E6%8F%92%E4%BB%B6%E5%95%86%E5%BA%97-0ca678?style=flat-square" alt="1024 插件商店收录"></a>
</p>

<p align="center">
  <strong>给 DeepSeek Harness 加一层服务器级认证网关，使其成为可公网部署的多租户平台</strong><br>
  <em>登录认证 · 自动 HTTPS · 多租户权限 · 会话授权 · 审计加密 · 中英双语</em>
</p>

<div align="center">

[功能](#功能) · [快速开始](#快速开始) · [首次配置](#首次配置) · [卸载](#卸载) · [自动 HTTPS](#自动-https) · [部署拓扑](#部署拓扑) · [配置参考](#配置参考) · [常见问题](#常见问题) · [安全与隐私](#安全与隐私) · [参与贡献](#参与贡献)

</div>

---

## 功能

- **登录认证**：首次配置创建主用户，之后所有访问先过登录页；会话 12 小时有效
- **自动 HTTPS**：向 Let's Encrypt 自动签发并续期证书，80 端口自动跳转 443，无需配置
- **多租户**：一个主用户加任意多个子用户，账号管理全部在 dsh 设置页完成
- **权限与配额**：工作区白名单、逐会话开关、每小时 token 上限、每日时长上限、沙盒三档、上传与下载开关、封禁
- **会话授权**：工作区权限不自动包含其中全部会话，主用户逐会话授予；归档状态在工作区列表与会话列表间保持一致
- **运维视图**：主用户可查看全部工作区与会话，下载非敏感普通文件
- **审计与安全**：登录限流与锁定、审计日志、SQLite 静态加密、登出即吊销会话
- **设置页卡片**：远程设置补丁重载、软件更新、账号与权限管理、站内留言，全部中英双语

## 界面截图

| 登录页 · 浅色 | 登录页 · 深色 | 登录页 · English |
|:---:|:---:|:---:|
| <img src="docs/screenshots/white-login.png" width="360"> | <img src="docs/screenshots/black-login.png" width="360"> | <img src="docs/screenshots/white-login-en.png" width="360"> |

| dsh 主界面 · 登录后 | 聊天 / 留言 | 设置页卡片 · 账号管理 |
|:---:|:---:|:---:|
| <img src="docs/screenshots/main-ui.png" width="360"> | <img src="docs/screenshots/chat.png" width="360"> | <img src="docs/screenshots/card-front.png" width="360"> |

| | 设置页卡片 · 权限与配额 | |
|:---:|:---:|:---:|
| | <img src="docs/screenshots/card-back.png" width="360"> | |

## 快速开始

### 前置条件

宿主机安装需要 Node.js 22.19+ 或 24+、可正常运行的 dsh 和 git。兼容门禁接受 DSH `0.1.7` 稳定版及其 alpha/rc 预发布版本，开发与 Docker 默认运行时锁定 `0.1.7-alpha.2`；同时保留 `0.1.6` / `0.1.5` 全系列与 `0.1.2` / `0.1.3` 接口边界。测试服务器已部署并验证 `0.1.7-alpha.2`。Docker 安装只需要 Docker Engine 或 Docker Desktop 和一个 DeepSeek API key。

### 安装

五种安装方式，任选其一。宿主机安装会自动完成装依赖、编译、生成 SETUP_KEY、注册 dsh 插件、应用远程设置补丁；已有 `.env` 时不覆盖，重复运行安全。

```bash
# 1. Linux / macOS 一键安装
curl -fsSL https://raw.githubusercontent.com/slywalker2006/dsh-passwords/main/install.sh | sudo bash

# 2. 先 clone 再安装
git clone https://github.com/slywalker2006/dsh-passwords && cd dsh-passwords
sudo bash install.sh

# 3. npm 全局安装，适用于任意平台
npm install -g dsh-passwords
dsh-passwords install
```

Windows 下载仓库里的 `install.bat` 双击运行。默认安装到 `%USERPROFILE%\dsh-passwords`。

```bash
# 4. Docker
docker run -d \
  --name dsh-passwords \
  --restart unless-stopped \
  --env-file .env \
  -p 127.0.0.1:3088:3088 \
  -v dsh-home:/data/dsh \
  -v dsh-passwords-state:/data/dsh-passwords \
  skywalker237234/dsh-passwords:2.7.4
```

`.env` 至少包含 `DEEPSEEK_API_KEY`。`MCP_GATEWAY_PUBLIC_HOST` 建议填实际访问的域名。宿主端口只发布在回环地址 `127.0.0.1:3088`，容器内监听 `0.0.0.0:3088`；公网访问由 nginx 或 Caddy 终结 TLS 后转发。镜像内置 DSH `0.1.7-alpha.2`（DSH 0.1.7 线当前锁定版本；该镜像尚未做运行验收）；初始化完成以 healthz/readyz 均返回 `ok:true` 为准。

说明：

- 宿主机安装默认目录为 `/opt/dsh-passwords`，可用 `DSH_PASSWORDS_DIR` 更改；检测到已有 dsh-passwords 目录时就地幂等重跑，其他同名目录会报错退出
- SETUP_KEY 打印在安装结束时，同时写入安装目录的 `setup-key.txt`
- Docker 的两个命名卷分别存 dsh profile 与 `.env`、数据库、证书；删除即丢数据
- Docker 中的“保命技能”不会尝试在容器内自删；Compose 部署需要彻底清理时，在宿主机执行 `docker compose down -v`，而 `docker run` 部署需要先 `docker rm -f dsh-passwords`，再执行 `docker volume rm dsh-home dsh-passwords-state`（都会永久删除卷数据）
- 分容器部署时给 dsh 容器加 `MCP_DSH_PATCH_ALLOW_BIND_ALL=1`，让网关容器能访问 dsh web

### 首次配置

1. 启动 dsh：`dsh web`。Docker 用户跳过此步，容器内自动启动。
2. 浏览器打开 `https://<服务器地址>`，首次访问自动进入配置页。
3. 输入 SETUP_KEY 创建主用户。此后该地址的所有访问都先过登录页。

首次配置成功后 `setup-key.txt` 自动删除，`.env` 中的密钥自动固化并轮换。

Docker 用户需要先用 nginx 或 Caddy 把 80/443 反代到 `http://127.0.0.1:3088`；一次性 SETUP_KEY 用 `docker exec dsh-passwords cat /data/dsh-passwords/setup-key.txt` 读取。

## 卸载

宿主机安装可在 dsh-passwords 安装目录执行：

```bash
node dist/cli.js uninstall
# 全局 npm 安装也可直接执行：
dsh-passwords uninstall
```

该命令只从 DSH web profile 移除 `dsh-passwords` 的 link 与 bundle，并回滚本插件管理的 dsh 补丁；其他插件和 bundle 会保留。完成后按提示重启 `dsh-web`。

卸载不会删除安装目录、`.env`、数据库、TLS/ACME 证书或其他插件。profile 依赖重建或补丁回滚失败时会恢复原 profile，避免留下半卸载状态。Docker 部署请按所用 Compose 或容器编排停止并移除容器；不要删除命名卷，除非也要永久清除数据。

## 自动 HTTPS

默认探测公网 IP 并用 `<IP>.sslip.io` 向 Let's Encrypt 签发 90 天证书，到期前 30 天自动续期，新证书热加载。有自己的域名时在 `.env` 加 `MCP_GATEWAY_DOMAIN`。签发失败拒绝启动，不降级明文；续期失败但旧证书仍在有效期内时继续使用并后台重试。

| 错误码 | 含义 | 处理 |
|---|---|---|
| 30 | 证书签发失败 | 检查 80/443 放行与占用情况，确认能连通 Let's Encrypt |
| 31 | 拿不到公网 IP 或域名 | 设置 `MCP_GATEWAY_DOMAIN`，或使用 HTTP 模式 |
| 32 | 端口被占用 | 更换 `MCP_GATEWAY_PORT` 或释放端口 |

证书域名使用 `<IP>.sslip.io` 是因为 Let's Encrypt 不给纯 IP 签发证书。直接访问裸 IP 的 https 地址会提示主机名不匹配，从 80 端口入口进入会自动跳转到正确地址。

## 部署拓扑

| 场景 | 做法 |
|---|---|
| 公网服务器，80/443 可用 | 默认配置即可，自动 HTTPS |
| 已有域名证书 | `.env` 填 `MCP_GATEWAY_TLS_CERT` / `MCP_GATEWAY_TLS_KEY`，无需 80 端口 |
| 已有 nginx / Caddy 反代 | 反代终结 TLS，`.env` 设 `MCP_GATEWAY_AUTO_TLS=0` 与高位端口，网关只监听回环 |
| Cloudflare | CF 边缘终结 TLS 转发源站，配置同反代 |
| 纯内网 / 裸 IP 无法开 80 | 使用 HTTP 模式 |

http-01 验证只在签发与续期时访问 80 端口，约每 60 天一次。

## HTTP 模式

默认拒绝明文 HTTP。内网环境确需使用时：

```bash
node scripts/start-http.mjs [端口]    # 默认 8080，需确认风险提示
```

或在 `.env` 写入 `MCP_GATEWAY_AUTO_TLS=0` 与 `MCP_GATEWAY_PORT=8080`，dsh 启动时插件以 HTTP 模式拉起网关。该模式不依赖公网 IP、DNS、ACME 或外部 CDN，可用于内网部署；首次安装仍需要 npm/GitHub 可访问，或提前准备项目 tarball、依赖缓存和本地 DSH 安装。模型对话仍需要配置上游模型提供方（例如 `DEEPSEEK_API_KEY`）；没有外部模型服务时，登录、权限、文件与管理功能可运行，但不会产生模型回复。

## 设置页卡片

登录后打开设置，能看到「dsh-passwords · 密码门」卡片。

| 功能 | 使用者 | 说明 |
|---|---|---|
| 重载补丁 | 仅主用户 | dsh 升级后设置页异常时一键重打补丁并重启网页服务 |
| 软件更新 | 状态所有人可见，操作仅主用户 | 自动检查、限速下载、空闲后安装重启，详见下节 |
| 修改密码 / 用户名 | 本人；主用户可操作任何人 | 改密后旧会话全部失效 |
| 子用户管理 | 仅主用户 | 创建、删除子用户 |
| 子用户权限 | 仅主用户 | 工作区白名单、逐会话授权、token 与时长上限、沙盒、上传下载开关、WebSocket 路径授权、封禁 |
| 聊天 / 留言 | 所有登录用户 | 支持标签；子用户消息默认私信主用户，仅主用户可广播 |
| 退出登录 | 所有登录用户 | 登出当前账号 |

密码要求：至少 12 位，含大写、小写、数字、符号。

## 软件更新

- 版本发现走 GitHub Release，包始终从 npm registry 下载并按 `dist.integrity` 的 sha512 校验
- 自动模式：每 24 小时检查，发现新版本后限速下载，平台连续空闲 1 小时后安装重启；主用户可手动跳过等待
- 手动模式：检