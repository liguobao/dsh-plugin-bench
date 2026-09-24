<p align="center">
  <img src="https://img.shields.io/github/stars/wqty123/dsh-browser?style=flat&amp;label=%E2%98%85&amp;color=08C" alt="GitHub stars">
  <img src="https://img.shields.io/npm/v/dsh-builtin-browser?style=flat&amp;label=npm&amp;color=CB3837" alt="npm version">
  <img src="https://img.shields.io/badge/license-MIT-2EA44F?style=flat" alt="MIT License">
  <img src="https://img.shields.io/badge/DSH-Plugin-47848F?style=flat" alt="DeepSeek Harness plugin">
  <img src="https://img.shields.io/badge/Platform-Windows-4493F8?style=flat-square" alt="Platform: Windows (verified)">
</p>

<p align="center"><sub>中文 · <a href="README.en.md">English</a></sub></p>

<h3 align="center">为 DeepSeek Harness 生态打造的<b>共享真实浏览器</b>插件（装好即用，人机同页）</h3>

<h4 align="center">agent 驱动一个真实、可见、可随时人工接管的浏览器——人与 agent 操作的是<b>同一个页面</b>。</h4>

## 文档

| 目标 | 入口 |
| --- | --- |
| 了解插件为什么存在、与无头方案的区别 | [为什么做共享真实浏览器](docs/why-browser.md) |
| 安装、配置与日常使用 | [用户指南](docs/user-guide.md) |
| 全部 33 个工具的参数、输出与示例 | [工具参考](docs/tool-reference.md) |
| 了解 seam / provider / 工具三层与自托管实现 | [架构说明](docs/architecture.md) |
| 查看全部文档与 README 分工 | [文档索引](docs/README.md) |

## 这是什么

`dsh-builtin-browser` 给 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 提供浏览器能力:

- **真实视图,而非转播**:浏览器是原生 `WebContentsView`,用户直接看到 agent 在做什么,随时可以上手接管;
- **装好即用**:有桌面外壳时嵌入外壳视图;纯 `dsh web` 也能**自托管**——插件自己拉起一个 Electron 窗口,不需要任何额外配置;
- **一插件即一套工具**:安装后 agent 自动获得 33 个 `browser_*` 工具(打开、查看、无障碍树、等待、语义/坐标操作、滚动、回退、批量/单控件填表、按键、结构化提取、截图、下载、登录态管理……)。

一句话:**安装插件 = 获得一个与用户共享、可被 agent 驱动的真实浏览器。**

## 快速开始

```sh
# 方式一:从 npm 安装(已发布)
dsh plugin --profile web add dsh-builtin-browser

# 方式二:从源码目录安装(独立仓库,一插件一仓库)
dsh plugin --profile web add <本仓库路径>
```

安装后,agent 即可使用浏览器工具,例如:

| 想做什么 | 用哪个工具 | 说明 |
| --- | --- | --- |
| 打开页面 | `browser_open` | 打开 URL,返回带编号元素的快照 |
| 了解页面 | `browser_snapshot` | 输入框/按钮/链接的编号清单,可据此定位 |
| 操作页面 | `browser_execute` | 在页面里执行 JS(原生 setter,框架友好) |
| 填写表单 | `browser_fill` | 一次填写多个字段,可选提交 |
| 看到页面 | `browser_screenshot` | PNG 截图,可存文件交给视觉模型 |

