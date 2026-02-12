# CanonCanvas Install (derived)

ModuleID: CanonCanvas
Version: 0.2.0
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

## 3) Core operations
- Canon pass: `canoncanvas canonize`
- Cleanup pass: `canoncanvas cleanup`
- Pre-fork pass: `canoncanvas lastcall`
- Resolve Open Question: `canoncanvas resolve B2`
- Prune option(s): `canoncanvas prune B1,3,D3`
- Export: `canoncanvas export markdown`

## 4) Naming rule
- Use `🛜 <ProjectName> - <CanvasPurpose>` for any CanonCanvas-bound canvas.
- Use PascalCase for `<ProjectName>` when applicable.
- Example: `🛜 LogKit - dev R6`

## 5) If the module seems out of sync
Symptoms: stale decisions, mixed open/resolved items, noisy canvas body.
Recovery:
1. Run `canoncanvas cleanup`.
2. Run `canoncanvas canonize`.
3. Run `canoncanvas status` and verify active state.
4. If sections are missing, provide the latest canvas content and rerun.

## 6) Collision behavior
If another active module requires a conflicting output shape, CanonCanvas must ask user to choose a single winner.
