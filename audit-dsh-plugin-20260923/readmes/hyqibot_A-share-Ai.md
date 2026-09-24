# 幻银量化A股AI交易系统A-share-Ai

基于四大国内大模型（幻银超i、DeepSeek、通义千问、豆包）的A股自动交易系统，支持全市场选股和实盘交易。

接入自产龙虾iClaw，手机端一句话同时控制四大模型全自动交易。

## 交易执行说明

- **买入**：按总资产×仓位比例计算金额，并受「单轮最多使用可用现金一定比例」限制。
- **卖出（模型自动 SELL 信号）**：按当前持仓**全部卖出**，不受可用现金上限影响（避免资金紧张时卖单被算成 0 股）。

## 功能特性

🎯 让AI在A股市场中一展身手，让多个大语言模型在A股全市场股票中完全自主决策、同台竞技！

🎯 接入A股真实交易账户，实时展示ai真实交易过程，实时+真实交易让系统有更广阔的应用空间

🎯 多模型集成：支持幻银超i、DeepSeek、通义千问、豆包等多种大语言模型

🎯 策略进化：基于交易表现，AI模型能够不断优化自己的投资策略

⏰ 秒级别实盘交易支持 - 接入实盘秒级精度交易,需拥有合规通道

🚀 服务部署与并行执行 - 部署生产服务 + 并行模型执行

🎨 ai交易逻辑展示 - 详细的交易日志可视化（完整交易过程展示）

🎯 核心特色: 100% AI自主决策，零人工干预，ai策略自我发现、自我训练、自我进化

🎯 特别功能：交易中可添加实时人工干预和Ai进行互动（可选），接入自产龙虾iClaw，接管互动过程并随时指令四大ai同时干活。

🎯 新增了异步执行功能，提高系统运行速度

🤖 **4大模型并行**：幻银超i、DeepSeek、Qwen通义千问、豆包同时运行，比较收益
📈 **全市场选股**：AI自主从全市场选择有潜力的股票，自定义股票池（可选）
💹 **实时行情**：集成实时A股数据，供ai使用并用于实际交易
💹 **历史行情+财务数据**：集成A股历史行情和财务数据，供ai分析和训练
🎯 **智能交易**：基于AI分析生成买卖信号并全自动执行交易
🌈 **多种策略**：包括趋势跟踪、均线策略、技术指标策略、量化套利策略等，完全由ai自动选择并不断进化
📊 **实时监控**：UI界面实时显示收益曲线和交易日志
🔒 **风险控制**：内置仓位控制和止损机制

## 📱 iClaw钉钉配置说明

方法1（已取消）：启用 `config/dingtalk.json` 后，程序启动会提示先在钉钉私聊机器人发送一次 `/status` 完成绑定；绑定成功会自动把你的账号ID写入 `default_conversation_id`，后续每轮交易完成将自动推送到你的钉钉私聊（无需手动配置个人ID）。

方法2：通过测试脚本或钉钉平台获取 `sender_id` 写入 `config/dingtalk.json` 的 `default_conversation_id` 字段，同时配置其他必要参数（见exampl文件），程序启动后会直接将每轮交易结果推送到该账号，同时实现钉钉对项目所有大模型的远端实时控制。

> **Stream 长连接**：入站消息走 WebSocket Stream，出站通知走 REST API（二者独立）。若长时间收不到私聊指令但交易通知仍正常，日志中会出现 `Stream 已断开，10s 后重连...`；程序会自动重连，无需重启。

## 💬 iClaw智能聊天与自然语言指令交易

- **智能聊天（多模型）**：发送 `@模型名 你的问题`，机器人会调用对应大模型回复（只聊天不下单）。
  - 示例：`@幻银超i 今天市场怎么看？`、`@deepseek 解释一下市盈率`
- **自然语言指令AI交易**：发送 `@iClaw 你的自然语言交易意图`，机器人会调用你文本中提到的模型把意图翻译为 JSON 指令，经校验后复用 `/buy`、`/sell` 链路执行。
  - 示例：`@iClaw 用幻银超i买入002961 1000股，价格26.9`
- **/开头的指令交易**：  
  - **买入/卖出**：`/buy [模型名] 股票代码 数量 [价格]`、`/sell [模型名] 股票代码 数量 [价格]`，模型名可省略。示例：`/buy 000001 1000`、`/sell 幻银超i 000001 500 27.0`
  - **批量买入**：`/batch_buy [模型名] 股票代码:数量,股票代码:数量,...`，模型名可省略（省略则用默认模型）。示例：`/batch_buy 000001:1000,000002:500` 或 `/batch_buy 幻银超i 000001:1000,000002:500`
  - **条件交易**：`/condition [模型名] 股票代码 条件 买入/卖出 [数量]`，模型名可省略。条件支持 `price>数字`、`price<数字`、`price_between 低 高`，示例：`/condition 000001 price>11 buy 1000` 或 `/condition 幻银超i 000001 price>11 buy 1000`；**数量可省略**：不写时买入按风险与可用资金自动算数量、卖出为全部持仓；若当下价格未满足条件，系统会在后台按交易轮次间隔持续监控，触发即按市价下单（默认有效期6小时）。**条件单监控在独立任务中运行，不占用主程序每轮交易循环**。创建后机器人会返回条件单ID，**撤销**：`/cancel <条件单ID>`（如 `/cancel COND-1734567890-000001`）。
