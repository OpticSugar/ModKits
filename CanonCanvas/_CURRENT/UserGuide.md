# CanonCanvas UserGuide (canonical)

ModuleID: CanonCanvas
Version: 0.3.4
DocRole: UserGuide
Audience: Humans + module engineers (canonical source of truth)

---

## 0) What this is
CanonCanvas is durable long-term project memory designed to survive a forking event with as little amnesia as possible.

It separates exploration from law:
- chat is where ideas are explored
- canvas is where durable decisions, unresolved choices, constraints, and continuity notes are preserved

Strategic purpose:
- reduce restart cost after handoffs, pauses, and forks
- prevent re-litigation of already-set decisions
- preserve momentum by making next actions and context legible to the next operator

Core law: if a decision affects future behavior, record it in canon canvas.

CanonCanvas is not module-only. It applies to any long-running project where decisions, rationale, and unresolved choices must stay coherent across forks and time.

Success condition: a new assistant (or future-you) can open the `🛜` canvas, grab the torch quickly, and continue with minimal context loss.

This doc is canonical. If anything conflicts with Install, QuickRefCard, or MachineManual, this document wins.

## 1) Mission
CanonCanvas exists to reduce project amnesia across long timelines, assistant handoffs, and forking events.

Strategic outcomes:
- Preserve durable decisions and constraints across forks, not just within one chat thread.
- Keep project context skim-fast and executable so the next operator can resume quickly.
- Reduce re-litigation by separating Open Questions from resolved law.
- Preserve rationale without bloating the body by using a compact footnote layer.
- Convert "context currently in my head" into durable handoff memory before context is lost.

### 1.1 Origin story and operating posture
CanonCanvas was built after repeated handoff/fork failures where critical reasoning lived only in transient chat text. By the time a new operator took over, the "why" behind key decisions was gone.

Operating posture:
- enforce deterministic structure for durable memory (`sections`, `question IDs`, `resolve/prune mechanics`)
- allow human/adaptive phrasing when writing explanation blocks and handoff notes
- preserve practical context and rationale even when cleanup pressure favors short rewrites

If a refactor makes canon cleaner but less informative for the next operator, that refactor failed.

## 2) Architecture contract (ModuleMill)
### 2.1 Surface area
Inputs/triggers:
- Lifecycle controls (`canoncanvas load|activate|sleep|unload|status`)
- Canon pass controls (`canoncanvas canonize`, `canoncanvas cleanup`, `canoncanvas lastcall`)
- Open Questions controls (`canoncanvas resolve`, `canoncanvas prune`)
- Export control (`canoncanvas export markdown`)
- Emoji aliases (`🛜`, `🧹`, `🍺`, `❌`) when unambiguous
- Client-context signals (for example explicit "this is a client project" or pasted client brief text)

Outputs:
- ACK/status confirmations
- Canon patch suggestions (or direct patch text when requested)
- Consolidated fork handoff notes
- Markdown export payload

### 2.2 State (authoritative)
CanonCanvas keeps an internal state block:
- `canoncanvas.active` (bool)
- `canoncanvas.canvas_name` (string)
- `canoncanvas.canvas_bound` (bool)
- `canoncanvas.last_canon_pass_at` (timestamp or null)
- `canoncanvas.last_savepoint_at` (timestamp or null)
- `canoncanvas.last_fork_rehydrate_at` (timestamp or null)
- `canoncanvas.client_mode` (bool)
- `canoncanvas.open_questions_index` (map letter -> question metadata)
- `canoncanvas.resolved_index` (map letter -> chosen option)
- `canoncanvas.footnote_counter` (int)

### 2.3 Lifecycle
- Available: no active state
- Loaded: state initialized
- Active: policy enforced and commands executed
- Sleeping: state preserved, enforcement suppressed

Lifecycle command canon:
- `canoncanvas load`
- `canoncanvas activate`
- `canoncanvas sleep`
- `canoncanvas unload`
- `canoncanvas status`

Default when installed: Active.

### 2.4 ResponseEnvelope contract
- Default: `main_plus_patch`
- Status: `structured_status`
- Export: `markdown_payload`

