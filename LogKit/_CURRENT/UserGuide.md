# LogKit UserGuide

ModuleID: LogKit
Version: 0.4.6
DocRole: UserGuide
Audience: Users, developers, and assistants operating LogKit

## Mission
LogKit captures durable signals from chat into a reliable log lifecycle:
`capture -> triage -> commit -> package -> serve -> retrieve -> archive`.

The goal is one module that can handle software issues, product ideas, feedback inboxes, household inventory logs, and creative production workflows.

### Mission backstory (why this exists)
LogKit exists because high-value discoveries in chat tend to disappear once the thread moves on. The module turns fragile conversational memory into durable, queryable records without requiring a separate app workflow mid-conversation.

Non-negotiable intent:
- preserve retrieval-grade records, not just short-term notes
- keep commit explicit so accidental logging does not pollute the ledger
- preserve emoji-first operator ergonomics while maintaining ASCII canon fallback

## Scope
- Default runtime ledger in chat: `🖨️ Log` JSON code canvas (capital `L` required).
- Additional ledgers are allowed when needed and must be named `🖨️ <PurposeName>`.
- Every LogKit ledger canvas name must start with `🖨️ ` (emoji + one space).
- Portable transfer format: `🛅 LogPak` (`.jsonl`).
- Long-term storage: `🗄️ LogVault` (service + files).
- Retrieval in any chat/account/project by attaching or indexing LogPak/Vault artifacts.

## Rationale and tradeoffs
- LogKit favors durable capture over short-term speed because retrieval and auditability matter more than minimal turn latency.
- Explicit commit is preserved as a guardrail to prevent accidental writes from ambiguous chat turns.
- Emoji aliases stay first-class for ergonomics, while ASCII canon remains mandatory for command fallback.
- Ledger naming is emoji-canonical: default is `🖨️ Log`, and additional ledgers follow `🖨️ <PurposeName>`.
- Fail-closed preconditions can feel strict, but they prevent silent corruption of ledger state.

## Guardrailed improvisation contract
LogKit is structured, but not robotic. Assistants should improvise wording in summaries and recommendations while preserving deterministic contracts.

Safe improv zones:
- title/description phrasing for captured entries
- concise recap language in `main_plus_microtail` responses
- query guidance wording during retrieval help

Locked zones:
- command semantics
- commit/flush gating behavior
- schema requirements
- ledger guardrails and fail-closed checks

## Examples
- Capture then commit all:
  - `🖨️Log: tighten module lint checks`
  - `🖨️Flush`
- Commit selected chips only:
  - `🖨️001,003`
- Export and retrieve:
  - `🛅 export lane=infra`
  - `🗄️ find lint regressions`

## Use-case playbooks
- Software/dev workflow:
  - capture regressions, architecture decisions, and patch notes into lane-specific streams
  - export `🛅 LogPak` for handoff or incident review
- Product and UX workflow:
  - log feedback snippets, hypotheses, and decision outcomes with traceable revisions
  - retrieve prior rationale quickly when roadmap debates recur
- Personal/home operations:
  - track inventory changes, recurring issues, and purchase decisions with clear audit history
  - keep one durable record model across contexts instead of ad hoc note formats

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

### Natural-language intent inference
- LogKit accepts explicit syntax and natural-language command intent.
- If wording maps with high confidence to a single canon command, execute that command.
- If confidence is low or multiple commands are plausible, ask one short clarification.
- Confidence should consider current lifecycle, queue state, and immediate turn context.
- Inferred intent never bypasses commit/overwrite safety checks or fail-closed artifact rules.

## Emoji-First Alias Contract
- Emoji aliases are first-class language, not decorative hints.
- If a concept has an emoji alias, assistants must preserve it in docs, runtime prompts, and examples.
- Emoji-only user commands are valid when they match a declared alias.
- Canonical ASCII commands remain the stable fallback.
- If any alias is ambiguous in context, ask a one-line clarification instead of guessing.

### Emoji-Only Command Map
Use these direct mappings when users communicate only by emoji tokens.

