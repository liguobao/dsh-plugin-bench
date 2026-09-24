# deepseek-harness-sdk

English | [中文](README.zh.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Language](https://img.shields.io/badge/language-Rust-orange)](Cargo.toml)
[![crates.io](https://img.shields.io/crates/v/deepseek-harness-sdk)](https://crates.io/crates/deepseek-harness-sdk)

See the [CHANGELOG](CHANGELOG.md) for the release history.

Rust client SDK for the [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)
(DSH) runtime. The runtime is the `dsh` CLI booted under a named profile —
this crate spawns it as a subprocess (`dsh --profile sdk`, the profile
default) and speaks its stdio JSON-RPC 2.0 protocol. One crate, two layers:
the high-level Python-parity API (`DeepSeekHarness` / `Session::run` /
`RunResult`) and the low-level protocol client (`HarnessClient`).

The crate is the design twin of the official
[Python SDK](https://github.com/deepseek-ai/deepseek-harness), sharing the
same runtime peer, wire protocol, and layering; the Python SDK surface is the
alignment baseline for every public type and error. The TypeScript SDK's
divergences are documented (notably `RunResult`, see below), as are the
crate's own deliberate divergences from both references (see
[Deliberate divergences](#deliberate-divergences)).

This crate is a **pure client**. It contains no agent, LLM, or persistence
logic — the spawned runtime process does all of that. The runtime is
bring-your-own: this crate never downloads, bundles, or ships one (see
[Runtime acquisition](#runtime-acquisition)).

## Installation

```sh
cargo add deepseek-harness-sdk
```

or in `Cargo.toml`:

```toml
[dependencies]
deepseek-harness-sdk = "*"
```

Pick the version that suits you (`cargo search deepseek-harness-sdk` or the
[crates.io page](https://crates.io/crates/deepseek-harness-sdk) shows the
latest). While the crate is on a pre-release line, a bare
`cargo add deepseek-harness-sdk` may not resolve to the newest pre-release —
request it explicitly (e.g. `cargo add deepseek-harness-sdk@0.1.0-alpha`) when
you want it. The API may still change before `0.1.0`.

Two prerequisites before the first run: a DSH runtime (see
[Runtime acquisition](#runtime-acquisition)) and model credentials
(`DEEPSEEK_API_KEY` in the environment, or `Config::api_key` /
`Config::base_url`).

## Quickstart

```rust
use deepseek_harness_sdk::{Config, DeepSeekHarness, Input};
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut harness = DeepSeekHarness::start(Config {
        dsh_bin: std::env::var("DSH_RUNTIME_BIN").ok(),
        request_timeout: Some(Duration::from_secs(120)),
        ..Config::default()
    })
    .await?;

    let session = harness.start_session(None);
    let result = session
        .run(Input::Text("Reply with exactly: ok".into()), None)
        .await?;

    println!("finish_reason: {:?}", result.finish_reason);
    println!("final_response: {}", result.final_response);

    harness.close().await?;
    Ok(())
}
```

`DeepSeekHarness::start` is eager: it resolves the runtime, resolves (and
creates) the harness home, spawns the subprocess, and completes the
`initialize` handshake before returning. The runtime inherits
`DEEPSEEK_BASE_URL` / `DEEPSEEK_API_KEY` from the environment unless the
crate injects overrides, so callers can use real model endpoints directly or
point those variables at a local proxy.

## Runtime acquisition

The runtime is bring-your-own; the SDK only resolves and launches it. There
is **no separate JSON-RPC agent program**: the stdio JSON-RPC server the SDK
talks to is a plugin row inside the runtime's profile bundle. The runtime is
the ordinary `dsh` CLI from
[deepseek-harness](https://github.com/deepseek-ai/deepseek-harness), booted
under the `sdk` profile (or any profile you name via `Config::profile`).

Three routes to a runtime:

### Route A — the npm-published CLI (recommended)

```sh
npm install -g @deepseek-ai/dsh
export DSH_RUNTIME_BIN="$(command -v dsh)"
```

The `dsh` CLI is published on npm as `@deepseek-ai/dsh`. A bare
`npm install -g @deepseek-ai/dsh` installs the `latest` dist-tag, which can
lag behind upstream's newest release; `npm install -g @deepseek-ai/dsh@alpha`
tracks the newest. This crate's CI verifies the npm route with a keyless
handshake on every pull request, and the exact version under test lives in
`.github/workflows/ci.yml`.

The installed bin is a Node.js script, so **Node.js must be on `PATH`** for
the SDK to launch it. The crate spawns the resolved program directly without
a shell, and the npm bin is a Node.js script rather than a native executable
— on Windows, prefer the self-contained wheel route (Route B).

### Route B — the platform wheel (self-contained, no Node.js)

```sh
python -m pip install deepseek-harness-runtime-bin
export DSH_RUNTIME_BIN="$(python -c 'import deepseek_harness_runtime as r; print(r.bundled_runtime_path())')"
```

The `python -c` invocation only *locates* the installed executable and prints
its path — **no Python runs at SDK runtime**. The SDK launches the executable
directly (always injecting the resolved `DSH_HOME`, so the home is explicit
even on first boot).

The wheel ships the runtime as a self-contained single-file executable — no
system Node.js needed at runtime (the plugin tree is embedded) — and installs
the normal `dsh` CLI as `deepseek-harness-sdk-runtime-<platform>-<arch>`.
Published targets are **Linux x64, Linux arm64, macOS arm64, macOS x64, and
Windows x64** (Windows uses the `.exe` suffix); no Windows arm64 wheel is
published. macOS needs its sibling `-spawn-helper` beside the executable
(`node-pty`), and the Linux/macOS wheels carry a `-rg` ripgrep sidecar
(Windows `-rg.exe`) — copy any sidecar along when you relocate the executable.
Because the wheel needs no system Node.js at runtime, it stays the fallback
for Windows and for users who cannot install Node.js.

### Route C — build from source

Build the runtime executable from source with the
`build-exe-for-python-sdk` script from the
[official repository](https://github.com/deepseek-ai/deepseek-harness), then
point `DSH_RUNTIME_BIN` (or `Config::dsh_bin`) at the built executable.
Building from source is the only route that reproduces the upstream ref
the contract specs are frozen at (`git checkout c389f96bf3` in the
official repository before building) — the specs' citation basis, distinct
from the runtime version under test, which CI owns via its own pin in
`.github/workflows/ci.yml`. Building from source is also the route for any
platform that has no published wheel.

### How the SDK resolves the runtime

1. `Config::dsh_bin` (non-empty);
2. `DSH_RUNTIME_BIN` from the parent environment (non-empty);
3. otherwise `Error::RuntimeNotFound`, whose message names the acquisition
   routes and cites the official repository.

An empty `Config::dsh_bin` and an empty `DSH_RUNTIME_BIN` both count as
absent, so resolution never produces an unlaunchable empty program.
`DSH_RUNTIME_BIN` is **explicitly preserved** after the `runtime_bin` →
`dsh_bin` rename: it is a supported product surface, not a compatibility
shim for a removed field.

The launch argv is exactly `--profile <profile>` (default `"sdk"`) followed
by one `--patch <absolute path>` pair per configured `Config::patches` entry,
in caller order. Patch paths are resolved absolute before spawn. The crate
never passes application arguments and never emits the diagnostic
`--dump-config` / `--dump-default-config` subcommands. An empty `profile`
is rejected locally before spawn.

## `DSH_HOME` resolution

The harness home resolves with the **runtime's own precedence**, highest
first:

1. an explicit `Config::dsh_home`;
2. a **non-empty** `$DSH_HOME` (first from `Config::env`, then inherited from
   the parent environment) — blank or whitespace-only counts as **unset**;
3. `~/.dsh`.

The resolved home is normalized to an absolute path with `~` expanded, is
created when absent so a fresh