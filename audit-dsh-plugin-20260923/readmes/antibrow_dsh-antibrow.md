# dsh-antibrow

A [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) plugin that
gives the agent a browser with an identity.

The browser is [AntiBrow](https://antibrow.com): a Chromium fork with fingerprint
configuration at engine level, driven through the standard Playwright API. SDK docs are
at [antibrow.com/docs](https://antibrow.com/docs), and the dated detection measurements -
including the checks that fail - are at [antibrow.com/reports](https://antibrow.com/reports).

```
dsh plugin --profile <name> add dsh-antibrow
```

## Why not a plain browser plugin

Every other browser plugin hands the agent a fresh Chromium. That is fine for
reading a public page and useless for anything behind a login: the session dies
with the process, the fingerprint is a stock automation build, and the traffic
leaves from your machine.

| | A plain Playwright plugin | dsh-antibrow |
|---|---|---|
| Identity between runs | new browser every time | one persistent profile per name |
| Logins | gone when the process ends | cookies and passkeys persist, optionally synced across machines |
| Fingerprint | stock build, patched from page scripts | spoofed inside the engine, before any page script runs |
| Egress | your own IP | residential proxy, with timezone, language and reported connection following its exit |
| Parallel identities | one data directory to share | one isolated profile per agent or per account |
| Tabs | start from nothing | last session restored, so the agent resumes where it stopped |

The difference shows up the first time an agent has to *be someone*: check a
mailbox, watch a dashboard, keep a marketplace account warm. A browser with no
memory has to log in again on every run, and logging in again is exactly what a
site treats as suspicious.

## What it brings

- **Unlimited profiles, on the free tier.** Not five, not fifty - profiles live
  on your disk, not on a plan, and creating one costs nothing. Give every
  account, every marketplace, every persona its own browser and stop reasoning
  about which cookie jar the agent is holding. Syncing them between machines and
  the managed residential proxies are the paid parts; the profiles themselves
  never are.
- **16 tools** for the model: sessions, profiles, proxies, page control, live
  view. All under `mcp__antibrow__*`, all reachable from Code Mode as ordinary
  async calls.
- **An Android phone, from the same API.** One argument - `deviceType:
  'android'` - and the agent is a phone: touch points, mobile client hints,
  phone viewport, phone GPU. See below.
- **Engine-level spoofing.** The user agent, platform, screen, fonts, canvas,
  WebGL and audio are answered by the engine itself. Nothing is injected into
  the page, so there is no injected script for a detector to find.
- **A coherent story, not a pile of overrides.** Timezone, locale and the
  reported network profile are derived from the proxy's real exit, because a US
  IP that reports Shanghai time is a contradiction a page can check in one line.
- **Passkeys survive.** WebAuthn credentials are stored with the profile, not in
  the machine's keychain, so a passkey registered on one run still signs in on
  the next - and, with sync on, on another computer.
- **Watch it work.** `start_live_view` streams the agent's browser to a
  dashboard, so a long unattended run is something you can look at instead of
  guess about.
- **Identities from real machines.** On a paid plan a profile can be minted from
  a captured real-device fingerprint rather than a generated one - a whole
  coherent row off one physical machine, not a field-by-field invention.
- **Four builds, three operating systems**: Windows, macOS, and Linux on both
  x86_64 and arm64. The same profile runs on any of them.
- **Portable, and not only to agents.** Export a profile as a file and import it
  on another machine; leave it unsynced and it is still there, in the desktop
  app, for a human to open and finish by hand. The agent's browser and yours can
  be the same browser.

### The phone

```json
{ "profile": "shop-mobile", "deviceType": "android", "temporary": true }
```

Android profiles are built from whole captured devices - the screen, the GPU
report and the client hints agree with each other because they came off the same
physical phone, and the plugin picks a row rather than assembling one. Three of
them ship inside the package, so a free-tier agent can create an Android profile
with no network round trip at all.

The device type is fixed when the profile is created and never drifts
afterwards: a profile that was a phone stays that phone. Android needs engine
151 or newer - if none is available the launch fails rather than quietly handing
you a desktop browser that claims to be a phone.

### Measured

On a macOS host, through a US residential proxy, 2026-08-15, engine 151:

| Check | Result |
|---|---|
| whoer.net disguise | 90% |
| creepjs headless signal | 0% |
| creepjs stealth signal | 0% |
| creepjs platform hints | `Arial, "Segoe UI"` - no font from the host |
| Reported platform vs user agent | agree (Win32 / Windows) |
| Timezone vs proxy exit | agree (America/Los_Angeles) |

The 10% whoer deducts is WebRTC, which had no route to a STUN server on that
run. Reproduce all of it with `tests/smoke` - the harness is in this repository,
and it fails loudly rather than printing a number nobody checks.

## Install

```
dsh plugin --profile <name> add dsh-antibrow
export ANTI_DETECT_BROWSER_KEY=<key>
dsh --profile <name>
```

## The tools

| | |
|---|---|
| Sessions | `launch_browser` `close_browser` `list_sessions` |
| Profiles | `list_profiles` `create_profile` `delete_profile` |
| Proxies | `list_proxies` `claim_proxy` |
| Page | `navigate` `click` `fill` `evaluate` `get_content` `screenshot` |
| Live view | `start_live_view` `stop_live_view` |

`launch_browser` takes a profile name and creates it on first use. Pass
`temporary: true` for automation work: those profiles are local-only and stay
out of the desktop app's list, while still persisting on disk.

## Before you rely on it

- **One browser at a time on a free key.** The concurrency limit is carried by
  the license and counted per machine, across every application using the same
  engine. Fan an agent out into parallel sessions only on a plan whose limit
  covers them, or the extra launches are refused.
- **The engine downloads on first launch** (190-320 MB depending on platform),
  into a shared cache directory. The first `launch_browser` of a fresh install
  pays for that; later ones do not.
- **A persistent identity is a real identity.** Two agents driving one profile
  at once is the same mistake as two people sharing one browser: last one to
  close wins. Give each its own.

## Configuration

The bundle inserts one row, `mcp-antibrow`, configuring the harness's MCP client
against the `anti-detect-browser` CLI. Override it from your profile's own
`cordis.patch.yml` by targeting that id - a patch replaces the row's whole
`config`, so restate every key you keep:

```yaml
- id: mcp-antibrow
  config:
    serverName: antibrow
    transport: stdio
    command: npx
    args: ['-y', 'anti-detect-browser@^2.19.1', '--mcp']
    env:
      ANTI_DETECT_BROWSER_KEY: !!js process.env.MY_OWN_VAR
      ANTI_DETECT_BROWSER_CACHE_DIR: /var/lib/antibrow
```

Turn it off without uninstalling:

```yaml
- id: mcp-antibrow
  disabled: true
```

To run the SDK from a checkout instead of npm, use the overlay this package
ships:

```
export ANTIBROW_SDK_CLI=<checkout>/dist/cli.js
dsh --profile <name> --patch node_modules/dsh-antibrow/cordis.patch.local.yml
```

## Compatibility

Verified against dsh `0.1.0-rc.6` and `anti-detect-browser` 2.19.1, 2026-08-15.
DeepSeek Harness is a developer preview and says it will break compatibility;
this line is the claim, and it rots without a re-test.

The SDK version floor is real: 2.19.1 is the first release whose close path ends
the browser process instead of only dropping t