| Emoji input | Resolved command | Notes |
|---|---|---|
| `🖨️` | authorize logging intent for current turn | authorization only, not commit |
| `🖨️Flush` | `logkit commit all` | commit pending queue |
| `🖨️LogIt!` | `logkit commit all` | commit pending queue |
| `🖨️001,003` | `logkit commit ids 001,003` | commit selected chip ids |
| `🖨️Log: <text>` | `logkit capture <text>` | force capture |
| `🖨️Amend <id>: <delta>` | `logkit amend <id> <delta>` | append amendment |
| `🖨️Overwrite <id>: <replacement>` | `logkit overwrite <id> <replacement>` | replace entry |
| `🛅 export` | `logkit export <filter>` | package export |
| `🗄️ find <query>` | `logkit retrieve <query>` | retrieval query |
| `🖨️ status` | `logkit status` | state report |

## ResponseEnvelope
- Default runtime envelope: `main_plus_microtail`.
- `main`: direct answer or action summary.
- `microtail`: compact operational tail when state changed, format:
  - `LK[life=<state> queue=<n> ledger=<ok|missing|inactive> lane=<lane>]`
- `logkit status`, `logkit export`, `logkit retrieve` may return structured blocks.

## State Contract
Authoritative persisted artifacts:
- One or more `🖨️ <Name>` canvases (default `🖨️ Log`; chat-level ledgers)
- `🛅 LogPak` JSONL exports
- `🗄️ LogVault` data/index

Volatile runtime state keys:
- `logkit.lifecycle`: `unloaded|loaded|active|sleep`
- `logkit.lane`: active lane name
- `logkit.pending`: array of uncommitted candidates
- `logkit.last_chip_set`: map of chip id to candidate payload
- `logkit.config`: config object (schema below)
- `logkit.ledger_health`: `ok|missing|inactive|invalid_meta|wrong_type|duplicate|duplicate_default|ambiguous_target`

## Canvas Naming Contract
- Single-active-ledger rule: multi-ledger is allowed, but each write turn targets exactly one active ledger.
- Default ledger name: 🖨️ Log.
- Emoji-first ledger naming: 🖨️ <PurposeName>.
- Default ledger canvas name is `🖨️ Log` (capital `L` required).
- Additional ledgers must be named `🖨️ <PurposeName>`.
- The `🖨️` emoji must be the first character in every ledger canvas name.
- LogKit ledger canvases must be JSON code canvases.
- Look-before-leap binding: discover/open existing `🖨️` ledgers before creating any new ledger.
- User-side binding signal: opening a ledger canvas in UI is the primary target-selection control.
- If runtime cannot read active-canvas state, request one explicit bind confirmation (`use 🖨️ <Name>`) and treat it as authoritative.
- Never instruct non-existent UI controls for setting active canvas.
- Bind uncertainty alone is never permission to create a new ledger.
- Never create a second `🖨️ Log` when one already exists.
- Create an additional ledger only when user explicitly requests one.
- No ASCII fallback canvas name is allowed for canonical operations.
- Never rename any ledger to a legacy ASCII fallback name.
- Assistants must never emit or treat a lone variation selector (`U+FE0F`) as a valid alias token.
- If emoji rendering is unavailable or ambiguous, fail closed and ask user to confirm/open a canonical `🖨️ <Name>` canvas.
- Older docs may reference a legacy ASCII fallback name; treat that as legacy wording and map to default `🖨️ Log`.

## Required Ledger Guardrails
1. Multi-ledger allowed, but exactly one target ledger may be active for a write turn.
2. Target-ledger naming rule: active ledger name must match `🖨️ <Name>` (default `🖨️ Log`).
3. Pre-write checks (all required):
- Active canvas is the selected target ledger.
- If active-canvas telemetry is unavailable, explicit user bind confirmation for exact title is accepted as target proof.
- Active target is a JSON code canvas.
- Line 1 META header exists exactly:
```json
{"_":"META","tool":"LogKit","format":"PrettyJSONWithSentries","schema":"logkit.entry.v1"}
```
4. Fail closed: if checks fail, queue to `logkit.pending`; do not write elsewhere.

## Entry Schema (`logkit.entry.v1`)
Required keys:
- `id`: `LE-YYMMDD-aaa`
- `date`: `YYYY-MM-DD`
- `time`: `HH:MM:SS` (24-hour local capture time; required fallback for deterministic ID repair)
- `lane`: string
- `source`: `userDump|userDirect|assistantObservation|systemImport`
- `title`: short newspaper-style headline (scan-fast; no horizontal scroll target)
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

Title writing rule:
- Write `title` values like newspaper headlines, not article sentences.
- If a title requires horizontal scrolling in common editor panes, shorten and tighten wording.

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
- Deterministic suffix formula (seconds-in-day / 2 rule):
  - `seconds_in_day = HH*3600 + MM*60 + SS` (from `time`)
  - `tick = floor(seconds_in_day / 2)`
  - `aaa = BASE36_UPPER(tick).padStart(3, "0")`
