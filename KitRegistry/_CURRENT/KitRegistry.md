# 📇 KitRegistry
Runtime Module Index v0.3.7

RegistryID: KitRegistry
ModuleID: KitRegistry
Version: 0.3.7
DocRole: UserGuide
Audience: Runtime assistants and module operators
Updated: 2026-02-19
Scope: Runtime ModuleKits only

## 0) Policy
- Source of truth for runtime module discovery and doc pointers.
- Registry never invents module commands.
- Module behavior authority remains in module `UserGuide` canon.
- ModuleMill is developer infrastructure and is intentionally excluded to avoid day-to-day chat noise.

## 1) Schema
Each module entry must include:
- `Module`
- `ModuleEmoji` (single canonical emoji shorthand name)
- `ModuleAliases` (ASCII + emoji address forms)
- `Mission`
- `🎛️ EngagePolicy` (`AUTO | OFFER | MANUAL`)
- `🧲 NeedSignals` (`Keywords`, `Intents`, optional `Formats`, optional `DoNotFireIf`)
- `AutoRunScope`
- `DefaultLoad` (`yes|no`)
- `SingleEmojiActivate` (`yes|no`)
- `Docs` (`Manifest`, `Install`, `QuickRef`, `MachineManual`, `UserGuide`)
- `Version`
- `Compatibility`

## 2) Modules
### Module: FaxAx
- ModuleEmoji: `📠`
- ModuleAliases: `faxax`, `fax`, `📠`
- Mission: Scope-first response protocol with opt-in depth and hold/release comment stacking.
- 🎛️ EngagePolicy: `AUTO`
- 🧲 NeedSignals:
  - Keywords: `verbosity`, `short answer`, `expand`, `hold`, `stack comments`, `ask chatgpt`, `too long`
  - Intents: `control answer depth`, `batch feedback`, `delay response until release`
  - Formats: `emoji mode switches`, `expansion chips`
  - DoNotFireIf: `user requests raw JSON only`, `another module explicitly invoked`
- AutoRunScope: `response_formatting`
- DefaultLoad: `yes`
- SingleEmojiActivate: `yes`
- Docs:
  - Manifest: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/ModuleManifest.yaml`
  - Install: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/Install.md`
  - QuickRef: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/QuickRefCard.md`
  - MachineManual: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/MachineManual.md`
  - UserGuide: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/UserGuide.md`
- Version: `0.2.0`
- Compatibility: `Uses ModuleMill-style doc roles; ask user to choose on output-shape collisions.`

### Module: CanonCanvas
- ModuleEmoji: `🛜`
- ModuleAliases: `canoncanvas`, `canon canvas`, `🛜`
- Mission: Canvas-as-canon workflow for fork-survivable project memory and decision governance.
- 🎛️ EngagePolicy: `OFFER`
- 🧲 NeedSignals:
  - Keywords: `canvas`, `canon`, `fork`, `lastcall`, `open questions`, `resolved decisions`, `cleanup`
  - Intents: `preserve project memory`, `govern decisions`, `prepare fork handoff`
  - Formats: `markdown canvas`, `question-option shorthand`, `emoji aliases`
  - DoNotFireIf: `user explicitly invokes another module with conflicting output envelope`
- AutoRunScope: `canvas_governance`
- DefaultLoad: `no`
- SingleEmojiActivate: `yes`
- Docs:
  - Manifest: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/ModuleManifest.yaml`
  - Install: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/Install.md`
  - QuickRef: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/QuickRefCard.md`
  - MachineManual: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/MachineManual.md`
  - UserGuide: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanonCanvas/_CURRENT/UserGuide.md`
- Version: `0.3.6`
- Compatibility: `Uses ModuleMill-style doc roles, dynamic section materialization, standard header library guidance, LastCall-as-ritual semantics, final-position transient 👴🏼 handoff notes, official 🚸 younger-self note header, explicit no-assumed-client gating, conditional ⚖️/💡 client workflow, markdown-canvas binding guardrails, active-canvas exact-title bind fallback, duplicate-prevention preflight, and fail-closed arbitration on output-shape conflicts.`

