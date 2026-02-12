# LogKit QuickRef

ModuleID: LogKit
Version: 0.4.4
DocRole: QuickRefCard
Audience: Users and assistants

## Startup
1. `logkit load [lane]`
2. `logkit activate`
3. Confirm target ledger is `🖨️ <Name>` with valid META header (default `🖨️ Log`, capital `L`)

## Guardrails
- Multi-ledger allowed, but only one target ledger may be active for a write turn.
- Pre-write checks required:
  - active canvas is selected target `🖨️ <Name>`
  - default target name uses capital `L`: `🖨️ Log`
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
- `logkit.ledger_health`: `ok|missing|inactive|invalid_meta|duplicate|ambiguous_target`

## Entry Schema Minimum
Required:
- `id`, `date`, `time`, `lane`, `source`, `title`, `description`, `status`, `kind`

Title rule:
- Write titles like newspaper headlines.
- If a title causes horizontal scrolling, shorten it.

Enums:
- `source`: `userDump|userDirect|assistantObservation|systemImport`
- `status`: `PROPOSED|LOCK`
- `kind`: `WIN|LANDMINE|DECISION|EXPERIMENT|WORKFLOW|FIX|EXPORT|IDEA|ISSUE|SUGGESTION|ASSET`

## ID Rule
- `LE-YYMMDD-aaa`
- `seconds_in_day = HH*3600 + MM*60 + SS`
- `tick = floor(seconds_in_day / 2)`
- `aaa = BASE36_UPPER(tick).padStart(3, "0")`
- `aaa` is uppercase base36 2-second tick from `time`
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
- Default canonical ledger name is `🖨️ Log` (capital `L`).
- Additional ledger names follow `🖨️ <PurposeName>`.
- `🖨️` must be the first character in any ledger canvas name.
- If emoji rendering is unreliable, fail closed and ask user to confirm/open target `🖨️ <Name>`.
- Never rename the ledger to `LogKit Log` (retired fallback).
