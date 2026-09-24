English | [中文](README.zh.md)

# Unity Plugin for DeepSeek Harness

**Build Unity games with an AI agent.** This plugin connects [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) to the [Unity Game Engine](https://unity.com/), so you can describe what you want in plain language and the agent does the work inside the Unity Editor: creating projects, building scenes, writing and attaching C# scripts, importing your Asset Store purchases, running tests, and producing builds.

It talks to the Editor through Unity's official [`unity` command-line tool](https://docs.unity3d.com/hub/manual/CLI.html), so everything happens in a real, running Editor and stays in sync with what you see on screen.

## What you can do

- **Start a game from scratch.** "Create a new 3D project called SpaceRunner using the URP template" and the agent picks the template, creates the project, and opens the Editor.
- **Build scenes by talking.** Add GameObjects, position them, attach components, wire up prefabs. Scene commands round-trip in well under a second with no recompile.
- **Write gameplay code.** The agent creates C# scripts, waits for the recompile, and attaches them to the right objects. It can also run C# directly inside the Editor for anything that has no dedicated command.
- **Put your Asset Store library to work.** The agent can search the assets you own on the Unity Asset Store ("My Assets"), download them, and import them straight into the open project. See [Using your Asset Store assets](#using-your-asset-store-assets).
- **See and test the result.** Take screenshots of the Scene view, enter and exit Play mode, run EditMode and PlayMode tests.
- **Ship it.** Kick off player builds for your target platform.
- **Learn from Unity's own playbooks.** The plugin bundles Unity's official agent skill collection (UI, physics, optimization, multiplayer, package management, and more), so the agent follows Unity best practices instead of guessing.

## Prerequisites

Before installing, make sure you have:

1. **DeepSeek Harness 0.1.2-alpha.5 or newer.** Older versions are not supported.
2. **The `unity` command-line tool**, installed, signed in, and with an activated license. Check with:

   ```sh
   unity auth status
   unity license status
   ```

3. **Unity 6.0 or newer** installed through the Unity Hub. Live control of the Editor requires Unity 6.
4. **Python 3.9 or newer** (only needed for the Asset Store feature; no extra packages required).

Each project you want the agent to drive needs the `com.unity.pipeline` package. You do not have to add it by hand: the agent can install it for you, or you can run it once yourself:

```sh
unity pipeline install --project-path /path/to/MyGame
```

## Install

Add the plugin to the DeepSeek Harness profile you use:

```sh
dsh plugin --profile <name> add @opdsh/unity-plugin
dsh --profile <name>
```

That's it. Start the harness and ask the agent to make a Unity game.

<details>
<summary>Other install sources (GitHub or a local checkout)</summary>

```sh
dsh plugin --profile <name> add github:opdsh/unity-plugin  # from GitHub
dsh plugin --profile <name> add /path/to/unity-plugin      # local checkout
```

Installing from GitHub builds the package on install, which pnpm blocks until the package is allowlisted. If the first attempt fails with `ERR_PNPM_GIT_DEP_PREPARE_NOT_ALLOWED`, add this to the profile's `pnpm-workspace.yaml` and run the command again:

```yaml
onlyBuiltDependencies:
  - "@opdsh/unity-plugin"
```

A local checkout installs as a link and needs no allowlist entry, but you must build it first with `pnpm install && pnpm build`.

To confirm the plugin loaded, run `dsh --profile <name> --dump-config` and look for the `# == unity-plugin` section.
</details>

## Your first session

1. Open the Editor for your project, or let the agent create a new one.
2. Ask for something concrete, for example:

   > Open the project at C:\Games\SpaceRunner, add a Player capsule at the origin with a Rigidbody, and write a script that moves it with WASD.

3. The agent checks which Editors are running, discovers the commands the Editor offers, makes the changes, and saves the scene.

Tips:

- The agent launches the Editor with the `-automated` flag so no dialog boxes block it. If you open the Editor yourself, that's fine too; the agent will find it.
- The first time a new project opens, Unity imports assets and can take a few minutes. The agent waits for the Editor to report "ready".
- Ask the agent to take a screenshot whenever you want to see what the scene looks like.

## Using your Asset Store assets

Everything you have bought or claimed on the [Unity Asset Store](https://assetstore.unity.com/) is available to the agent. It signs in with the same Unity account the `unity` CLI and Unity Hub already use, so there is nothing extra to set up.

Ask for an asset by name or by description:

> Add the 2D Game Kit to this project.

> Find a low-poly nature pack in my assets and import it.

The agent then:

1. Searches your "My Assets" library and picks the matching package.
2. Checks that the package supports your project's Unity version and warns you if it does not.
3. Downloads the `.unitypackage` from Unity's servers.
4. Imports it into the open project silently, with no import dialog.
5. Waits for any recompile to finish and tells you which folder under `Assets/` the files landed in.

Only assets you already own are available this way. To use something new, buy or claim it on the Asset Store in your browser and it appears in your library right away. If your Unity sign-in has expired, the agent will ask you to run `unity auth login` or sign in through the Unity Hub, then continue.

The Asset Store feature works on Windows and macOS and needs Python 3.9 or newer.

## Configuration

Most people never need to change anything. If you do:

**In the web GUI:** open **Settings → Plugins → Plugin configuration** and find the **Unity Plugin** card. There you can adjust the two timeouts and the output size cap. Changes apply immediately without a restart, and empty fields fall back to the defaults.

**In the profile:** for everything else (default project path, the path to the `unity` binary, CI credentials), edit the profile's `cordis.patch.yml`. A patch replaces the plugin's whole `config` block, so include every key you want to keep:

```yaml
- insert:
    - id: unity
      name: '@opdsh/unity-plugin'
      config:
        unityBin: unity                    # path to the unity CLI if it is not on PATH
        projectPath: /abs/path/to/MyGame   # default project for Editor commands
        commandTimeoutMs: 120000           # per Editor command; must be > 0
        cliTimeoutMs: 600000               # for builds, tests, and other CLI calls; must be > 0
        graceMs: 5000
        outputMaxBytes: 512000             # must be > 0
        env: {}                            # e.g. UNITY_SERVICE_ACCOUNT_ID / SECRET for CI
        warmShell: true                    # keep one `unity shell` alive for fast Editor commands
        shellIdleMs: 300000                # close the idle shell after this long
        unitySkillsRepo: https://github.com/Unity-Technologies/skills  # '' disables the download
        unitySkillsRef: 87fac23d66a1f44f5e06c2935eccce0b40b9715a       # or a branch such as main
```

`unitySkillsRef` pins the version of Unity's official skills. The default is a tested commit; set it to `main` to follow the latest content. Skills are downloaded once per ref into `<dshHome>/cache/unity-plugin/unity-skills`; if the download fails, an existing cache keeps working.

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| The agent says no Editor instance was found (`STATUS_NO_INSTANCES`) | Open the project in Unity 6, and make sure `unity pipeline install` has been run for it. |
| A CLI call fails with exit code 3 | Sign in again with `unity auth login`. |
| A CLI call fails with exit code 4 | No license is available. Check 