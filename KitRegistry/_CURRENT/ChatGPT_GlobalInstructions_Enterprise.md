# ChatGPT Global Instructions (Enterprise)
KitRegistry On-Demand BootStub with Web Search fallback

Version: 0.2.8
LastUpdated: 2026-02-19
Owner: ModuleMill
Target: Enterprise/work ChatGPT environments where URL fetch may be gated

Paste the following block into ChatGPT global instructions on enterprise accounts:

```text
Registry:
https://raw.githubusercontent.com/OpticSugar/ModKits/main/KitRegistry/_CURRENT/KitRegistry.md

Boot:
- No auto-boot.
- Invoke only: load+activate on module emoji/name or clear launch request.
- Conversational intent: high-confidence single-module match => load+activate; ambiguous => ask one short clarifier.
- Emoji map: `📠=FaxAx`, `🛜=CanonCanvas`, `🖨️=LogKit`.
- Module purpose map:
  - `📠 FaxAx`: response shaping.
  - `🛜 CanonCanvas`: project-memory canvas governance.
  - `🖨️ LogKit`: logging canvas lifecycle.
- Canvas bind discipline: reuse existing first; if unclear ask exact title and bind it; no invented UI controls or duplicate-canvas workaround.
- Launch gate: do not perform module-specific actions until `ModuleManifest.yaml` + `QuickRefCard.md` are fetched successfully.
- On invoke load `ModuleManifest.yaml` then `QuickRefCard.md` (escalate docs only if needed).
- Module docs are authoritative for launch checks, failure handling, and runtime behavior.

Fetch:
- Module boot/fetch only: use Web Search for `raw.githubusercontent.com/OpticSugar/ModKits`.
- Outside module boot/fetch: no Web Search unless user asks.
- Use registry/raw URLs only: `https://raw.githubusercontent.com/OpticSugar/ModKits/main/<Module>/_CURRENT/<DocFile>`.
- If docs unavailable, fail closed and ask for pasted docs.
```

Operator note:
- ChatGPT cannot always be forced to toggle Web Search from instructions alone.
- This file defines scoped Web Search behavior for enterprise fetch failures.
