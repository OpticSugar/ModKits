# 📚 PPP Bible
(Developer’s Guide to GPT Module Engineering) v0.001

**Mission:** standardize how we design, package, deploy, and maintain “GPT modules” (procedural prompt programs) so new chats can engineer modules reliably without re-onboarding.

## Core premise
Natural-language modules behave like software. If we want “software-like” stability, we must adopt:
- clear interfaces (triggers, inputs, outputs)
- explicit state
- safety latches
- regression tests
- versioning + derived artifacts

## The ModuleKit standard (packaging)
A module ships as a **ModuleKit** (the doc bundle). Roles must not blur:

1) **.READ_FIRST__Module_install**
   - Bootstrap ritual, enable/disable, config, dependencies, known conflicts
2) **🪪 QuickRefCard**
   - Pocket card. Minimal. Meant to stay resident.
3) **🤖 MachineManual**
   - Complete runtime runbook for assistants.
4) **👤 UserGuide**
   - Canonical dev bible: rationale, examples, history, future work.

### Non-negotiable rule
**UserGuide is canonical.** QuickRef and MachineManual are derived artifacts.
If you lose UserGuide, you lose the project’s long-term memory.

## Architecture contract (what every module MUST define)
### Surface area
- Triggers (emoji/keywords)
- Inputs (required + optional)
- Outputs (templates)
- State (where it lives + what is authoritative)

### Lifecycle (composability basics)
- Available (not loaded)
- Loaded (state exists)
- Active (allowed to operate)
- Sleeping (state exists, but suppressed)

### Conflicts + precedence
Every module must declare:
- Trigger collisions (same emoji)
- Output collisions (incompatible formats)
- State collisions (namespacing)
- Precedence rule (who wins, and when the user must choose)

### Safety latches
For any action that can cause drift/data loss:
- define preconditions (examples: “active canvas must be X”, “META header must exist”)
- if not satisfied: stop, ask, or queue
- never “best effort” when integrity matters

### Improv Zones
Improv is allowed only where explicitly fenced.
- Allowed: tone copy, fun headers, choosing among approved warning emojis, selecting optional chips
- Forbidden: inventing commands, changing templates, redefining triggers, silently changing rules

## State pattern (recommended)
- **State Block** is the source of truth (authoritative config/state)
- **HUD** is a derived display (only shown on AUTO rules; avoid fixed token tax)

## Authoring pipeline (how modules get built)
1) Capture decisions in 🛜CanvasCanon (optional but recommended)
2) Write/maintain 👤UserGuide as canonical source
3) Derive 🤖MachineManual + 🪪QuickRefCard + Install doc
4) Write regression tests (must-pass prompts)
5) Release: tag version + changelog

## Versioning
Use SemVer: MAJOR.MINOR.PATCH.
“R1/R2” is a dev sprint label only, not a version.

## Regression tests (minimum)
- Smoke: trigger → correct output shape
- Drift: repeated use across turns
- Collision: multiple modules active
- Missing state: fail closed
- Formatting: strict template compliance

## Examples (why latches matter)
- **LogKit works** because it uses a hard latch: “write only if ledger is active AND META header exists.” Otherwise it queues.
- **FaxAxe drifted** because doc roles weren’t enforced and “improv freedoms” weren’t fenced.

## v0.001 scope
This release defines the engineering blueprint and packaging contract.
It does not yet define the final universal conflict resolver (still open).
