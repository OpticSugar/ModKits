# LogKit MachineManual

ModuleID: LogKit
Version: 0.4.0
DocRole: MachineManual
Audience: Assistant runtime operator

## Runtime Intent
Operate LogKit safely with fail-closed writes, explicit commit control, and configurable triage/export/retrieval behavior.

## Non-negotiables
- Treat `UserGuide.md` as canon.
- Write only to active `🖨️ Log` with valid META header.
- `🖨️` authorizes logging intent; it does not flush.
- Commit pending only on `logkit commit all` / `🖨️Flush`.
- If required artifacts are missing, fail closed and queue pending.

## Command Execution Contract

| Canon | Aliases | Inputs | Runtime action |
|---|---|---|---|
| `logkit load` | `🖨️ on` | `lane?: string` | Set lifecycle `loaded`; init state/config |
| `logkit activate` | `🖨️ activate` | none | Set lifecycle `active` |
| `logkit sleep` | `🖨️ sleep` | none | Set lifecycle `sleep` |
| `logkit unload` | `🖨️ off` | none | Clear volatile state, keep committed data |
| `logkit status` | `🖨️ status` | none | Emit lifecycle/queue/ledger status |
| `logkit capture` | `🖨️Log:` | `text: string` | Append candidate to pending |
| `logkit commit all` | `🖨️Flush`, `🖨️LogIt!` | none | Validate ledger, commit pending, clear queue |
| `logkit commit ids` | `🖨️001,003` | `ids: csv<int>` | Commit selected chip candidates |
| `logkit amend` | `🖨️Amend <id>:` | `id`, `delta` | Append linked amendment entry |
| `logkit overwrite` | `🖨️Overwrite <id>:` | `id`, `replacement` | Replace entry, increment revision |
| `logkit export` | `🛅 export` | `filter` | Produce JSONL + provenance |
| `logkit retrieve` | `🗄️ find` | `query`, `filter?` | Query attached/indexed logs |
| `logkit config set` | `🖨️ config` | `key`, `value` | Update config key |

## State Keys
- `logkit.lifecycle`
- `logkit.lane`
- `logkit.pending`
- `logkit.last_chip_set`
- `logkit.config`
- `logkit.ledger_health`

## Ledger Validation Routine
Before any write:
1. Verify exactly one `🖨️ Log` exists.
2. Verify active canvas is `🖨️ Log`.
3. Verify line 1 META header:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
4. If any check fails, set `logkit.ledger_health` and queue pending.

## Triage Routine
- Honor `logkit.config.triage_mode` (`strict|balanced|capture_all`).
- AutoLog only for high-confidence durable records.
- Use PrintGate chips for uncertain candidates.
- Keep chip numbering monotonic for the chat session.

## Lifecycle Controls
- `load`: initialize config + lane defaults.
- `activate`: allow capture/commit behavior.
- `sleep`: pause proactive triage, keep state.
- `unload`: clear volatile state and deactivate behavior.
- `status`: report lifecycle, queue depth, and artifact readiness.

## Output Envelope
- Default: `main_plus_microtail`.
- Microtail format: `LK[life=<state> queue=<n> ledger=<health> lane=<lane>]`.
- Structured outputs for `status`, `export`, and `retrieve`.

## Export and Retrieval Rules
- Export format is JSONL entry-per-line with provenance record.
- Retrieval may only search attached/indexed artifacts.
- Never fabricate results from inaccessible contexts.

## Security Rules
- Respect `logkit.config.privacy` policy.
- Block export when policy forbids data class transfer.
- Apply redaction behavior before export when configured.
- Track provenance for export/retrieval actions.

## Failure Behavior
- Missing ledger/canvas/meta: fail closed and provide exact remediation.
- Duplicate ledger: halt commits until user designates canonical ledger.
- Unavailable service/index: return failure and request artifact attachment.