### 2.5 Canon command table (ASCII-first)
| Command | Canon | Aliases | Inputs | Output shape | State effects |
|---|---|---|---|---|---|
| Load module | `canoncanvas load` | `Enable CanonCanvas` | none | `ack_only` | initialize `canoncanvas.*`, set `canoncanvas.active=true` |
| Activate module | `canoncanvas activate` | `Activate CanonCanvas` | none | `ack_only` | set `canoncanvas.active=true` |
| Sleep module | `canoncanvas sleep` | `Sleep CanonCanvas` | none | `ack_only` | set `canoncanvas.active=false` |
| Unload module | `canoncanvas unload` | `Disable CanonCanvas` | none | `ack_only` | clear `canoncanvas.*` |
| Show status | `canoncanvas status` | `CanonCanvas status` | none | `structured_status` | none |
| Canon pass | `canoncanvas canonize` | `🛜 canon pass` | optional `scope:string` | `main_plus_patch` | update `canoncanvas.last_canon_pass_at` |
| Cleanup pass | `canoncanvas cleanup` | `🧹CleanUp` | optional `scope:string` | `main_plus_patch` | none |
| Fork prep pass | `canoncanvas lastcall` | `🍺LastCall` | optional `scope:string` | `main_plus_patch` | update `canoncanvas.last_canon_pass_at` |
| Resolve question | `canoncanvas resolve <letter><option>` | `B2`, `C1` | `letter: A-Z`, `option:int>=1` | `main_plus_patch` | update `canoncanvas.resolved_index` |
| Prune options | `canoncanvas prune <refs>` | `❌B1,3,D3` | `refs:list` | `main_plus_patch` | none |
| Export canvas | `canoncanvas export markdown` | `🛜export` | none | `markdown_payload` | none |

Command semantics guardrail:
- `canoncanvas lastcall` / `🍺LastCall` is a routine/ritual command, not a module and not a canvas header title.
- Never render `🍺LastCall` or variants such as `🍺 Last Call snapshot` as section headers.

### 2.6 Natural-language intent inference
- CanonCanvas supports explicit commands and natural-language invocation when intent is clear.
- If natural-language phrasing maps with high confidence to one canon command, execute it directly.
- If confidence is low or multiple commands fit, ask one-line clarification before acting.
- Confidence decisions should use recent chat context and current `canoncanvas.*` state.
- Inferred intent never bypasses fail-closed rules for missing/ambiguous canvas artifacts.

## 3) Core behavior laws
### 3.1 Chat vs canvas contract
- Chat is exploration.
- Canvas is compiled canon.
- Never rely on chat transcript as canonical state if canvas exists.

### 3.2 Canon inclusion rule
If content changes future decisions or behavior, include it in canvas.

High-priority examples:
- decisions, constraints, assumptions, and definitions
- unresolved options and explicit tradeoffs
- dependencies, risks, and caveats that can break future execution
- momentum-critical next actions and handoff pointers

Canvas-first memory discipline:
- When CanonCanvas is active, treat the canvas as the only long-term project memory.
- Durable items should be captured promptly into canvas, not left only in chat.
- Chat remains a debate/workbench layer; canvas is the durable memory layer.

Practical decision gate (Canvas vs transient chat):
- Put it in canvas if at least one is true:
  - likely needed beyond a few chat turns
  - affects roadmap, implementation, constraints, or acceptance criteria
  - captures rationale that would be expensive to rediscover
  - represents a non-trivial progression of project state
- Keep in transient chat if all are true:
  - exploratory or speculative with no decision yet
  - low-cost to recreate
  - not needed for future operator continuity

### 3.3 Clean-body rule
Main body should contain current law, not narrative history.
Rejected options should not remain as active candidates.

Keep historical signal without clutter:
- use strikeout + `❌` for pruned options where history matters
- collapse resolved items instead of leaving full deliberation blocks in active flow

### 3.4 Rationale rule
Rationale belongs in `Appendix A: Footnotes` using inline markers (`[1]`, `[2]`).

Purpose:
- keep main sections fast to scan
- keep reasoning recoverable when decisions are revisited later
- reduce accidental loss of "why we chose this" during forks

Required footnote capture:
- When a material decision/rule is added, changed, or resolved, attach or update at least one footnote marker.
- Each such footnote should capture:
  - relevant context
  - decision reasoning/tradeoff logic
  - final rationale for the chosen direction
- Do not strip existing rationale footnotes during cleanup unless the decision itself is removed or superseded and the change is explicitly reflected.

### 3.5 Fail-closed
If the target canvas or required sections are missing/ambiguous, stop speculative edits and ask for exact section or latest canvas content.

