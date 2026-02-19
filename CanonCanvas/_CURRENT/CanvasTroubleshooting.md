# CanonCanvas Troubleshooting
Use only when `CanonCanvas` launch failed to create/open a real `🛜` canvas.

ModuleID: CanonCanvas
Version: 0.1.2
DocRole: QuickRefCard
Audience: Users and assistants
LastUpdated: 2026-02-18
Owner: ModuleMill

## Truth Rule
- Never claim CanonCanvas is launched unless a real canvas is created/opened and bound.
- Never fake canvas creation by dumping canvas-shaped content in chat.
- If checks fail, keep CanonCanvas inactive.

## Success Checks
- Canvas title matches `🛜 <ProjectName> - <CanvasPurpose>`.
- Canvas is real/open and bound for this turn.
- If active-canvas telemetry is missing, exact user bind confirmation is accepted.
- Target canvas type is markdown.

## Failure Report Format (exact)
- `Blocker`
- `Detected conditions`
- `What you need to do`
- `Retry command`

## Common Blockers
### Unsupported model for canvas
Detected conditions:
- active model is Pro-series (for example `GPT-5.2 Pro`)
What you need to do:
1. Switch to a non-Pro model.
2. Retry launch.
Retry command:
- `load canon canvas`

### Canvas capability disabled in GPT
Detected conditions:
- fails in this GPT but works in normal chat/another GPT
What you need to do:
1. Enable Canvas in GPT Builder capabilities.
2. Save and retry.
Retry command:
- `load canon canvas`

### Workspace or service issue
Detected conditions:
- `/canvas` or add-canvas fails despite eligible model/settings
What you need to do:
1. Hard refresh and retry in a new chat.
2. Check `https://status.openai.com`.
3. If still failing, contact admin/support with model, workspace, time, and error text.
Retry command:
- `load canon canvas`

### Wrong target canvas type
Detected conditions:
- target `🛜` canvas is code/plain type instead of markdown
What you need to do:
1. Do not write canon content into the wrong-type canvas.
2. Open/create a markdown `🛜 <ProjectName> - <CanvasPurpose>` canvas.
3. Retry with the markdown canvas bound as target.
Retry command:
- `load canon canvas`

### Duplicate matching canvases
Detected conditions:
- multiple matching `🛜` canvases exist for the same project/purpose
What you need to do:
1. Choose one canonical winner.
2. Bind/reuse that winner for CanonCanvas operations.
3. Avoid creating another duplicate unless explicitly needed.
Retry command:
- `load canon canvas`

### Active-canvas signal unavailable
Detected conditions:
- user has intended `🛜` canvas open but runtime cannot detect active canvas binding
What you need to do:
1. Keep the intended canvas open.
2. Reply with explicit exact-title bind text: `use 🛜 <ProjectName> - <CanvasPurpose>`.
3. Assistant must bind that exact title and continue without creating a duplicate fallback canvas.
Retry command:
- `load canon canvas`
