# dsh-strata

[![npm version](https://img.shields.io/npm/v/dsh-strata?logo=npm&color=cb3837)](https://www.npmjs.com/package/dsh-strata)
[![license](https://img.shields.io/npm/l/dsh-strata?color=blue)](LICENSE)
[![listed on awesome-dsh-plugin](https://img.shields.io/badge/awesome--dsh--plugin-listed-6f42c1)](https://awesome-dsh-plugin.com/p/jsdvjx/dsh-strata/)

> *Read the strata of a run.*

English | [中文](README.zh.md)

**A real minimap of the session trajectory for the DeepSeek Harness Web GUI** — it takes
the transcript's scrollbar seat and turns it into a scaled, colored picture of the whole
loaded conversation, with your own messages emphasised and clickable anchors beside it.

Not a tick rail. Every other conversation navigator draws one evenly-spaced dot per prompt,
which throws away the only thing a long agent session has too much of: *volume*. Here a
band's height is the row's **real rendered height**, so the map is a proportional
compression of the scroll extent — a 300-line answer looks like 300 lines, forty tool calls
look like forty tool calls, and the viewport lens maps 1:1 onto the scrollbar. What you get
is the shape of the run at a glance: where you spoke, how much work each prompt cost, and
where it went wrong.

<p align="center">
  <img src="https://raw.githubusercontent.com/jsdvjx/dsh-strata/main/docs/demo.gif" alt="Live demo: hovering expands the rail and lights the band under the cursor, clicking a band or an anchor dot jumps, dragging the lens scrubs the whole session" width="840">
</p>

## What the map shows

| Band | Meaning |
|---|---|
| **Full-width blue** | your message (and steering) — always the widest, brightest, never thinner than 5px |
| Grey block | a model reply; block height is how much it wrote |
| Thin grey tick | one tool call |
| Green | a slash command |
| Amber | a model retry, or a turn cut short by the output cap |
| Red | a failed turn — or any tool/command row that reported an error |
| Horizontal rule | a compaction checkpoint: where the model stopped seeing the history above |
| Rounded outline | the viewport lens (drag it) |

The ragged left edge is the index: every blue bar is a turn you started, and the block of
agent work under it is what that turn cost.

## It replaces the scrollbar

The rail sits in the transcript's own scrollbar gutter and the native thumb is suppressed
while it is up, so there is one scroll control, not two — no layout shifts, because the
gutter stays reserved either way. It is a takeover, not a theft: the moment the map stands
down (Trajectory tab, no session, a transcript that does not scroll) the native scrollbar
comes straight back, and uninstalling restores it permanently.

## …and the turn rail beside it

DSH 0.1.2-rc.1 grew a navigator of its own: a fixed-pitch rail of turn marks
down the right edge of the transcript — the same strip this map lives in, so
the two land on top of each other and the host's rail covers the anchor dots.
The map treats it exactly like the scrollbar: while the map is up the host
rail is hidden, and the moment the map stands down (Trajectory, no session, a
transcript that does not scroll) it is handed straight back. Nothing reflows
either way — that rail is absolutely positioned inside a zero-height sticky
slot, so hiding it costs no layout.

Want both? Keep the host's rail with

```js
localStorage['dsh-strata.native-turn-rail'] = 'keep'
```

and reload. On DSH releases without that rail (0.1.1-rc.2 and earlier) there
is nothing to hide and nothing changes.

## Anchors

Beside the rail is a column of clickable anchor dots — **blue for every message you sent,
red for every failed tool call or command**. Click one to jump there. The dot for wherever
you are reading stays enlarged, so the anchors double as a position indicator. Anchors that
would collide collapse to keep the column readable; failures never collapse, since they are
usually the reason you reached for the map.

## The clue wall

**Hovering a user anchor dot** floats the clue wall over the right half of
the screen: **every user message in the session — including the ones above
the loaded window** (read from the session's own export log) — packed
like an evidence board: every card takes exactly the size its content needs
(a one-word prompt is a small slip, a long one a tall note), flowing into
masonry columns so the whole session fits on one board whenever it can.
Each card is tied to its anchor dot by a bezier that tracks live as the
transcript scrolls; unloaded prompts get a dashed border, tag and dashed
string, and the message you came from is spotlighted. Only when the board
truly cannot hold everything do **↑/↓ pager buttons** appear. **Click a card** to jump — an unloaded one
chain-loads the missing history first. The wall retires when the pointer
leaves it (grace period), or instantly on **Esc**; clicking a dot jumps
straight to that message.

## Map scale

A small **近 / 中 / 全** switcher sits under the rail while it is awake:

- **近** (initial) restores the view from when the session opened — however
  much history has been loaded since, the map keeps that scale and slides
  with your reading position;
- **中** (medium) spans twice the initial view, loading the difference on
  demand;
- **全** (full) maps everything — pulling in any unloaded history first,
  with the same rail progress bar the unloaded jump uses.

The choice persists per browser. Zoomed scales are pinned: loading more
history shifts the window, never the scale.

## Use

- **Click an anchor dot** to jump to that message or failure.
- **Hover** the rail — it widens, the band under the cursor lights up, and on one of
  your own messages the clue wall opens (an anchor dot's tooltip carries the kind and
  `n/total`).
- **Click** a band to scroll it into reading position; the row flashes when it lands.
- **Click empty track or drag** to scrub proportionally, like a scrollbar.
- **Wheel** over the rail or the dots to scroll the transcript.
- **Keyboard**: the rail is focusable — arrows nudge, PageUp/PageDown page,
  Home/End jump to the ends (`role=scrollbar` with a live `aria-valuenow`).
- **Double-click** to pin the rail open (persisted per browser).
- Older history loads by itself: scroll (or drag the lens) to the top and the transcript's
  own *load older* fires, the map rescaling as history arrives. The faint `⌃` above the rail
  just says *there is more above*; it retires once everything is loaded.

The map hides itself when there is nothing to navigate: no session, a transcript that does
not scroll, or a non-chat view such as Trajectory.

## Compatibility

| DSH | Status |
|---|---|
| 0.1.2-rc.1 | Tested — turn folding, the turn navigator, the width handle and the locale switch are all accounted for (see below) |
| 0.1.1-rc.2 | Tested — nothing 0.1.2-specific is required; every seam degrades to the old behaviour |

What 0.1.2 brought, and what the map does about it:

- **Turn folding** (Compact mode hides a finished turn's process rows in place): folded
  rows leave the map the moment they fold, and come back the moment they open.
- **The turn navigator**: hidden while the map is up, handed back when it stands down
  (`localStorage['dsh-strata.native-turn-rail'] = 'keep'` keeps both).
- **The content-width handle** sits under the dot column at laptop widths: the column
  owns its 14px, so a gap between two dots is not a resize grip.
- **Language switching**: labels come through the host's locale service and follow a
  switch in Settings → General without a reload; a language pack can translate the
  `dsh-strata` namespace into a third-party language. A host without the service
  gets the built-in zh/en table keyed on the document language.
- **Pager lifecycle**: 0.1.2 unmounts the "load older" control while a page is in
  flight; the load chain waits for it to come back instead of calling the history
  exhausted, and measures progress by rows landed rather than by scroll height.

## Install

```sh
dsh plugin --prof