# @awiki/dsh-plugin

AWiki identity and messaging for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness).
The package installs one Host service, its production Rust SDK provider,
the model tools, and a Web client with a draggable AWiki Me launcher.

[中文说明](./README.zh.md)

Identity-entry failures preserve the currently mounted form and local pending identity material. The
phone and OTP never enter browser persistence, controller snapshots, or public
Remote results. Closed registration, unavailable verification state, and commit conflicts each give
a safe next action without exposing remote response details.

The Rust SDK exclusively owns the identity, SecretVault, database, cache, and metadata below the
configured `stateRoot`. This release performs a clean cutover and does not import the former
TypeScript SDK `identity.json`; create a new Rust-backed identity after upgrading.

## Features

- Enter a Handle and phone through one Web UI flow. Before any code is sent, the Host classifies the Handle: a new Handle receives a registration OTP and creates the deployment identity, while an existing Handle receives one Recovery V4 OTP and enters the recovery state machine directly.
- Open the top-left AWiki account menu to sign out locally without deleting the encrypted identity or message database; **Resume local identity** restores the same DID and Handle, including across DSH restarts. The signed-out screen reveals phone recovery only after local resume fails. Switching identities requires an explicit confirmation that permanently clears local AWiki data first.
- Reuse that identity across the root Agent and its subagents.
- Direct-message and existing-group conversation lists, unread counts, latest-message previews, and persisted display names. Core SQLite remains the persistent source of truth: the Host joins persisted peer profiles onto Direct roster rows, while the browser keeps the active identity's last trustworthy Direct profile and group title. Sparse polling identifiers therefore cannot overwrite a resolved display name or real group title. After an existing Handle is recovered, the Host synchronizes account projections before asking Core to restore old group memberships; pending or blocked groups expose a retryable status without disabling Direct messages or other groups. Opening a conversation renders the committed local timeline first, hydrates group sender labels from the Core display-profile cache, reconciles remote history and Direct profile data in the background, and keeps local messages visible if refresh fails. A failed background roster poll also leaves the usable local view quiet; explicit loads still surface their errors. This local-first path covers the newest projected page; loading older messages still requires the remote history service. Scrolling up reveals a latest-message control that counts newer arrivals without interrupting reading. A conversation is marked read only after its newest rendered message reaches the visible bottom.
- Create a private-discovery, open-join, transport-protected group from the Web UI with a name and 1–50 initial Handle or DID members. The group opens immediately; members that could not be added are reported without hiding the successfully created group.
- Text messages plus one attachment per message, with Enter-to-send, Shift+Enter line breaks, optimistic sending bubbles reconciled by an exact client message ID, image previews, and SHA verification. Verified image bytes use three bounded layers: a browser-runtime LRU makes conversation remounts immediate, identity-scoped IndexedDB survives full page reloads without a Host call, and the private Host disk cache survives browser-storage loss and Harness restarts. Clear Local Data removes all three layers.
- A draggable circular launcher that defaults to the lower-left sidebar area, adaptive popup placement, dark mode, and remembered active conversation.
- User-triggered AI summaries for up to 50 recent or unread messages, kept only in runtime memory with explicit stale, retry, copy, and source-navigation states.
- OTP identity access keeps the verification form visible and disables resend with a visible server-directed cooldown countdown. Handle classification happens before OTP delivery, so each attempt sends exactly one purpose-correct registration or recovery code.
- After Recovery V4 reaches `applied`, the Host activates the recovered identity immediately. Automatic restoration of the historical mailbox and canonical model billing account is currently deferred, so those optional account projections cannot block identity recovery. The Browser clears its blocking operation marker while Core retains the authoritative recovery journal; no recovery attestation or model reconciliation request is issued.
- When the separate `@awiki/dsh-model-proxy` package is installed, an AWiki-hosted DeepSeek choice appears before the official API-key onboarding step only when Harness has no usable model provider, with an explicit opt-in and an unchanged API-key escape path. New sessions do not show AWiki model or payment prompts after the official or another provider is usable.
- The optional model-proxy package owns the Host short-token flow and every model-hosting Browser surface: onboarding plus Settings → Quick Recharge with Account & Recharge and Usage tabs. It registers `awiki-deepseek` with `deepseek-v4-flash` and `deepseek-v4-pro`; Flash is recommended and credentials never enter the Browser.
- AWiki identity, domain, and local-data settings remain in the main package. Installing only the main package does not register model opt-in, recharge, usage, or model onboarding UI.
- A typed second confirmation in the Settings danger zone before permanently clearing local AWiki identity, key, token, registration-draft, and message-index state.
- Five messaging Agent tools: identity status, conversations, history, approved text send, and approved attachment send.
- A mail Web UI that selects, reviews, removes, and sends up to 10 bounded attachments, then explicitly downloads one metadata-matched attachment with Base64, size, and SHA-256 verification.
- Five on-demand mail Agent tools: mailbox account, inbox, plain-text read, approved mark-read, and approved plain-text send. Mail read exposes attachment metadata plus a Browser-UI-only download note; Agent mail send remains attachment-free because DSH has no authorized file-resource handle for this tool.
- An opt-in realtime listener that lets exact-allowlisted Direct peers continue one DSH Agent session or use `/new`, `/status`, and `/help`.

## Screenshots

### Messaging

![AWiki direct and group messaging in DeepSeek Harness](./assets/screenshots/awiki-messaging.png)

### Mail

![AWiki mailbox in DeepSeek Harness](./assets/screenshots/awiki-mail.jpg)

The first release does not implement end-to-end encryption, multiple identities,
post-creation group administration or multiple attachments in one message. The Agent listener accepts only
plain Direct text; Groups, attachments, encrypted/payload content, and unknown slash commands never
reach the Agent.

Mail remains on demand and does not wake an Agent for new mail, render or send HTML, or implement
reply, forward, and threading. The Browser reads only user-selected `File` objects, freezes the
approved draft during its one send attempt, and enforces the Host-provided count, single-file, and
total-size limits before canonical Base64 crosses Remote. Attachment downloads are always explicit;
the Browser matches the returned metadata and verifies canonical Base64, byte count, and SHA-256
before creating a temporary Blob URL, then revokes that URL immediately. It never auto-opens HTML,
SVG, or another attachment. Sent history stores only the service message id, file metadata, and
SHA-256, never attachment bytes. Mail subject, addresses,
preview, body, timestamps, and attachment metadata are
untrusted external data, never Agent instructions. `awiki_mail_mark