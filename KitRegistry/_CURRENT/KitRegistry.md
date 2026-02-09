# 📇 KitRegistry
Runtime Module Index v0.3.0

RegistryID: KitRegistry
ModuleID: KitRegistry
Version: 0.3.0
DocRole: UserGuide
Audience: Runtime assistants and module operators
Updated: 2026-02-09
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
- Version: `0.1.0`
- Compatibility: `Uses ModuleMill-style doc roles; ask user to choose on output-shape collisions.`

### Module: CanvasCanon
- ModuleEmoji: `🛜`
- ModuleAliases: `canvascanon`, `canvas canon`, `🛜`
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
  - Manifest: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanvasCanon/_CURRENT/ModuleManifest.yaml`
  - Install: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanvasCanon/_CURRENT/Install.md`
  - QuickRef: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanvasCanon/_CURRENT/QuickRefCard.md`
  - MachineManual: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanvasCanon/_CURRENT/MachineManual.md`
  - UserGuide: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/CanvasCanon/_CURRENT/UserGuide.md`
- Version: `0.2.0`
- Compatibility: `Uses ModuleMill-style doc roles, ASCII-first canon commands, and fail-closed arbitration on output-shape conflicts.`

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
- Version: `0.4.1`
- Compatibility: `Uses ModuleMill-style doc roles, explicit lifecycle controls, fail-closed ledger guards, configurable triage/security policies, and emoji-first alias mapping.`

## 3) Boot contract (for BootStub consumers)
- At start of a new chat, fetch this registry and auto-load `DefaultLoad=yes` modules using Manifest + QuickRef first.
- User can opt out for the chat with: `skip modules`.
- Single-emoji module addressing is valid:
  - If a message is exactly a module emoji, treat it as module activation/invocation intent for that module.
  - If module is loaded but inactive, activate it.
  - If module is not loaded and `SingleEmojiActivate=yes`, load then activate it.
  - If multiple modules share an emoji alias, fail closed and ask user to choose.
- Fetch failure: fail closed and request pasted registry entry or required module doc.
