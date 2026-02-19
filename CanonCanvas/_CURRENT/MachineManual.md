# CanonCanvas MachineManual (derived)

ModuleID: CanonCanvas
Version: 0.3.6
DocRole: MachineManual
Audience: Assistants operating CanonCanvas at runtime

---

## Runtime contract
- Treat `UserGuide` as canonical.
- Enforce fail-closed behavior when canvas artifacts are missing.
- CanonCanvas target must be a markdown canvas.
- Bind/open existing matching `🛜` canvas before creating new canvases.
- Treat user-opened canvas as primary selection signal; never invent hidden UI controls.
- Do not invent commands, state keys, or output shapes.
- Do not pre-populate empty template sections.
- Materialize headers only when content exists for that section.
- Treat canvas as long-term project memory while module is active.
- Do not assume client context unless user explicitly provides it.
- Treat LastCall as a ritual command, never as a module title or section header.

## ResponseEnvelope
- Default: `main_plus_patch`
- Status: `structured_status`
- Export: `markdown_payload`

## 1) Minimal state
Maintain:
- `canoncanvas.active`
- `canoncanvas.canvas_name`
- `canoncanvas.canvas_bound`
- `canoncanvas.last_canon_pass_at`
- `canoncanvas.last_savepoint_at`
- `canoncanvas.last_fork_rehydrate_at`
- `canoncanvas.client_mode`
- `canoncanvas.open_questions_index`
- `canoncanvas.resolved_index`
- `canoncanvas.footnote_counter`

## 2) Lifecycle controls
- `canoncanvas load`: initialize state and activate
- `canoncanvas activate`: set active true
- `canoncanvas sleep`: set active false, preserve state
- `canoncanvas unload`: clear state
- `canoncanvas status`: emit structured status

### 2.1 Canvas binding routine
Before canon operations:
1. Discover canvases whose names start with `🛜 `.
2. If `canoncanvas.canvas_name` already points to an existing canvas, open/bind that canvas.
3. Otherwise, if one matching canvas exists for the current project/purpose, bind it and do not create a new one.
4. Create a new `🛜` canvas only when no suitable match exists or user explicitly requests a new canvas.
5. Verify bound canvas type is markdown and title matches naming validator.
6. If active-canvas telemetry is unavailable, ask for exact-title bind confirmation (`use 🛜 <ProjectName> - <CanvasPurpose>`) and bind that title.
7. Never create a new canvas to bypass missing active-canvas telemetry.
8. If multiple matches are ambiguous, fail closed and ask user to choose one winner.

## 3) Command interpretation
### 3.1 Canon/care commands
- `canoncanvas canonize`: produce canon patch from recent decisions.
- `canoncanvas cleanup`: remove duplication/noise while preserving rules.
- `canoncanvas lastcall`: pre-handoff continuity pass (canon sync + OQ integrity + momentum handoff capture).
- `canoncanvas lastcall` / `🍺LastCall` is a ritual. Never emit headings like `🍺 Last Call snapshot`.
- LastCall is safety-net behavior for loose ends; routine turns should keep canvas continuously groomed.
- `🧹CleanUp` is an alias for `canoncanvas cleanup`.
- For `canonize|cleanup|lastcall`, preserve rationale traceability:
  - maintain `Appendix A: Footnotes` when present or fail closed if missing where rationale markers are required
  - keep inline markers (`[1]`, `[2]`, ...) attached to material decisions/rules
  - when a material decision changes, create/update a footnote that records context, reasoning, and final rationale
  - do not drop rationale footnotes unless the linked decision is explicitly removed/superseded

### 3.2 Open Questions operations
- `canoncanvas resolve <letter><option>` accepts `B2` shorthand.
- Multi-question answer lines are valid: `C2, F3, G1` or `B2 C3 D1`.
- Optional answer-mode marker is accepted when present: leading `❓`, `[?]`, `[OQ]`, or `[Answers]`.
- `canoncanvas prune <refs>` accepts `B1,3,D3`; emoji alias `❌B1,3,D3` is equivalent.
- Inline prune syntax is valid: `Bx4`, `Bx2,5` (`x` is case-insensitive).
- Lone trailing `❌` on a canvas line is prune intent for that line item.
- Keep-list semantics: in single-select questions, `B1,3,5` means keep listed options and strike all others in B.
- Choose-many override: if the question explicitly says choose-many/choose any/select all that apply, `B1,3,5` selects those options and does not prune the rest.
- Keep-list interpretation does not finalize the question by itself; keep the question open unless user supplies a final single choice.
- Do not inject shorthand helper lines into canvas content; if user appears confused, provide a tiny cheat sheet in chat only.
- OQ questions are markdown headers (`### B) ...`), not bullets.

### 3.3 Export
- `canoncanvas export markdown` returns the current canonical canvas as markdown payload.

### 3.4 Client-mode gating and capture rules
- Default to non-client mode (`canoncanvas.client_mode=false`) unless user explicitly indicates client context.
- Treat explicit client context as any of:
  - user states the project has a client
  - user pastes a client brief/request text
  - user asks for client-request tracking behavior
- In non-client mode:
  - do not create `Client comments` or `⚖️ Client Requests` sections
  - route requirements into neutral sections (for example Requirements, Constraints, Goals)
- In client mode:
  - maintain `## ⚖️ Client Requests` only when client requests exist
  - capture short client requests verbatim when source wording is available
  - if decomposition is needed, keep the original client wording and add derived targets beneath it
  - treat `⚖️` items as mandatory/inflexible unless user marks specific items negotiable
  - maintain `## 💡 Our Ideas` for additive ideas that support client requests
  - never pre-create empty `⚖️`/`💡` sections

