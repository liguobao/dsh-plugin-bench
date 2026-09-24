# dsh-auth-gate

**English** | [简体中文](README.zh.md)

[![npm version](https://img.shields.io/npm/v/dsh-auth-gate.svg)](https://www.npmjs.com/package/dsh-auth-gate)
[![npm downloads](https://img.shields.io/npm/dt/dsh-auth-gate.svg)](https://www.npmjs.com/package/dsh-auth-gate)
[![npm monthly downloads](https://img.shields.io/npm/dm/dsh-auth-gate.svg)](https://www.npmjs.com/package/dsh-auth-gate)
[![node](https://img.shields.io/node/v/dsh-auth-gate.svg)](https://www.npmjs.com/package/dsh-auth-gate)
[![types](https://img.shields.io/npm/types/dsh-auth-gate.svg)](https://www.npmjs.com/package/dsh-auth-gate)
[![CI](https://github.com/TecFancy/dsh-auth-gate/actions/workflows/ci.yml/badge.svg)](https://github.com/TecFancy/dsh-auth-gate/actions/workflows/ci.yml)
[![license](https://img.shields.io/npm/l/dsh-auth-gate.svg)](LICENSE)

A login door for your [DeepSeek Harness](https://github.com/deepseek-ai/dsh)
(dsh) web instance. Put it in front of a public dsh deployment and nobody can
reach your agents, your chat sessions, or your LLM credentials without signing
in first.

## Built on dsh-plugin-framework

This plugin is developed on the engineering conventions of
[dsh-plugin-framework](https://github.com/TecFancy/dsh-plugin-framework), the
reference plugin framework for the dsh ecosystem. The `src/` layout
(features/shared layers with barrel-only cross-slice imports), the engineering
gates (`npm run verify`, bundle/slice/no-emdash checks) and the decision-record
discipline all align with it - conventions that have held up across the dsh
codebase. Solid engineering worth building on.

## What it does

- **Everything needs a login.** Every page, API call, and WebSocket connection
  is checked. Visitors without a valid session are sent to a simple login page
  (or rejected with `401` for API/script requests). The one exception is
  `GET /manifest.webmanifest`: browsers fetch the Web App Manifest without
  credentials, so that exact path is public (name / icons / display mode only).
- **Two ways to sign in** (pick one in the configuration):
  - **Password** (recommended): each admin gets a username and password.
  - **Token**: one shared secret token for the whole instance.
- **Works for browsers and scripts.** Browsers use the login page; scripts and
  curl can pass `Authorization: Bearer <token>` and skip the page entirely.
- **Optional two-factor authentication (TOTP).** In password mode, a user with
  a TOTP secret added to their account signs in with password **plus** a 6-digit
  code from an authenticator app (RFC 6238, configurable off/optional/required).
- **Safe by default.** Passwords are stored hashed, logins are rate-limited
  (repeated wrong attempts temporarily lock the address), session cookies are
  secure, and any missing or broken configuration **blocks access instead of
  silently opening the door**. A wrong username or password re-renders the
  login card with an inline `Invalid username or password.`: the username is
  kept, the password must be retyped. A lockout (HTTP 429 + `retry-after`)
  shows the same card with the retry seconds and a message scoped to "this
  network"; the number of remaining attempts is deliberately never shown, and
  with JavaScript a page refresh no longer spends another failure.
- **A small command-line tool** for managing users:

  ```sh
  dsh-auth user add admin --password-stdin   # add a user
  dsh-auth user list                          # list users
  dsh-auth user disable admin                 # block future logins + revoke that user's live sessions
  dsh-auth user totp enable admin             # generate a TOTP secret (prints an otpauth:// URI)
  dsh-auth user totp disable admin            # remove the TOTP secret
  ```

  `dsh-auth` is directly on your PATH when the package is installed globally.
  After `dsh plugin add` the binary lives inside the profile and must be called
  through it — see [Quick start](#quick-start).

## Quick start

```sh
# 1. Install the plugin from npm into your dsh profile.
#    Since 0.4.1 the package declares a `dsh.bundle` manifest, so `dsh plugin add`
#    also registers the mount (dsh.profile.bundles) automatically:
dsh plugin --profile web add dsh-auth-gate

# 2. Create an admin account.
#    `dsh plugin add` installs the plugin into the profile's node_modules
#    ($DSH_HOME/profiles/web, default ~/.dsh/...) — the CLI is NOT added to your
#    PATH, so call it through the profile. `dsh plugin` already requires pnpm:
printf '%s\n' 'choose-a-strong-password' | \
  pnpm --dir "$DSH_HOME/profiles/web" exec dsh-auth user add admin --password-stdin

# 3. Turn on password login: override the plugin config in $DSH_HOME/cordis.patch.yml
#    (a ready-to-use config-override template ships in deploy/cordis.patch.yml;
#    see Configuration below — the mount itself needs no manual patch row)

# 4. Restart dsh. Open your site — you will be asked to sign in.
```

## See it in action

Visitors without a session are sent to the login page:

![Login page](docs/demo/login-page.png)

When TOTP is enabled for your account, signing in continues with a second step — a
6-digit code from your authenticator app (password first, then the code):

![TOTP verification step](docs/demo/totp-code.png)

After signing in, they land on your instance:

![dsh instance](docs/demo/dashboard.png)

On dsh 0.1.2-alpha+ (which guards pages with a launch token), signing in
auto-bridges the token gate: the login redirect goes through a short relative
`/?token=…` hop that mints the dsh cookie, then lands on `/` (details in
`docs/implemented/impl-launch-token-bridge.md`).

A prominent **Sign out / 退出登录** button sits inside the **Settings panel**
(the Settings → General page, below the last preference row). It's a centered,
danger-styled filled button (16px door icon + localized label, theme tokens
for light/dark), and its label follows the GUI language through the same
locale mechanism the Settings language switch uses. Clicking it runs the same
native `POST /auth/logout?next=/` flow as before.

## Configuration

The bundle mount (id `dsh-auth-gate`, inserted by `dsh plugin add`) uses the
default config: `mode: "token"` backed by the `DSH_AUTH_TOKEN` environment
variable. To change it, override the config in `$DSH_HOME/cordis.patch.yml`
(or the profile's `cordis.patch.yml` — a ready-to-use override template ships
in `deploy/cordis.patch.yml`). The override targets the mounted row by id
(no `insert` — adding one would double-mount the plugin):

```yaml
- id: dsh-auth-gate
  config:
    mode: "password" # "password" (recommended) or "token"
    totp: "optional" # "off" (default), "optional", or "required"
    cookieSecure: true # keep true when you use https
```

| Option              | Default                      | What it does                                                                                                                                                                                                                                                                                                         |
| ------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mode`              | `"token"`                    | `"password"` = username/password login; `"token"` = one shared secret                                                                                                                                                                                                                                                |
| `totp`              | `"off"`                      | Password mode only. `"optional"`: users with a TOTP secret sign in with password + code; `"required"`: all users must have a secret