### Module: LogKit
- ModuleEmoji: `🖨️`
- ModuleAliases: `logkit`, `log kit`, `🖨️`
- Mission: Durable logging lifecycle from chat capture through triage, export, retrieval, and archive.
- 🎛️ EngagePolicy: `OFFER`
- 🧲 NeedSignals:
  - Keywords: `log`, `capture`, `flush`, `pending`, `logpak`, `vault`, `triage`, `retrieve`
  - Intents: `record durable decisions`, `track issues/ideas`, `export or retrieve logs across contexts`
  - Formats: `json ledger`, `jsonl export`, `emoji aliases`
  - DoNotFireIf: `user requests no logging`, `another module explicitly invoked with conflicting output envelope`
- AutoRunScope: `durable_logging`
- DefaultLoad: `no`
- SingleEmojiActivate: `yes`
- Docs:
  - Manifest: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/ModuleManifest.yaml`
  - Install: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/Install.md`
  - QuickRef: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/QuickRefCard.md`
  - MachineManual: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/MachineManual.md`
  - UserGuide: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/LogKit/_CURRENT/UserGuide.md`
- Version: `0.4.6`
- Compatibility: `Uses ModuleMill-style doc roles, explicit lifecycle controls, fail-closed ledger guards, configurable triage/security policies, emoji-first alias mapping, emoji-first ledger naming (default `🖨️ Log`), JSON code-canvas binding guardrails, active-canvas exact-title bind fallback, and duplicate-prevention preflight.`

## 3) Boot contract (for BootStub consumers)
- No auto-boot. Load/activate only on explicit invoke.
- Explicit invoke forms:
  - exact module emoji (`📠`, `🛜`, `🖨️`)
  - module name/alias
  - clear natural-language launch intent
- Conversational intent rule:
  - high-confidence single-module match => load+activate
  - ambiguous => ask one short clarifier
- Module purpose quick map:
  - `📠 FaxAx`: response shaping (short/long, hold/release feedback stack)
  - `🛜 CanonCanvas`: durable project-memory canvas and decision governance
  - `🖨️ LogKit`: durable logging canvas lifecycle (capture/commit/export/retrieve)
- On invoke, load `ModuleManifest.yaml` then `QuickRefCard.md`; escalate to other docs only if needed.
- Launch gate: do not perform module-specific actions until `ModuleManifest.yaml` + `QuickRefCard.md` fetch succeeds.
- Canvas bind discipline:
  - bind/reuse existing matching canvas first
  - if bind state is unclear, ask for exact title and bind that title
  - do not invent hidden UI controls or create duplicate-canvas workarounds
- Fetch discipline (mandatory):
  - Resolve module docs from registry URLs first; do not browse for module names.
  - Allowed doc sources are `raw.githubusercontent.com/OpticSugar/ModKits` (preferred) and direct GitHub mirrors only if raw links fail.
  - If Web Search is required, constrain queries to `site:raw.githubusercontent.com/OpticSugar/ModKits/main`.
  - Do not use unrelated websites for module bootstrapping.
- Deterministic URL pattern (fallback when registry is known but one doc URL is missing):
  - `https://raw.githubusercontent.com/OpticSugar/ModKits/main/<Module>/_CURRENT/<DocFile>`
  - `<DocFile>`: `ModuleManifest.yaml`, `Install.md`, `QuickRefCard.md`, `MachineManual.md`, `UserGuide.md`
- Single-emoji module addressing is valid:
  - If a message is exactly a module emoji, treat it as module activation/invocation intent for that module.
  - If module is loaded but inactive, activate it.
  - If module is not loaded and `SingleEmojiActivate=yes`, load then activate it.
  - If multiple modules share an emoji alias, fail closed and ask user to choose.
- Fetch failure (strict, required):
  - Never claim any module is loaded/active when required docs were not successfully fetched.
  - Step A: ask user to enable Web Search and retry fetch.
  - Step B: if fetch still fails, provide a code block with the exact module doc URLs and ask user to paste the returned content.
  - If both steps fail or are declined, continue as a normal assistant and explicitly state module behavior is not active.
