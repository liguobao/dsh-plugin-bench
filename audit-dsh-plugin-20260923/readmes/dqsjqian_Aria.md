<div align="center">

# ⚡ Aria

**为工业级跨平台软件而生的现代 C++ MVVM 框架** · 支持 C++23（最低 C++20） · 响应式 · 协程优先

一套 C++ 核心，六大平台。以优雅架构承载复杂业务，以工程契约支撑长期演进。

Windows / macOS / Linux / iOS / Android / Web

[![支持 C++23](https://img.shields.io/badge/C%2B%2B-23%20supported-blue.svg)](https://en.cppreference.com/w/cpp/23)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/dqsjqian/Aria/actions/workflows/ci.yml/badge.svg)](https://github.com/dqsjqian/Aria/actions/workflows/ci.yml)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20iOS%20%7C%20Android%20%7C%20Web-lightgrey.svg)](#)

[English](README.en.md) | [简体中文](README.md)

</div>

---

## 📚 从入门到精通：AriaTutorial

想系统地学 Aria？配套教程仓库 **[AriaTutorial](https://github.com/dqsjqian/AriaTutorial)** 提供 20 章中英双语渐进式教程，**每一章都配一个可以编译、可以运行的最小 demo**。

- 正文里每个代码块都与 `demos/` 下的源文件**逐字一致**，不是手抄的示意代码；
- 每段输出都是 demo 在 Windows / MSVC 下的**真实 stdout**，并由脚本自动校验；
- 每章配一张结论图（数据流 / 依赖图 / 状态机 / 时间线），图里的数字同样取自 demo 的真实运行结果；
- 教学路径覆盖：响应式核心 → 集合与表单 → 绑定与适配器 → 异步、诊断与测试 → 一个完整应用。

## 🌟 旗舰示例：AriaTools

想先看 Aria 如何落到真实应用？请从 [AriaTools](https://github.com/dqsjqian/AriaTools) 开始。它是 Aria 唯一的旗舰跨平台示例，同一份 C++ ViewModel 驱动 Qt、iOS、Android 与 Web 四端。本仓库只保留框架、验收测试和文档中的最小代码片段。

## 🚀 30 秒看懂 Aria

Aria 把一个界面切成两半：**ViewModel** 是纯 C++，不认识任何 UI 库；**View** 是各平台原生控件。
中间由 `BindingEngine` 连接，它只认 `IViewAdapter` 这个接口，所以换平台只换适配器。

**上半 —— ViewModel（纯 C++，可单元测试，所有平台共用这一份）**

```cpp
// AA 制账单：总额 ÷ 人数 = 每人多少
struct BillViewModel {
    aria::Property<double> bill{100.0};   // 可读写的状态
    aria::Property<int>    people{2};

    // Computed 是只读派生值。它的依赖不用手写：首次求值时读到了
    // bill 和 people，就自动记下这两个依赖。
    aria::Computed<double> per_person{[this] {
        return bill.get() / people.get();
    }};
};
```

这段代码里没有一行 UI，也没有 `#include` 任何界面库 —— 它在命令行下就能测。

**下半 —— View 侧接线（每个平台十几行，界面本身仍用各平台原生方式写）**

先说清最容易误会的一点：**界面不用 C++ 写。** 按钮、布局、动画照旧用 Qt Designer、
Storyboard、Compose、HTML 写。下面这十几行只是"把已经存在的控件交给 engine"的接线代码，
三步永远一样 —— ① 造平台适配器 ② 用它造 `BindingEngine` ③ 把控件和 Property 绑上。

<details open>
<summary><b>Qt6</b>（Windows / macOS / Linux · 纯 C++）</summary>

```cpp
auto adapter = std::make_shared<aria::adapters::qt6::QtAdapter>();
aria::binding::BindingEngine engine{adapter};

BillViewModel vm;
// label_view 包住你在 Qt Designer 里拖出来的那个 QLabel
aria::adapters::qt6::QtView label_view{real_label};
engine.bind_text_projected(vm.per_person, label_view,
    [](double v) { return std::format("¥{:.2f}", v); });
```
</details>

<details>
<summary><b>iOS / UIKit</b>（接线文件是 Objective-C++ <code>.mm</code>，界面仍是 Storyboard / SwiftUI）</summary>

```objc++
#import "aria/adapters/uikit/UIKitAdapter.hpp"

auto adapter = std::make_shared<aria::adapters::uikit::UIKitAdapter>();
aria::binding::BindingEngine engine(adapter, ui_dispatcher,
    aria::binding::BindingEngine::DispatchPolicy::SmartMarshal);

// 把 Storyboard 里的 UILabel* 包一层，C++ 侧就能绑它
auto label = std::make_shared<aria::adapters::uikit::UIKitView>(self.totalLabel);
engine.bind_text_projected(vm.per_person, *label,
    [](double v) { return std::format("¥{:.2f}", v); });
```

`UIKitView` 用 ARC 强引用持有 `UIView*`，析构时会在原生 view 还活着的时候通知
`BindingEngine` 清理订阅，所以不会回调到已释放的控件上。
</details>

<details>
<summary><b>macOS / AppKit</b>（同上，<code>.mm</code> + NSView）</summary>

```objc++
#import "aria/adapters/appkit/AppKitAdapter.hpp"

auto adapter = std::make_shared<aria::adapters::appkit::AppKitAdapter>();
aria::binding::BindingEngine engine(adapter, ui_dispatcher,
    aria::binding::BindingEngine::DispatchPolicy::SmartMarshal);

auto label = std::make_shared<aria::adapters::appkit::AppKitView>(self.totalField);
engine.bind_text_projected(vm.per_person, *label, /* ... */);
```
</details>

<details>
<summary><b>Android</b>（界面写 Kotlin / Compose，C++ 只接线）</summary>

```cpp
// 在 Android UI 线程上调用，传进来的是真实的 android.view.View 对象
auto adapter = std::make_shared<aria::adapters::jni::JniAdapter>(env);
aria::binding::BindingEngine engine(adapter);

aria::adapters::jni::JniView total_view(env, total_text_view);
engine.bind_text_projected(vm.per_person, total_view,
    [](double v) { return std::format("¥{:.2f}", v); });   // → TextView
```

Kotlin 侧的监听器把原生事件转发回来（`adapter->notify_text_changed(...)` /
`notify_click(...)`），**监听器归属仍在 Android 侧**，C++ 这边保持强类型。
Compose 没有可寻址的 view 对象，用文档里的 side-channel 形态。
</details>

<details>
<summary><b>Web</b>（浏览器里没有 C++ —— 前端是 HTML/JS，C++ 跑在服务端）</summary>

```cpp
aria::adapters::http::HttpAdapterConfig config;
config.port = 9090;
auto http = std::make_shared<aria::adapters::http::HttpAdapter>(config);

// "控件"在这里是字符串 ID，对应浏览器里的 DOM 元素
auto& total = http->register_view("total", "text");

aria::binding::BindingEngine engine{http};
engine.bind_text_projected(vm.per_person, total,
    [](double v) { return std::format("¥{:.2f}", v); });
http->start();  // Property 变化经 SSE 推给浏览器，用户操作经 REST 回来
```
</details>

**这才是重点**：五份接线代码长得几乎一样，而上面那个 `BillViewModel` **一个字都没改过**。
你换平台换的是这十几行，不是业务逻辑。

**接线之后 —— 只改数据，界面自己跟着变**

上面每个平台绑完，剩下的事就跟平台无关了。下面这段在五个平台上行为完全一致，
**没有一行手写的刷新代码**：

```cpp
BillViewModel vm;                       // per_person = 100/2 = ¥50.00
// ... 按上面任意一个平台绑定到 label ...

vm.people = 4;                          // label → ¥25.00
vm.bill   = 200.0;                      // label → ¥50.00
```

改 `bill` 或 `people` 任意一个，`per_person` 都会重算并推给 label —— 因为它的依赖是
`Computed` 首次求值时自动记下的，你没写过任何"people 变了要更新 label"这类代码。

连续改多个值时有一个细节值得知道：

```cpp
// 逐个改 → 每次都推一次，label 会闪过中间值
vm.bill = 300.0;    // label → ¥150.00  ← 中间态
vm.people = 4;      // label → ¥75.00

// 包进 batch → 只在结束时推一次，不出现中间态
aria::reactive::batch([&] {
    vm.bill   = 1200.0;
    vm.people = 8;
});                 // label → ¥150.00（一次）
```

还有一条省心的默认行为：**如果最终结果和当前值相同，一次通知都不会发。**
比如上面之后再 `batch` 里设 `bill=600, people=4`（仍是 150），label 不会被打扰。

整个架构一张图看全——上半是纯 C++ 的 ViewModel，中间是 `BindingEngine`（只认 `IViewAdapter` 接口），下半是五个原生适配器：

![Aria 架构总览](docs/marketing/images/aria-arch.png)

继续阅读：[绑定指南](docs/guide/binding.md) · [各平台适配器指南](docs/guide/adapters/) · [Cookbook](docs/cookbook/README.md) · [AriaTools](https://github.com/dqsjqian/AriaTools)（Qt / iOS / Android / Web 四端完整应用）。

## 🎯 设计理念与工程实力

Aria 将**响应式状态、异步协程与跨端绑定统一为独立于 UI 工具包的现代 C++ 架构**，让复杂业务只实现一次，让各端界面充分发挥原生能力。

优雅来自清晰的分工：ViewModel 是普通 C++ 类，无需继承框架基类、编写宏或运行代码生成器；
UI 通过 `IViewAdapter` 接入。Qt6 / AppKit / UIKit / JNI / HTTP 五个适配器共享同一套绑定协议，切换 UI 工具包无需改写 ViewModel。

**以世界级工业软件的工程标准打造 C++ 框架**：把生命周期、线程、错误处理与集合事件写成可追踪的[工程契约](docs/index.md#reference)，用自动化测试、模糊测试和可复现的[性能基准](docs/reference/performance.md)检验实现。架构之美，落实到每一次状态更新、异步取消与跨端交付。

| 架构优势 | 工程设计 |
|---|---|
| **现代 C++ 基础** | 最低 C++20，支持 C++23，使用完整的协程与 concepts 能力（GCC 12+ / Clang 15+ / MSVC v143）；集成项目需采用 C++20 或更高标准。 |
| **原生 UI 自由** | 控件、布局和动画交给所选 UI 工具包，Aria 统一状态与界面之间的单向/双向数据流；共享业务核心，各端保留原生体验。 |
| **分层兼容策略** | `aria-abi` / `aria-runtime` / `aria-binding` 在主版本号内保持 ABI 稳定，要求编译器、标准库与构建选项一致；`Property<T>` 等模板及其宿主类型更新后需重新编译。 |
| **开放适配协议** | Qt6 / AppKit / UIKit / JNI / HTTP 开箱可用；其他 UI 工具包通过实现 `IViewAdapter` 接入（见[适配器指南](docs/guide/adapters/)）。 |
| **应用实践与开发资料** | AriaTools、AriaAgent 与 OpenRead 展示跨端工作台、Agent GUI 和阅读引擎中的应用实践；[指南](docs/index.md)、[Cookbook](docs/cookbook/README.md) 与工程契约覆盖从入门到扩展的开发路径。 |

**为共享 C++ 业务核心、原生多端 UI 和长期维护而设计。** Aria 负责业务与状态层，控件渲染与界面复用由所选 UI 工具包负责；两层通过明确的适配协议协作。

## ✨ 核心特性

- 📦 **模板化响应式核心** —— `Property<T>` / `Computed<T>` / `Effect` / `Command<>` / `ObservableList<T>` / `Validator<T>` 共享同一个响应式依赖图引擎。`Computed` 自动跟踪依赖，`reactive::batch` / `reactive::untracked` 精确控制通知范围。
- 🔌 **共享基础库与 ABI 层** —— `aria::core` 自动链接 `aria::abi`，统一跨动态库的响应式图、诊断和信号存储。ABI 要求一致的编译器、标准库、构建选项和主版本；模板及其宿主类型在更新后需要重新编译。
- ⚡ **C++ 协程** —— `Task<T>`、执行器、`co_await schedule_on(pool)`，异步代码写起来像同步代码。
- 🖥 **适配器抽象** (`IViewAdapter`) —— Qt6 / AppKit / UIKit / JNI / HTTP，任何 UI 工具包都能用同一套业务逻辑驱动。

## 🏗 架构（10 个模块）

```
┌────────────────────────────────────────────────────────────────────────┐
│                         应用层 (Application)                            │
└────────────────────────────────┬───────────────────────────────────────┘
              ┌────────────────