Fail-closed is mandatory because fabricated memory is worse than missing memory:
- if unsure, ask
- if artifacts are missing, pause canon edits
- resume only with authoritative input

### 3.6 Guardrailed improvisation contract
CanonCanvas is not a rigid text template engine. Assistants should improvise phrasing where safe, but never improvise structure-critical mechanics.

Safe improv zones:
- explanation paragraph wording under each OQ header
- handoff note voice/tone (while keeping required payload fields)
- compact recap phrasing in chat responses

Locked zones:
- question letter stability
- option numbering stability
- resolve/prune semantics
- preservation of ranking and strikeout signals when present

### 3.7 Continuous grooming law
- Keep canvas continuously groomed during normal operation; do not defer most updates to LastCall.
- Prune obsolete or irrelevant material from main sections as decisions mature.
- If historical context is still useful, move pruned remnants into appendix-style sections instead of leaving core flow noisy.

### 3.8 Client-context gating and source fidelity
- Do not assume a client exists.
- Client workflow is conditional and activates only when user explicitly states client context or provides client-source text.
- Without explicit client context, do not create or route content into client-specific headers (for example `Client comments` or `⚖️ Client Requests`).
- In client mode:
  - Use `## ⚖️ Client Requests` only when concrete client requirements exist.
  - Treat `⚖️` items as mandatory/inflexible unless user explicitly marks an item negotiable.
  - If client wording is short and available, capture it verbatim.
  - If decomposition is needed, keep original client wording and add derived targets beneath it; do not replace originals with paraphrase-only summaries.
  - Use `## 💡 Our Ideas` for additive ideas that support and build on client requirements rather than contradicting them.
- In non-client projects, use neutral section names (for example Requirements, Constraints, Goals, Notes) and avoid client labels entirely.

### 3.9 LastCall ritual semantics
- LastCall is an execution ritual, not a namespace or document title.
- Output from a LastCall pass must reconcile into canonical sections rather than accumulating as standalone snapshots.
- If a temporary handoff block is created, it must use the standardized header `## 👴🏼 Fork Handoff Notes`.
- Handoff notes are transient: once items are propagated upward into canonical sections (or deemed irrelevant), remove consumed items and clear the section when empty.

## 4) Canvas structure contract
CanonCanvas is a strategic framework, not a fixed prefilled template.

Header materialization rules:
- Headers appear only when needed.
- Do not pre-populate empty sections.
- If a section becomes empty after cleanup/pruning, remove it.
- Header sets in this guide are examples and style guides, not mandatory forms.
- Assistants may improvise new headers using the same style/naming language when project context requires it.

Logical ordering model (intro -> working core -> end matter):
1. Intro/context sections used for current project orientation
2. Active working sections (for example Open Questions, Decisions, Constraints, Plan, Risks)
3. End-matter sections used only when needed:
  - Archived scraps near the end, only when archive content exists
  - Appendix A: Footnotes near the end, and only when footnotes exist
  - `## 👴🏼 Fork Handoff Notes` as the final section, and only when performing fork/handoff work

Anti-noise rule:
- Do not dump a full empty outline on first invoke.
- Build structure incrementally from actual content.
- Do not place handoff snapshots at the top of canvas.

Client-mode section pattern (conditional):
- For explicitly client-driven work, a common core sequence is:
  1. `## ⚖️ Client Requests`
  2. `## 💡 Our Ideas`
  3. Other active working sections (Decisions, OQ, Plan, Risks, etc.)
- Do not create these client sections when no client context is declared.
- Never pre-create empty `⚖️`/`💡` sections.

### 4.1 Standard Header Library (WIP)
Purpose:
- Provide a stable menu of recurring headers so canvases stay consistent.
- Preserve flexibility: assistants may improvise new headers when needed, then propose additions back into this library if they prove useful.

