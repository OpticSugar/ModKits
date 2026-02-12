# 🏭 ModuleMill DevGuide
(Developer Canon for ModuleKit Engineering) v0.7.1

ModuleID: ModuleMill
Version: 0.7.1
DocRole: UserGuide
Audience: Module developers (Codex-first), maintainers, and auditors

## 0) Mission
ModuleMill standardizes how ModuleKits are designed, authored, deployed, and maintained so behavior stays stable across chats and over time.

ModuleMill exists to protect user-authored module behavior from accidental erosion during refactors, derivation, and standardization.
The framework is intentionally anti-neutering: if standardization removes defining functionality, templates, or rationale, the framework has failed.

This is the canonical narrative document for the framework.
If anything conflicts with derived framework docs, this file wins.

## 1) Scope, origin, and runtime intent
- Origin story: modules were created to add elaborate, specialized behavior to regular ChatGPT chats.
- Practical definition: a runtime module is "a skill for regular ChatGPT" packaged as a ModuleKit.
- Codex has native `skills`; regular ChatGPT does not, so ModuleKits provide the equivalent capability through docs + runtime discipline.
- ModuleMill's job is to preserve that authored capability while keeping execution deterministic.
- ModuleMill is developer infrastructure, not a day-to-day chat skill.
- Primary operator is Codex.
- A general assistant can use it only when explicitly directed.
- ModuleMill itself should not create background operational noise in normal chat flows.

### 1.1 Guardrailed improvisation model
- Runtime modules are guardrails plus scaffolding, not rigid script engines.
- Practical analogy: run modules like a DM in a tabletop session; obey the rules and structure, then adapt phrasing to the live context.
- Determinism applies to contracts (`commands`, `state`, `output shapes`, invariants), not to forcing repetitive canned prose.
- If canonical `UserGuide` includes style behavior guidance (for example playful/non-repetitive invitation copy), preserve it during derivation.
- Do not flatten expressive guidance into generic robotic wording when that guidance is part of module behavior.

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
- Every runtime module must declare explicit non-negotiable invariants in `ModuleManifest.must_preserve`.
- `must_preserve` terms are anti-neutering guards and must stay present in canonical `UserGuide` text.
- Any feature expressed as `Emoji + PascalCaseName` is an official non-prunable mechanism.
- Any `Emoji + PascalCaseName` feature name must be preserved verbatim unless feature removal is explicitly approved or an explicit rename is explicitly approved.
- If canon marks style guidance as behavior-critical, derived docs must preserve it; do not replace it with static boilerplate.

UserGuide preservation law (hard rule):
- The canonical `UserGuide` is the human-facing maximal document and the module DNA/blueprint.
- The canonical `UserGuide` must explicitly preserve:
  - Why the module exists and what problem it solves.
  - How the module helps users in practical terms.
  - Reasoning, rationale, context, and tradeoffs behind rules and structure.
  - Full instruction set, scenarios, example use-cases, formatting templates, and migration notes.
- Heavy compression, "cleanup," or trimming in canonical `UserGuide` is forbidden unless functionality is intentionally changing.
- If functionality intentionally changes, document it explicitly in canonical `UserGuide` and changelog before derived docs are regenerated.
- If unresolved conflict exists between "concise rewrite" and "preserve behavior/rationale", preserve behavior/rationale and escalate for user decision.

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

### 4.1.1 Natural-language intent layer (required)
- Runtime modules must support command invocation from either explicit syntax or clear natural-language intent.
- If user phrasing maps with high confidence to exactly one canonical command, execute it without forcing exact syntax.
- If confidence is low, or multiple commands are plausible, ask one brief clarification question.
- Confidence decisions must use live chat context and current module state (for example hold/release state).
- Natural-language intent execution never bypasses safety gates, required inputs, or fail-closed constraints.
- Design for mixed typing + speech-to-text input: prefer frictionless execution when confidence is high.