完整清单见[工具参考](#工具参考)。

## 主要功能

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>共享真实浏览器</h3>
      <p>原生视图而非无头截屏。用户与 agent 操作同一个页面:用户能看到每一步,随时接管;agent 驱动的就是用户眼前那个窗口。</p>
    </td>
    <td width="50%" valign="top">
      <h3>DOM 级驱动,框架友好</h3>
      <p><code>browser_snapshot</code> 返回带编号的交互元素;<code>browser_execute</code> 在页面内执行 JS(受控输入用原生 setter + input/change 事件),React/Vue 页面也能可靠交互。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>多标签会话</h3>
      <p>并行打开 URL,查看/切换/关闭/重置标签,每个会话的状态独立保持。</p>
    </td>
    <td width="50%" valign="top">
      <h3>多格式内容</h3>
      <p>以 html / markdown / txt / json 抓取页面,支持 CSS selector 限定、字符上限与超时控制。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>任务级会话隔离</h3>
      <p>每个 DSH 任务(会话)拥有独立的浏览器会话(独立标签页与历史),并发任务互不抢页面、互不污染;同一任务内多次调用复用同一会话。</p>
    </td>
    <td width="50%" valign="top">
      <h3>登录态持久化</h3>
      <p><code>browser_auth</code> 导出/恢复 cookie,重启后登录态不丢;自托管实例的 cookie 本身也落盘持久。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>人机验证识别</h3>
      <p>自动检测 Cloudflare / reCAPTCHA / hCaptcha / Turnstile 等挑战(<code>browser_challenge</code>,快照也会标注),提示人工在共享窗口完成,不再盲目重试。</p>
    </td>
    <td width="50%" valign="top">
      <h3>批量表单填充</h3>
      <p><code>browser_fill</code> 一次填写多个字段:按选择器/名称/标签匹配,支持受控输入、下拉、单选/复选,可选提交;单个字段失败不影响其余字段。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>操作历史与回放</h3>
      <p><code>browser_history</code> 记录操作日志(打开/执行/点击/输入/填表/下载/登录),<code>browser_replay</code> 可按序号回放某一步。</p>
    </td>
    <td width="50%" valign="top">
      <h3>带登录态下载</h3>
      <p><code>browser_download</code> 在页面上下文内携带会话 cookie 拉取文件并落盘,登录后才能访问的内容也能直接下载。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>安全限制</h3>
      <p><code>browser_restrict</code> 限制允许的浏览器动作(白名单),防止 agent 误点、误导航;只读工具(snapshot/content/screenshot)不受限。</p>
    </td>
    <td width="50%" valign="top">
      <h3>截图即存即读</h3>
      <p><code>browser_screenshot</code> 支持 <code>savePath</code> 直接落盘 PNG,交给视觉模型(modlens 等)做基于视觉的元素定位。</p>
    </td>
  </tr>
</table>

## 为什么选它

- **装好即用,零配置**:不需要桌面外壳、不需要额外启动步骤;纯 `dsh web` 环境自托管拉起 Electron 窗口,`browser_*` 工具照常可用。
- **人机协同,互不干扰**:用户能看到并接管 agent 的每一个动作;任务级会话隔离让多个并行任务各自拥有独立的标签页与历史。
- **面向真实世界的自动化**:人机验证识别、登录态持久化、批量填表、带登录态下载、操作回放、动作限制——把"真实浏览器"变成可靠的 agent 能力。
- **可测试、可替换的架构**:provider 与 Electron 通过 `ElectronBrowserViewHost` 接缝解耦,同一套工具层未来可对接无头转播 provider,无需改动模型侧。

## 工具参考

| 工具 | 用途 | 守卫 |
| --- | --- | --- |
| `browser_open` | 打开 URL(可选新标签),返回页面快照 | ✅ |
| `browser_wait` | 等待页面加载完成(可选期望 URL / CSS 选择器),返回是否就绪 | – |
| `browser_snapshot` | 交互元素(输入框/按钮/链接)带编号清单(穿透同源 iframe 与 Shadow DOM) | – |
| `browser_a11y` | 无障碍树:每个交互节点的语义角色/名称/值/状态 + 坐标(穿透同源 iframe 与 Shadow DOM) | – |
| `browser_execute` | 在页面执行 JS;参数以 `arguments[0..n]` 传入 | ✅ |
| `browser_content` | 以 html / markdown / txt / json 抓取页面(selector、maxChars、timeoutMs) | – |
| `browser_click` | 点击:语义目标(`target`: css/text/xpath,滚动到元素并点中心)或视口坐标(配合截图视觉定位) | ✅ |
| `browser_type` | 输入文本(可先按 `target` 聚焦元素;CDP `Input.insertText`) | ✅ |
| `browser_key` | 按命名按键(Enter/Tab/方向键/Home/End 等) | ✅ |
| `browser_scroll` | 滚动页面(像素增量 / 选择器定位 / 顶部底部) | ✅ |
| `browser_back` | 页面历史后退一步(无前项时为空操作) | ✅ |
| `browser_forward` | 页面历史前进一步(无后项时为空操作) | ✅ |
| `browser_refresh` | 刷新当前页(等价浏览器的刷新按钮) | ✅ |
| `browser_fill` | 批量填充表单(选择器/名称/标签匹配,受控输入、下拉、单选/复选,可选提交) | ✅ |
| `browser_set_value` | 单个控件设值(按 `target` 定位;原生 setter + input/change,React 受控输入可用) | ✅ |
| `browser_check` | 勾选/取消勾选 checkbox 或 radio(按 `target` 定位) | ✅ |
| `browser_select` | 选中 `<select>` 的某个选项(按值/文本/索引,按 `target` 定位) | ✅ |
| `browser_clear` | 清空输入/文本域/contenteditable,或取消勾选(按 `target` 定位) | ✅ |
| `browser_get_value` | 读取元素当前值(操作后验证用;按 `target` 定位) | – |
| `browser_scrape` | 结构化提取:容器选择器 + 字段映射(`选择器[@属性]`),静态 CSS 查询、CSP 安全 | – |
| `browser_screenshot` | 截图,可选 `fullPage`、`savePath`、JPEG(`format`/`quality`)与缩放(`maxWidth`/`maxHeight`);`savePath` 与下载同一准入门(限定在 `downloadDir` 内、不覆盖已有文件) | – |
| `browser_list_tabs` | 当前会话的标签列表 | – |
| `browser_switch_tab` | 按 id 切换标签(自托管下同步切换可见视图) | ✅ |
| `browser_close_tab` | 按 id 关闭标签;关闭活动标签后激活下一个 | – |
| `browser_reset` | 关闭本任务所有标签,回到一个空白标签 | ✅ |
| `browser_session` | 查看本任务的浏览器会话与标签 | – |
| `browser_reset_session` | 关闭并重建本任务的浏览器会话 | ✅ |
| `browser_history` | 操作日志(最新在后),含成功/失败与结果摘要 | – |
| `browser_replay` | 按序号回放某一步(navigate/execute/click/type) | ✅ |
| `browser_download` | 带会话 cookie 下载 HTTP(S) URL 到本地文件(`savePath` 必须绝对路径且位于 `downloadDir` 内,不覆盖已有文件,上限 256MB) | ✅ |
| `browser_auth` | 导出/恢复 cookie(登录态持久化,自托管可用) | ✅ |
| `browser_challenge` | 检测人机验证(CAPTCHA / Cloudflare / reCAPTCHA / hCaptcha / Turnstile) | – |
| `browser_restrict` | 限制允许的浏览器动作(白名单;空列表解除)。**软护栏**,模型可自行解除,非安全边界 | – |

> 「守卫」列:打 ✅ 的动作受 `browser_restrict` 白名单约束;只读工具(snapshot/content/screenshot/list_tabs/session/challenge/history)永不拦截。

### 等待页面就绪

- **`browser_open`/导航已有界等待新文档解析完成**(`readyState` + 文档指纹,不把同 URL 重载或 A→B→A 重定向误判成旧文档),但仍**不等异步内容**:慢站点或依赖 XHR 渲染的页面,请在 `browser_snapshot` 之前先 `browser_wait`——传 `url`(你打开的地址)与可选的 `selector`,等它返回 `ready: true` 再拍照,否则拍到的是旧页面或白屏/空元素列表。
- 页面里看不到的内容先想 iframe / Shadow DOM:快照与无障碍树会穿透同源 iframe 与 shadow root 并标注 `(iframe)`,坐标始终是顶层文档坐标,可直接用 `browser_click`;DOM 选择器则是 frame 作用域的,需用 `browser_execute` 经 `iframe.contentDocument` 访问。

### 语义定位(`target`)与无障碍树

- **`browser_a11y` 是理解页面的首选**:它返回每个交互节点的语义角色(button/textbox/checkbox…)、可访问名称、当前值、状态(enabled/checked/expanded…)与坐标,比编号快照更能说明“这是什么、能做什么”;拿到坐标后可直接 `browser_click`/`browser_type`。
- **`browser_click`/`browser_type` 支持 `target` 定位**:`{by: css|text|xpath, value, index?}`——`text` 按元素自身可见文本匹配(精确优先、退化包含、最深元素优先);点击会把元素滚动到视口中央再点;输入会先聚焦该元素。
- **单控件操作用 `browser_set_value`/`browser_check`/`browser_select`/`browser_clear`/`browser_get_value`**,批量用 `browser_fill`,列表页结构化抓取用 `browser_scrape`。

### 操作纪律(点击/填表)

- **优先用 DOM 语义而非坐标**:表单提交优先 `form.requestSubmit()`;点击优先 `element.click()`;坐标点击是最后手段。
- **选中正确的元素**:页面常有隐藏副本(如移动端按钮),用 `browser_execute` 过滤可见元素(`getBoundingClientRect()` 宽高 > 0、`getComputedStyle` 非 `di