Header standards:
| Header | Purpose | When to use | Placement |
|---|---|---|---|
| `## 🧭 Project Overview` | What the project is and what problem it solves. | Most projects. | Intro. |
| `## 🎯 Goals and Success Criteria` | Defines target outcomes and acceptance bar. | When success needs explicit criteria. | Early core. |
| `## 🧱 Constraints and Guardrails` | Captures fixed limits and non-negotiables. | When constraints exist. | Early core. |
| `## 🗺️ Plan and Milestones` | Execution sequence and near-term roadmap. | When planning work. | Core. |
| `## ❓ Open questions` | Active unresolved decisions. | When unresolved choices exist. | Core, before resolved. |
| `## ↔️ Resolved decisions` | Collapsed record of chosen options. | When items are resolved. | Core, after open questions. |
| `## ⚠️ Risks and Gotchas` | Known risks and mitigations. | When risk signal exists. | Core. |
| `## 📎 Sources and Pointers` | Files/URLs/evidence needed to resume quickly. | When references matter for continuity. | Core or end-matter. |
| `## ⚖️ Client Requests` | Mandatory client asks captured from source text. | Client mode only, when requests exist. | Early core. |
| `## 💡 Our Ideas` | Additive ideas that build on client requests. | Client mode only, when additive strategy exists. | Core after `⚖️`. |
| `## 🧾 Archived scraps` | Preserved rejected or superseded material for context. | Only when archive content exists. | End-matter. |
| `## Appendix A: Footnotes` | Compact rationale trail with inline markers. | When rationale notes exist. | End-matter, above handoff notes. |
| `## 👴🏼 Fork Handoff Notes` | Temporary baton-pass payload for forks/handoffs. | Only during fork/handoff work. | Always final section. |

Header library operating rules:
- Use this library first for common patterns.
- If no listed header fits, improvise one that matches CanonCanvas style and intent.
- If an improvised header proves repeatedly useful, promote it into this library in a future revision.
- Do not pre-populate unused headers.

## 5) Open Questions (OQ) operating system
This section defines Open Questions (OQ) as a hard-format UX contract. The intent is fast scan, low-friction voting, and clean resolution without follow-up clarification.

### 5.0 What OQ solves
- Questions are real markdown headers for skim speed.
- Each question includes plain-English context so the header can stay brief.
- Numbered options enable shorthand replies like `B4`, `C2`, `F3`.
- Assistant preference signals are visible at a glance (`🥇`, `🥈`, `🥉`, `👎🏼`).
- On resolve, the chosen answer keeps its vote emoji so recommendation context stays visible.
- User pruning preserves history via strikeout plus trailing `❌`.
- Resolved questions keep letter slots but collapse to near-zero noise.

### 5.1 Placement and separation
- Create OQ sections only when unresolved questions actually exist.
- OQ must appear before Resolved Decisions.
- Open and resolved items are never mixed in the same active list.
- Canon section flow is `Open Questions -> Resolved Decisions`.
- Recommended heading pair:
  - `## ❓ Open questions`
  - `## ↔️ Resolved decisions`

### 5.2 Shorthand help (chat-only, conditional)
Shorthand replies are supported, but do not embed a how-to-reply cluster inside canvas content (no `*Reply shorthand:* ...` and no `*Example answer line:* ...`).

If the user appears confused about response format, provide a tiny cheat sheet in chat only (not copied into canvas).

Suggested chat-only cheat sheet (when needed):
- `A2` = pick option 2 for question A
- `A1,3` = keep-list (single-select) or multi-select (if the question says choose-many)
- `Ax2` or `❌A2` = strike option 2
- `C` resolved items: respond only if reopening is explicitly requested

### 5.3 Stable IDs
- Questions use stable letter headers: `### B) Title`.
- Option numbering uses markdown ordered lists (`1.`, `2.`, `3.`).
- Do not renumber options after shorthand votes/references exist.
- Do not express questions as bullet points.

### 5.4 Explanation block rules
Immediately under each question header, include a short paragraph explaining:
- what decision is being made
- why it matters
- what changes depending on the choice

Rules:
- Do not use labels like `Layman:`.
- Keep wording plain and human-readable.

### 5.5 Option list rules
- Use markdown ordered lists with `1.` style markers.
- Do not use `1)` or lettered bullets for options.
- Keep numbering stable after shorthand references begin.
- If assistant rankings are present, put them at the end of each option line.

### 5.6 Assistant picks
Assistant preference tags:
- `🥇` strongest recommendation
- `🥈` second recommendation
- `🥉` third recommendation
- `👎🏼` least recommended / avoid

Rules:
- Apply ranking symbols consistently within a question.
- Rankings may change if new context arrives.
- Neutral options may omit ranking symbols.
- Rankings go at the end of an option line.
- Rankings should survive an answered question and remain with the chosen answer.

### 5.7 User answer lines (shorthand replies)
Users may answer with compact tokens instead of full sentences.

