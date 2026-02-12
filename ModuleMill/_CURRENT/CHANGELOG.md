# ModuleMill Changelog

All notable changes to ModuleMill are documented in this file.

## [0.7.0] - 2026-02-12
### Added
- Natural-language command-intent contract in ModuleMill framework canon:
  - New required `ModuleManifest.intent_policy` key with allowed values:
    - `explicit_only`
    - `infer_high_confidence`
  - Runtime policy now requires:
    - high-confidence natural-language command intent -> execute mapped canon command
    - low-confidence or ambiguous intent -> ask one short clarification
- Compiler manifest lint validation for `intent_policy` values.
- Advisory compiler parity check:
  - warns when `intent_policy=infer_high_confidence` but canonical `UserGuide` lacks natural-language intent/confidence signals.
- Failure-mode hardening in framework docs for missing remote docs:
  - explicitly instruct enable-Web-Search retry first
  - then provide copy/paste-ready URL block request
  - never claim module-compliant execution when docs are unavailable

### Changed
- `ModuleMill_DevGuide.md` and `ModuleMill_MachineManual.md` upgraded to `v0.7.0` with inference-first command handling and stronger fail-closed transport guidance.
- Runtime manifests for `FaxAx`, `CanonCanvas`, and `LogKit` now declare `intent_policy: "infer_high_confidence"`.
- `ModuleMill` `ModuleManifest` template updated to include `intent_policy`.

## [0.6.0] - 2026-02-11
### Added
- Origin and intent canon in ModuleMill DevGuide:
  - Modules are documented as "skills for regular ChatGPT."
  - ModuleMill mission now explicitly frames anti-neutering protection for authored module behavior.
- Codex skill sync contract in DevGuide:
  - ModuleMill is authored in Git but operationally executed through the installed Codex skill.
  - Every ModuleMill change must include exact skill update and verification commands.
  - Assistants must not claim updates are active in Codex when skill files are stale.
- Conflict-resolution documentation duty in DevGuide for policy disputes and behavior-preservation decisions.
- Protected feature-name contract in ModuleMill canon:
  - Any `Emoji + PascalCaseName` token is an official non-prunable mechanism.
  - These names must be preserved verbatim and represented in `must_preserve` (and `must_preserve_runtime` when runtime-critical).
  - Strict compiler lint enforces `EmojiGlossary` -> `must_preserve` anti-drift coverage for these tokens.
- Emoji drift-prevention lint gates:
  - Strict lint now fails on inline-code spans that start with variation-selector bytes (`\ufe0e`/`\ufe0f`) because this indicates a dropped emoji base token.
  - Strict lint now enforces UserGuide command-alias emoji parity in `MachineManual` and `QuickRefCard`.

### Changed
- UserGuide preservation law hardened in framework canon:
  - Canonical UserGuide is defined as maximal module DNA/blueprint.
  - Heavy compression/cleanup of canonical UserGuide is forbidden unless functionality intentionally changes.
- ModuleMill MachineManual enforcement updated:
  - Explicitly prohibits trimming templates/scenarios/rationale from canonical UserGuide without explicit functional-change approval.
  - Release routine now requires mandatory skill-sync handoff when framework artifacts change.

## [0.5.0] - 2026-02-10
### Added
- Anti-neutering invariant contract for runtime modules:
  - New required `ModuleManifest.must_preserve` list.
  - Compiler strict lint now fails when `must_preserve` invariants are missing from canonical `UserGuide`.
- Compiler strict parity checks between canonical and derived runtime docs:
  - namespaced state keys declared in `UserGuide` must appear in `MachineManual`
  - lifecycle canonical commands from `UserGuide` must appear in `MachineManual`
  - QuickRef lifecycle gaps are reported as warnings

### Changed
- ModuleManifest template now includes `must_preserve`.
- Runtime manifests for `CanonCanvas`, `FaxAx`, and `LogKit` now declare module-specific `must_preserve` invariants.
- ModuleMill DevGuide and MachineManual now explicitly treat `must_preserve` as a non-negotiable anti-compression guard.

## [0.4.4] - 2026-02-09
### Added
- Emoji-first module addressing is now mandatory in KitRegistry:
  - `ModuleEmoji`
  - `ModuleAliases`
  - `SingleEmojiActivate`
- Single-emoji activation semantics added to boot contract (for example `📠`, `🛜`, `🖨️`).
- ModuleManifest template and compiler checks expanded for emoji module identity fields:
  - `module_emoji`
  - `module_aliases`
  - `single_emoji_activate`

### Changed
- `FaxAx`, `CanonCanvas`, and `LogKit` manifests now include module emoji identity and alias lists.
- Global instruction blocks now explicitly support single-emoji module activation/invocation.

## [0.4.3] - 2026-02-09
### Added
- Enterprise bootstrap instructions file:
  - `KitRegistry/_CURRENT/ChatGPT_GlobalInstructions_Enterprise.md`
  - Includes explicit Web Search fallback guidance for work accounts where direct URL fetch can fail with cache miss.

