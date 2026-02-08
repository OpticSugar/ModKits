# LogKit Install

ModuleID: LogKit
Version: 0.4.0
DocRole: Install
Audience: Users and assistants deploying LogKit

## Required Artifacts
- `UserGuide.md` (canon)
- `MachineManual.md`
- `QuickRefCard.md`
- `🖨️ Log` canvas (JSON code canvas)

## Install Steps
1. Place LogKit docs in the project/module folder.
2. Create or verify exactly one `🖨️ Log` canvas.
3. Ensure line 1 is:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
4. Start runtime:
- `logkit load [lane]`
- `logkit activate`
- `logkit status`
5. Validate guardrails by attempting a capture and explicit flush.

## Post-install Validation
- `logkit status` returns `life=active` and `ledger=ok`.
- `🖨️` alone does not flush pending entries.
- `🖨️Flush` commits and clears pending.
- Export produces JSONL with provenance entry.

## Failure Handling
- If canvas cannot be created: stop and request manual creation/opening of `🖨️ Log`.
- If duplicate ledgers exist: resolve to one canonical ledger before enabling commits.
- If META is missing: add required line and re-run `logkit status`.