Accepted formats:
- Single answer token: `B2`
- Multi-question answer line: `C2, F3, G1` (commas optional)
- Space-grouped answer line: `B2 C3 D1` (spaces optional)

Optional answer-mode marker (for ambiguity):
- `❓` (single leading emoji)
- `[?]`
- `[OQ]`
- `[Answers]`

These markers are equivalent and interchangeable. If surrounding context is clearly about Open Questions, the marker is optional.

Multi-select within one question has two modes:
- Mode 1, choose-many question: if the question explicitly says choose-many/select all that apply, `B1,3,5` selects those options and does not prune others.
- Mode 2, single-select question (default): if not labeled choose-many, `B1,3,5` is keep-list shorthand. It means those are the only viable options, so all other options in B are struck while B stays open unless the user also gives one final choice.

Practical upshot: `B1,3,5` either selects-many (for choose-many questions) or becomes keep-list with implied pruning (default single-select).

### 5.8 Pruning shorthand
Pruning removes options from contention without deleting history.

Supported prune syntaxes:
- Prune syntax: `❌B1,3,D3`.
- Inline prune marker: `Bx4` or `Bx2,5` (the `x` means strike).

Rules:
- `x` is case-insensitive (`Bx4` = `BX4`).
- Inline prune marker applies the same strike behavior as canonical prune syntax.
- Render pruned options as strikeout with trailing `❌`; do not silently delete.
- If user places a lone `❌` at end of a line inside canvas content, strike/prune that target immediately.
- Keep existing preference emoji inside strikeout when already present.
- Place `❌` outside strikeout text.

Keep-list implied pruning:
- In a single-select question, `B1,3,5` means keep these and strike every other option in B.
- Apply the same visual strikeout treatment used for explicit pruning.
- If the question is explicitly choose-many, do not apply keep-list pruning.

Example answer line using answer + prune + keep-list (documentation only):
- `❓A1  B1,3,5  Cx4  Dx2,5`

### 5.9 Resolve (collapse) rules
On resolve, collapse the question to:
- `### ~~B) Title~~ ✅`
- `Chosen: \`<value>\``

Rules:
- Keep the letter slot in place (no missing letters).
- Remove explanation and option list once resolved.
- `Chosen:` value is inline code.
- Chosen value must include the assistant vote emoji (`🥇/🥈/🥉/👎🏼`).
- Do not strip, relocate, or clean up vote emoji on resolve.
- Best practice: copy selected option text verbatim, including vote emoji, into `Chosen:`.

### 5.10 Leaning vs. final
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
This is an optional example block. Do not auto-insert it unless the project currently needs these sections populated.

## ❓ Open questions

### A) First question
This description provides enough context so the short header stays readable and self-explanatory.

1. ~~First multiple choice option 🥉~~ ❌
2. Second multiple choice option 🥇
3. Third multiple choice option 👎🏼

### B) OQ mechanics placeholder topic
This description demonstrates why lettered headers, numbered options, and line-end ranking emojis reduce decision friction.

1. Shorthand IDs reduce typing (`B1`) 🥇
2. Line-end ranking emojis keep recommendations scannable 🥈
3. ~~Unstructured prose-only options (avoid) 👎🏼~~ ❌

### ~~C) Resolved example question~~ ✅
Chosen: `Second multiple choice option 🥇`

## 6) Fork survival protocol
### 6.1 Durability truth (operational invariant)
- Canvases are durable across chat forks and exist independently of any specific thread timeline.
- This persistence behavior is treated as a tested operational invariant for CanonCanvas workflows.
- CanonCanvas should rely on this durability for long-term memory and fork-based iteration.
- If documentation elsewhere is ambiguous, preserve this operational behavior for CanonCanvas runtime decisions.

### 6.2 What LastCall is
`canoncanvas lastcall` / `🍺LastCall` is a pre-handoff continuity pass. It should leave the canvas in a state where the next assistant can resume with minimal guesswork and minimal momentum loss.
It is a ritual command, not a module and not a section title.

### 6.3 LastCall execution order (required)
On `canoncanvas lastcall` / `🍺LastCall`:
1. Canon sync pass.
2. OQ integrity sweep.
3. Continuity capture and handoff write.
4. Final confirmation check.

LastCall role constraint:
- LastCall is a safety net for loose ends, not the primary mechanism for routine canvas updates.

