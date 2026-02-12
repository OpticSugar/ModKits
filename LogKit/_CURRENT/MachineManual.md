# LogKit MachineManual

ModuleID: LogKit
Version: 0.4.4
DocRole: MachineManual
Audience: Assistant runtime operator

## Runtime Intent
Operate LogKit safely with fail-closed writes, explicit commit control, and configurable triage/export/retrieval behavior.

## Non-negotiables
- Treat `UserGuide.md` as canon.
- Write only to one active target ledger named `🖨️ <Name>` (default `🖨️ Log`, capital `L`) with valid META header.
- `🖨️` authorizes logging intent; it does not flush.
- Commit pending only on `logkit commit all` / `🖨️Flush`.
- If required artifacts are missing, fail closed and queue pending.
- If a command has an emoji alias, accept emoji-only invocations per UserGuide mapping.
- Every entry includes `time` in `HH:MM:SS` (24-hour) for deterministic ID repair.
- Entry `title` is a newspaper-style headline; if it needs horizontal scroll, rewrite shorter.

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
1. Discover candidate ledgers whose names start with `🖨️ `.
2. Verify exactly one target ledger is selected for the write turn.
3. Verify active canvas equals selected target ledger.
4. Verify selected target ledger name is either default `🖨️ Log` (capital `L`) or `🖨️ <PurposeName>`.
5. Verify line 1 META header:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
6. If any check fails, set `logkit.ledger_health` and queue pending.

## Triage Routine
- Honor `logkit.config.triage_mode` (`strict|balanced|capture_all`).
- AutoLog only for high-confidence durable records.
- Use PrintGate chips for uncertain candidates.
- Keep chip numbering monotonic for the chat session.

## Entry Schema Routine
Before commit, enforce minimum entry fields:
- `id`, `date`, `time`, `lane`, `source`, `title`, `description`, `status`, `kind`
- `time` must match `HH:MM:SS` (24-hour local capture time)
- `title` must be short headline style (not long sentence blocks)

## ID Generation Routine
Deterministic suffix formula (seconds-in-day / 2 rule):
1. Parse `time` as `HH:MM:SS`.
2. Compute `seconds_in_day = HH*3600 + MM*60 + SS`.
3. Compute `tick = floor(seconds_in_day / 2)`.
4. Compute `aaa = BASE36_UPPER(tick).padStart(3, "0")`.
5. Assemble ID as `LE-YYMMDD-aaa` using `date` for `YYMMDD`.
6. On collision, increment `tick` until unique.
7. If existing `id` and `time` disagree, recompute from `time` and correct `id`.

## Emoji Resolution Routine
When a user message includes only emoji tokens:
1. Resolve via declared alias map in `UserGuide.md`.
2. If a unique mapping exists, execute it.
3. If multiple mappings are possible, ask a one-line disambiguation question.
4. Never drop a declared emoji alias from interpretation.

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
- Ambiguous target when multiple ledgers exist: fail closed and request explicit target (`🖨️ <PurposeName>`).
- Unavailable service/index: return failure and request artifact attachment.
- Ambiguous or malformed emoji-only names (for example lone `️`): fail closed and require explicit `🖨️ <Name>` confirmation.
- Never rename the ledger canvas to a legacy ASCII fallback name.
