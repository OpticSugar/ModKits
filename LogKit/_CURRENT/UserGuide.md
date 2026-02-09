# LogKit UserGuide

ModuleID: LogKit
Version: 0.4.0
DocRole: UserGuide
Audience: Users, developers, and assistants operating LogKit

## Mission
LogKit captures durable signals from chat into a reliable log lifecycle:
`capture -> triage -> commit -> package -> serve -> retrieve -> archive`.

The goal is one module that can handle software issues, product ideas, feedback inboxes, household inventory logs, and creative production workflows.

## Scope
- Canonical runtime ledger in chat: `LogKit Log` canvas (emoji alias: `🖨️ Log`).
- Portable transfer format: `🛅 LogPak` (`.jsonl`).
- Long-term storage: `🗄️ LogVault` (service + files).
- Retrieval in any chat/account/project by attaching or indexing LogPak/Vault artifacts.

## Canonical Commands

| Command | Canon | Aliases | Inputs | Output shape | State effects |
|---|---|---|---|---|---|
| Load module | `logkit load` | `🖨️ on` | `lane?: string` | `main_plus_microtail` | Sets `logkit.lifecycle=loaded`; initializes defaults |
| Activate session | `logkit activate` | `🖨️ activate` | none | `main_plus_microtail` | Sets `logkit.lifecycle=active`; enables capture |
| Sleep session | `logkit sleep` | `🖨️ sleep` | none | `main_plus_microtail` | Sets `logkit.lifecycle=sleep` |
| Unload module | `logkit unload` | `🖨️ off` | none | `main_plus_microtail` | Clears volatile state; keeps committed ledger |
| Status | `logkit status` | `🖨️ status` | none | `structured_status` | Reports lifecycle, queue, ledger health |
| Force capture | `logkit capture` | `🖨️Log:` | `text: string` | `main_plus_microtail` | Appends candidate to `logkit.pending` |
| Commit pending | `logkit commit all` | `🖨️Flush`, `🖨️LogIt!` | none | `main_plus_microtail` | Writes pending entries, clears queue |
| Commit selected chips | `logkit commit ids` | `🖨️001,003` | `ids: csv<int>` | `main_plus_microtail` | Commits selected candidates |
| Amend entry | `logkit amend` | `🖨️Amend <id>:` | `id: string`, `delta: string` | `main_plus_microtail` | Appends amendment entry linked via `supersedes` |
| Overwrite entry | `logkit overwrite` | `🖨️Overwrite <id>:` | `id: string`, `replacement: string` | `main_plus_microtail` | Replaces target entry, increments `rev` |
| Export package | `logkit export` | `🛅 export` | `filter: lane|ids|dateRange` | `structured_export` | Emits JSONL + provenance record |
| Retrieve logs | `logkit retrieve` | `🗄️ find` | `query: string`, `filter?: object` | `structured_results` | Reads service/index; no ledger mutation |
| Configure runtime | `logkit config set` | `🖨️ config` | `key: string`, `value: json` | `structured_status` | Updates `logkit.config` |

### Trigger Rule
- Any user message containing `🖨️` authorizes logging intent for the current turn.
- Authorization does not imply commit. Commit is explicit via `logkit commit all` (or alias `🖨️Flush`).

## ResponseEnvelope
- Default runtime envelope: `main_plus_microtail`.
- `main`: direct answer or action summary.
- `microtail`: compact operational tail when state changed, format:
  - `LK[life=<state> queue=<n> ledger=<ok|missing|inactive> lane=<lane>]`
- `logkit status`, `logkit export`, `logkit retrieve` may return structured blocks.

## State Contract
Authoritative persisted artifacts:
- `LogKit Log` canvas (emoji alias `🖨️ Log`, chat-level ledger)
- `🛅 LogPak` JSONL exports
- `🗄️ LogVault` data/index

Volatile runtime state keys:
- `logkit.lifecycle`: `unloaded|loaded|active|sleep`
- `logkit.lane`: active lane name
- `logkit.pending`: array of uncommitted candidates
- `logkit.last_chip_set`: map of chip id to candidate payload
- `logkit.config`: config object (schema below)
- `logkit.ledger_health`: `ok|missing|inactive|invalid_meta|duplicate`

## Canvas Naming Contract
- Canonical ASCII ledger canvas name: `LogKit Log`
- Emoji alias: `🖨️ Log`
- If emoji rendering is unavailable or ambiguous, always use `LogKit Log`.
- Assistants must never infer names like `️ Log`; unresolved names fail closed.

