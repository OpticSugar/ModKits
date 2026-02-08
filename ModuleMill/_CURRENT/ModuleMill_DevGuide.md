# 🏭 ModuleMill DevGuide
(Developer Canon for ModuleKit Engineering) v0.2.0

ModuleID: ModuleMill
Version: 0.2.0
DocRole: UserGuide
Audience: Module developers (Codex-first), maintainers, and auditors

## 0) Mission
ModuleMill standardizes how ModuleKits are designed, authored, deployed, and maintained so behavior stays stable across chats and over time.

This is the canonical narrative document for the framework.
If anything conflicts with derived framework docs, this file wins.

## 1) Scope and runtime intent
- ModuleMill is developer infrastructure, not a day-to-day chat skill.
- Primary operator is Codex.
- A general assistant can use it only when explicitly directed.
- ModuleMill itself should not create background operational noise in normal chat flows.

## 2) Taxonomy
- `Module` / `Skill`: behavior contract executed by an assistant.
- `ModuleKit`: document bundle for one module.
- `KitRegistry`: deploy-time index of runtime modules and pointers to their docs.

## 3) Canon and derived roles
For runtime modules, doc roles remain strict:
1. `Install`
2. `QuickRefCard`
3. `MachineManual`
4. `UserGuide` (canonical)

Derived-doc rule:
- `Install`, `QuickRefCard`, and `MachineManual` may not invent new commands, triggers, state keys, output shapes, or policies.
- Any new rule must be authored in `UserGuide` first, then derived.

Tripwire:
- If rationale appears in `MachineManual`, move rationale to `UserGuide` and keep only executable rules in `MachineManual`.

## 4) Interface standards
### 4.1 ASCII-first command canon (required)
Every runtime module must publish one canonical command table in its `UserGuide`.

Required columns:
- `Command`
- `Canon` (ASCII-only canonical form)
- `Aliases` (emoji/punctuation optional)
- `Inputs` (typed, explicit)
- `Output shape`
- `State effects`

Rules:
- Emoji forms are aliases only.
- Canonical invocation must always be representable in plain ASCII.
- Bare-token overload is forbidden (for example `3`, `ok`, lone emoji).

### 4.2 Emoji glossary (required for user-facing modules)
Any module that exposes emoji aliases must include an `EmojiGlossary` section in its `UserGuide`.

Rules:
- Each emoji maps to a single term and behavior meaning.
- The mapping must be expandable to full text in assistant responses.
- If an emoji meaning changes, bump version and changelog.

## 5) State and lifecycle standards
Each runtime module must define:
- namespaced state keys (for example `faxax.hold_on`)
- authoritative state location
- lifecycle commands or controls for:
  - `load`
  - `activate`
  - `sleep`
  - `unload`
  - `status`

Fail-closed rule:
- If required state or artifacts are missing, do not guess behavior. Ask, halt, or queue.

## 6) Output contract standards
ModuleMill does not impose one universal response style.
Each runtime module must declare `ResponseEnvelope` in `MachineManual` and `QuickRefCard`.

Examples:
- `main_only`
- `main_plus_microtail`
- `structured_json_only`

## 7) Multi-module arbitration
Default Arbiter policy:
1. Explicit invocation wins.
2. If output shapes conflict, ask the user to choose one winner.
3. Otherwise prefer an already-loaded `AUTO` module.
4. Persist chosen winner for the chat/session until changed.

## 8) Deployment: Remote KitRegistry boot · 📇 KitRegistry
### 8.1 Three-layer architecture
1. BootStub (global behavior)
2. KitRegistry (index)
3. ModuleKit docs (Install/QuickRef/MachineManual/UserGuide)

### 8.2 Canonical registry path
`KitRegistry/_CURRENT/KitRegistry.md`

### 8.3 Registry required fields
Each module entry must provide:
- `Module`
- `Mission` (single line)
- `🎛️ EngagePolicy` (`AUTO | OFFER | MANUAL`)
- `🧲 NeedSignals` (`Keywords`, `Intents`, optional `Formats`, optional `DoNotFireIf`)
- `AutoRunScope`
- `DefaultLoad` (`yes|no`)
- `Docs` (Install/QuickRef/MachineManual/UserGuide URLs)
- `Version`
- `Compatibility`

Registry guardrail:
- Registry never invents commands. It only points to canonical docs.

### 8.4 Boot behavior
- Start chat: no automatic fetch.
- After second user message (or explicit modules request): offer once `boot / skip`.
- `boot`: fetch registry, load `DefaultLoad` modules, QuickRef first.
- `skip`: persist skip state and suppress further boot prompts in that chat.

### 8.5 Failure behavior
If registry or docs cannot be fetched:
- fail closed
- ask for pasted registry entry or required doc
- do not fabricate module behavior

## 9) Tooling and verification
### 9.1 Minimum lint pass
- Canon command list complete and unique.
- One canonical spelling per command.
- Derived docs do not invent rules.
- State keys are namespaced.
- Output templates match canon.
- User-facing emoji aliases are documented in `EmojiGlossary`.

### 9.2 Regression harness minimum
For each module, define prompt tests with:
- expected output shape
- must include constraints
- must not include constraints

## 10) Versioning and naming
- Use SemVer (`MAJOR.MINOR.PATCH`).
- `R2` and similar labels are sprint labels, not semantic versions.
- Legacy name `PPP` is historical alias only.
- Record framework deltas in `ModuleMill/_CURRENT/CHANGELOG.md`.
- Runtime ModuleKit filename convention inside `<Module>/_CURRENT/` is role-based and unprefixed:
  - `Install.md`
  - `QuickRefCard.md`
  - `MachineManual.md`
  - `UserGuide.md`
- ModuleMill framework artifacts are allowed to keep `ModuleMill_*` names for clarity.

## 11) Migration law (PPP → ModuleMill)
- `PPP` namespace is retired.
- Canon files are now under `ModuleMill/_CURRENT/`.
- `ModuleKit_Index.md` is retired in favor of `KitRegistry/_CURRENT/KitRegistry.md`.
