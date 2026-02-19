# CanonCanvas Install (derived)

ModuleID: CanonCanvas
Version: 0.3.6
DocRole: Install
Audience: Users + assistants (bootstrap + recovery)

---

## 1) Enable or disable
Say one of:
- "Enable CanonCanvas in this chat."
- "Disable CanonCanvas in this chat."
- "Sleep CanonCanvas for now."

ASCII canon equivalents:
- `canoncanvas load`
- `canoncanvas activate`
- `canoncanvas sleep`
- `canoncanvas unload`
- `canoncanvas status`

## 2) Default behavior when enabled
- Treat canvas as authoritative canon.
- Keep chat exploratory and compile conclusions into canvas patches.
- Treat canvas as long-term memory for durable project progress.
- CanonCanvas operates on markdown canvases.
- Look-before-leap binding: open an existing matching `🛜` canvas before creating a new one.
- Treat user-opened canvas as primary selection signal.
- If active-canvas telemetry is unclear, request exact-title bind confirmation (`use 🛜 <ProjectName> - <CanvasPurpose>`).
- Never suggest non-existent UI controls for setting active canvas.
- Never create a duplicate canvas as a workaround for bind uncertainty.
- Build sections dynamically; do not prefill empty outlines.
- Do not assume a client exists; client sections are conditional.

## 3) Core operations
- Canon pass: `canoncanvas canonize`
- Cleanup pass: `canoncanvas cleanup`
- Pre-fork pass: `canoncanvas lastcall`
- LastCall is a ritual pass, not a module and not a header title.
- LastCall ends with a short "note to younger self" tail line by default (fun/snarky is encouraged unless user requests formal tone).
- Use this exact header for that tail block: `### 🚸 assistant's 👴🏼 note to → 📝 → younger 👶🏻 self`.
- Resolve Open Question: `canoncanvas resolve B2`
- Prune option(s): `canoncanvas prune B1,3,D3`
- Export: `canoncanvas export markdown`

Fork signal helpers:
- `💾` marks a save-point anchor before deep execution.
- `⚡` means fork-back happened; re-read canvas immediately before proceeding.

## 4) Naming rule
- Use `🛜 <ProjectName> - <CanvasPurpose>` for any CanonCanvas-bound canvas.
- Use PascalCase for `<ProjectName>` when applicable.
- Example: `🛜 LogKit - dev R6`
- Re-open the existing matching `🛜` canvas when present; do not create duplicates by default.
- Create a new `🛜` canvas only when no suitable match exists or user explicitly requests a new canvas.

## 5) Header library (WIP)
- Use standard recurring headers from UserGuide `4.1` before inventing new ones.
- Handoff header standard: `## 👴🏼 Fork Handoff Notes`.
- `👴🏼` appears only when needed, must be final section, and is consumed as items are merged into canonical sections.

## 6) Client-mode toggle (context-driven)
- Non-client default: use neutral sections; do not create `Client comments` / `⚖️ Client Requests`.
- Client mode: when user explicitly indicates a client project or provides client brief text.
- In client mode:
  - capture short client wording verbatim under `⚖️ Client Requests`
  - track additive strategy under `💡 Our Ideas`

## 7) If the module seems out of sync
Symptoms: stale decisions, mixed open/resolved items, noisy canvas body.
Recovery:
1. Run `canoncanvas cleanup`.
2. Run `canoncanvas canonize`.
3. Run `canoncanvas status` and verify active state.
4. If sections are missing, provide the latest canvas content and rerun.

## 8) Collision behavior
If another active module requires a conflicting output shape, CanonCanvas must ask user to choose a single winner.
