# CanvasCanon UserGuide (canonical)

ModuleID: CanvasCanon
Version: 0.2.0
DocRole: UserGuide
Audience: Humans + module engineers (canonical source of truth)

---

## 0) What this is
CanvasCanon is a workflow that treats canvas as the durable project canon and chat as exploration.

Core law: if a decision affects future behavior, record it in canvas canon.

CanvasCanon is not module-only. It applies to any long-running project where decisions, rationale, and unresolved choices must stay coherent across forks and time.

This doc is canonical. If anything conflicts with Install, QuickRefCard, or MachineManual, this document wins.

## 1) Mission
- Preserve decisions through long timelines and forks.
- Keep project context skim-fast and executable.
- Reduce re-litigation by separating Open Questions from resolved law.
- Preserve rationale in a compact footnote layer instead of bloating core sections.

## 2) Architecture contract (ModuleMill)
### 2.1 Surface area
Inputs/triggers:
- Lifecycle controls (`canvascanon load|activate|sleep|unload|status`)
- Canon pass controls (`canvascanon canonize`, `canvascanon cleanup`, `canvascanon lastcall`)
- Open Questions controls (`canvascanon resolve`, `canvascanon prune`)
- Export control (`canvascanon export markdown`)
- Emoji aliases (`🛜`, `🧹`, `🍺`, `❌`) when unambiguous

Outputs:
- ACK/status confirmations
- Canon patch suggestions (or direct patch text when requested)
- Consolidated fork handoff notes
- Markdown export payload

### 2.2 State (authoritative)
CanvasCanon keeps an internal state block:
- `canvascanon.active` (bool)
- `canvascanon.canvas_name` (string)
- `canvascanon.canvas_bound` (bool)
- `canvascanon.last_canon_pass_at` (timestamp or null)
- `canvascanon.open_questions_index` (map letter -> question metadata)
- `canvascanon.resolved_index` (map letter -> chosen option)
- `canvascanon.footnote_counter` (int)

### 2.3 Lifecycle
- Available: no active state
- Loaded: state initialized
- Active: policy enforced and commands executed
- Sleeping: state preserved, enforcement suppressed

Lifecycle command canon:
- `canvascanon load`
- `canvascanon activate`
- `canvascanon sleep`
- `canvascanon unload`
- `canvascanon status`

Default when installed: Active.

### 2.4 ResponseEnvelope contract
- Default: `main_plus_patch`
- Status: `structured_status`
- Export: `markdown_payload`

### 2.5 Canon command table (ASCII-first)
| Command | Canon | Aliases | Inputs | Output shape | State effects |
|---|---|---|---|---|---|
| Load module | `canvascanon load` | `Enable CanvasCanon` | none | `ack_only` | initialize `canvascanon.*`, set `canvascanon.active=true` |
| Activate module | `canvascanon activate` | `Activate CanvasCanon` | none | `ack_only` | set `canvascanon.active=true` |
| Sleep module | `canvascanon sleep` | `Sleep CanvasCanon` | none | `ack_only` | set `canvascanon.active=false` |
| Unload module | `canvascanon unload` | `Disable CanvasCanon` | none | `ack_only` | clear `canvascanon.*` |
| Show status | `canvascanon status` | `CanvasCanon status` | none | `structured_status` | none |
| Canon pass | `canvascanon canonize` | `🛜 canon pass` | optional `scope:string` | `main_plus_patch` | update `canvascanon.last_canon_pass_at` |
| Cleanup pass | `canvascanon cleanup` | `🧹CleanUp` | optional `scope:string` | `main_plus_patch` | none |
| Fork prep pass | `canvascanon lastcall` | `🍺LastCall` | optional `scope:string` | `main_plus_patch` | update `canvascanon.last_canon_pass_at` |
| Resolve question | `canvascanon resolve <letter><option>` | `B2`, `C1` | `letter: A-Z`, `option:int>=1` | `main_plus_patch` | update `canvascanon.resolved_index` |
| Prune options | `canvascanon prune <refs>` | `❌B1,3,D3` | `refs:list` | `main_plus_patch` | none |
| Export canvas | `canvascanon export markdown` | `🛜export` | none | `markdown_payload` | none |

## 3) Core behavior laws
### 3.1 Chat vs canvas contract
- Chat is exploration.
- Canvas is compiled canon.
- Never rely on chat transcript as canonical state if canvas exists.

### 3.2 Canon inclusion rule
If content changes future decisions or behavior, include it in canvas.

### 3.3 Clean-body rule
Main body should contain current law, not narrative history.
Rejected options should not remain as active candidates.

### 3.4 Rationale rule
Rationale belongs in `Appendix A: Footnotes` using inline markers (`[1]`, `[2]`).

