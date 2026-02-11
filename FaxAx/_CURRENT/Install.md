# .READ_FIRST__FaxAx_install (derived)

ModuleID: FaxAx  
Version: 0.2.0  
DocRole: Install  
Audience: Users + assistants (bootstrap + recovery)

---

## 1) Enable / disable
Say one of:
- “Enable FaxAx in this chat.”
- “Disable FaxAx in this chat.”
- “Sleep FaxAx for now.” (state kept, behavior suppressed)

ASCII canon equivalents:
- `fax load`
- `fax activate`
- `fax sleep`
- `fax unload`
- `fax status`

## 2) Default behavior once enabled
- Scope-first answers.
- Offer opt-in expansions via FaxCluster when useful.

## 3) Configure verbosity
- One-shot: start message with `🔈/🔉/🔊`
- N-shot: `🔊3`
- Persistent: `📠🔉` (mode only)

## 4) Use Hold (batch comments)
- Start: `🔇` (alone/prefix/final char)
- Keep sending comments.
- Auto-flush on #12.
- Release: `🔈/🔉/🔊` or “your thoughts?”
- Cancel: `🟥 cancel`

## 5) Known collisions
- If another module demands a conflicting output format, FaxAx should ask you to choose.

## 6) If it feels half-installed
Symptoms: clusters not appearing, hold not behaving, modes ignored.
Recovery:
1) Say “Disable FaxAx” then “Enable FaxAx” (reset state).
2) If still weird, request the QuickRefCard and re-lint the kit.

## 7) Regression quick-check
Run these prompts:
- “Explain a compiler.” → concise main answer + optional cluster
- `📠2` → expands item 2
- `📠🔊` → latches loud mode
- `🔇` + 3 notes + `🔉` → consolidated reply
- “Show a canonical FaxCluster example.” → includes:
  - one `📠` header line
  - header starts with `📠`
  - `1.`..`3.` headlines (chip + short description)
  - ChipRack with glued indices (`4:`...)
  - every ChipRack chip has a leading emoji token
  - ChipRack chips with unique emoji (no duplicates)