### 3.5 Header library and placement contract
- Prefer standardized headers defined in canonical UserGuide section `4.1 Standard Header Library (WIP)`.
- If no standard header fits, improvise a style-consistent header and keep placement logical.
- `## 👴🏼 Fork Handoff Notes` is the only standard handoff header and must be final section when present.
- Do not place fork handoff notes at top or middle of canvas.

## 4) Open Questions enforcement
- Use OQ terminology (`Open Questions` / `OQ`) consistently in all outputs.
- Create OQ sections only when unresolved questions exist.
- OQ section appears before Resolved Decisions; unresolved and resolved items are not mixed in one active list.
- Recommended heading pair is `## ❓ Open questions` then `## ↔️ Resolved decisions`.
- Keep stable question letters.
- Keep letter slots in place after resolution (no skipped letters).
- Question format: `### <Letter>) <Title>`.
- Each open question includes a short explanation paragraph describing decision, importance, and what changes by choice.
- Keep stable option numbering after references exist.
- Keep options in markdown ordered-list format (`1.` style).
- Do not use `1)` or lettered bullets for options.
- If ranking emojis are present, place them at option line end and apply consistently within the question.
- Ranking order is contextual and may change if new information arrives.
- Neutral options may omit ranking emojis.
- Pruned options are rendered as strikeout with trailing `❌`; never delete silently.
- Keep existing ranking emoji inside strikeout when already present; keep trailing `❌` outside strikeout text.
- Resolved form collapses to `### ~~<letter>) <Title>~~ ✅` plus `Chosen: \`<value>\``.
- On resolve, remove explanation and option list.
- Preserve ranking emoji in the resolved `Chosen:` value; do not strip or relocate it.
- Best practice: copy selected option text verbatim (including ranking emoji) into `Chosen:`.
- Do not mix unresolved queue with resolved records.

## 5) Fork protocol
Operational invariant:
- Canvases are durable across chat forks and persist outside any one chat timeline.

On `canoncanvas lastcall` / `🍺LastCall`:
1. Run canon sync on recent context:
   - write newly settled decisions/rules into canonical sections
   - apply pending OQ actions reflected in chat (`B2`, `❌B1,3`, keep-list effects, resolved collapses)
   - capture new constraints, dependencies, risks, assumptions, and source pointers that affect next choices
   - capture/refresh rationale footnotes in `Appendix A: Footnotes` for material decision changes
2. Run OQ integrity sweep:
   - Open vs Resolved sections remain separate
   - letter IDs and option numbering remain stable
   - resolved entries preserve chosen-value ranking emoji
   - pruned entries are strikeout plus trailing `❌`
3. Write/update fork handoff notes with:
   - required heading: `## 👴🏼 Fork Handoff Notes`
   - keep this heading as final section while handoff is active
   - phase + timestamp
   - what changed in this pass
   - context-only carry-forward items not yet canonized
   - next actions (ordered), risks/gotchas, and pointers
   - explicit momentum bridge: what lets the next operator "grab the torch" quickly
   - consume/remove entries after they are propagated into canonical sections or become irrelevant
4. Optional tail line:
  - append one short "note to younger self" line at the very end of canvas by default (skip only if user requests strict-formal tone)
  - required header for this block: `### 🚸 assistant's 👴🏼 note to → 📝 → younger 👶🏻 self`
  - do not improvise variant header text
  - style may be playful/snarky/sarcastic/inside-joke when context supports it; light roast is allowed
  - this is additive only and never replaces required handoff facts

Fork signal handling:
- On `💾` (`SavePointMarker`): treat current point as a fork-back anchor and keep canon current.
- On `⚡` (`ForkedMarker`): immediately reload canvas content, refresh state/context from latest canon, consume stale `👴🏼` carry-forward items into canonical sections, then continue.

## 6) Naming rules
- Enforce canvas title format: `🛜 <ProjectName> - <CanvasPurpose>`.
- Require `🛜` prefix for all CanonCanvas-bound canvases.
- CanonCanvas-bound canvases must be markdown canvases.
- Re-open existing matching canvases; do not create duplicates by default.
- Use PascalCase for `<ProjectName>` when applicable.
- Runtime validator (strict): `^🛜 [A-Z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)* - .+$`
- If a CanonCanvas-bound title fails the validator, fail closed and request a corrected title before continuing canon operations.
- Reference example: `🛜 LogKit - dev R6`.
- Module folder and references use PascalCase `CanonCanvas` unless user overrides naming policy.

## 7) Failure handling
If canvas is unavailable, stale, or structurally ambiguous:
1. Stop speculative edits.
2. Ask for missing section/content.
3. Resume only after authoritative input is provided.

If a matching canvas exists but is wrong type (non-markdown):
1. Fail closed and do not write canon updates into that canvas.
2. Ask user to select or create a markdown `🛜` canvas target.

If multiple matching `🛜` canvases exist:
1. Fail closed and ask user to choose one canonical winner.
2. Bind winner and continue without creating another duplicate by default.

If active-canvas telemetry is unavailable and no explicit title confirmation is provided:
1. Fail closed and request exact bind text (`use 🛜 <ProjectName> - <CanvasPurpose>`).
2. Do not create a new canvas as workaround.

If client-context status is ambiguous:
1. Ask one-line clarification before creating client-specific sections.
2. Keep non-client structure until clarified.

If a non-standard LastCall heading is detected (for example `🍺 Last Call snapshot`):
1. Normalize to `## 👴🏼 Fork Handoff Notes`.
2. Move the section to final position.
3. Consume/migrate stale items and remove empty residue.

If a non-standard younger-self note heading is detected:
1. Normalize to `### 🚸 assistant's 👴🏼 note to → 📝 → younger 👶🏻 self`.
2. Keep it as the final tail block under the fork handoff section.