## Required Ledger Guardrails
1. Single-ledger rule: exactly one ledger canvas per chat named `LogKit Log` or `🖨️ Log`.
2. Pre-write checks (both required):
- Active canvas is `LogKit Log` or `🖨️ Log`.
- Line 1 META header exists exactly:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
3. Fail closed: if checks fail, queue to `logkit.pending`; do not write elsewhere.

## Entry Schema (`logkit.entry.v1`)
Required keys:
- `id`: `LE-YYMMDD-aaa`
- `date`: `YYYY-MM-DD`
- `lane`: string
- `source`: `userDump|userDirect|assistantObservation|systemImport`
- `title`: short headline (no horizontal scroll target)
- `description`: concise summary paragraph
- `status`: `PROPOSED|LOCK`
- `kind`: `WIN|LANDMINE|DECISION|EXPERIMENT|WORKFLOW|FIX|EXPORT|IDEA|ISSUE|SUGGESTION|ASSET`

Recommended keys:
- `scope`: string[]
- `details`: string[]
- `keywords`: string[]
- `security`: object
- `related`: string[]
- `supersedes`: string|null
- `rev`: integer

Compatibility rule:
- Legacy `discovery` maps to `description` on ingest/export.

## Config Schema (`logkit.config.v1`)
```json
{
  "schema": "logkit.config.v1",
  "default_lane": "General",
  "triage_mode": "balanced",
  "autolog": {
    "enabled": true,
    "confidence_threshold": 0.85
  },
  "privacy": {
    "redaction_mode": "warn",
    "block_pii_on_export": true,
    "allow_secrets": false
  },
  "storage": {
    "adapter": "file_jsonl",
    "service_profile": "personal_local"
  },
  "retrieval": {
    "index_mode": "keyword",
    "max_results": 12
  }
}
```

### Triage Modes
- `strict`: mostly PrintGate, low AutoLog.
- `balanced`: AutoLog for durable signals; PrintGate for uncertain entries.
- `capture_all`: high capture for intake/brainstorm sessions.

## Lifecycle Design
### 1) Capture from chat
- Signals arrive from normal chat, explicit commands, or chip selection.
- Entries enter pending if commit preconditions are not met.

### 2) Triage
- AutoLog when confidence is high on durable value.
- PrintGate chips for uncertain candidates (`001`, `002`, ... monotonic).

### 3) Service and serving model
- `LogVault` service can be file-backed, repo-backed, or API-backed.
- Minimum service responsibilities:
- schema validation
- dedupe (`id` + hash)
- amendment linkage (`supersedes`)
- export/retrieval endpoints

### 4) Retrieval across contexts
- Retrieval requires explicit artifact availability. No hidden cross-account memory.
- Supported contexts:
- Enterprise project chat: attach/import LogPak or index enterprise vault.
- Personal account chat: attach/import personal LogPak or index personal vault.
- Project-root chat and non-project chat: same rule, attach/import artifacts first.
- Recommended bridge format between accounts/projects: signed or checksummed LogPak JSONL.

### 5) Security model
- Data classes: `public|internal|confidential|restricted` via `security.classification`.
- Enforce per-export policy:
- redact secrets/PII when configured
- disallow restricted export to lower-trust destinations
- append provenance record for every export/retrieve operation
- Never assume account-level permissions transfer between enterprise and personal contexts.

## ID Strategy
- Format: `LE-YYMMDD-aaa`
- `aaa`: uppercase base36 2-second tick.
- On collision: bump tick until unique.
- Overflow uses remaining base36^3 headroom.

## Arbitration Policy
When multiple modules may respond:
1. Explicit invocation wins.
2. If output shapes conflict, ask user which module wins.
3. Otherwise prefer currently active `AUTO` module.
4. Persist winner for session until changed.

## EmojiGlossary
- `🖨️`: alias for logging intent and ledger canvas `LogKit Log`.
- `🛅`: export/transport package alias (`LogPak`).
- `🗄️`: archive/retrieval alias (`LogVault`).
- `🛂`: PrintGate triage metaphor.
- `🫟`: InkTest triage rubric metaphor.

## Regression Minimum
Must pass before release:
1. Missing ledger fails closed and queues pending.
2. Wrong active canvas never commits.
3. `🖨️` alone does not flush.
4. `🖨️Flush` commits and clears pending.
5. Chip commit (`🖨️001,003`) writes selected only.
6. Amend creates linked revision behavior.
7. Export emits JSONL with provenance record.
8. Retrieval returns only attached/indexed artifacts.
9. Security policy blocks restricted export.

## Version Notes
- Previous runtime lineage mapped to `0.3.2`.
- This upgrade is `0.4.0` for lifecycle + config + security expansion while remaining pre-1.0.
