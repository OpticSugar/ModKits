# CanonCanvas UserGuide (canonical)

ModuleID: CanonCanvas
Version: 0.2.0
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
This is a formatting template. Replace domain content as needed, but preserve structure and mechanics.

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
### 6.1 What LastCall is
`canoncanvas lastcall` / `🍺LastCall` is a pre-handoff continuity pass. It should leave the canvas in a state where the next assistant can resume with minimal guesswork and minimal momentum loss.

### 6.2 LastCall execution order (required)
On `canoncanvas lastcall` / `🍺LastCall`:
1. Canon sync pass.
2. OQ integrity sweep.
3. Continuity capture and handoff write.
4. Final confirmation snapshot.

### 6.3 Canon sync pass (what "recent changes" means)
"Run canon pass on recent changes" means compiling all material decisions and constraints from the current context into canon canvas, not just applying a cosmetic cleanup.

Include, at minimum:
- decisions or rules settled since the last canon pass
- OQ activity in chat not yet reflected in canvas (`B2`, `❌B1,3`, keep-list outcomes, resolve actions)
- constraints, assumptions, dependencies, risks, and definitions now affecting future choices
- important file/source pointers surfaced in chat but not yet captured in canvas
- rationale/context that would be lost without Appendix A footnotes

If required canvas sections are missing or ambiguous, fail closed and request authoritative canvas content before finalizing LastCall.

### 6.4 OQ integrity sweep
During LastCall, verify OQ mechanics are still coherent:
- Open Questions and Resolved Decisions remain separate.
- Letter IDs and option numbering remain stable.
- Any resolve collapse preserves chosen-value ranking emoji.
- Any prune action is rendered as strikeout plus trailing `❌`.

### 6.5 Continuity capture (the handoff payload)
LastCall must explicitly capture:
- anything important in current context that is not yet in `🛜`
- anything that would help the next operator "grab the torch" and keep momentum

### 6.6 Fork handoff notes template
- Phase + timestamp
- What changed in this pass (3-7 bullets)
- Context-only carry-forward items not yet canonized (critical)
- Next actions (3-7 bullets, ordered)
- Risks/gotchas (+ mitigation when known)
- File/source pointers
- Optional: "If I had to resume in 2 minutes, start with: ___"

### 6.7 Optional tail note (fun but useful)
At the bottom of the `🛜` canvas (or the handoff block), assistant may add one short "note to younger self" line. This can be reflective, funny, or human, but must stay brief and never replace required handoff facts.

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
