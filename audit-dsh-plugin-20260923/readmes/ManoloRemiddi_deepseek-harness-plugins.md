<!-- Copyright © 2026 Manolo Remiddi · SPDX-License-Identifier: MIT -->

# DeepSeek Harness Plugins

Plugins by [Manolo Remiddi](https://github.com/ManoloRemiddi) for
[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness).
Choose a plugin below, download its release and follow its installation guide.
Each plugin has its own repository, license, issues and version history.

## Augmentor Desktop and Browser

**[Augmentor Agent](https://github.com/ManoloRemiddi/augmentor-agent)** is the
single active project for Augmentor Desktop and Browser. Use its
[current installation guide](https://github.com/ManoloRemiddi/augmentor-agent/blob/main/docs/COMPLETE-INSTALL.md)
or [guided website installation](https://augmentoragent.com/#installation)
for the matched 0.2.10 complete Linux preview, including its required plugins.
Source changes, issues and future Augmentor releases belong in that repository.
This repository is a catalogue and collection builder for independent DSH plugins.

## Download the dated collection

[Download all six September 14 packages as one ZIP](https://github.com/ManoloRemiddi/deepseek-harness-plugins/releases/download/collection-2026.09.14/augmentor-plugins-2026.09.14.zip)
· [SHA-256 checksums](https://github.com/ManoloRemiddi/deepseek-harness-plugins/releases/download/collection-2026.09.14/augmentor-plugins-2026.09.14-SHA256SUMS)
· [Browse current plugin downloads](https://augmentoragent.com/plugins.html).

The **14 September 2026 snapshot** contains legacy Augmentor Browser **0.1.32**,
Metafolder **1.2.1**, Model Picker **1.1.2**, Adaptive Reasoning **0.2.0 preview**,
Prompt Library **0.2.1 preview** and Steering **0.1.0**. It does not contain
Desktop or the matching 0.2.10 Browser companion. Adaptive Reasoning's standalone
release below is newer than the version in this ZIP.

The archive contains original versioned packages, a setup guide and checksums.
Nothing installs automatically; choose only what you need.
[Version-specific collection installation guide](docs/COLLECTION-INSTALL.md).

## Current standalone plugins

Versions checked on 23 September 2026. These downloads are separate from the
frozen collection above.

| Plugin | What it adds | Release | Get started |
| --- | --- | --- | --- |
| **[Metafolder](https://github.com/ManoloRemiddi/DSH-Metafolder-Plugin)** | Coloured sidebar groups for workspaces and sessions, plus folder browsing | **1.2.1** | [Download](https://github.com/ManoloRemiddi/DSH-Metafolder-Plugin/releases/tag/v1.2.1) · [Guide](https://github.com/ManoloRemiddi/DSH-Metafolder-Plugin/blob/v1.2.1/README.md) |
| **[Model Picker Augmented](https://github.com/ManoloRemiddi/dsh-model-picker-augmented)** | Search, pin and hide models; refresh provider catalogues | **1.1.2** | [Download](https://github.com/ManoloRemiddi/dsh-model-picker-augmented/releases/tag/v1.1.2) · [Guide](https://github.com/ManoloRemiddi/dsh-model-picker-augmented/blob/v1.1.2/README.md) |
| **[Adaptive Reasoning](https://github.com/ManoloRemiddi/dsh-adaptive-reasoning)** | Automatically chooses effort for each request without a classifier model or GPU keep-alive | **0.2.3 preview** — model-specific configuration required | [Download](https://github.com/ManoloRemiddi/dsh-adaptive-reasoning/releases/tag/v0.2.3) · [Setup](https://github.com/ManoloRemiddi/dsh-adaptive-reasoning/blob/v0.2.3/docs/SETUP.md) |
| **[Prompt Library](https://github.com/ManoloRemiddi/dsh-prompt-library)** | Save and edit reusable prompts, with standalone storage or an existing Augmentor service | **0.2.1 preview** | [Download](https://github.com/ManoloRemiddi/dsh-prompt-library/releases/tag/v0.2.1) · [Guide](https://github.com/ManoloRemiddi/dsh-prompt-library/blob/v0.2.1/README.md) |
| **[Steering](https://github.com/ManoloRemiddi/dsh-steering)** | Applies corrections during model output while preserving queued follow-ups and running tools | **0.1.0** | [Download](https://github.com/ManoloRemiddi/dsh-steering/releases/tag/v0.1.0) · [Guide](https://github.com/ManoloRemiddi/dsh-steering/blob/v0.1.0/README.md) |

Published plugin checks target **DSH 0.1.5-rc.1**. They are community
plugins, not official DeepSeek products. Other DSH versions may change plugin
interfaces. Check each repository for its Node.js, profile and platform requirements.

## Install

First install DSH and configure a working model. Use the complete local web URL
printed by DSH, including its authentication token, when opening the web app.

For a single-package plugin, download its `.tgz` release asset and run:

```sh
dsh plugin --profile web add /absolute/path/to/downloaded-plugin.tgz
```

Use the package asset under **Assets**, not GitHub's automatically generated
“Source code” archive. Use your actual DSH profile if different from `web`.
Finish running tasks, restart your existing DSH process and reload the web page.
An existing manual `link:` or symlink installation should be updated in place
following its guide, without adding a second copy.

**Current Augmentor** uses the complete installer linked above. Its required
plugins and shared prompt library are already included. The older Browser
0.1.32 ZIP has a separate version-specific guide in the collection instructions.
**Prompt Library** needs Python 3 with SQLite for its standalone store; existing
Augmentor users can configure their shared service socket instead. Its default
standalone store starts empty without migrating or deleting previous data.
**Adaptive Reasoning** requires a one-time allowlist/effort configuration for
your own model. Version 0.2.3 starts with empty routes and remains inactive
until configured.
**Steering** is already included in Augmentor’s Linux preset. Install the
standalone plugin only when you need the behavior for other DSH agents.

To remove a CLI-installed package:

```sh
dsh plugin --profile web remove PACKAGE_NAME
```

Restart DSH afterward. Augmentor's native host and browser extension have their
own removal steps. For manual installations, follow the repository's guide.

## Compatibility and release checks

The [September 13 checks](docs/RELEASE-CHECK-2026-09-13.md) and
[September 14 Steering addition](docs/RELEASE-CHECK-2026-09-14.md) record the
original collection checks. The [September 23 catalogue check](docs/LINK-CHECK-2026-09-23.md)
records the current link and download audit. Test results are not a promise of compatibility with every
model, browser or future DSH version. Adaptive Reasoning is explicitly a preview;
its fast paths are conservative English rules, not a trained difficulty judge.
Metafolder stores groups in browser localStorage; cross-device sync is not provided.

## Help and contributions

For Augmentor Desktop or Browser, use the
[active Augmentor issue tracker](https://github.com/ManoloRemiddi/augmentor-agent/issues).
For a standalone plugin, open an issue in that plugin's repository. Include the plugin and DSH
versions, operating system/browser, install method, reproduction steps and the
error message. Use synthetic examples and remove credentials and private logs.
For a broken catalogue link, open an issue in this repository.

The repositories share the `deepseek-harness`, `dsh-plugin` and
`manolo-dsh-plugins` topics. You can also
[browse the collection by topic](https://github.com/search?q=user%3AManoloRemiddi+topic%3Amanolo-dsh-plugins&type=repositories).
Watch an individual repository's **Releases** for new versions. This catalogue
is updated when a release is published; it does not run a background updater.

## Licenses

This catalogue is MIT © 2026 Manolo Remiddi. The standalone plugins and original
September 14 packages have their own MIT licenses. Current Augmentor Desktop
and Browser use **MIT with Augmentor Resale Restriction**: free personal and
business use and modifications; reselling Augmentor requires written permission.
See the [current Augmentor license](https://github.com/ManoloRemiddi/augmentor-agent/blob/main/LICENSE)
and [website explanation](https://augmentora