### 6.4 Canon sync pass (what "recent changes" means)
"Run canon pass on recent changes" means compiling all material decisions and constraints from the current context into canon canvas, not just applying a cosmetic cleanup.

Include, at minimum:
- decisions or rules settled since the last canon pass
- OQ activity in chat not yet reflected in canvas (`B2`, `❌B1,3`, keep-list outcomes, resolve actions)
- constraints, assumptions, dependencies, risks, and definitions now affecting future choices
- important file/source pointers surfaced in chat but not yet captured in canvas
- rationale/context that would be lost without Appendix A footnotes

If required canvas sections are missing or ambiguous, fail closed and request authoritative canvas content before finalizing LastCall.

### 6.5 OQ integrity sweep
During LastCall, verify OQ mechanics are still coherent:
- Open Questions and Resolved Decisions remain separate.
- Letter IDs and option numbering remain stable.
- Any resolve collapse preserves chosen-value ranking emoji.
- Any prune action is rendered as strikeout plus trailing `❌`.

### 6.6 Continuity capture (the handoff payload)
LastCall must explicitly capture:
- anything important in current context that is not yet in `🛜`
- anything that would help the next operator "grab the torch" and keep momentum

### 6.7 Fork handoff notes template
Standard header (required):
- `## 👴🏼 Fork Handoff Notes`

Placement and lifecycle:
- This header must be the final section in the canvas when present.
- It must not appear at the top or middle of the canvas.
- Contents are temporary. As notes are integrated into canonical sections above (or become irrelevant), remove them from `👴🏼`.
- Do not allow `👴🏼` notes to accumulate unbounded across repeated `⚡` cycles.

Payload:
- Phase + timestamp
- What changed in this pass (3-7 bullets)
- Context-only carry-forward items not yet canonized (critical)
- Next actions (3-7 bullets, ordered)
- Risks/gotchas (+ mitigation when known)
- File/source pointers
- Optional: "If I had to resume in 2 minutes, start with: ___"

### 6.8 Optional tail note (fun but useful)
At the very end of the `🛜` canvas during `🍺LastCall`, assistant should leave one short "note to younger self" line by default (unless user explicitly asks for strict-formal tone only).

Official header (required when note is present):
- `### 🚸 assistant's 👴🏼 note to → 📝 → younger 👶🏻 self`

Style guidance:
- Keep it short (typically one line).
- Encourage playful creativity: inside jokes, light snark, sarcasm, humor, or a witty reminder.
- A friendly roast of the user is allowed when it fits chat tone and consent context.
- Keep it non-destructive: do not replace required handoff facts with the joke line.
- Place this note block after `## 👴🏼 Fork Handoff Notes` content so it is the final tail block in the canvas for that pass.
- Do not improvise alternative header text for this block.

### 6.9 Fork signal semantics (`💾` and `⚡`)
Signal markers used in chat:
- `💾` (`SavePointMarker`): marks a clean save-point suitable for fork-back after a later parallel work pass.
- `⚡` (`ForkedMarker`): means "you were forked back to an earlier point after parallel progress was recorded into canvas."

Runtime behavior:
- On `💾`: treat current state as a potential return anchor; keep canvas current before major execution phases.
- On `⚡`: immediately read/reload canonical canvas content, hydrate current context from it, consume stale `👴🏼` carry-forward items into canonical sections, and continue from latest canon rather than stale chat-local memory.

## 7) Naming and branding
- CanonCanvas branding emoji is `🛜`.
- Any canvas that follows CanonCanvas rules must start with `🛜 ` (emoji + space).
- Required canvas title format: `🛜 <ProjectName> - <CanvasPurpose>`.
- Use PascalCase for `<ProjectName>` when applicable.
- Canvas title must never include module names (`CanvasCanon`, `CanonCanvas`).
- Naming validator (strict): `^🛜 [A-Z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)* - .+$`
- Example: `🛜 LogKit - dev R6`.
- Preferred canonical module folder and references use PascalCase: `CanonCanvas`.
- Naming scheme remains configurable; if user provides an official naming variant, treat it as an explicit override.

