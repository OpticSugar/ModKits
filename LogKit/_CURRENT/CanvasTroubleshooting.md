# LogKit Canvas Troubleshooting
Use only when `LogKit` launch failed to create/open a real `🖨️` canvas.

ModuleID: LogKit
Version: 0.1.2
DocRole: QuickRefCard
Audience: Users and assistants
LastUpdated: 2026-02-18
Owner: ModuleMill

## Truth Rule
- Never claim LogKit is launched unless a real canvas is created/opened and bound.
- Never fake canvas creation by dumping canvas-shaped content in chat.
- If checks fail, keep LogKit inactive.

## Success Checks
- Canvas title starts with `🖨️ ` and target is `🖨️ Log` unless user selected another ledger.
- Canvas is real/open and bound for this turn.
- If active-canvas telemetry is missing, exact user bind confirmation (`use 🖨️ <Name>`) is accepted.
- Target canvas type is JSON code canvas.
- META line 1 exists exactly:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```

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
- `load log kit`

### Canvas capability disabled in GPT
Detected conditions:
- fails in this GPT but works in normal chat/another GPT
What you need to do:
1. Enable Canvas in GPT Builder capabilities.
2. Save and retry.
Retry command:
- `load log kit`

### Workspace or service issue
Detected conditions:
- `/canvas` or add-canvas fails despite eligible model/settings
What you need to do:
1. Hard refresh and retry in a new chat.
2. Check `https://status.openai.com`.
3. If still failing, contact admin/support with model, workspace, time, and error text.
Retry command:
- `load log kit`

### Wrong target canvas type
Detected conditions:
- target `🖨️` canvas is markdown/plain canvas instead of JSON code canvas
What you need to do:
1. Do not write to the wrong-type canvas.
2. Create/open a JSON code canvas ledger named `🖨️ <PurposeName>` (default `🖨️ Log` when available).
3. Add the required META line and retry.
Retry command:
- `load log kit`

### Duplicate default ledger names
Detected conditions:
- more than one canvas named `🖨️ Log`
What you need to do:
1. Choose one canonical winner for active writes.
2. Mark the other as non-active archive/scratch.
3. Retry with explicit target confirmation.
Retry command:
- `load log kit`

### Active-canvas signal unavailable
Detected conditions:
- user has canvas open but runtime cannot detect active canvas binding
What you need to do:
1. Keep the intended ledger canvas open.
2. Reply with explicit bind text using exact title: `use 🖨️ <Name>` (default `use 🖨️ Log`).
3. Assistant must bind that exact title and continue; do not create a duplicate ledger.
Retry command:
- `load log kit`
