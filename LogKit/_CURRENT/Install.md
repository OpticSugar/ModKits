# LogKit Install

ModuleID: LogKit
Version: 0.4.4
DocRole: Install
Audience: Users and assistants deploying LogKit

## Required Artifacts
- `UserGuide.md` (canon)
- `MachineManual.md`
- `QuickRefCard.md`
- Default `🖨️ Log` canvas (JSON code canvas)

## Install Steps
1. Place LogKit docs in the project/module folder.
2. Create or verify default ledger canvas named `🖨️ Log` (capital `L`).
3. Optional: create additional ledgers using `🖨️ <PurposeName>`.
4. Ensure line 1 is:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
5. Ensure writes target exactly one active ledger per turn.
6. Start runtime:
- `logkit load [lane]`
- `logkit activate`
- `logkit status`
7. Validate guardrails by attempting a capture and explicit flush.

## Post-install Validation
- `logkit status` returns `life=active` and `ledger=ok`.
- `🖨️` alone does not flush pending entries.
- `🖨️Flush` commits and clears pending.
- Export produces JSONL with provenance entry.
- Emoji-only invocation check: `🖨️ status` resolves to `logkit status`.

## Failure Handling
- If canvas cannot be created: stop and request manual creation/opening of `🖨️ Log`.
- If multiple ledgers exist: require explicit target selection before enabling commits.
- If META is missing: add required line and re-run `logkit status`.
- If emoji name renders blank/ambiguous (for example, visually blank emoji-prefixed tokens): fail closed and request explicit `🖨️ <Name>` confirmation.
