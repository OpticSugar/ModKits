# 📇 KitRegistry
Runtime Module Index v0.2.0

RegistryID: KitRegistry
ModuleID: KitRegistry
Version: 0.2.0
DocRole: UserGuide
Audience: Runtime assistants and module operators
Updated: 2026-02-08
Scope: Runtime ModuleKits only

## 0) Policy
- Source of truth for runtime module discovery and doc pointers.
- Registry never invents module commands.
- Module behavior authority remains in module `UserGuide` canon.
- ModuleMill is developer infrastructure and is intentionally excluded to avoid day-to-day chat noise.

## 1) Schema
Each module entry must include:
- `Module`
- `Mission`
- `🎛️ EngagePolicy` (`AUTO | OFFER | MANUAL`)
- `🧲 NeedSignals` (`Keywords`, `Intents`, optional `Formats`, optional `DoNotFireIf`)
- `AutoRunScope`
- `DefaultLoad` (`yes|no`)
- `Docs` (`Manifest`, `Install`, `QuickRef`, `MachineManual`, `UserGuide`)
- `Version`
- `Compatibility`

## 2) Modules
### Module: FaxAx
- Mission: Scope-first response protocol with opt-in depth and hold/release comment stacking.
- 🎛️ EngagePolicy: `OFFER`
- 🧲 NeedSignals:
  - Keywords: `verbosity`, `short answer`, `expand`, `hold`, `stack comments`, `ask chatgpt`, `too long`
  - Intents: `control answer depth`, `batch feedback`, `delay response until release`
  - Formats: `emoji mode switches`, `expansion chips`
  - DoNotFireIf: `user requests raw JSON only`, `another module explicitly invoked`
- AutoRunScope: `response_formatting`
- DefaultLoad: `no`
- Docs:
  - Manifest: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/ModuleManifest.yaml`
  - Install: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/Install.md`
  - QuickRef: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/QuickRefCard.md`
  - MachineManual: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/MachineManual.md`
  - UserGuide: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/FaxAx/_CURRENT/UserGuide.md`
- Version: `0.1.0`
- Compatibility: `Uses ModuleMill-style doc roles; ask user to choose on output-shape collisions.`

## 3) Boot contract (for BootStub consumers)
- After second user message in a new chat, offer once: `boot / skip`.
- `boot`: fetch this registry; load `DefaultLoad=yes` modules using Manifest + QuickRef first.
- `skip`: persist skip state for the chat.
- Fetch failure: fail closed and request pasted registry entry or required module doc.