### 3.5 Fail-closed
If the target canvas or required sections are missing/ambiguous, stop speculative edits and ask for exact section or latest canvas content.

## 4) Canvas structure contract
Recommended section order:
1. Open Questions
2. Resolved Decisions
3. Fork handoff notes (when needed)
4. Appendix A: Footnotes
5. Archived scraps (optional)

Minimum viable headings for active projects:
- `## Open Questions`
- `## Resolved Decisions`
- `## Appendix A: Footnotes`

## 5) Open Questions (OQ) operating system
This section defines the OQ system as a hard-format UX contract. The goal is self-serve decision flow with fast scan, shorthand replies, and low-noise resolution.

### 5.0 What OQ solves
- Each open question is a real markdown header for skim speed.
- Each question carries plain-English context so users do not need follow-up clarification just to vote.
- Option lists are numbered for shorthand replies (`B4`, `C2`, `F3`).
- Assistant preference signals are visible at a glance (`🥇`, `🥈`, `🥉`, `👎🏼`).
- User pruning preserves history through strikeout plus trailing `❌`.
- Resolved questions keep letter slots but collapse to near-zero noise.

### 5.1 Placement and separation
- OQ section must precede Resolved Decisions.
- Open and resolved items are never mixed in the same active list.
- Canon section flow is `Open Questions -> Resolved Decisions`.
- Recommended heading pair is:
  - `## 3) Open questions (❓)`
  - `## 4) Resolved decisions`

### 5.2 Reply shorthand line (required)
At the top of the OQ section include:
- `*Reply shorthand:* \`B5\`, \`C2\`, \`F3\`, etc.`

The shorthand line is always present and appears once per OQ section.

### 5.3 Stable IDs
- Questions use stable letter headers: `### B) Title`.
- Option numbering uses markdown ordered lists (`1.`, `2.`, `3.`).
- Do not renumber options once shorthand votes/references exist.
- Do not express OQ questions as bullet points.

### 5.4 Explanation block rules
- Immediately under each question header, include a short paragraph explaining:
  - what decision is being made
  - why it matters
  - what changes depending on the choice
- Do not use a label such as `Layman:`.
- Keep wording plain and human-readable.

### 5.5 Option list rules
- Use markdown ordered lists with `1.` style markers.
- Do not use `1)` or lettered bullets for options.
- Keep numbering stable after shorthand references begin.

### 5.6 Visual signals
Preference tags:
- `🥇` strongest recommendation
- `🥈` second recommendation
- `🥉` third recommendation
- `👎🏼` least recommended / avoid

Rules:
- Apply ranking symbols consistently within a question.
- Rankings may change if new context arrives.
- Neutral options may omit ranking symbols.

### 5.7 Shorthand resolution
- Accept shorthand replies like `B2`, `F1`.
- On resolve, collapse question to:
  - `### ~~B) Title~~ ✅`
  - `Chosen: \`<value>\``
- Keep the letter slot in place (no missing letters).
- Remove explanation and option list once resolved.

### 5.8 Pruning rule
- Prune syntax: `❌B1,3,D3`.
- Render pruned options as strikeout with trailing `❌`; do not silently delete.
- If user places a lone `❌` at end of a line inside canvas content, strike/prune that target immediately.
- Keep existing preference emoji inside strikeout when already present.
- Place `❌` outside strikeout text.

### 5.9 Multi-answer shorthand
User can answer multiple items in one line:
- `C2, F3, G1`

Assistant applies all in one pass.

### 5.10 Leaning vs final
If user indicates a non-final lean:
- keep the question open
- annotate the chosen option with `(Stu lean; discuss)` or equivalent

### 5.11 Hygiene
- Keep letters stable.
- Keep numbering stable.
- Keep explanations current.
- Keep resolved items collapsed.
- Never reorder question letters.
- Pruning preserves history; deletion does not.

### 5.12 OQ formatting template
This is a formatting template. Replace domain content as needed, but preserve structure and mechanics.

## 3) Open questions (❓)

*Reply shorthand:* `B5`, `C2`, `F3`, etc.

### ~~A) Version mapping (R3.2 -> SemVer)~~ ✅
Chosen: `v0.3.2`

### B) LogVault location (where the archive actually lives)
After entries leave a chat, where do they physically live so future chats can load/search them without guesswork?

1. ~~ChatGPT Project files (vault folder inside the project) 🥉~~ ❌
2. Git repo folder (versioned vault) 🥈
3. ~~Local synced folder (Drive/Dropbox/etc.) 👎🏼~~ ❌
4. Hybrid (repo for index + cloud for bulk JSONL) 🥇
5. Other: ________ (Stu lean; discuss)

