<p align="center">
  <img src="assets/logo-dsh-im-connecting-readme-3x2.png" alt="DSH-IM — Connecting DeepSeek Harness" width="420" height="280" align="middle">&nbsp;&nbsp;
  <img src="assets/logo-plugin-phone.png" alt="DSH-IM phone logo" width="280" height="280" align="middle">
</p>

---

<div align="center">
  <p><strong>让 DeepSeek Harness 触手可及</strong></p>
  <p><strong>Connecting DeepSeek Harness</strong></p>

  <p>
    <img src="https://dsh-im-random-badge.xmanrui-dsh-im.workers.dev" alt="滑动变祖器：今天是梁子或今天是梁圣（随机）">
    <a href="LICENSE"><img src="https://img.shields.io/github/license/xmanrui/dsh-im" alt="MIT 许可证"></a>
    <a href="#recognition"><img src="https://img.shields.io/badge/DeepSeek%20Harness-%E5%AE%98%E6%96%B9%E8%B5%9E%E5%8A%A9-4176E6?style=flat" alt="DeepSeek Harness 官方赞助"></a>
    <a href="https://deepseek1024.com/"><img src="https://img.shields.io/badge/deepseek1024-%E4%B8%8B%E8%BD%BD%E9%87%8FTop%2010-D97706?style=flat" alt="deepseek1024 下载量Top 10"></a>
    <a href="https://dshfind.com/zh/plugins/xmanrui/dsh-im"><img src="https://img.shields.io/badge/dshfind-%E5%88%86%E7%B1%BB%E7%AC%AC%E4%B8%80-d97706" alt="dshfind: 分类第一"></a>
    <a href="https://dshfind.com/zh/plugins/xmanrui/dsh-im?ref=badge"><img src="https://dshfind.com/api/badge/xmanrui/dsh-im?metric=downloads&amp;lang=zh" alt="dshfind downloads"></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1-07C160?logo=wechat&amp;logoColor=white" alt="微信">
    <img src="https://img.shields.io/badge/%E9%A3%9E%E4%B9%A6-3370FF?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTcuMiA0LjVoNy42YzEuMiAwIDIuMS41NSAyLjcgMS41OCAxLjA1IDEuOCAxLjU1IDMuNDUgMS41OCA0Ljk1LTIuMDQtLjYyLTQuMi0uMTUtNi4yMiAxLjQ1QzExLjMgOS43IDkuNDIgNy4wNCA3LjIgNC41WiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0xMC44IDEzLjU1YzMuMy0yLjkzIDUuNzItNC4yNCA5LjQ3LTIuNTItMS4yIDEuNDUtMi4yNyA0LjE4LTMuODYgNS40My0xLjY3IDEuMzEtMy45LjUtNS42MS0uNjR2LTIuMjdaIi8%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQuNCA4LjM1YzMuNDcgMy42MSA3LjI1IDYuMSAxMC4zMyA1LjcgMS4wNi0uMTQgMi4yLS43MiAzLjQtMS43Mi0xLjA0IDIuNjUtMi42IDQuOC01LjA2IDYtMi40NiAxLjItNS41Ni41Mi03LjQyLS43MkEyLjc2IDIuNzYgMCAwIDEgNC40IDE1LjNWOC4zNVoiLz48L3N2Zz4%3D" alt="飞书">
    <img src="https://img.shields.io/badge/%E9%92%89%E9%92%89-1677FF?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTM3LjA1IDIyLjc4M2MtNi43NTgtNS4yMTYtMTQuMzc4LTEyLjEyOC0yMi43My0xOS41MzgtLjY1NS0uNTg1LTEuMjQyLS4zNTQtMS41MzYuNDItMS44OCA0Ljk3My0uMDU4IDkuMzg2IDIuODg5IDExLjkzMnM3LjM2OCA0LjkxMiAxMC4wNTggNi4xNTVjLjEwNS4wNDkuMDEzLjIwMy0uMDkzLjE2My00Ljk1My0yLjE4Mi04LjM5Ny0zLjc2NS0xMy4wNy03LjM2OC0uNDk3LS4zODgtMS4wMS0uMjQyLTEuMDcuNTIxLS4zODQgNC43NDggMi42NTcgOC40ODMgNi4wNTggOS43NDUgMi4xLjc4MSA0LjM5OCAxLjIxMiA2LjUzIDEuNDc0LjEwOS4wMTUuMDg0LjE3OC0uMDI3LjE3OC0yLjc0Ny4wMS02LjA1OC0uNjU0LTguOTM1LTEuNzUxLS42MDYtLjIzMy0uODE4LjI1LS43MjIuNjMzLjQ5MSAyLjAwOCAyLjk3NCA1LjA3NiA2LjkyNiA1LjczYTEyIDEyIDAgMCAwIDIuMjI4LjExNWMuMTY0IDAgLjIwOC4wODkuMTU0LjIxN3EtMi42ODUgNC42LTIuODAzIDQuNzk3Yy0uMDkxLjE1Mi0uMDM2LjI3NS4xNTYuMjc1aDMuNTQzYy4xNjQgMCAuMjY0LjEwNi4xOC4yNDZsLTQuOTU4IDguMTk2Yy0uMTkxLjMyOC4wMzUuNTY1LjM5NS4zMDFzMTUuMjEyLTExLjEzMyAxNS42MzYtMTEuNDQ4Yy4xOTUtLjE0Mi4xNDgtLjMyNy0uMTI0LS4zMjdoLTMuMThjLS4yMDYgMC0uMjUyLS4xNC0uMTExLS4yOC4xNC0uMTQxIDMuNjAyLTMuNTk0IDQuODM3LTQuODg4IDEuMjgzLTEuMzUgMS45MzgtMy44MjUtLjIzMS01LjQ5OCIvPjwvc3ZnPg%3D%3D" alt="钉钉">
    <img src="https://img.shields.io/badge/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1-3370FF?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjIuMzUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTE3LjcgMTQuNWMxLjA1LTEuMTIgMS42NS0yLjUyIDEuNjUtNC4wMyAwLTMuODItMy41OC02LjkyLTgtNi45MnMtOCAzLjEtOCA2LjkyIDMuNTggNi45MiA4IDYuOTJjMS4xNyAwIDIuMjgtLjIyIDMuMjgtLjYyIi8%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTE2LjEgMTUuMTVjLjctLjcgMS44My0uNyAyLjUzIDBzLjcgMS44MyAwIDIuNTMtMS44My43LTIuNTMgMC0uNy0xLjgzIDAtMi41M1pNMTkuMjUgMTMuNDVhMS4zNiAxLjM2IDAgMSAxIDEuOTIgMS45MiAxLjM2IDEuMzYgMCAwIDEtMS45Mi0xLjkyWk0xOS41NSAxOC4wNWExLjE2IDEuMTYgMCAxIDEgMS42NCAxLjY0IDEuMTYgMS4xNiAwIDAgMS0xLjY0LTEuNjRaTTE1LjI1IDE4Ljc1YS45Mi45MiAwIDEgMSAxLjMgMS4zLjkyLjkyIDAgMCAxLTEuMy0xLjNaIi8%2BPC9zdmc%2B" alt="企业微信">
    <img src="https://img.shields.io/badge/QQ-1EBAFC?logo=qq&amp;logoColor=white" alt="QQ">
    <img src="https://img.shields.io/badge/Slack-4A154B?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTYgMTVhMiAyIDAgMSAxLTItMmgydjJabTEgMGEyIDIgMCAxIDEgNCAwdjVhMiAyIDAgMSAxLTQgMHYtNVptMi04YTIgMiAwIDEgMSAyLTJ2Mkg5Wm0wIDFhMiAyIDAgMSAxIDAgNEg0YTIgMiAwIDEgMSAwLTRoNVptOCAyYTIgMiAwIDEgMSAyIDJoLTJ2LTJabS0xIDBhMiAyIDAgMSAxLTQgMFY1YTIgMiAwIDEgMSA0IDB2NVptLTIgOGEyIDIgMCAxIDEtMiAydi0yaDJabTAtMWEyIDIgMCAxIDEgMC00aDVhMiAyIDAgMSAxIDAgNGgtNVoiLz48L3N2Zz4%3D" alt="Slack">
    <img src="https://img.shields.io/badge/Telegram-26A5E4?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTIzLjk1IDQuNTdjLS4zNi0xLjQ1LTEuNDMtMS43Ni0yLjgyLTEuMjRMMS41IDEwLjljLTEuMzQuNTItMS4zMiAxLjI3LS4yNCAxLjZsNS4wMyAxLjU3IDExLjY2LTcuMzZjLjU1LS4zNCAxLjA1LS4xNi42NC4yMWwtOS40NCA4LjUyLS4zNyA1LjEyYy41NCAwIC43OC0uMjQgMS4wOC0uNTNsMi41OS0yLjUxIDUuMzggMy45N2MuOTkuNTUgMS43LjI3IDEuOTUtLjkyTDIzLjk1IDQuNTdaIi8%2BPC9zdmc%2B" alt="Telegram">
    <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&amp;logoColor=white" alt="Discord">
    <img src="https://img.shields.io/badge/WhatsApp-25D366?logo=whatsapp&amp;logoColor=white" alt="WhatsApp">
    <img src="https://img.shields.io/badge/iMessage-34C759?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDNDNS45MjUgMyAxIDcuMDI5IDEgMTJjMCAyLjc1MSAxLjUxNCA1LjIxNCAzLjkwMSA2Ljg2NS4yOTEgMS41MjYtLjE3NCAyLjY0OC0xLjI1OCAzLjY0IDIuMDQ3LjAyNSAzLjQ0Mi0uNTA5IDQuNjQzLTEuNThBMTMuMiAxMy4yIDAgMCAwIDEyIDIxYzYuMDc1IDAgMTEtNC4wMjkgMTEtOVMxOC4wNzUgMyAxMiAzWiIvPjwvc3ZnPg%3D%3D" alt="iMessage">
  </p>

  <p><strong>简体中文</strong> · <a href="README.en.md">English</a></p>
