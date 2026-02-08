# CanvasCanon Install (derived)

ModuleID: CanvasCanon
Version: 0.2.0
DocRole: Install
Audience: Users + assistants (bootstrap + recovery)

---

## 1) Enable or disable
Say one of:
- "Enable CanvasCanon in this chat."
- "Disable CanvasCanon in this chat."
- "Sleep CanvasCanon for now."

ASCII canon equivalents:
- `canvascanon load`
- `canvascanon activate`
- `canvascanon sleep`
- `canvascanon unload`
- `canvascanon status`

## 2) Default behavior when enabled
- Treat canvas as authoritative canon.
- Keep chat exploratory and compile conclusions into canvas patches.

## 3) Core operations
- Canon pass: `canvascanon canonize`
- Cleanup pass: `canvascanon cleanup`
- Pre-fork pass: `canvascanon lastcall`
- Resolve Open Question: `canvascanon resolve B2`
- Prune option(s): `canvascanon prune B1,3,D3`
- Export: `canvascanon export markdown`

## 4) Naming rule
- Use `🛜<ProjectName> - <Purpose>` for any CanvasCanon-bound canvas.
- Use PascalCase for `<ProjectName>` when applicable.
- Example: `🛜LogKit - dev R6`

## 5) If the module seems out of sync
Symptoms: stale decisions, mixed open/resolved items, noisy canvas body.
Recovery:
1. Run `canvascanon cleanup`.
2. Run `canvascanon canonize`.
3. Run `canvascanon status` and verify active state.
4. If sections are missing, provide the latest canvas content and rerun.

## 6) Collision behavior
If another active module requires a conflicting output shape, CanvasCanon must ask user to choose a single winner.