### C) Scope governance (tag drift control)
\"Scope\" tags help retrieval later. This decides whether tags are locked-down (clean but rigid) or flexible (fast but messy over time).

1. Controlled list (strict) 🥈
2. Recommended list + alias mapping (soft strict) 🥇
3. Freeform tags (status quo) 👎🏼

### D) Sentry wrappers (BEGIN/END bulk vs integrity)
Sentries reduce corruption risk but add body noise. This decides safety/readability tradeoff and whether compact mode exists.

1. Mandatory (status quo) 🥈
2. Optional compact mode + linter/validator 🥇
3. ~~Remove sentries (not recommended) 👎🏼~~ ❌

### E) Retrieval UX placement
For \"find me that item from last month,\" this decides whether retrieval stays outside the module or includes a minimal internal read-only path.

1. Retrieval outside module (separate retrieval module) 🥇
2. Minimal retrieval inside module (read-only find/slice) 🥈
3. Full retrieval inside module (likely bloat) 👎🏼

### F) Fork cursor design (state vs movable marker)
Fork cursor defines what is \"new\" after jumping across forks. This decides marker-only, state-only, or hybrid tracking.

1. Movable marker only (position = cursor) 🥈
2. Top-of-ledger state object only (cursor in state) 👎🏼
3. Hybrid marker + state cursor key 🥇

### G) Collision policy (trigger conflicts)
If two modules can respond to the same input, this decides deterministic precedence vs in-the-moment user arbitration.

1. Deterministic precedence list 🥈
2. Ask user in the moment (selection chips) 🥇
3. Namespace required in multi-module chats (`LK:` etc.) 👎🏼

## 6) Fork survival protocol
### 6.1 LastCall
On `canvascanon lastcall` / `🍺LastCall`:
1. Run canon pass on recent changes.
2. Validate OQ vs Resolved consistency.
3. Produce/update Fork handoff notes.

### 6.2 Fork handoff notes template
- Phase + timestamp
- In-flight thoughts (1-5 bullets)
- Next actions (3-7 bullets)
- Risks/gotchas
- File or source pointers

## 7) Naming and branding
- CanvasCanon branding emoji is `🛜`.
- Any canvas that follows CanvasCanon rules must start with `🛜`.
- Required canvas title format: `🛜<ProjectName> - <Purpose>`.
- Use PascalCase for `<ProjectName>` when applicable.
- Naming validator (strict): `^🛜[A-Z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)* - .+$`
- Example: `🛜LogKit - dev R6`.
- Preferred canonical module folder and references use PascalCase: `CanvasCanon`.
- Naming scheme remains configurable; if user provides an official naming variant, treat it as an explicit override.

## 8) EmojiGlossary
| Emoji | Term | Meaning |
|---|---|---|
| `🛜` | `CanvasCanonMark` | Alias for CanvasCanon namespace and canon-pass intent. |
| `🧹` | `CleanUpPass` | Alias for cleanup/refactor pass over canvas structure. |
| `🍺` | `LastCallPass` | Alias for pre-fork canon + handoff pass. |
| `❓` | `OpenQuestionTag` | Marks unresolved decisions in Open Questions. |
| `✅` | `ResolvedTag` | Marks collapsed resolved questions/decisions. |
| `❌` | `PruneTag` | Marks pruned options/items that should remain visibly struck. |
| `🥇` | `PreferredOptionGold` | Optional ranking hint for top recommendation. |
| `🥈` | `PreferredOptionSilver` | Optional ranking hint for second recommendation. |
| `🥉` | `PreferredOptionBronze` | Optional ranking hint for third recommendation. |
| `👎🏼` | `DeprioritizedOption` | Optional marker for weak option before prune. |

## 9) Arbitration and precedence
- Explicit module invocation wins.
- If output-shape conflict exists with another active module, ask user to choose one winner.
- If no conflict and CanvasCanon is active, keep using its response envelope for canon-edit tasks.

## 10) Regression checklist
1. `canvascanon status` reports lifecycle + key state.
2. `canvascanon canonize` yields concrete patch and updates last pass timestamp.
3. `canvascanon cleanup` removes duplication and preserves law.
4. `canvascanon resolve B2` collapses B and records chosen value.
5. `canvascanon prune B1,3` strikes targeted options with `❌`.
6. `canvascanon lastcall` produces fork handoff template output.
7. `canvascanon export markdown` returns clean markdown payload.
8. Canvas naming enforcement follows `🛜<ProjectName> - <Purpose>` with PascalCase project name when applicable.
9. OQ formatting rules enforce: shorthand line, header-based questions, ordered options, stable letters, strikeout pruning, and resolved collapse.
10. Missing canvas/sections triggers fail-closed clarification request.