### 4.2 ModuleManifest contract (required)
Every runtime module must include `<Module>/_CURRENT/ModuleManifest.yaml` with these keys:
- `module`
- `module_emoji`
- `module_aliases`
- `version`
- `mission`
- `must_preserve` (list of critical invariants that must not be compressed away)
- `must_preserve_runtime` (optional list; if present, each term must appear in UserGuide + MachineManual + QuickRefCard)
- `engage_policy` (`AUTO | OFFER | MANUAL`)
- `intent_policy` (`explicit_only | infer_high_confidence`)
- `single_emoji_activate` (`true|false`)
- `use_when` (list)
- `do_not_use_when` (list)
- `required_inputs` (list)
- `response_envelope`
- `failure_mode`
- `docs` (`install`, `quickref`, `machinemanual`, `userguide`)

Purpose:
- Decouple trigger/selection metadata from long-form docs.
- Enable deterministic arbitration and fail-closed behavior before loading large documents.
- Preserve module identity and core guarantees even when documents are refactored or shortened.
- Make command-intent handling explicit (exact syntax only vs high-confidence natural-language inference).

### 4.3 Emoji glossary (required for user-facing modules)
Any module that exposes emoji aliases must include an `EmojiGlossary` section in its `UserGuide`.

Rules:
- Each emoji maps to a single term and behavior meaning.
- The mapping must be expandable to full text in assistant responses.
- If an emoji meaning changes, bump version and changelog.
- Emoji aliases are first-class input forms and must not be omitted from canonical docs.
- Any `Emoji + PascalCaseName` feature name (for example `🪓AxFactor`) must be listed in `ModuleManifest.must_preserve`.
- If runtime behavior depends on that feature contract, mirror the exact term in `must_preserve_runtime`.

## 5) Progressive disclosure load policy
Use staged loading to reduce context and improve precision:
1. Selection stage: read `KitRegistry` entry plus module `ModuleManifest.yaml`.
2. Operating stage: load `QuickRefCard.md` for minimal behavior surface.
3. Execution-hardening stage: load `MachineManual.md` before complex or risky tasks.
4. Canon escalation stage: load `UserGuide.md` only when needed for policy disputes, derivation, or module development.

Rules:
- Do not start from full `UserGuide` for routine runtime usage.
- Escalate stages only when uncertainty or conflict requires it.
- Escalate to `UserGuide` before any policy edit, spec rewrite, or behavior dispute; do not resolve those from `QuickRefCard` alone.
- Progressive disclosure is a loading strategy only; it never permits canonical `UserGuide` compression or feature removal.

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
Enterprise variant:
`KitRegistry/_CURRENT/ChatGPT_GlobalInstructions_Enterprise.md`

Operational rule:
- When that file changes, manually replace ChatGPT global instructions with the updated block.
- ModuleMill release notes must explicitly call out this replacement requirement.

### 9.2.2 Codex skill sync contract (required)
Operational reality:
- ModuleMill is authored in this Git repo, but operationally executed in Codex through the installed `ModuleMill` skill.
- Repo-only edits do not fully change Codex behavior until skill files are updated.

Policy:
- Every ModuleMill framework change must include a skill-sync proposal.
- The assistant must always provide exact copy/update commands and verification commands after ModuleMill edits.
- If the assistant cannot directly modify skill files in the active environment, it must provide a complete runbook and stop short of claiming the update is active.

Minimum sync runbook:
```bash
cp ModKits/ModuleMill/_CURRENT/ModuleMill_DevGuide.md ~/.codex/skills/ModuleMill/references/ModuleMill_DevGuide.md
cp ModKits/ModuleMill/_CURRENT/ModuleMill_MachineManual.md ~/.codex/skills/ModuleMill/references/ModuleMill_MachineManual.md
cp ModKits/ModuleMill/_CURRENT/CHANGELOG.md ~/.codex/skills/ModuleMill/references/ModuleMill_CHANGELOG.md
cp ModKits/KitRegistry/_CURRENT/KitRegistry.md ~/.codex/skills/ModuleMill/references/KitRegistry.md
cp ModKits/KitRegistry/_CURRENT/ChatGPT_GlobalInstructions.md ~/.codex/skills/ModuleMill/references/ChatGPT_GlobalInstructions.md
cp ModKits/KitRegistry/_CURRENT/ChatGPT_GlobalInstructions_Enterprise.md ~/.codex/skills/ModuleMill/references/ChatGPT_GlobalInstructions_Enterprise.md
cp ModKits/ModuleMill/_CURRENT/ModuleMill_Compiler.py ~/.codex/skills/ModuleMill/scripts/modulemill_compiler.py
```

