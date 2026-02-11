# 🪪 FaxAx QuickRefCard (derived)

ModuleID: FaxAx  
Version: 0.2.0  
DocRole: QuickRefCard  
Audience: Users (pocket cheat sheet)

---

## Core
- Scope-first answers. Depth is opt-in.
- ResponseEnvelope: `main_plus_optional_faxcluster` (or `numbered_consolidated_reply` on hold release/auto-flush).

## Lifecycle
- `fax load` (or "Enable FaxAx in this chat")
- `fax activate`
- `fax sleep`
- `fax unload` (or "Disable FaxAx in this chat")
- `fax status`

## Expand
- `📠2` / `📠 2,5,7`
- `📠 keyword`
- `📠🕵🏻‍♂️` / `📠🧪`
- “expand on X”

## SpeakerScale (verbosity)
- `🔈` light (1–2 lines)
- `🔉` default focused
- `🔊` max (on-scope)
- `🔊3` next 3 replies
- `📠🔉` latch default mode (mode only)
- Mode + expand same turn: `📠🔉 📠2,5`

## Hold / Stack comments
Trigger `🔇` only when **alone / prefix / final char**.
- ASK (Ask ChatGPT): ACK gauge only  
  `🔇 : : : : 4/12 💬`
- CHAT (presentation): 1-line reaction + optional unnumbered teaser ChipRack
- Auto-flush on #12
- Release with `🔈/🔉/🔊` or “your thoughts?”
- Cancel: `🟥 cancel`

## FaxCluster hygiene
- One `📠` in header only.
- Header must start with `📠`.
- No `📠` in chips.
- Headlines use `1:` `2:` `3:` with chip + short description (colon form).
- ChipRack uses glued indices: `4:` `5:` `6:` ...
- Every ChipRack chip has a leading emoji token.
- ChipRack chips must use unique emoji (no repeated lead emoji in one rack).
- Keep headline descriptions <= ~85 chars (target 70-85).

## FaxCluster canonical example
📠 TestMode: FaxCluster

1:`🧲showCluster`  – Force FaxCluster every reply so we can validate spacing + chip behavior.
2:`🧼hygieneCheck`  – Verify trigger-only header. Glued indices. Clean rack. No nesting weirdness.
3:`🧷chipEmoji`  – Make ChipRack read like a control panel, not a sad text-only menu.

4:`🔥stressTest`  5:`📄onePager`  6:`🌳decisionTree`  7:`🛠️toolingSketch`  8:`⚠️contextLeak`
