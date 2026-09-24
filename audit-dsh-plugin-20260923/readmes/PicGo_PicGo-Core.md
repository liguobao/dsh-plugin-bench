<div align="center">
  <h3>Special thanks to</h3>
  <table>
    <tr>
      <td align="center" valign="middle" width="50%">
        <a href="https://modelflare.dev/sign-up?partner=1GIMVVBLWP1V">
          <img alt="Modelflare sponsorship" width="400" src="https://pics.picgo.app/m/ef1a160c-c9ce-4605-9b9c-b2d355cd2de4.png">
        </a>
        <h3><a href="https://modelflare.dev/sign-up?partner=1GIMVVBLWP1V">Modelflare</a></h3>
        <p>Full strength, stable, nothing watered down. Global SOTA models at a lower cost.</p>
      </td>
      <td align="center" valign="middle" width="50%">
        <a href="https://castaly.modelflare.dev/sign-up?partner=1GIMVVBLWP1V">
          <img alt="Castaly sponsorship" width="400" src="https://pics.picgo.app/m/284def41-2f23-47e6-9d64-7017d386a221.png">
        </a>
        <h3><a href="https://castaly.modelflare.dev/sign-up?partner=1GIMVVBLWP1V">Castaly</a></h3>
        <p>Full strength, no upscaling. 40+ image and video models, including NSFW.</p>
      </td>
    </tr>
    <tr>
      <td align="center" valign="middle" width="50%">
        <a href="https://www.nocobase.com/?utm_source=picgo">
          <img alt="NocoBase sponsorship" width="400" src="https://static-docs.nocobase.com/Logo-Black.png">
        </a>
        <h3><a href="https://www.nocobase.com/?utm_source=picgo">NocoBase</a></h3>
        <p>AI + No-Code Build reliable business systems</p>
      </td>
      <td align="center" valign="middle" width="50%">
        <a href="https://console.neon.tech/app/?promo=PicGo">
          <picture>
            <source media="(prefers-color-scheme: dark)" srcset="https://neon.com/brand/neon-logo-dark-color.svg">
            <source media="(prefers-color-scheme: light)" srcset="https://neon.com/brand/neon-logo-light-color.svg">
            <img alt="Neon sponsorship" width="400" src="https://neon.com/brand/neon-logo-dark-color.svg">
          </picture>
        </a>
        <h3><a href="https://console.neon.tech/app/?promo=PicGo">Neon</a></h3>
        <p>Fast Postgres Databases for Teams and Agents</p>
      </td>
    </tr>
  </table>
</div>

---

# PicGo-Core

![standard](https://img.shields.io/badge/code%20style-standard-green.svg?style=flat-square)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fpicgo%2Fpicgo-core%2Fbadge%3Fref%3Dmaster&style=flat-square)](https://actions-badge.atrox.dev/picgo/picgo-core/goto?ref=master)
![npm](https://img.shields.io/npm/v/picgo.svg?style=flat-square)
[![PicGo Convention](https://img.shields.io/badge/picgo-convention-blue.svg?style=flat-square)](https://github.com/PicGo/bump-version)
![node](https://img.shields.io/badge/node-%3E%3D20.0.0-blue?style=flat-square)

![picgo-core](https://cdn.jsdelivr.net/gh/Molunerfinn/test/picgo/picgo-core-fix.jpg)

A tool for image uploading. Both CLI & api supports. It also supports plugin system, please check [Awesome-PicGo](https://github.com/PicGo/Awesome-PicGo) to find powerful plugins.

More details please see the [Homepage](https://picgo.app/) of PicGo.

**Typora supports PicGo-Core natively**.

## Installation

PicGo requires Node.js >= 20.19.0 or >= 22.12.0. For older PicGo versions (<= v1.5.x), Node.js >= 16 is sufficient. Cause we need the [stability of ES Module support](https://joyeecheung.github.io/blog/2025/12/30/require-esm-in-node-js-from-experiment-to-stability/).

### Global install

```bash
npm install picgo -g

# or

yarn global add picgo
```

### Local install

```bash
npm install picgo -D

# or

yarn add picgo -D
```

## Usage

### Use in CLI

> PicGo uses `SM.MS(S.EE)` as the default upload image host.

Show help:

```bash
$ picgo -h

  Usage: picgo [options] [command]

  Options:
    -v, --version                            output the version number
    -d, --debug                              debug mode
    -s, --silent                             silent mode
    -c, --config <path>                      set config path
    -p, --proxy <url>                        set proxy for uploading
    -h, --help                               display help for command

  Commands:
    install|add [options] <plugins...>       install picgo plugin
    uninstall|rm <plugins...>                uninstall picgo plugin
    update [options] <plugins...>            update picgo plugin
    set <module> [name] [configName]         configure config of picgo modules (uploader/transformer/plugin)
    upload|u [input...]                      upload, go go go
    use [module] [name] [configName]         use module (uploader/transformer/plugin) of picgo
    get                                       get current picgo module config (uploader/transformer/plugins)
    i18n [lang]                              change picgo language
    uploader                                 manage uploader configurations
    server [options]                         run PicGo as a standalone server
    login [token]                            login to cloud.picgo.app
    logout                                   logout from cloud.picgo.app
    cloud                                    manage PicGo Cloud
    help [command]                           display help for command
```

#### Upload a picture from path

```bash
picgo upload /xxx/xx/xx.jpg
```

#### Upload with a saved configuration

Use `--configName` to choose a saved configuration for one upload. Add `--uploader` when the same name exists in multiple uploader types. You can also use `--configId`; a unique ID match takes precedence over the name, and an unresolved ID falls back to the name when provided.

```bash
picgo upload ./photo.png --configName=Work
picgo upload ./photo.png --uploader=github --configName="Work Images"
picgo upload ./photo.png --uploader=github --configId=your-config-id --configName=Work

# Upload from the clipboard with a saved configuration.
picgo upload --configName=Work
```

These options use the same lookup rules as HTTP and SDK uploads and do not change saved defaults. Without these options, `picgo upload` retains its existing default behavior. Existing local input files are retained after upload; only temporary multipart files and clipboard images created by PicGo are cleaned up. Clipboard filenames keep the existing `YYYYMMDDHHmmssSSS.png` format.

#### Upload a picture from clipboard

> picture from clipboard will be converted to `png`

```bash
picgo upload
```

Thanks to [vs-picgo](https://github.com/Spades-S/vs-picgo) && [Spades-S](https://github.com/Spades-S) for providing the method to upload picture from clipboard.

#### Run as a server

```bash
picgo server -p 36677 -h 127.0.0.1
```

##### Select a configuration for one upload

Add `uploader`, `configName`, or `configId` to `POST /upload` to choose an existing saved configuration for that request. Configuration names are recommended for readability. Use URL encoding for names containing spaces, Chinese characters, or other special characters:

```js
const url = new URL('http://127.0.0.1:36677/upload')
url.searchParams.set('uploader', 'github')
url.searchParams.set('configName', 'Work')

const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ list: ['/absolute/path/photo.png'] })
})
const result = await response.json()
```

The same query parameters work with an empty body for clipboard uploads, JSON without `list` or with an empty `list`, and multipart uploads using the `files` field. If server authentication is enabled, include your existing `Authorization: Bearer <secret>` header.

| Upload options | Behavior |
| --- | --- |
| No upload options | Existing default upload behavior. |
| `uploader=github` | Use GitHub's currently selected configuration (`defaultId`, falling back to its first configuration). |
| `uploader=github&configName=Work` | Find `Work` within GitHub, ignoring case and surrounding whitespace. |
| `configNam