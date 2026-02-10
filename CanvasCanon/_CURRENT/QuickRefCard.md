# CanvasCanon QuickRefCard (derived)

ModuleID: CanvasCanon
Version: 0.2.0
DocRole: QuickRefCard
Audience: Users (pocket cheat sheet)

---

## Core
- Chat is exploration; canvas is canon.
- ResponseEnvelope: `main_plus_patch` (or `markdown_payload` for export).

## Lifecycle
- `canvascanon load`
- `canvascanon activate`
- `canvascanon sleep`
- `canvascanon unload`
- `canvascanon status`

## Canon passes
- `canvascanon canonize`
- `canvascanon cleanup` (alias: `🧹CleanUp`)
- `canvascanon lastcall` (alias: `🍺LastCall`)
- LastCall output must include:
  - canon sync of recent decisions/constraints
  - Appendix A footnote capture for decision reasoning/context changes
  - OQ integrity sweep
  - handoff notes with context-not-in-`🛜` + "grab-the-torch" next actions
  - optional one-line "note to younger self"

## Open Questions controls
- Resolve: `canvascanon resolve B2` (or shorthand `B2`)
- Multi-answer shorthand: `C2, F3, G1` or `B2 C3 D1`
- Optional answer marker: leading `❓`, `[?]`, `[OQ]`, `[Answers]`
- Prune: `canvascanon prune B1,3,D3` (or `❌B1,3,D3` / `Bx4`)
- Keep-list shorthand (single-select default): `B1,3,5` keeps listed options and strikes other B options
- Choose-many override: if question says choose-many/select all that apply, `B1,3,5` selects many and does not auto-prune others
- OQ question format: `### B) Title` (header, not bullet)
- Resolved collapse format:
  - `### ~~B) Title~~ ✅`
  - `Chosen: \`selected option text 🥇\``
- Do not add shorthand helper lines inside canvas; if needed, provide a tiny cheat sheet in chat only.

## Export
- `canvascanon export markdown` (alias: `🛜export`)

## Naming
- Use `🛜<ProjectName> - <Purpose>` for CanvasCanon canvases.
- Use PascalCase for `<ProjectName>` when applicable.
- Example: `🛜LogKit - dev R6`

## OQ hygiene
- Stable question letters.
- Stable option numbers.
- Ordered-list options use `1.` style.
- Keep ranking emojis at the end of option lines when present.
- Strike pruned options with trailing `❌`.
- Keep Open Questions and Resolved Decisions separate.
