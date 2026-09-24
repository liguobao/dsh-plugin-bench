# dsh-theme-plugin

Chinese traditional colors as a **DeepSeek Harness theme pack**. 49 anchor colors × light/dark = **98 themes**, each writing the full token vocabulary (98 tokens: 89 `--dsw-*` plus 9 `--shiki-token-*` syntax slots) and clearing WCAG AA on all 3136 contrast assertions. Twelve of the anchors are marked as a curated shortlist.

📖 [中文文档](./README.zh-CN.md)

<p align="center">
  <img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/theme-zhuqing-light.png" alt="竹青 light: raw-silk paper, a green wash on the bubble, and a send button in the anchor green itself" width="49%">
  <img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/theme-zhuhong-dark.png" alt="朱红 dark: sized-xuan paper in warm ink, a deep maroon wash, and a vermilion send button" width="49%">
  <br>
  <img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/theme-qunqing-light.png" alt="群青 light: violet-tinted silk paper, a blue wash, and a blue send button" width="49%">
  <img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/theme-tenghuang-dark.png" alt="藤黄 dark: ochre paper in olive ink, an olive wash, and a gold send button" width="49%">
</p>
<p align="center">
  <sub>竹青 · light（素绢）&nbsp; | &nbsp;朱红 · dark（熟宣）<br>群青 · light（雪青）&nbsp; | &nbsp;藤黄 · dark（赭纸）</sub><br>
  <sub>One anchor per paper family, same conversation in each. The most saturated patch on screen is always the color you picked.</sub>
</p>

## Install

```sh
npx -y @deepseek-ai/dsh plugin --profile web add dsh-theme-plugin@latest
npx -y @deepseek-ai/dsh --profile web          # boot → open http://127.0.0.1:3080/
```

This pulls the prebuilt bundle from npm — no clone, no build step. The `web` profile is created on first boot under `~/.dsh/profiles/web`.

- **Verify** — the browser console logs `registered 98/98 themes (49 light / 49 dark)`, and `dsh --profile web --dump-config` shows a `theme-zhongguo` row.
- **Update** — run the same `add` command again.
- **Uninstall** — `dsh plugin --profile web remove dsh-theme-plugin`

## Usage

Open **Settings → Traditional Colors** and pick a theme; it applies immediately. Themes also have deep links:

```
http://127.0.0.1:3080/#theme=zhuqing-light      # 竹青 light
http://127.0.0.1:3080/#theme=qunqing-dark       # 群青 dark
```

Changing the hash switches themes live. A deep link wins over your remembered pick. The remembered pick lives in `localStorage`, not in `settings.yaml`, so it does not follow you across devices.

### Four ways to find a theme

<table>
<tr>
<td width="50%"><img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/use-browse.png" alt="The picker on its default view: all 49 anchors of the light branch, grouped into the four paper families"></td>
<td width="50%"><img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/use-tier.png" alt="The 凌晨 夜航 chip pressed: the list narrows to the eight dark-and-quiet themes, spanning all four paper families"></td>
</tr>
<tr>
<td><b>Browse</b> — opens on all 49 anchors of the current branch, grouped by paper family. Each row's chip is the theme's real paper, veil and focus, so the list previews itself.</td>
<td><b>By working mood</b> — six chips read left to right as one day: 晨起 morning → 天亮 dawn. Pick <code>凌晨 夜航</code> and you get the eight dark-and-quiet themes, whatever their color.</td>
</tr>
<tr>
<td><img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/use-search.png" alt="Typing the pinyin lv into the search box narrows the list to the twelve green themes"></td>
<td><img src="https://raw.githubusercontent.com/nevertoday/dsh-theme-plugin/main/docs/img/use-curated-dark.png" alt="Curated only on the dark branch: twelve edited picks, the panel itself rendered in 竹青 dark"></td>
</tr>
<tr>
<td><b>Search</b> — matches the Chinese name, its pinyin, the seal's name and the mood. Typing <code>lv</code> finds all twelve greens without switching keyboards.</td>
<td><b>Curated only</b> — twelve edited picks covering all four papers and all six moods. Use it when 49 is too many; the panel is themed by the pack, so the dark branch looks like this.</td>
</tr>
</table>

The panel references nothing but `--dsw-*` tokens, which is why it changes color with your pick and doubles as a preview of whatever you are about to choose.

## Design: 纸 · 帘 · 印

Chinese painting does not start with color. It prepares the paper, washes over it, and signs last. These themes are built in that order, and the three characters name three layers.

**纸 Paper** — about 60% of the screen. The ground is not "the traditional color, lightened"; it is a different material. Four families — 素绢 raw silk, 熟宣 sized xuan, 雪青 violet-tinted silk, 赭纸 ochre paper — carry deliberately separated chroma (OKLab ≈ 0.010 / 0.019 / 0.015 / 0.024 respectively), so the four papers are told apart by eye and not only in the data. Light grounds sit at L ≈ 0.963–0.971: off-white rather than white, which is what leaves room for a raised surface above them.

**帘 Veil** — about 25%. The sidebar and message bubbles are the anchor color itself, undiluted by paper, held inside a band of 1.25–1.55 contrast against the paper so the wash can neither disappear nor harden into a slab. **You recognize which traditional color you are in by the bubbles, not by the background.**

**印 Seal** — **the focus is the anchor itself.** The primary button and the send button are the anchor pressed darker. This reverses the pack's original law, under which the primary button was filled by a curated *relative* of the anchor sitting a median 109° away in hue — so choosing 竹青 handed you a crimson call-to-action. That relative is still chosen, still recorded per theme as `sealName` / `sealRel` / `sealWhy`, and now appears only as the active-nav accent: a signature rather than a focus. The picker shows the reasoning ("茜红 · 策展印 · 冷暖对冲").

**Ink** — text, rules and secondary surfaces run down one ink ramp, the paper color pushed darker. Every `nb-XX` step of the base stylesheet becomes a tinted neutral of the same lightness, and hover offsets, elevation steps, borders and interaction alphas are copied verbatim: hue changes, relations do not. The ramp's two **endpoints** are the deliberate exception — those are set here rather than inherited, because the base stylesheet's are the extremes. Light and dark now share one shape: body 16.7–17.5, secondary 7.4–8.0, tertiary 4.6–5.5.

**Syntax** — the code block is where a programmer's eyes actually live, so the highlighter is themed too. The harness highlights through shiki's css-variables theme (nine `--shiki-token-*` slots), and every theme fills them: the five chromatic slots (keyword / string / constant / function / parameter) keep the hue conventions programmers already know, but each color is a real named color picked from the 742-color roster; when the anchor's hue falls within a slot's window, **the anchor itself plays that slot** — in 竹青 the strings are 竹青, in 群青 the constants are 群青. Comments and punctuation are ink, not color: the tertiary and secondary ink steps re-gated against the code-block ground. All nine slots clear 4.5 on that ground, and the five chromatic slots are asserted pairwise ≥ 15° apart in hue.

**Gates** — AA is a floor, and elegance lives at the ceiling, so most rules are two-sided. `pnpm check` re-derives every claim above from the emitted tokens: 3136 contrast rows, plus invariants for veil chroma, the single focus (both focus tokens must be the anchor's own hue and the most saturated patches on screen), syntax-slot hue separation, the anchor-on-stage rule, elevation direction, and full token coverage. It trusts nothing the generator says about itself.

**Six tiers** — 49 color names are not a usable set of options for someone who does not already know traditional colors, so every theme also carries a "how do I want