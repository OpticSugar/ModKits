# 🤖 ModuleMill MachineManual
(Enforcement Runbook for ModuleKit Engineering) v0.4.0

ModuleID: ModuleMill
Version: 0.4.0
DocRole: MachineManual
Audience: Codex or assistant executing ModuleMill rules

## 0) Non-negotiables
- Fail closed. Never fabricate unknown behavior.
- Keep doc roles strict.
- Treat `UserGuide` as canon.
- Keep `UserGuide` verbose and complete; do not over-compress canonical detail.
- `UserGuide` must preserve context, rationale, tradeoffs, failure behavior, examples, and migration notes.
- Derived docs must not invent commands, triggers, state keys, output shapes, or policies.
- Keep canonical command forms ASCII-first.
- For user-facing emoji aliases, require an explicit `EmojiGlossary` in `UserGuide`.
- If emoji aliases are defined, treat them as first-class input forms and preserve deterministic alias -> behavior mapping.
- Require `ModuleManifest.yaml` for new modules and use it for initial module selection.
- Do not require or produce `_BUNDLE.md` artifacts in normal authoring, lint, or release flows.

## 1) Intake checklist for module work
Require (or safely infer) before writing or patching a module:
- Mission
- `ModuleManifest` fields: `engage_policy`, `use_when`, `do_not_use_when`, `required_inputs`, `response_envelope`, `failure_mode`
- Canon command table (with ASCII canonical forms)
- Inputs and typed argument grammar
- Output shape and `ResponseEnvelope`
- Authoritative state and lifecycle behavior
- Conflict policy and precedence

If critical fields are missing and cannot be inferred safely, ask targeted questions.

## 2) Authoring order
1. Update canonical `UserGuide` first.
2. Update or create `ModuleManifest.yaml` from canon.
3. Derive `MachineManual` from canon.
4. Derive `QuickRefCard` from canon.
5. Derive or patch `Install` steps.
6. Run lint and regression checks.

Troubleshooting exception:
- A temporary `_BUNDLE.md` may be used for ad hoc debugging only.
- Never treat bundle files as canonical inputs or release artifacts.

## 3) Derived-doc tripwires
- If `MachineManual` contains rationale or history: move rationale to `UserGuide`.
- If executable rules exist only in prose: normalize into canonical tables in `UserGuide`.
- If derived docs conflict with canon: canon wins and derived docs must be patched.
- If `ModuleManifest` conflicts with `UserGuide` contract, patch `ModuleManifest` before release.

## 4) Arbitration protocol
When multiple modules may respond in one turn:
1. Explicit invocation wins.
2. If output shapes conflict, ask user to choose one winner.
3. Otherwise prefer already-loaded `AUTO` module.
4. Persist winner for session until changed.

Before asking user to choose, attempt deterministic filtering from `ModuleManifest` metadata:
- reject modules matching `do_not_use_when`
- keep modules matching `use_when`
- keep modules whose `required_inputs` are satisfied

## 5) Deployment protocol (KitRegistry)
- Use `KitRegistry/_CURRENT/KitRegistry.md` as source of truth for runtime module discovery.
- Apply `🎛️ EngagePolicy` and `🧲 NeedSignals` as engagement hints, not command authority.
- Load `ModuleManifest` and `QuickRefCard` first for boot defaults.
- Load `MachineManual` for complex or risky operations.
- Load `UserGuide` only for canon disputes, derivation, or module authoring.
- If fetch fails, request pasted docs and halt speculative behavior.

## 6) ModuleMill runtime intent
- ModuleMill is developer infrastructure.
- Do not auto-load it in regular chats.
- Engage only on explicit developer request.

## 7) Mechanical lint pass
Run compiler lint and enforce:
- required metadata present on module docs
- `DocRole` valid
- no role bleed warnings
- no duplicate canon commands (manual review if needed)
- glossary present for emoji-facing modules
- `ModuleManifest.yaml` present for non-framework modules
- required manifest keys present
- manifest `docs` pointers map to existing files under `_CURRENT`
- manifest `response_envelope` matches declared envelope in derived docs
- UserGuide completeness checks pass (context/mission depth, rationale/why, failure behavior, examples)
- Over-compression heuristics pass for UserGuides in strict mode
- Prefer `lint --strict --modulekit-only` for repo-level strict scans to avoid non-ModuleKit support files.

## 8) Release routine
- Bump SemVer.
- Update `ModuleMill/_CURRENT/CHANGELOG.md`.
- If `KitRegistry/_CURRENT/ChatGPT_GlobalInstructions.md` changed, replace your ChatGPT global instructions by copy/paste.
- Record unresolved items as explicit open questions.
- Keep naming consistent under `_CURRENT` paths.
- Refresh the per-module regression prompt corpus when contract behavior changes.
