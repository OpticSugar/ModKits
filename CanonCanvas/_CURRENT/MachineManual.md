# CanonCanvas MachineManual (derived)

ModuleID: CanonCanvas
Version: 0.2.0
DocRole: MachineManual
Audience: Assistants operating CanonCanvas at runtime

---

## Runtime contract
- Treat `UserGuide` as canonical.
- Enforce fail-closed behavior when canvas artifacts are missing.
- Do not invent commands, state keys, or output shapes.

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
- `canoncanvas.open_questions_index`
- `canoncanvas.resolved_index`
- `canoncanvas.footnote_counter`

## 2) Lifecycle controls
- `canoncanvas load`: initialize state and activate
- `canoncanvas activate`: set active true
- `canoncanvas sleep`: set active false, preserve state
- `canoncanvas unload`: clear state
- `canoncanvas status`: emit structured status

## 3) Command interpretation
### 3.1 Canon/care commands
- `canoncanvas canonize`: produce canon patch from recent decisions.
- `canoncanvas cleanup`: remove duplication/noise while preserving rules.
- `canoncanvas lastcall`: pre-handoff continuity pass (canon sync + OQ integrity + momentum handoff capture).
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

## 4) Open Questions enforcement
- Use OQ terminology (`Open Questions` / `OQ`) consistently in all outputs.
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
   - phase + timestamp
   - what changed in this pass
   - context-only carry-forward items not yet canonized
   - next actions (ordered), risks/gotchas, and pointers
   - explicit momentum bridge: what lets the next operator "grab the torch" quickly
4. Optional tail line:
   - may append one short "note to younger self" line at the bottom of canvas/handoff block
   - this is additive only and never replaces required handoff facts

## 6) Naming rules
- Enforce canvas title format: `🛜 <ProjectName> - <CanvasPurpose>`.
- Require `🛜` prefix for all CanonCanvas-bound canvases.
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
