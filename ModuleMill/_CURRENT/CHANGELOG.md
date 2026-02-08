# ModuleMill Changelog

All notable changes to ModuleMill are documented in this file.

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