## 8) EmojiGlossary
| Emoji | Term | Meaning |
|---|---|---|
| `🛜` | `CanonCanvasMark` | Alias for CanonCanvas namespace and canon-pass intent. |
| `🧹` | `CleanUpPass` | Alias for cleanup/refactor pass over canvas structure. |
| `🍺` | `LastCallPass` | Alias for pre-fork canon + handoff pass. |
| `❓` | `OpenQuestionTag` | Marks unresolved decisions in Open Questions. |
| `✅` | `ResolvedTag` | Marks collapsed resolved questions/decisions. |
| `❌` | `PruneTag` | Marks pruned options/items that should remain visibly struck. |
| `🥇` | `PreferredOptionGold` | Optional ranking hint for top recommendation. |
| `🥈` | `PreferredOptionSilver` | Optional ranking hint for second recommendation. |
| `🥉` | `PreferredOptionBronze` | Optional ranking hint for third recommendation. |
| `👎🏼` | `DeprioritizedOption` | Optional marker for weak option before prune. |
| `⚖️` | `ClientRequestsTag` | Marks mandatory client requirements in explicitly client-driven projects. |
| `💡` | `OurIdeasTag` | Marks additive internal ideas that build on client requirements. |
| `💾` | `SavePointMarker` | Chat save-point marker for planned fork-back anchors. |
| `⚡` | `ForkedMarker` | Chat marker meaning fork-back occurred and canvas must be re-read. |
| `👴🏼` | `ForkHandoffNotesHeader` | Standard transient handoff header placed as final section only. |
| `🚸` | `YoungerSelfNoteHeaderTag` | Marks the official younger-self note header block during LastCall. |
| `👶🏻` | `YoungerSelfRecipientTag` | Marks younger-assistant recipient context in the note header. |
| `📝` | `YoungerSelfNoteToken` | Marks note payload concept in the official younger-self header. |

## 9) Arbitration and precedence
- Explicit module invocation wins.
- If output-shape conflict exists with another active module, ask user to choose one winner.
- If no conflict and CanonCanvas is active, keep using its response envelope for canon-edit tasks.

### 9.1 Documentation access fail-closed policy
If required CanonCanvas docs are unavailable, do not claim CanonCanvas is loaded, active, or being followed.

Required recovery flow:
1. Ask user to enable Web Search and retry doc fetch.
2. If fetch still fails, provide this URL pack and ask user to copy/paste returned content:
```text
https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/ModuleManifest.yaml
https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/Install.md
https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/QuickRefCard.md
https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/MachineManual.md
https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/UserGuide.md
```
3. Until docs are available, respond as a normal assistant and explicitly state that CanonCanvas module behavior is not active for that turn.

## 10) Regression checklist
1. `canoncanvas status` reports lifecycle + key state.
2. `canoncanvas canonize` yields concrete patch and updates last pass timestamp.
3. `canoncanvas cleanup` removes duplication and preserves law.
4. `canoncanvas resolve B2` collapses B and records chosen value.
5. `canoncanvas prune B1,3` strikes targeted options with `❌`.
6. `canoncanvas lastcall` captures context-not-in-`🛜`, preserves OQ integrity, and produces momentum-ready handoff notes.
7. `canoncanvas export markdown` returns clean markdown payload.
8. Canvas naming enforcement follows `🛜 <ProjectName> - <CanvasPurpose>` with PascalCase project name when applicable, and never includes module names.
9. OQ formatting rules enforce: no canvas-embedded shorthand helper line, header-based questions, ordered options, stable letters, keep-list semantics, strikeout pruning, and resolved collapse with vote-emoji preservation.
10. Material decisions retain footnote markers with rationale/context in `Appendix A: Footnotes`.
11. Missing canvas/sections triggers fail-closed clarification request.
12. CanonCanvas does not pre-populate empty templates; sections appear only when needed.
13. LastCall is used as safety net, while routine turns keep canvas continuously groomed.
14. On `⚡`, assistant re-reads canvas before resuming project work.
15. Without explicit client context, CanonCanvas does not auto-create client-specific headers.
16. In client mode, short client-source text is preserved verbatim under `⚖️` and additive design work is tracked under `💡`.
17. LastCall is treated as a ritual command and never rendered as a canvas header title.
18. `## 👴🏼 Fork Handoff Notes` is used (when needed) as the final section and is continuously consumed/pruned rather than allowed to accumulate.
19. `🍺LastCall` should end with a short, creative "note to younger self" tail line by default.
20. Younger-self tail notes use the exact official header `### 🚸 assistant's 👴🏼 note to → 📝 → younger 👶🏻 self` when present.
