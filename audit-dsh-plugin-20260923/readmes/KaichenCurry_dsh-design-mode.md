<div align="center">

# DSH Design Mode

English | [中文](README.zh.md)

### Turn one idea into a visual result you can keep refining—inside DeepSeek Harness.

DSH Design Mode connects guided intent clarification, image generation, an infinite canvas, contextual image tools, and location-aware comments to the native DSH conversation.

[Watch the workflow](#workflow) · [Quick start](#quick-start) · [Product PDF](pitch/DSH-Design-Mode-%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.pdf)

[![DSH plugin](https://img.shields.io/badge/DSH-plugin-3975EE)](https://github.com/topics/dsh-plugin) [![MIT License](https://img.shields.io/badge/license-MIT-111317)](LICENSE) [![Desktop + Web](https://img.shields.io/badge/Desktop%20%2B%20Web-supported-5A83F7)](#quick-start) [![Image only v1](https://img.shields.io/badge/v1-image%20only-6F7682)](#current-v1-scope)

<a href="showcase/public/media/03-tools.mp4?raw=1"><img src="showcase/public/media/readme-overview.gif" alt="Real DSH Design Mode workflow: turn on Design Mode, work on an image, and place a comment" width="900"></a>

**One conversation. One canvas. Every edit stays traceable.**

</div>

> Developer preview based on `dsh-v0.1.1-rc.2`. This independent community project is listed under the GitHub [`dsh-plugin` topic](https://github.com/topics/dsh-plugin) and is not an official DeepSeek release.

## Why Design Mode exists

Image models can already produce impressive pixels. The surrounding workflow still asks the user to behave like a product manager: translate an idea into a production prompt, choose the correct tool, move context between panels, and reconstruct why each revision exists.

DSH Design Mode makes that coordination part of the Agent session. A user can begin with ordinary language, clarify only the decisions that materially affect the result, generate or import an image, select the object to edit, and send precise visual comments back through the same conversation.

| Without a continuous workflow | With DSH Design Mode |
| --- | --- |
| A blank canvas or a wall of tools appears before the brief is clear. | Design Mode stays armed but opens the canvas only after text, an image, or both create real visual work. |
| The user must know how to write a production prompt. | `ask_user` converts an ambiguous request into 3–5 focused decisions before generation. |
| Editing tools are detached from the selected image and its history. | Tools appear for the selected object and write their results back to the current canvas. |
| Comments live in a separate review panel. | Point, rectangle, and brush comments return to chat and are processed in order. |

## The product in one minute

<p align="center"><img src="pitch/product-workflow.jpg" alt="DSH Design Mode six-step workflow from arming Design Mode to returning results to the conversation" width="1000"></p>

1. **Arm Design Mode.** The mode is explicit and reversible; an empty canvas does not interrupt the conversation.
2. **Send text, an image, or both.** The native Composer remains the single entry point.
3. **Clarify material ambiguity.** The Agent asks one focused question per round, with three recommendations and a UI-owned “Other” input.
4. **Generate or import.** The canvas opens when there is an image to inspect, compare, or edit.
5. **Edit in context.** Selecting an image reveals the capabilities relevant to that object and task.
6. **Comment and continue.** Location-aware requests return to the native conversation, preserving the visible reasoning and modification record.

<a id="workflow"></a>

## Watch the real workflow

These recordings come from the working DSH build. Select a card to play the full MP4.

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="showcase/public/media/01-entry.mp4?raw=1"><img src="showcase/public/media/01-entry-poster.jpg" alt="Enter Design Mode from the native DSH composer"></a>
      <h3>01 · Enter from chat</h3>
      <p><strong>User action:</strong> arm Design Mode and describe the desired image in ordinary language.<br><strong>System response:</strong> keep the native conversation visible and begin the visual workflow without opening an empty canvas.</p>
      <p><a href="showcase/public/media/01-entry.mp4?raw=1">▶ Play full recording</a></p>
    </td>
    <td width="50%" valign="top">
      <a href="showcase/public/media/02-clarify.mp4?raw=1"><img src="showcase/public/media/02-clarify-poster.jpg" alt="Clarify a generation request with ask_user cards"></a>
      <h3>02 · Clarify intent</h3>
      <p><strong>User action:</strong> answer short questions about use, style, composition, materials, or constraints.<br><strong>System response:</strong> synthesize the answers into one production-ready image request before calling the provider.</p>
      <p><a href="showcase/public/media/02-clarify.mp4?raw=1">▶ Play full recording</a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="showcase/public/media/03-tools.mp4?raw=1"><img src="showcase/public/media/03-tools-poster.jpg" alt="Use contextual image tools on the infinite canvas"></a>
      <h3>03 · Edit the selected image</h3>
      <p><strong>User action:</strong> select an image and choose a focused capability such as background removal, upscale, outpaint, erase, text editing, or translation.<br><strong>System response:</strong> show the task-specific controls and place the resulting asset back on the canvas.</p>
      <p><a href="showcase/public/media/03-tools.mp4?raw=1">▶ Play full recording</a></p>
    </td>
    <td width="50%" valign="top">
      <a href="showcase/public/media/04-comments.mp4?raw=1"><img src="showcase/public/media/04-comments-poster.jpg" alt="Place a location-aware comment and continue the edit in chat"></a>
      <h3>04 · Comment where the change belongs</h3>
      <p><strong>User action:</strong> point, frame, or brush the exact region and write the requested change.<br><strong>System response:</strong> return comments to the left conversation and process multiple requests in order, keeping the edit trail readable.</p>
      <p><a href="showcase/public/media/04-comments.mp4?raw=1">▶ Play full recording</a></p>
    </td>
  </tr>
</table>

## What you can do today

| Goal | Capabilities |
| --- | --- |
| **Create** | Generate from natural language, use up to 14 image references, upload, paste, drag, or add an existing chat image. |
| **Refine** | Remove or replace a background, upscale, edit detected text, translate selected text regions, and remove an authorized mark. |
| **Reframe** | Outpaint, erase, change angle, recolor, and preserve the original subject while producing a new child result. |
| **Review** | Add point, rectangle, or brush comments; send them to chat; process multiple comments sequentially; retry recoverable failures. |
| **Deliver** | Export PNG, PDF, standalone HTML, ZIP, or PPTX from the canvas. |

The canvas also supports pointer-centered zoom, pan, single and multi-selection, move, proportional resize, rotate, lock, hide, download, fit-to-view, and local undo/redo.

## Product principles

### Intent before generation

An ambiguous request such as “design a hiking backpack” is not sent directly to an image model. The Agent asks 3–5 adaptive questions, never repeats a resolved decision, and generates only after the minimum clarification rounds are complete.

### Context before controls

The selected image determines which tools appear. Each task owns its own parameters, confirmation step, provider label, progress state, and recoverable error message instead of sharing one generic side-panel form.

### Conversation as the record

The canvas is the visual workspace; the DSH conversation is the durable explanation of intent, tool calls, failures, and completed revisions. Comments therefore flow back to chat rather than becoming a second isolated task system.

### Host-owned execution

The browser never calls image providers directly. UI actions and Agent tools use the same Host service, request mode