### Changed
- Standard bootstrap instructions now explicitly handle cache-miss/blocked fetch by asking for Web Search enablement or pasted docs.
- Framework deployment docs now formalize transport fallback:
  - URL fetch preferred
  - Web Search fallback in enterprise environments
  - fail-closed pasted-doc fallback

## [0.4.2] - 2026-02-09
### Changed
- Boot behavior switched to default-on loading:
  - Chat bootstrap now auto-loads `DefaultLoad=yes` modules at chat start.
  - Explicit prompt flow `boot / skip` removed from canonical global instructions.
  - Chat-level opt-out command is now `skip modules`.
- `FaxAx` is now configured for default runtime load:
  - `KitRegistry`: `DefaultLoad=yes`, `EngagePolicy=AUTO`
  - `FaxAx ModuleManifest`: `engage_policy: AUTO`

## [0.4.1] - 2026-02-09
### Added
- `KitRegistry/_CURRENT/ChatGPT_GlobalInstructions.md` as the canonical copy/paste source for ChatGPT global instructions.
- Compiler lint flag `--modulekit-only` to scope strict scans to canonical ModuleKit artifacts in `_CURRENT`.

### Changed
- Framework docs now require manual global-instructions replacement when `ChatGPT_GlobalInstructions.md` changes.
- Strict scan guidance now prefers `lint --strict --modulekit-only` for repo-wide checks.

### Removed
- Obsolete `FaxAx/_CURRENT/Personalization_SML.md`.

## [0.4.0] - 2026-02-09
### Added
- UserGuide completeness lint checks for runtime modules:
  - context/mission depth
  - rationale/why
  - failure behavior
  - examples/template coverage
  - EmojiGlossary integrity checks when emoji aliases are used
- UserGuide over-compression heuristics:
  - non-empty line minimum
  - heading count minimum
  - strict mode escalates these findings to hard errors

### Changed
- Framework policy now explicitly requires verbose canonical UserGuides with preserved context, rationale, tradeoffs, failure modes, examples, and migration notes.
- Role intent clarified:
  - `UserGuide` = most detailed source of truth
  - `MachineManual` = executable runtime rules
  - `QuickRefCard` = compact operational reference
  - `Install` = deployment/runbook only
- Emoji alias policy hardened:
  - emoji aliases are first-class input forms when declared
  - alias mappings must remain deterministic in docs
- `LogKit` and `FaxAx` UserGuides patched with explicit rationale/failure/examples sections to align with strict completeness checks.

## [0.3.0] - 2026-02-08
### Added
- New `ModuleManifest` contract in framework canon for trigger metadata and fail-closed gating.
- New template: `ModuleMill/_CURRENT/templates/ModuleManifest.yaml`.
- `FaxAx/_CURRENT/ModuleManifest.yaml` as first runtime manifest implementation.
- Compiler lint checks for `ModuleManifest.yaml` schema and doc-pointer validation.
- Explicit bundle policy: `_BUNDLE.md` files are optional troubleshooting artifacts and are not part of normal ModuleMill authoring or release workflow.

### Changed
- `ModuleMill_DevGuide.md` updated with staged progressive-disclosure loading policy:
  - Registry + Manifest for selection
  - QuickRef for low-cost runtime behavior
  - MachineManual for execution hardening
  - UserGuide for canon disputes and authoring
- `ModuleMill_MachineManual.md` updated with manifest-first intake and enforcement workflow.
- `ModuleMill_Compiler.py` upgraded to v0.3:
  - Adds lint warnings/errors for missing runtime manifests
  - Adds constrained manifest parser and `docs` pointer cross-checks
  - Adds optional `--require-manifest` lint gate
- `KitRegistry/_CURRENT/KitRegistry.md` schema now includes `Docs.Manifest` and boot guidance uses Manifest + QuickRef first.

## [0.2.0] - 2026-02-08
### Added
- New canonical framework docs under `ModuleMill/_CURRENT/`:
  - `ModuleMill_DevGuide.md`
  - `ModuleMill_MachineManual.md`
  - `ModuleMill_Compiler.py`
- Deployment standard for remote registry boot via `KitRegistry`.
- Explicit interface standards:
  - ASCII-first canonical command forms
  - Emoji aliases as optional forms
  - Required `EmojiGlossary` for user-facing modules that use emoji aliases
- Lint rule in compiler to enforce `EmojiGlossary` presence for emoji-using module UserGuides.

### Changed
- Rebrand from `PPP` to `ModuleMill` across framework canon.
- Registry/index strategy changed from `ModuleKit_Index.md` to `KitRegistry/_CURRENT/KitRegistry.md`.
- FaxAx UserGuide aligned with ModuleMill state-key namespacing and glossary requirements.
- Naming convention clarified: runtime module docs use role-based unprefixed filenames inside each module `_CURRENT` directory.

### Removed
- `PPP/` namespace and files.
- `ModuleKit_Index.md` at repository root.