Minimum verification runbook:
```bash
diff -u ModKits/ModuleMill/_CURRENT/ModuleMill_DevGuide.md ~/.codex/skills/ModuleMill/references/ModuleMill_DevGuide.md
diff -u ModKits/ModuleMill/_CURRENT/ModuleMill_MachineManual.md ~/.codex/skills/ModuleMill/references/ModuleMill_MachineManual.md
diff -u ModKits/ModuleMill/_CURRENT/ModuleMill_Compiler.py ~/.codex/skills/ModuleMill/scripts/modulemill_compiler.py
diff -u ModKits/KitRegistry/_CURRENT/KitRegistry.md ~/.codex/skills/ModuleMill/references/KitRegistry.md
diff -u ModKits/KitRegistry/_CURRENT/ChatGPT_GlobalInstructions.md ~/.codex/skills/ModuleMill/references/ChatGPT_GlobalInstructions.md
diff -u ModKits/KitRegistry/_CURRENT/ChatGPT_GlobalInstructions_Enterprise.md ~/.codex/skills/ModuleMill/references/ChatGPT_GlobalInstructions_Enterprise.md
```

### 9.3 Registry required fields
Each module entry must provide:
- `Module`
- `ModuleEmoji` (single canonical emoji shorthand)
- `ModuleAliases` (ASCII + emoji address forms)
- `Mission` (single line)
- `🎛️ EngagePolicy` (`AUTO | OFFER | MANUAL`)
- `🧲 NeedSignals` (`Keywords`, `Intents`, optional `Formats`, optional `DoNotFireIf`)
- `AutoRunScope`
- `DefaultLoad` (`yes|no`)
- `SingleEmojiActivate` (`yes|no`)
- `Docs` (Install/QuickRef/MachineManual/UserGuide URLs)
- `Version`
- `Compatibility`

Registry guardrail:
- Registry never invents commands. It only points to canonical docs.

### 9.4 Boot behavior
- Start chat: fetch registry and auto-load `DefaultLoad=yes` modules using `ModuleManifest` + `QuickRefCard` first.
- `skip modules`: persist opt-out state for the chat and suppress module loading.
- Single-emoji module activation must work for all modules with `SingleEmojiActivate=yes`.
- If user sends a single registered module emoji, treat it as module activation/invocation intent.

### 9.5 Failure behavior
If registry or docs cannot be fetched:
- fail closed
- ask the user to enable Web Search before retrying fetch (especially in enterprise/work environments)
- if fetch still fails, provide a copy/paste-ready code block with required doc URLs and ask the user to paste needed docs
- do not claim module activation or pretend module-compliant execution while docs are unavailable
- if offering best-effort help anyway, label it as non-module improvisation

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
- `must_preserve` exists and every invariant term appears in canonical `UserGuide`.
- If `must_preserve_runtime` is provided, each term appears in `UserGuide`, `MachineManual`, and `QuickRefCard`.
- `intent_policy` exists in `ModuleManifest.yaml` and uses a supported value.
- For `intent_policy=infer_high_confidence`, canonical docs include confidence policy (`high => execute`, `low => clarify`).
- Strict lint fails when an inline code span starts with variation selector bytes (`\ufe0e`/`\ufe0f`), which indicates a dropped emoji base token.
- Strict lint enforces emoji-alias parity from UserGuide command-table aliases into `MachineManual` and `QuickRefCard`.
- Manual parity check: behavior-critical guided-improv directives in `UserGuide` are preserved in `MachineManual` and `QuickRefCard`.
- Strict parity checks pass for lifecycle command/state coverage between `UserGuide` and `MachineManual`.
- ChatGPT global-instruction ` ```text ` block length must stay <= 1400 chars to reserve personalization room.
- After ModuleMill framework edits, repo-vs-skill parity diff checks pass for DevGuide, MachineManual, Compiler, and KitRegistry/global-instruction references.
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

## 13) Conflict resolution and documentation duty
- If maintainers or assistants disagree on module behavior, preserve existing canonical behavior by default and fail closed on destructive rewrites.
- Any intentional behavior reduction must be treated as a functional change request, not formatting cleanup.
- When policy disagreements occur, document:
  - the competing interpretations
  - the chosen outcome
  - rationale for the decision
  - migration impact on existing modules
- Record that decision in canonical docs before deriving or releasing.
