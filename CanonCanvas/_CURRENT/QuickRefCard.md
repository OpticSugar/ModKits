# CanonCanvas QuickRefCard (derived)

ModuleID: CanonCanvas
Version: 0.3.6
DocRole: QuickRefCard
Audience: Users (pocket cheat sheet)

---

## Core
- Chat is exploration; canvas is canon.
- Canvas is long-term project memory while CanonCanvas is active.
- CanonCanvas targets markdown canvases only.
- Look-before-leap: bind/open existing matching `🛜` canvas before creating any new one.
- Opening the canvas in UI is the primary user selection signal; never instruct non-existent "set active" controls.
- If bind state is unclear, ask for exact-title confirmation (`use 🛜 <ProjectName> - <CanvasPurpose>`) and bind that title.
- Sections are dynamic: create only when needed; avoid empty template prefill.
- Do not assume client context; use client sections only when explicitly requested/provided.
- ResponseEnvelope: `main_plus_patch` (or `markdown_payload` for export).

## Lifecycle
- `canoncanvas load`
- `canoncanvas activate`
- `canoncanvas sleep`
- `canoncanvas unload`
- `canoncanvas status`

## Canon passes
- `canoncanvas canonize`
- `canoncanvas cleanup` (alias: `🧹CleanUp`)
- `canoncanvas lastcall` (alias: `🍺LastCall`)
- LastCall is a ritual pass, not a module and not a header title.
- LastCall is safety-net pass, not the primary update mechanism.
- LastCall output must include:
  - canon sync of recent decisions/constraints
  - Appendix A footnote capture for decision reasoning/context changes
  - OQ integrity sweep
  - handoff notes with context-not-in-`🛜` + "grab-the-torch" next actions
  - younger-self tail block using exact header `### 🚸 assistant's 👴🏼 note to → 📝 → younger 👶🏻 self`
  - one short note line in that block by default (playful/snarky allowed)

## Open Questions controls
- OQ headers appear only when unresolved questions exist.
- Resolve: `canoncanvas resolve B2` (or shorthand `B2`)
- Multi-answer shorthand: `C2, F3, G1` or `B2 C3 D1`
- Optional answer marker: leading `❓`, `[?]`, `[OQ]`, `[Answers]`
- Prune: `canoncanvas prune B1,3,D3` (or `❌B1,3,D3` / `Bx4`)
- Keep-list shorthand (single-select default): `B1,3,5` keeps listed options and strikes other B options
- Choose-many override: if question says choose-many/select all that apply, `B1,3,5` selects many and does not auto-prune others
- OQ question format: `### B) Title` (header, not bullet)
- Resolved collapse format:
  - `### ~~B) Title~~ ✅`
  - `Chosen: \`selected option text 🥇\``
- Do not add shorthand helper lines inside canvas; if needed, provide a tiny cheat sheet in chat only.

## Export
- `canoncanvas export markdown` (alias: `🛜export`)

## Naming
- Use `🛜 <ProjectName> - <CanvasPurpose>` for CanonCanvas canvases.
- Use PascalCase for `<ProjectName>` when applicable.
- Example: `🛜 LogKit - dev R6`
- Re-open existing matching `🛜` canvas when present; avoid duplicate creation by default.
- Create a new `🛜` canvas only when no match exists or user explicitly asks for a new one.
- Do not create a new canvas as a workaround for missing active-canvas telemetry.

## Header library (WIP)
- Prefer standard recurring headers from UserGuide `4.1`.
- Improvise only when needed, then keep placement logical.
- Handoff header standard: `## 👴🏼 Fork Handoff Notes` only.

## Client mode (conditional)
- Enable only with explicit client context (user says client project or provides client brief text).
- `⚖️ Client Requests`: mandatory client asks; preserve short source wording verbatim when available.
- `💡 Our Ideas`: additive ideas that build on `⚖️` requirements.
- In non-client work, avoid client headers and use neutral sections instead.

## Fork signals
- `💾` = SavePoint marker (good fork-back anchor).
- `⚡` = Forked marker (immediately re-read canvas, consume stale handoff carry-forward, then continue).
- Canvas persistence across forks is treated as an operational invariant for this workflow.
- `## 👴🏼 Fork Handoff Notes` is transient, final-position only, and should not accumulate across repeated forks.

## OQ hygiene
- Stable question letters.
- Stable option numbers.
- Ordered-list options use `1.` style.
- Keep ranking emojis at the end of option lines when present.
- Strike pruned options with trailing `❌`.
- Keep Open Questions and Resolved Decisions separate.
