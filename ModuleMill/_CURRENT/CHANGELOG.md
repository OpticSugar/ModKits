# ModuleMill Changelog

All notable changes to ModuleMill are documented in this file.

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
