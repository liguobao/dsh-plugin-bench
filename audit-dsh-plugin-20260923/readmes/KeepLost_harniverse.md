# Harniverse

English | [中文](README.zh.md)

Harniverse is a source-first downstream of [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) maintained in this repository. It preserves the Cordis-powered **everything is a plugin** architecture while composing Harniverse-specific capabilities and security policy through the same plugin seams.

Harniverse has no independent npm release yet. `npx @deepseek-ai/dsh` installs the official DeepSeek Harness package, not this downstream. Use the source workflow below for Harniverse.

## Quick start

This tutorial starts with a new machine and ends when the Web UI receives its first model response.

### 1. Check the prerequisites

Install:

- Git 2.26 or newer.
- Node.js 22.19.x, or Node.js 24 or newer.
- pnpm 11.7.0. The repository pins this version through `packageManager`; enable Corepack or install pnpm through its official installation method if `pnpm --version` is unavailable.

Verify the tools before cloning:

```sh
git --version
node --version
pnpm --version
```

You do not need a model API key to install or start the Web UI. You configure a provider after signing in.

<a id="run-from-source"></a>

### 2. Install Harniverse from source

```sh
git clone https://github.com/KeepLost/harniverse.git
cd harniverse
pnpm install
pnpm run build
```

The build produces the Host, Client, and Web frontend artifacts used by the source launcher. Keep this checkout: the commands below run Harniverse through its root `pnpm dsh` script.

### 3. Start the Web UI

In terminal A, from the Harniverse checkout:

```sh
pnpm dsh --profile web
```

The first run initializes the `web` profile and prints the live URL. The default is `http://127.0.0.1:3080`. Keep terminal A running and open the printed URL in a browser.

Runtime profiles, authentication Grants, credentials, settings, and sessions live under `$DSH_HOME`, which defaults to `~/.dsh`.

### 4. Approve the first browser

The browser opens the device-pairing page before it loads the application:

1. Enter a device name of 1-64 letters or numbers, with optional spaces, dots, underscores, or hyphens. Unicode names such as `我的设备` are accepted.
2. Select **Pair personal device**.
3. Keep the page open while it displays the approval code and request id.

In terminal B, from the same checkout and as the same operating-system user, approve that request as the first owner:

```sh
pnpm dsh auth device approve <request-id> --profile owner
```

List pending requests if you need to recover the id:

```sh
pnpm dsh auth device list
```

The browser polls the request and enters the application automatically after approval. The page shows the installed-form command as `dsh auth ...`; source users run the same command through `pnpm dsh auth ...`.

Both terminals must resolve the same `DSH_HOME`. If you override it, apply the same value to the Web and auth commands; otherwise the auth command cannot see the browser request.

List approved devices and API clients with `pnpm dsh auth grant list`; unlike `device list`, this command shows committed Grants with their id, name, kind, capabilities, and expiry. An authenticated owner browser can also open `/auth/manage` on the same Web origin, for example `https://127.0.0.1:3000/auth/manage`, to inspect pending requests and approved Grants. Authentication activity is retained as owner-only JSONL under `$DSH_HOME/auth/access.jsonl`; follow it while testing with:

```sh
tail -f "${DSH_HOME:-$HOME/.dsh}/auth/access.jsonl"
```

The Web profile prints a trust-policy line and connection/authentication events to its server terminal. Each event includes the method or channel, path, peer address, Host, Origin, and the non-secret Grant name/id when known; cookies, Authorization values, public keys, and request bodies are never printed. The owner-only audit file remains the durable privacy-minimal record.

### Pair with an invitation code

Instead of approving the first browser in a terminal, an owner can pre-issue one-time enrollment invitations. Submit the device form on the pairing page, then enter the invitation where the page offers it; pairing completes immediately without the terminal approval.

Issue an invitation on the host (`--profile` and `--capability` are mutually exclusive and exactly one is required):

```sh
pnpm dsh auth code issue --ttl 30m --profile owner
```

`--ttl` accepts `30s`, `5m`, `12h`, `7d`, or raw milliseconds, and sets how long the invitation stays redeemable. `--profile` selects the Grant profile the redeemed invitation grants (`observer`, `operator`, `administrator`, or `owner`); `--capability` grants explicit `harniverse.*` capabilities instead, which requires an already-active authorizing Grant, so a fresh installation issues its first invitations with `--profile owner`. `--kind temporary` yields a Grant that expires after a fixed lifetime, goes idle after a fixed timeout, and cannot carry `harniverse.authorize`; the default `device` kind persists like an approved browser. `--bind <name>` requires that exact device name at redemption, and `--count <n>` issues several invitations in one command.

Each invitation prints one tab-separated line: token, id, kind, capabilities, and expiry. The token starts with `dshi1_` and is shown only when issued. List retained invitations, and revoke one before it is redeemed, with:

```sh
pnpm dsh auth code list
pnpm dsh auth code revoke <code-id>
```

### 5. Configure and select a model

A new installation has no usable model route until you configure one:

1. Open **Settings → Models**.
2. Select **Add provider** for an installed catalog provider, or **Add a custom provider** for an OpenAI-compatible endpoint.
3. Enter the required credential and save the provider.
4. Select one of that provider's models in the model picker.

The provider becomes available without restarting Harniverse. Keys saved through the UI are write-only: the credential store keeps the secret under `$DSH_HOME/.credentials.yaml`, while settings retain its reference. See [Configure models](docs/user/guide/providers.md) for native credentials, custom endpoints, and model capabilities.

### 6. Choose a workspace and run the first task

Select **Choose workspace**, add the project directory Harniverse may operate on, and select it. A fresh Web UI deliberately has no selected workspace, and the composer remains unavailable until both a workspace and model are selected.

Create a session and send:

> Summarize this workspace and list its main components.

Receiving the assistant response completes the first-run path. The active permission policy asks for approval before protected operations.

## Daily use and updates

After the first setup, start the same checkout with:

```sh
cd harniverse
pnpm dsh --profile web
```

Stop it with `Ctrl+C`. Browser Grants, provider settings, profiles, and sessions remain in `$DSH_HOME`.

After updating the checkout, refresh dependencies and all runtime artifacts before starting it again:

```sh
git pull
pnpm install
pnpm run build
pnpm dsh --profile web
```

## Headless use

The headless profile uses the same Harniverse home, provider settings, and credential store. After configuring a model, run one task without the Web UI:

```sh
pnpm dsh --profile headless "Summarize the current project"
```

The invoking directory is the default workspace for headless execution. The command prints the final assistant response and exits.

## Network security

Authentication remains enabled on the default loopback listener. Do not use `--dangerously-skip-authentication` as an installation shortcut. Non-loopback listeners require a TLS certificate and key; see the [Web UI guide](docs/user/guide/index.md#remote-access) before exposing Harniverse to another machine.

For a container whose published port requires `0.0.0.0`, use the container launcher instead of invoking the Web profile directly:

```sh
pnpm run web:container -- --port 3000
```

`web:container` is not another profile or Web c