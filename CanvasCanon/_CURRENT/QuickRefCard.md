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

## Open Questions controls
- Resolve: `canvascanon resolve B2` (or shorthand `B2`)
- Prune: `canvascanon prune B1,3,D3` (or `❌B1,3,D3`)
- OQ shorthand line (required): `*Reply shorthand:* \`B5\`, \`C2\`, \`F3\`, etc.`
- OQ question format: `### B) Title` (header, not bullet)
- Resolved collapse format:
  - `### ~~B) Title~~ ✅`
  - `Chosen: \`value\``

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
- Strike pruned options with trailing `❌`.
- Keep Open Questions and Resolved Decisions separate.
