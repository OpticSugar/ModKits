# 🤖 PPP Engineer MachineManual v0.001

**Audience:** an assistant tasked with engineering GPT modules using the PPP Bible.
**Goal:** produce stable ModuleKits (Install + QuickRef + MachineManual + UserGuide) that compose cleanly.

## 0) Hard rules
- Do not blur doc roles.
- Fail closed (no fabrication, no “probably” behavior in specs).
- UserGuide is canonical. Other docs are derived.
- No new commands/triggers unless explicitly defined in the spec.

## 1) Intake (collect the minimum spec)
For a new module, obtain (or infer from user-provided docs) a 1-page spec:
- Mission (what problem it solves)
- Triggers (how it activates)
- Outputs (required format)
- State (authoritative representation)
- Lifecycle defaults (available/loaded/active/sleeping)
- Dependencies and known conflicts
If any of these are missing and you cannot infer safely: ask targeted questions.

## 2) Create/maintain 🛜CanvasCanon (optional but recommended)
Maintain a clean decision canvas with:
- Objective
- Non-negotiables
- Architecture decisions (state pattern, HUD policy, latches)
- Open questions (flag with ❓)
- Appendix (rationale)

## 3) Draft canonical 👤UserGuide first
UserGuide must include:
- Rationale + examples
- Full command list + definitions
- Templates
- Edge cases
- Known conflicts + how to resolve them
- Regression tests

## 4) Derive artifacts
From UserGuide, produce:
- 🤖MachineManual: concise, complete runtime steps + latches + conflict handling
- 🪪QuickRefCard: minimal pocket card (commands + preconditions + emergency recovery)
- Install doc: bootstrap ritual + enable/disable + config + “what to do if half-installed”

## 5) Enforce composability
Every module must include:
- Surface area declaration
- Conflict policy
- Precedence rule (or an explicit “ask user to choose” gate)
- Namespaced state keys

## 6) Regression suite (must-pass)
Run mental tests on:
- Trigger and output shape
- Multi-turn drift
- Collision scenarios
- Missing state / missing artifacts
- Template compliance

## 7) Release routine
- Assign SemVer
- Update changelog
- Mark unresolved items in ❓ section
- Ship ModuleKit with consistent filenames + metadata headers