- **完整指令列表**：在钉钉中发送 `/help` 或 `/h` 可查看完整指令列表与示例。
- **远程启动本地应用**：发送 `/runapp <应用别名或内置名称>`，由主程序在本机尝试启动白名单中的桌面应用。
   - 别名通过 `user_config.json` 的 `APP_LAUNCH_CONFIG.aliases` 配置，例如 `"mytrader": "C:\\Users\\you\\Desktop\\MyTrader\\MyTrader.exe"`
   - 对于 `notepad`、`calc` 这类规范化程序，可直接 `/runapp notepad` 使用（也可通过 `builtin_allow` 扩展）

## 📊 Ai炒股大赛排行榜、实时收益及决策日志、实时投资组合

[![Ai炒股大赛历史排行榜(基金运作)](https://img.shields.io/badge/📈_Ai炒股大赛历史排行榜(基金运作)-GitHub_Pages-blue?style=for-the-badge&logo=github)](https://hyqibot.github.io/A-share-Ai/reports/report.html)

[![Ai炒股大赛历史排行榜(全市场)](https://img.shields.io/badge/📈_Ai炒股大赛历史排行榜(全市场)-GitHub_Pages-blue?style=for-the-badge&logo=github)](https://hyqibot.github.io/A-share-Ai/reportsall/report.html)

[![实时收益及决策日志](https://img.shields.io/badge/🎯_实时收益及决策日志-Dashboard-green?style=for-the-badge&logo=chart-line)](https://hyqibot.github.io/A-share-Ai/)

[![实时投资组合](https://img.shields.io/badge/📊_实时投资组合-Portfolio-orange?style=for-the-badge&logo=pie-chart)](https://hyqibot.github.io/A-share-Ai/portfolio.html)


**安装及启动**
    项目已打包成windows桌面exe，可直接运行，获取方法：前往https://hyqibot.com/card-shop.html 捐赠相应期限的服务卡即可获得，如需接入实盘需拥有合规通道并自行完成或有要求的相关报备。有疑问可发送您的github地址（必需）+简短介绍到：hyqi@tradey.dpdns.org，更多信息，可点：https://www.hyqibot.com/  有永久免token费的龙虾iclaw赠送。    

   启动方法很简单：傻瓜式，无需python基础
   下载Releases安装包，解压，将user_config.json.example重命名为user_config.json，填写参数
   需要用到的参数有几类：1）真实交易账户需合规接入，比如机构自有通道或各大券商QMT；2）自选股票池通达信本地路径；3）deepseek等大模型api-key；4）licence：hyqibot
   填好参数保存，右键以管理员身份运行解压好的exe文件，图形界面上点击启动交易即可。

## 核心飞跃：真正的AI自我发现

1. 从空白或使用者设定的风格开始
    所有AI初始可以都是"自适应投资者"

    也可以预设投资风格

    通过实践发现自己的特长

2. 自我反思机制
    定期回顾投资表现

    分析什么策略对自己有效

    主动调整投资哲学

3. 风格进化
    记录风格变化轨迹

    基于表现调整风险偏好

    逐步形成稳定的投资人格

4. 真正的差异性
    现在4个AI将：

    自主发现风格：比如，幻银超i最明白博弈精髓，DeepSeek可能发现自己擅长量化，Qwen或者偏好价值投资

    不同的进化路径：每个AI基于自身特质和市场反馈形成独特风格

    动态调整：根据市场环境变化调整策略

    真正的个性：发展出反映其"性格"的投资哲学

    预期结果
    您将看到：

    真正的AI个性：每个AI发展出独特的投资身份

    动态的风格进化：投资风格会随着经验积累而改变

    基于表现的调整：成功的策略被保留，失败的被淘汰

    不可预测的结果：无法预先知道哪个AI会发展出什么风格

    这样设计后，您将见证真正的"AI投资经理成长史"，而不是预先编排的表演。每个AI都有机会找到最适合自己的投资道路！


## 🧠 幻银超i（HYQi）的愿景

我们正以实时的真实交易环境去训练Ai，以此来测试并提高Ai的智慧，运用开放式学习、大规模强化学习等技术来驾驭其复杂性。

心怀此念，我们正广纳贤才，招募资深ai研究员、创业伙伴与思维破局者。

如果您渴望为现实世界打造Alpha-HYQi，欢迎与我们携手。简历请发送至：hyqi@tradey.dpdns.org

"资本配置，是ai智慧接受真理检验的最佳试金石"。

———幻银超i与您共勉

📞 支持与社区

💬 讨论交流: GitHub Discussions

🐛 问题反馈: GitHub Issues

📜 许可证条款
1. 开源核心模块（MIT 许可证）

开源部分源代码（位于本仓库 ./codes目录下）基于 MIT 许可证 授权，你享有以下权利：

自由使用、复制、修改、合并、发布、分发、再授权及出售开源核心代码的副本；

将开源核心代码集成到个人 / 商业项目（包括闭源项目），但需保留原始版权声明和 MIT 许可证文本。

完整许可证文本：LICENSE

2. 商业闭源模块
商业模块（包括但不限于打包成exe文件内嵌的所有模块）受版权保护，基于 商业许可证 提供，核心条款如下：

使用需获得有效商业授权（联系我们获取订阅 / 授权方案）；

禁止未经授权分发、反编译、逆向工程或转售商业模块；

商业模块仅可与本项目的开源核心模块搭配使用，不可单独使用或集成到其他未授权项目。

完整商业许可证详情：LICENSE-COMMERCIAL（购买授权后提供）

🤝 贡献指南

我们欢迎对开源核心模块的贡献！贡献步骤：

Fork 本仓库；

仅在 ./codes 目录下修改代码；

提交 Pull Request，并清晰描述修改内容。

详细贡献规则：CONTRIBUTING.md

注意：商业模块为闭源性质，不接受外部代码贡献。

📞 联系与支持

开源核心用户

问题反馈：通过 GitHub Issues 提交开源核心模块相关的 Bug 报告或功能需求；

社区交流：加入我们的 [GitHub Discussions] 参与讨论。

商业授权用户

技术支持：通过 [hyqi@tradey.dpdns.org] 联系专属支持团队（24 小时内响应）；

授权咨询：发送邮件至 [hyqi@tradey.dpdns.org]，了解定价、订阅方案或定制授权服务。

⚠️ 免责声明

开源核心模块基于 MIT 许可证以 “原样” 提供，不提供任何明示或暗示的担保（详见完整 MIT 许可证文本）；

商业模块将按照许可证协议提供技术支持，但不保证与所有自定义环境兼容；

双许可证模式可能会调整，任何更新将在本 README 中公示，并通知商业授权用户。

© [2025] 幻银超i 保留所有权利。开源核心模块基于 MIT 许可证授权。商业模块基于商业许可证授权。

![GitHub Stars Trend](https://img.shields.io/github/stars/hyqibot/A-share-Ai?style=social&label=Stars&logo=github&color=yellow)
![Star Growth Curve](https://api.star-history.com/svg?repos=hyqibot/A-share-Ai&type=Date)


A-share-Ai: Phantom Silver Quantitative AI Trading System for A-Shares

An automated A-share trading system powered by four major domestic large language models (HYQi Phantom Silver Ultra-i, DeepSeek, Qwen, Doubao), supporting full-market stock selection and live trading.

Integrates our in-house lobster iClaw: control all four models' fully automated trading from your phone with a single sentence.

## Trade Execution

- **Buy**: Size by total assets × position ratio, and cap spend at a configured share of available cash per cycle.
- **Sell (model auto SELL)**: Sell the **entire current position**. Not limited by available-cash caps (so sells are not sized to 0 shares when cash is tight).

## Key Features

🎯 Let AI showcase its capabilities in the A-share market—multiple large language models make fully autonomous decisions and compete against each other across all A-share stocks!

🎯 Connect to real A-share trading accounts, display the AI's real trading process in real time. Real-time + real trading expands the system's application scenarios.

🎯 Multi-model Integration: Supports HYQi Phantom Silver Ultra-i, DeepSeek, Qwen, Doubao, and other large language models.

🎯 Strategy Evolution: Based on trading performance, AI models continuously optimize their investment strategies.

⏰ Second-level Live Trading Support - Connect to live trading with second-level precision. A compliant trading channel is required.

🚀 Service Deployment & Parallel Execution - Deploy production services + parallel model execution.

🎨 AI Trading Logic Visualization - Detailed trading log visualization (full trading process display).

🎯 Core Feature: 100% AI autonomous decision-making with zero human intervention. AI strategies self-discover, self-train, and self-evolve.

🎯 Special Function: Optional real-time human intervention and interaction with AI during trading. Integrates our in-house lobster iClaw to take over that interaction and command all four AIs at once.

🎯 Newly added asynchronous execution to improve system speed.

🤖 **4-Model Parallelism**: HYQi Phantom Silver Ultra-i, DeepSeek, Qwen, and Doubao run together t