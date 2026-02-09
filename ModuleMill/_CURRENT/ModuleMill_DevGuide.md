# 🏭 ModuleMill DevGuide
(Developer Canon for ModuleKit Engineering) v0.4.0

ModuleID: ModuleMill
Version: 0.4.0
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
- `ModuleKit`: document set for one module.
- `ModuleManifest`: trigger and contract metadata for fast selection and fail-closed gating.
- `KitRegistry`: deploy-time index of runtime modules and pointers to their docs.

## 3) Canon and derived roles
For runtime modules, role boundaries remain strict:
1. `UserGuide` (canonical and most detailed source of truth)
2. `MachineManual` (derived executable runtime rules)
3. `QuickRefCard` (derived compact operational reference)
4. `Install` (derived deployment and runbook-only procedure)

Non-negotiable canon depth:
- `UserGuide` must remain verbose and complete.
- `UserGuide` must retain full context, rationale, tradeoffs, failure modes, examples, and migration notes.
- Compression that removes canonical detail is a framework violation.

Required bundle artifacts under `<Module>/_CURRENT/`:
- `UserGuide.md`
- `MachineManual.md`
- `QuickRefCard.md`
- `Install.md`
- `ModuleManifest.yaml`

Bundle policy:
- Do not create or maintain `_BUNDLE.md` files as part of normal ModuleMill workflow.
- If a bundle is created for temporary troubleshooting, treat it as disposable and out-of-contract.
- Release and lint targets are the canonical `_CURRENT` role files plus `ModuleManifest.yaml`, not bundle files.

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
- Emoji forms are aliases only for canonical naming, but are first-class user input forms when declared.
- Canonical invocation must always be representable in plain ASCII.
- Bare-token overload is forbidden (for example `3`, `ok`, lone emoji).
- If a module defines emoji aliases, docs must preserve them and map each alias deterministically to one behavior.

### 4.2 ModuleManifest contract (required)
Every runtime module must include `<Module>/_CURRENT/ModuleManifest.yaml` with these keys:
- `module`
- `version`
- `mission`
- `engage_policy` (`AUTO | OFFER | MANUAL`)
- `use_when` (list)
- `do_not_use_when` (list)
- `required_inputs` (list)
- `response_envelope`
- `failure_mode`
- `docs` (`install`, `quickref`, `machinemanual`, `userguide`)

Purpose:
- Decouple trigger/selection metadata from long-form docs.
- Enable deterministic arbitration and fail-closed behavior before loading large documents.

### 4.3 Emoji glossary (required for user-facing modules)
Any module that exposes emoji aliases must include an `EmojiGlossary` section in its `UserGuide`.

Rules:
- Each emoji maps to a single term and behavior meaning.
- The mapping must be expandable to full text in assistant responses.
- If an emoji meaning changes, bump version and changelog.
- Emoji aliases are first-class input forms and must not be omitted from canonical docs.

## 5) Progressive disclosure load policy
Use staged loading to reduce context and improve precision:
1. Selection stage: read `KitRegistry` entry plus module `ModuleManifest.yaml`.
2. Operating stage: load `QuickRefCard.md` for minimal behavior surface.
3. Execution-hardening stage: load `MachineManual.md` before complex or risky tasks.
4. Canon escalation stage: load `UserGuide.md` only when needed for policy disputes, derivation, or module development.

Rules:
- Do not start from full `UserGuide` for routine runtime usage.
- Escalate stages only when uncertainty or conflict requires it.

## 6) State and lifecycle standards
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

## 7) Output contract standards
ModuleMill does not impose one universal response style.
Each runtime module must declare `ResponseEnvelope` in all of:
- `ModuleManifest.yaml`
- `MachineManual.md`
- `QuickRefCard.md`

Examples:
- `main_only`
- `main_plus_microtail`
- `structured_json_only`

## 8) Multi-module arbitration
Default Arbiter policy:
1. Explicit invocation wins.
2. If output shapes conflict, ask the user to choose one winner.
3. Otherwise prefer an already-loaded `AUTO` module.
4. Persist chosen winner for the chat/session until changed.

If no winner can be selected deterministically from manifest metadata:
- fail closed
- ask the user to choose

## 9) Deployment: Remote KitRegistry boot · 📇 KitRegistry
### 9.1 Three-layer architecture
1. BootStub (global behavior)
2. KitRegistry (index)
3. ModuleKit artifacts (`ModuleManifest` + Install/QuickRef/MachineManual/UserGuide)

### 9.2 Canonical registry path
`KitRegistry/_CURRENT/KitRegistry.md`

### 9.2.1 ChatGPT global instructions source
Maintain copy/paste-ready global instructions in:
`KitRegistry/_CURRENT/ChatGPT_GlobalInstructions.md`

Operational rule:
- When that file changes, manually replace ChatGPT global instructions with the updated block.
- ModuleMill release notes must explicitly call out this replacement requirement.

### 9.3 Registry required fields
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

### 9.4 Boot behavior
- Start chat: fetch registry and auto-load `DefaultLoad=yes` modules using `ModuleManifest` + `QuickRefCard` first.
- `skip modules`: persist opt-out state for the chat and suppress module loading.

### 9.5 Failure behavior
If registry or docs cannot be fetched:
- fail closed
- ask for pasted registry entry or required module doc
- do not fabricate module behavior

## 10) Tooling and verification
### 10.1 Minimum lint pass
- Canon command list complete and unique.
- One canonical spelling per command.
- Derived docs do not invent rules.
- State keys are namespaced.
- Output templates match canon.
- User-facing emoji aliases are documented in `EmojiGlossary`.
- `ModuleManifest.yaml` is present and contains required fields.
- `ModuleManifest` doc pointers map to existing local files in `_CURRENT`.
- For repo-level strict scans, use `--modulekit-only` to target canonical artifacts.

### 10.2 Regression harness minimum
For each module, define prompt tests with:
- expected output shape
- must include constraints
- must not include constraints

### 10.3 Contract regression corpus
Maintain a small prompt corpus per module (minimum 10 prompts):
- 3 nominal prompts
- 3 edge-case prompts
- 2 collision/arbitration prompts
- 2 fail-closed prompts

## 11) Versioning and naming
- Use SemVer (`MAJOR.MINOR.PATCH`).
- `R2` and similar labels are sprint labels, not semantic versions.
- Legacy name `PPP` is historical alias only.
- Record framework deltas in `ModuleMill/_CURRENT/CHANGELOG.md`.
- Runtime ModuleKit filename convention inside `<Module>/_CURRENT/` is role-based and unprefixed:
  - `Install.md`
  - `QuickRefCard.md`
  - `MachineManual.md`
  - `UserGuide.md`
  - `ModuleManifest.yaml`
- ModuleMill framework artifacts are allowed to keep `ModuleMill_*` names for clarity.

## 12) Migration law (PPP -> ModuleMill)
- `PPP` namespace is retired.
- Canon files are now under `ModuleMill/_CURRENT/`.
- `ModuleKit_Index.md` is retired in favor of `KitRegistry/_CURRENT/KitRegistry.md`.
- Legacy modules without `ModuleManifest.yaml` are supported temporarily, but all new modules must include it.
