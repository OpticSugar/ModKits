# ChatGPT Global Instructions
KitRegistry BootStub (copy/paste source)

Version: 0.2.1
LastUpdated: 2026-02-09
Owner: ModuleMill

Paste the following block into ChatGPT global instructions:

```text
Load and use this registry as source of truth for my modules:
https://raw.githubusercontent.com/OpticSugar/ModKits/main/KitRegistry/_CURRENT/KitRegistry.md

At the start of each new chat, auto-load modules marked DefaultLoad=yes (Manifest + QuickRef first).
Treat module emoji shorthand as valid module addressing/activation commands (for example: 📠, 🛜, 🖨️).
If a message is just one module emoji, activate/invoke that module (load first if needed and allowed by registry).
If I say "skip modules", disable module loading for that chat.
If fetch fails (including cache miss): ask me to enable Web Search or paste the needed registry/doc. Never guess.
```

Operator note:
- This file is the canonical copy/paste source for ChatGPT global instructions.
- If this file changes, replace global instructions manually.