</div>

---

<a id="recognition"></a>

> [!NOTE]
> **DSH-IM 已获得 DeepSeek Harness 官方**价值 **人民币 1,000 元的 Token 赞助**。感谢官方对本项目的肯定与支持！

## 简介

通过扫码、App Manifest 或已有机器人凭据把 IM 机器人接入 DeepSeek Harness，并让本机 Harness 主动连接公网 AI Office。一个插件、一个设置入口，统一管理内置 IM 渠道和 AI Office Connector。**每个 IM 渠道都支持接入多个机器人**，各机器人的连接状态、工作区、模型和会话绑定彼此独立；iMessage 是本机 Messages.app 身份接入的例外，详见[iMessage 渠道说明](docs/imessage.md)。

Connect IM bots to DeepSeek Harness by scanning a QR code, using an App Manifest, or entering existing bot credentials, and let the local Harness connect outward to a public AI Office. One plugin and one settings entry manage the built-in IM channels and the AI Office Connector.

## 界面

![IM 机器人页面](docs/images/imbot.png)

<img src="docs/images/Context_enhancement.png" alt="上下文增强页面" width="49%"> <img src="docs/images/access_mode.png" alt="访问模式页面" width="49%">

## 当前内置渠道

| 渠道 | 接入方式 | 消息与回复 |
| --- | --- | --- |
| 飞书 | 扫码创建机器人，或使用 App ID + App Secret 手动绑定 | 长连接接收消息；可选择飞书原生“实时直播”、单张实时过程卡或逐步消息展示任务过程 |
| 微信 | 使用微信扫码绑定机器人 | 腾讯 iLink 长轮询收发消息；等待 Harness 回答时显示“正在输入”，最终回复按 1,800 字符分段发送 |
| 钉钉 | 扫码创建机器人，或使用 Client ID + Client Secret 手动绑定 | 钉钉 Stream 长连接；通过 AI Card 流式显示回答 |
| 企业微信 | 使用企业微信 App 扫码创建智能机器人，或使用 Bot ID + Secret 手动绑定 | 官方 WebSocket 长连接；原生显示“正在思考中”、工具执行进度和流式回答 |
| 企业微信应用 | 在企业微信管理后台创建自建应用，填写企业 ID、AgentId、Secret、Token、EncodingAESKey（可选代理地址） | HTTP 回调接收；私聊支持流式回复（微信端不支持时自动改为分段文本），支持图片输入与结果文件回传；成员的微信关注该企业的微信插件后可在微信中直接使用 |
| QQ | 使用手机 QQ 扫码创建机器人，或使用 AppID + AppSecret 手动绑定 | WebSocket 长连接；私聊显示“正在输入”并以单条 Markdown 回复，群聊被 @ 后只发送最终答案 |
| Slack | 使用预置 App Manifest 创建应用，再填写 Bot Token（`xoxb-`）和 App Token（`xapp