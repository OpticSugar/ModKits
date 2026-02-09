# ModuleMill Changelog

All notable changes to ModuleMill are documented in this file.

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
- `FaxAx`, `CanvasCanon`, and `LogKit` manifests now include module emoji identity and alias lists.
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
