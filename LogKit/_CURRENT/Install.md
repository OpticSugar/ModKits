# LogKit Install

ModuleID: LogKit
Version: 0.4.6
DocRole: Install
Audience: Users and assistants deploying LogKit

## Required Artifacts
- `UserGuide.md` (canon)
- `MachineManual.md`
- `QuickRefCard.md`
- Default `🖨️ Log` canvas (JSON code canvas)

## Install Steps
1. Place LogKit docs in the project/module folder.
2. Discover existing canvases whose names start with `🖨️ `.
3. If `🖨️ Log` already exists, open/bind it and do not create another default ledger.
4. If no `🖨️` ledger exists, create default `🖨️ Log` as a JSON code canvas.
5. Optional additional ledgers use `🖨️ <PurposeName>` and are created only on explicit user request.
6. Treat user-opened canvas as primary selection signal; if active state is unclear, ask for exact bind confirmation (`use 🖨️ <Name>`) instead of creating a duplicate.
7. Never suggest non-existent "set active canvas" UI controls.
8. Never create a new ledger solely because active-canvas telemetry is unavailable.
9. Ensure line 1 is:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
10. Ensure writes target exactly one active ledger per turn.
11. Start runtime:
- `logkit load [lane]`
- `logkit activate`
- `logkit status`
12. Validate guardrails by attempting a capture and explicit flush.

## Post-install Validation
- `logkit status` returns `life=active` and `ledger=ok`.
- `🖨️` alone does not flush pending entries.
- `🖨️Flush` commits and clears pending.
- Export produces JSONL with provenance entry.
- Emoji-only invocation check: `🖨️ status` resolves to `logkit status`.

## Failure Handling
- If target ledger exists but is not a JSON code canvas: fail closed and request a JSON code ledger target.
- If more than one canvas is named `🖨️ Log`: fail closed and require explicit target selection.
- If active-canvas telemetry is unavailable: fail closed and request explicit bind text (`use 🖨️ <Name>`); do not create a duplicate ledger.
- If canvas cannot be created/opened: load `CanvasTroubleshooting.md` and report blocker conditions before retry.
- If multiple ledgers exist: require explicit target selection before enabling commits.
- If META is missing: add required line and re-run `logkit status`.
- If emoji name renders blank/ambiguous (for example, visually blank emoji-prefixed tokens): fail closed and request explicit `🖨️ <Name>` confirmation.
