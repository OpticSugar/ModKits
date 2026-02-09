# LogKit QuickRef

ModuleID: LogKit
Version: 0.4.1
DocRole: QuickRefCard
Audience: Users and assistants

## Startup
1. `logkit load [lane]`
2. `logkit activate`
3. Confirm one active ledger named `LogKit Log` (emoji alias `🖨️ Log`) with valid META header

## Guardrails
- Single-ledger rule: one `LogKit Log` ledger per chat (emoji alias `🖨️ Log`).
- Pre-write checks required:
  - active canvas is `LogKit Log` or `🖨️ Log`
  - META line 1 is:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
- `🖨️` is authorization, not flush.
- Flush only on `logkit commit all` / `🖨️Flush`.

## Canon Commands
- `logkit load` (`🖨️ on`)
- `logkit activate` (`🖨️ activate`)
- `logkit sleep` (`🖨️ sleep`)
- `logkit unload` (`🖨️ off`)
- `logkit status` (`🖨️ status`)
- `logkit capture "text"` (`🖨️Log: <text>`)
- `logkit commit all` (`🖨️Flush`, `🖨️LogIt!`)
- `logkit commit ids <csv>` (`🖨️001,003`)
- `logkit amend <id> "delta"` (`🖨️Amend <id>:`)
- `logkit overwrite <id> "replacement"` (`🖨️Overwrite <id>:`)
- `logkit export <filter>` (`🛅 export`)
- `logkit retrieve "query"` (`🗄️ find`)
- `logkit config set <key> <json>` (`🖨️ config`)

## Emoji-Only Shortcuts
- `🖨️` = authorize logging intent
- `🖨️Flush` or `🖨️LogIt!` = commit all pending
- `🖨️001,003` = commit selected chips
- `🖨️Log: <text>` = capture text
- `🛅 export` = export package
- `🗄️ find <query>` = retrieve logs
- `🖨️ status` = status report

Hard rule: if an emoji shortcut exists, it is always valid input.

## State Keys
- `logkit.lifecycle`: `unloaded|loaded|active|sleep`
- `logkit.pending`: pending entries queue
- `logkit.lane`: active lane
- `logkit.config`: runtime policy profile
- `logkit.ledger_health`: `ok|missing|inactive|invalid_meta|duplicate`

## Entry Schema Minimum
Required:
- `id`, `date`, `lane`, `source`, `title`, `description`, `status`, `kind`

Enums:
- `source`: `userDump|userDirect|assistantObservation|systemImport`
- `status`: `PROPOSED|LOCK`
- `kind`: `WIN|LANDMINE|DECISION|EXPERIMENT|WORKFLOW|FIX|EXPORT|IDEA|ISSUE|SUGGESTION|ASSET`

## ID Rule
- `LE-YYMMDD-aaa`
- `aaa` is uppercase base36 2-second tick
- bump tick on collision

## Output Envelope
- Default: `main_plus_microtail`
- Tail: `LK[life=<state> queue=<n> ledger=<health> lane=<lane>]`

## Lifecycle
- `load` -> `activate` -> `sleep` -> `unload`
- `status` reports current position and health

## Retrieval Context Rule
Retrieval only works against attached/indexed LogPak/Vault artifacts in the current chat context (enterprise, personal, project, or root).

## Naming Fallback
If emoji rendering is unreliable, always use `LogKit Log` as the ledger name.
