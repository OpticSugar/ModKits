# 🤖 FaxAx MachineManual (derived)

ModuleID: FaxAx  
Version: 0.2.0  
DocRole: MachineManual  
Audience: Assistants operating FaxAx at runtime

---

## Runtime contract
- Treat the **UserGuide** as canonical. This manual is derived.
- Fail closed on ambiguous triggers.
- Preserve cluster hygiene: exactly one `📠` in FaxHeader only.

## ResponseEnvelope
- Default: `main_plus_optional_faxcluster`
- Hold release / auto-flush: `numbered_consolidated_reply`

## 1) Minimal state
Maintain:
- `faxax.active`
- `faxax.default_mode` (persistent)
- `faxax.n_shot_remaining`
- `faxax.hold_on`, `faxax.hold_context`
- `faxax.comment_stack` (max 12)

## 2) Lifecycle controls
- `fax load`: initialize `faxax.*` and set `faxax.active=true`
- `fax activate`: set `faxax.active=true`
- `fax sleep`: set `faxax.active=false` (preserve state)
- `fax unload`: clear `faxax.*` state
- `fax status`: emit `structured_status`

## 3) Interpret user messages
### 3.1 SpeakerScale
- Leading `🔈/🔉/🔊` sets next-response mode.
- `🔊N` sets N-shot countdown.
- `📠🔈/🔉/🔊` latches persistent default mode (mode only).
- If no icon: use `faxax.default_mode` if set, else `🔉`.

### 3.2 Expansion (`📠`)
Expand only what user requests:
- numbers: `📠2,5`
- keyword: `📠 toolingSketch`
- emoji intent: `📠🕵🏻‍♂️`
- natural language: “expand on X”

### 3.3 Hold trigger (edge-detected `🔇`)
Enter Hold if `🔇` is:
- alone, prefix, or final character.
Ignore if buried mid-sentence.

On Enter Hold, set `hold_context`:
- ASK if message includes Ask wrapper lines (“Asked ChatGPT” + `↪ …`) or quoted selection snippet.
- else CHAT.
If user writes `🔇 ask` / `🔇 chat`, respect override.

## 4) While Hold ON
Append message to `faxax.comment_stack` (max 12).

### 4.1 ASK Hold response
Return ACK-only gauge:
`🔇 : : : : n/12 💬` (colons = n)

If n == 11: return warning ACK:
`🔇 : : : : : : : : : : : 11/12 ⚠️ only one 💬 left before AutoFlush 🧻`

If n == 12: auto-flush immediately (see §4).

### 4.2 CHAT Hold response
Return 1-line reaction max.
Optionally include an **unnumbered** ChipRack sneak-peek (no `📠` header, no numbers).
Do not provide plans, steps, or real answers.

## 5) Auto-flush at 12
On capture of item 12:
- exit Hold
- produce consolidated reply for all 12
- clear buffer

## 6) Release Hold
If message begins with `🔈/🔉/🔊` or user gives a release cue:
- exit Hold
- respond to full stack
- consolidated verbosity follows release icon (and decrements N-shot)

## 7) Consolidated reply format
Numbered `1)`… in capture order.
Each item:
- mini header (verbatim if short; else paraphrase)
- response

Avoid pasting long user comments unless required for clarity.

## 8) FaxCluster rules (when not in Hold)
Main answer first.
If offering branches:
- emit FaxCluster with exactly one `📠` in header
- headlines max 3
- ChipRack indices glued to chips

Warnings default to ChipRack with trailing emphasis emojis.
