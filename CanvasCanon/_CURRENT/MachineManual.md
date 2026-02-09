# CanvasCanon MachineManual (derived)

ModuleID: CanvasCanon
Version: 0.2.0
DocRole: MachineManual
Audience: Assistants operating CanvasCanon at runtime

---

## Runtime contract
- Treat `UserGuide` as canonical.
- Enforce fail-closed behavior when canvas artifacts are missing.
- Do not invent commands, state keys, or output shapes.

## ResponseEnvelope
- Default: `main_plus_patch`
- Status: `structured_status`
- Export: `markdown_payload`

## 1) Minimal state
Maintain:
- `canvascanon.active`
- `canvascanon.canvas_name`
- `canvascanon.canvas_bound`
- `canvascanon.last_canon_pass_at`
- `canvascanon.open_questions_index`
- `canvascanon.resolved_index`
- `canvascanon.footnote_counter`

## 2) Lifecycle controls
- `canvascanon load`: initialize state and activate
- `canvascanon activate`: set active true
- `canvascanon sleep`: set active false, preserve state
- `canvascanon unload`: clear state
- `canvascanon status`: emit structured status

## 3) Command interpretation
### 3.1 Canon/care commands
- `canvascanon canonize`: produce canon patch from recent decisions.
- `canvascanon cleanup`: remove duplication/noise while preserving rules.
- `canvascanon lastcall`: canon pass + OQ/Resolved check + handoff notes.

### 3.2 Open Questions operations
- `canvascanon resolve <letter><option>` accepts shorthand like `B2`.
- `canvascanon prune <refs>` accepts syntax like `B1,3,D3` and applies strikeout with `❌`.
- Lone trailing `❌` in canvas lines should be interpreted as prune intent for that line item.
- OQ section must include the shorthand line: `*Reply shorthand:* \`B5\`, \`C2\`, \`F3\`, etc.`
- OQ questions must be markdown headers (`### B) ...`), not bullets.

### 3.3 Export
- `canvascanon export markdown` returns the current canonical canvas as markdown payload.

## 4) Open Questions enforcement
- Use OQ terminology (`Open Questions` / `OQ`) consistently; do not emit `OC`.
- Keep stable question letters.
- Keep stable option numbering after references exist.
- Keep options in markdown ordered-list format (`1.` style).
- Resolved form must collapse to `~~<letter>) ...~~ ✅` plus `Chosen: <value>`.
- Do not mix unresolved queue with resolved records.

## 5) Fork protocol
On `canvascanon lastcall` / `🍺LastCall`:
1. Run canon pass.
2. Validate Open vs Resolved consistency.
3. Generate/update fork handoff notes with phase, in-flight items, next actions, risks, pointers.

## 6) Naming rules
- Enforce canvas title format: `🛜<ProjectName> - <Purpose>`.
- Require `🛜` prefix for all CanvasCanon-bound canvases.
- Use PascalCase for `<ProjectName>` when applicable.
- Runtime validator (strict): `^🛜[A-Z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)* - .+$`
- If a CanvasCanon-bound title fails the validator, fail closed and request a corrected title before continuing canon operations.
- Reference example: `🛜LogKit - dev R6`.
- Module folder and references use PascalCase `CanvasCanon` unless user overrides naming policy.

## 7) Failure handling
If canvas is unavailable, stale, or structurally ambiguous:
1. Stop speculative edits.
2. Ask for missing section/content.
3. Resume only after authoritative input is provided.
