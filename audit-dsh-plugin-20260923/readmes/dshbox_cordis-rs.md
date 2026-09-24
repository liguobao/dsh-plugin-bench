# Cordis

**English** | [简体中文](https://github.com/dshbox/cordis-rs/blob/main/README.zh-CN.md)

[![CI](https://github.com/dshbox/cordis-rs/actions/workflows/ci.yml/badge.svg)](https://github.com/dshbox/cordis-rs/actions/workflows/ci.yml)

Cordis is a typed runtime for long-lived, plugin-oriented Rust applications.
It gives application components one model for lifecycle, service dependencies,
typed events, resource cleanup, and explicit isolation boundaries.

Cordis is useful when your program is more than a collection of short-lived
function calls: plugins can appear and disappear, services can become available
or unavailable, configuration can change, and runtime resources must still be
cleaned up deterministically.

## Install

For applications, keep the historical package and import identity:

```toml
[dependencies]
cordis-rs = "0.8"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

```rust
use cordis::Context;
```

`cordis-rs` is now a thin application-facing facade over the v3 runtime contract.
Framework and plugin authors may depend on that contract directly:

```toml
[dependencies]
cordis-core = "0.3"
```

Optional capabilities stay explicit semantic dependencies:

```toml
cordis-timer = "0.3"
cordis-loader = "0.3"
```

Cordis v3 requires Rust **1.88** or newer and uses Rust 2024 Edition.

## Migrating from 0.6.x

`cordis-rs 0.8.x` is the current application-facing v3 release line. The v3
architecture first shipped on the `0.7.x` line. The `0.6.x` implementation remains
on the `legacy/0.6` maintenance branch for
critical bug and security fixes. The v3 transition is intentionally breaking;
see [`MIGRATION.md`](https://github.com/dshbox/cordis-rs/blob/main/MIGRATION.md) and [`docs/v3-migration.md`](https://github.com/dshbox/cordis-rs/blob/main/docs/v3-migration.md).

## The mental model

Five types carry most of the public model:

- **`Context`** — a cheap immutable view into one Cordis Runtime.
- **`Plugin`** — reusable behavior with typed source configuration and runtime input.
- **`FiberHandle`** — the lifecycle handle for one admitted non-root Fiber.
- **`Service`** — a typed, named capability published into an exact service realm.
- **`Event`** — a typed runtime communication contract with explicit routing.

A Plugin enters the Runtime through a deliberate boundary:

```text
Config
  │
  │ Plugin::prepare()
  ▼
Input
  │
  │ PreparedPlugin::from_input(...)
  ▼
PreparedPlugin
  │
  │ Context::spawn(...)
  ▼
FiberHandle / Fiber
```

`prepare()` runs before lifecycle admission. `spawn()` is the first operation
allowed to create Runtime lifecycle state.

## Quick start

The smallest complete flow is: define an Event, define a Plugin, prepare and
spawn it, dispatch the Event, then explicitly dispose the returned FiberHandle.

```rust
use std::convert::Infallible;

use cordis::event::{ListenerRegistrationError, observer_sync};
use cordis::{BoxError, Context, Event, Plugin, PreparedPlugin, Routing};

struct Ping;

impl Event for Ping {
    const NAME: &'static str = "ping";
    type Args = String;
    type Output = ();
}

struct Echo;
struct EchoInput;

impl Plugin for Echo {
    type Config = ();
    type Input = EchoInput;
    type PrepareError = Infallible;
    type ApplyError = ListenerRegistrationError;

    fn prepare(&self, (): ()) -> Result<Self::Input, Self::PrepareError> {
        Ok(EchoInput)
    }

    async fn apply(
        &self,
        ctx: Context,
        _input: &Self::Input,
    ) -> Result<(), Self::ApplyError> {
        let _listener = ctx.on::<Ping, _>(observer_sync(|_, name| {
            println!("hello, {name}");
            Ok::<_, Infallible>(())
        }))?;
        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<(), BoxError> {
    let ctx = Context::new();

    let plugin = Echo;
    let input = plugin.prepare(())?;
    let prepared = PreparedPlugin::from_input(plugin, input);
    let fiber_handle = ctx.spawn(prepared).await?;

    ctx.emit::<Ping>(Routing::Unscoped, "world".into()).await?;

    fiber_handle.dispose().await?;
    Ok(())
}
```

Run the repository's complete version with:

```bash
cargo run -p hello_plugin
```

## Lifecycle and convergence

A successful `Context::spawn()` returns a `FiberHandle` only after the new Fiber has
settled for the current service snapshot. The stable result is normally:

- **Active** — all required Services are available and `apply()` succeeded.
- **Pending** — a required Service is currently unavailable; `apply()` has not run.

Requirements are declared with `InjectSpec`. They are lifecycle prerequisites,
not constructor injection. When an exact required Service publication appears or
disappears, Cordis converges affected Fibers toward their new stable state.

A `FiberHandle` exposes the main lifecycle operations:

- `ready()` waits for the current stable state.
- `restart()` reapplies the current committed input on the same Fiber.
- `update(PreparedChange)` attempts a precommit-controlled typed input replacement; a committed update keeps the same Fiber.
- `era_swap(PreparedChange)` performs identity-breaking replacement; a successful successor has a fresh Fiber identity.
- `dispose()` ends the Fiber and runs its cleanup.

Dropping a `FiberHandle` does **not** dispose the Fiber. Lifecycle ownership is explicit.

Resources registered through a Plugin's apply `Context` are owned by that apply
generation. Listener registrations, Service publications, tasks, effects, and
timer operations can therefore be cleaned up with the generation instead of
being manually threaded through application code.


## Application teardown

Cordis deliberately has no Runtime-wide shutdown API. Applications retain the
delivered `FiberHandle`s they intend to end and call `dispose().await` during
normal shutdown. The demonstrated example Harness records handles in spawn order
and disposes them in reverse spawn order, attempt-all; that ordering is
application policy, not a hidden Fiber parent/child relation.

Dropping a `FiberHandle` or `Context` is ordinary Rust Drop, not lifecycle teardown,
and root-owned registrations do not disappear merely because Context clones are
dropped. See [Application teardown](docs/application-teardown.md) for the
complete demonstrated pattern, including repeated teardown, generation cleanup,
and Loader handoff ownership.

## Services: exact placement, not fallback lookup

A Service is identified by its semantic Service name and resolved from one exact
slot:

```text
(Service, ServiceRealm)
```

By default a Context uses the Runtime's default realm. Isolation changes the
realm selected for specific Service names.

To give one Service a fresh private slot:

```rust
let tenant_a = root.with_isolated_service(Database::NAME);
```

To isolate several Services, chain the operation:

```rust
let tenant_a = root
    .with_isolated_service(Database::NAME)
    .with_isolated_service(Cache::NAME)
    .with_isolated_service(Ledger::NAME);
```

Each call changes only that Service's placement. Other Service mappings are
inherited.

For explicit sharing and joining, allocate opaque realms and map Service names to
them:

```rust
let shared_metrics = root.new_service_realm();
let tenant_a_db = root.new_service_realm();
let tenant_b_db = root.new_service_realm();

let tenant_a = root.with_service_realms([
    (Database::NAME, tenant_a_db),
    (Metrics::NAME, shared_metrics.clone()),
])?;

let tenant_b = root.with_service_realms([
    (Database::NAME, tenant_b_db),
    (Metrics::NAME, shared_metrics),
])?;
```

Now the tenants resolve different Databases but the same Metrics slot.

A `ServiceRealm` is only an opaque Runtime-local placement identity. It has no
hierarchy, parent lookup, textual rendezvous, or fallback rule. If a Context maps
`Database` to a private realm and that realm has no visible Database publication,
lookup is unavailable; Cordis does not fall back to the default realm.

## Events: typed communication with explicit Scope routing

An `Ev