- `aaa`: uppercase base36 2-second tick derived from `time`.
- Full ID: `LE-YYMMDD-aaa` where `YYMMDD` comes from `date`.
- On collision: bump tick until unique.
- Overflow uses remaining base36^3 headroom.
- If stored `id` suffix and `time` disagree, recompute from `time` and correct `id` deterministically.

## Arbitration Policy
When multiple modules may respond:
1. Explicit invocation wins.
2. If output shapes conflict, ask user which module wins.
3. Otherwise prefer currently active `AUTO` module.
4. Persist winner for session until changed.

## EmojiGlossary
| Emoji | Term | Meaning |
|---|---|---|
| `🖨️` | `LogIntentOrLedgerAlias` | Alias for logging intent and ledger namespace (`🖨️ Log`, `🖨️ <PurposeName>`). |
| `🛅` | `LogPakAlias` | Export and transport package alias (`LogPak`). |
| `🗄️` | `LogVaultAlias` | Archive and retrieval alias (`LogVault`). |
| `🛂` | `PrintGateAlias` | PrintGate triage metaphor for explicit commit gating. |
| `🫟` | `InkTestAlias` | InkTest triage rubric metaphor for confidence-based capture. |

Rule: when a documented emoji alias exists, do not omit it from operational guidance; publish both ASCII canon and emoji alias forms.

## Recovery and drift checks
If behavior feels partially installed or inconsistent:
1. Run `logkit status` and verify lifecycle + ledger health.
2. Confirm active target ledger follows `🖨️ <Name>`, is a JSON code canvas, and meets META header preconditions.
3. If assistant cannot detect active target reliably, keep intended ledger open and send explicit bind text (`use 🖨️ Log` or exact `use 🖨️ <Name>`).
4. Confirm there is not more than one canvas named `🖨️ Log`.
5. Use a minimal smoke flow:
  - `🖨️Log: smoke entry`
  - `🖨️Flush`
  - `🗄️ find smoke entry`
6. If any precondition is ambiguous, fail closed, report the exact blocker, and request the missing artifact/input.

## Documentation access fail-closed policy
If required LogKit docs are unavailable, do not claim LogKit is loaded, active, or being followed.

Required recovery flow:
1. Ask user to enable Web Search and retry doc fetch.
2. If fetch still fails, provide this URL pack and ask user to copy/paste returned content:
```text
https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/ModuleManifest.yaml
https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/Install.md
https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/QuickRefCard.md
https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/MachineManual.md
https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/UserGuide.md
```
3. Until docs are available, respond as a normal assistant and explicitly state that LogKit module behavior is not active for that turn.

## Regression Minimum
Must pass before release:
1. Missing ledger fails closed and queues pending.
2. Wrong-type target ledger (non-JSON canvas) fails closed and never commits.
3. Duplicate default ledger (`🖨️ Log`) fails closed until a winner is selected.
4. Wrong or ambiguous target ledger never commits.
5. `🖨️` alone does not flush.
6. `🖨️Flush` commits and clears pending.
7. Chip commit (`🖨️001,003`) writes selected only.
8. Amend creates linked revision behavior.
9. Export emits JSONL with provenance record.
10. Retrieval returns only attached/indexed artifacts.
11. Security policy blocks restricted export.
12. If active-canvas signal is missing, explicit `use 🖨️ <Name>` binds target and avoids duplicate-creation fallback.

## Version Notes
- Previous runtime lineage mapped to `0.3.2`.
- `0.4.0` introduced lifecycle + config + security expansion while remaining pre-1.0.
- `0.4.1` restores emoji-first alias clarity and emoji-only command resolution guidance.
- `0.4.2` adds explicit ID suffix formula, required `time`, and headline-style title guidance.
- `0.4.3` removed legacy ASCII fallback naming and standardized emoji-ledger operations.
- `0.4.4` sets default ledger name to `🖨️ Log` (capital `L`) and allows additional ledgers via `🖨️ <PurposeName>`.
- `0.4.5` enforces look-before-leap binding, JSON code-canvas requirement, and duplicate-default fail-closed behavior.
- `0.4.6` formalizes UI-open/exact-title binding semantics and forbids duplicate-creation fallback when active-canvas telemetry is missing.
