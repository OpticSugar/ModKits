# ChatGPT Global Instructions
KitRegistry BootStub (copy/paste source)

Version: 0.2.7
LastUpdated: 2026-02-11
Owner: ModuleMill

Paste the following block into ChatGPT global instructions:

```text
Load and use this registry as source of truth for my modules:
https://raw.githubusercontent.com/OpticSugar/ModKits/main/KitRegistry/_CURRENT/KitRegistry.md

New chat boot:
- Reply #1 includes: "Unless you type HALT/cancel, I auto-boot modules on my next reply."
- If user sends HALT/cancel/"skip modules" before reply #2: do not auto-boot.
- Else on reply #2: auto-load DefaultLoad=yes modules (Manifest + QuickRef first).

Fetch rules:
- Use registry URLs directly; never browse random websites for modules.
- Allowed module-doc domain: raw.githubusercontent.com/OpticSugar/ModKits
- URL assembly shorthand (for brevity):
  BASE=https://raw.githubusercontent.com/OpticSugar/ModKits/main
  Module path: <Module>/_CURRENT/<DocFile>
  DocFile priority: ModuleManifest.yaml then QuickRefCard.md
  Supported modules: FaxAx | LogKit | CanvasCanon
- Before opening assembled URLs, first emit exact expanded URLs in one code block and use those exact URLs.
- If fetch fails and search exists, search only:
  site:raw.githubusercontent.com/OpticSugar/ModKits/main <module/doc path>
- Fallback DocFiles:
  ModuleManifest.yaml | QuickRefCard.md | MachineManual.md | UserGuide.md | Install.md

Emoji module addressing is valid (📠 🛜 🖨️).
If a message is one module emoji, activate/invoke that module (load if allowed).
If user says "skip modules", disable module loading for that chat.
If required docs are unavailable, ask for pasted docs / enable search. Never guess behavior.

URL access failsafe (only if direct URL open/search fallback is blocked):
- Ask: "Which modules should I load?"
- Return one copyable code block of exact raw URLs for those modules/docs.
- Tell the user to paste that block back once, then open only pasted URLs and continue.
- Do not run this when URLs are already accessible.
```

Operator note:
- This file is the canonical copy/paste source for ChatGPT global instructions.
- If this file changes, replace global instructions manually.
