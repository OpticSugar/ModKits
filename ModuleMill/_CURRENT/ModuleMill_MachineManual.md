# 🤖 ModuleMill MachineManual
(Enforcement Runbook for ModuleKit Engineering) v0.2.0

ModuleID: ModuleMill
Version: 0.2.0
DocRole: MachineManual
Audience: Codex or assistant executing ModuleMill rules

## 0) Non-negotiables
- Fail closed. Never fabricate unknown behavior.
- Keep doc roles strict.
- Treat `UserGuide` as canon.
- Derived docs must not invent commands, triggers, state keys, output shapes, or policies.
- Keep canonical command forms ASCII-first.
- For user-facing emoji aliases, require an explicit `EmojiGlossary` in `UserGuide`.

## 1) Intake checklist for module work
Require (or safely infer) before writing/patching a module:
- Mission
- Canon command table (with ASCII canonical forms)
- Inputs and typed argument grammar
- Output shape and `ResponseEnvelope`
- Authoritative state and lifecycle behavior
- Conflict policy and precedence

If critical fields are missing and cannot be inferred safely, ask targeted questions.

## 2) Authoring order
1. Update canonical `UserGuide` first.
2. Derive `MachineManual` from canon.
3. Derive `QuickRefCard` from canon.
4. Derive/install `Install` steps.
5. Run lint and regression checks.

## 3) Derived-doc tripwires
- If `MachineManual` contains rationale/history: move rationale to `UserGuide`.
- If executable rules exist only in prose: normalize into canonical tables in `UserGuide`.
- If derived docs conflict with canon: canon wins and derived docs must be patched.

## 4) Arbitration protocol
When multiple modules may respond in one turn:
1. Explicit invocation wins.
2. If output shapes conflict, ask user to choose one winner.
3. Otherwise prefer already-loaded `AUTO` module.
4. Persist winner for session until changed.

## 5) Deployment protocol (KitRegistry)
- Use `KitRegistry/_CURRENT/KitRegistry.md` as source of truth for runtime module discovery.
- Apply `🎛️ EngagePolicy` and `🧲 NeedSignals` as engagement hints, not command authority.
- Load QuickRef first for boot defaults.
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

## 8) Release routine
- Bump SemVer.
- Update `ModuleMill/_CURRENT/CHANGELOG.md`.
- Record unresolved items as explicit open questions.
- Keep naming consistent under `_CURRENT` paths.
