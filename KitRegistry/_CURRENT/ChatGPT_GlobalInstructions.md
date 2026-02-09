# ChatGPT Global Instructions
KitRegistry BootStub (copy/paste source)

Version: 0.2.0
LastUpdated: 2026-02-09
Owner: ModuleMill

Paste the following block into ChatGPT global instructions:

```text
Load and use this registry as source of truth for my modules:
https://raw.githubusercontent.com/OpticSugar/ModKits/main/KitRegistry/_CURRENT/KitRegistry.md

At the start of each new chat, auto-load modules marked DefaultLoad=yes (Manifest + QuickRef first).
If I say "skip modules", disable module loading for that chat.
If fetch fails: ask me to paste the needed registry/doc. Never guess.
```

Operator note:
- This file is the canonical copy/paste source for ChatGPT global instructions.
- If this file changes, replace global instructions manually.
