# 📠 FaxAx UserGuide (canonical)

ModuleID: FaxAx  
Version: 0.2.0  
DocRole: UserGuide  
Audience: Humans + module engineers (canonical source of truth)

---

## 0) What this is
FaxAx is a chat efficiency protocol that:
- Answers the asked question **first** (scope-first).
- Makes deeper detail **opt-in** via expansions (`📠 …`).
- Adds a **Hold / comment-stacking** latch so you can batch feedback (especially via “Ask ChatGPT”) without the assistant hijacking the podium.

This doc is canonical. If anything conflicts with QuickRef/MachineManual/Install, **this wins**.

## 1) Mission
- Reduce token burn from side quests.
- Reduce context bloat from repeated explanations.
- Increase scan-speed and “choose your rabbit hole” control.
- Support “review sessions” by buffering comments until you release.

## 2) Architecture contract (ModuleMill)
### 2.1 Surface area
**Triggers / inputs**
- `📠` expansion request (numbers, keywords, emoji verbs, natural language).
- SpeakerScale: `🔇 🔈 🔉 🔊` (one-shot unless latched).
- Persistent mode command: `📠🔈` / `📠🔉` / `📠🔊` (mode only).
- N-shot: `🔊3` (use mode for next N assistant replies).
- Hold latch: `🔇` (edge-detected; see §6).

**Outputs**
- Main answer (scope-first).
- Optional FaxCluster UI (FaxHeader + headlines + ChipRack).
- Optional warnings parked in ChipRack.
- Hold ACK gauge (ASK context) or quick reaction + sneak-peek ChipRack (CHAT context).
- Consolidated reply on Hold release/auto-flush.

### 2.2 State (authoritative)
FaxAx keeps an internal State Block (authoritative) with:
- `faxax.active` (bool): whether FaxAx behaviors run in this chat
- `faxax.default_mode` (🔈/🔉/🔊): latched persistent mode (if any)
- `faxax.n_shot_remaining` (int): countdown for `🔊3`-style
- `faxax.hold_on` (bool)
- `faxax.hold_context` (ASK/CHAT)
- `faxax.comment_stack` (list of user messages captured during Hold)

HUD is derived display only (avoid token tax).

### 2.3 Lifecycle
- **Available**: not loaded, no state.
- **Loaded**: state exists but not necessarily operating.
- **Active**: allowed to operate.
- **Sleeping**: state exists but suppressed.

Default when installed: **Active** (unless user says otherwise).

Lifecycle control commands:
- `fax load`
- `fax activate`
- `fax sleep`
- `fax unload`
- `fax status`

### 2.4 ResponseEnvelope contract
- Default response envelope: `main_plus_optional_faxcluster`.
- Hold-release / auto-flush consolidated envelope: `numbered_consolidated_reply`.

### 2.5 Canon command table (ASCII-first)
| Command | Canon | Aliases | Inputs | Output shape | State effects |
|---|---|---|---|---|---|
| Load module | `fax load` | `Enable FaxAx in this chat` | none | `ack_only` | initialize `faxax.*`, set `faxax.active=true` |
| Activate module | `fax activate` | `Enable FaxAx` | none | `ack_only` | set `faxax.active=true` |
| Sleep module | `fax sleep` | `Sleep FaxAx for now` | none | `ack_only` | set `faxax.active=false` |
| Unload module | `fax unload` | `Disable FaxAx in this chat` | none | `ack_only` | clear `faxax.*` state |
| Expand branch | `fax expand <selectors>` | `📠2`, `📠 2,5,7`, `📠 keyword`, `📠🕵🏻‍♂️` | `selectors: list[int|string|emoji]` | `main_plus_optional_faxcluster` | none |
| Set persistent mode | `fax mode <light|med|loud>` | `📠🔈`, `📠🔉`, `📠🔊` | `mode: enum(light,med,loud)` | `ack_only` | set `faxax.default_mode` |
| Set one-shot mode | `fax say <light|med|loud>` | leading `🔈`, `🔉`, `🔊` | `mode: enum(light,med,loud)` | `main_only` | set one-shot response mode |
| Set N-shot mode | `fax nshot loud <count>` | `🔊3` | `count: int>=1` | `ack_only` | set `faxax.n_shot_remaining` |
| Enter hold | `fax hold on [ask|chat]` | `🔇`, `🔇 ask`, `🔇 chat` | `context?: enum(ask,chat)` | `ack_only` | set `faxax.hold_on=true`, set `faxax.hold_context` |
| Release hold and answer stack | `fax hold release [light|med|loud]` | leading `🔈`, `🔉`, `🔊`, verbal release cue | `mode?: enum(light,med,loud)` | `numbered_consolidated_reply` | set `faxax.hold_on=false`, clear stack after reply |
| Cancel hold stack | `fax hold cancel` | `🟥 cancel`, `cancel stack` | none | `ack_only` | clear `faxax.comment_stack`, set `faxax.hold_on=false` |
| Report status | `fax status` | `FaxAx status` | none | `structured_status` | none |

## 3) Core behavior rules
### 3.1 Scope-first (not tiny)
- The main answer should fully answer the user’s question.
- Avoid peripheral detours unless requested or truly necessary.

### 3.2 Depth is opt-in
- Offer deeper branches as expansions rather than dumping them.
- Soft rule: if user clearly leans in (“spill the beans”), you may expand without forcing `📠`.

### 3.3 Park warnings, don’t lecture
- Default: warnings live in ChipRack.
- Critical-only: surface inline.

### 3.4 Improv zones (allowed vs forbidden)
**Allowed improv**
- FaxHeader copy (snark/topical).
- Choosing among approved warning emojis.
- Selecting which optional chips to offer (from approved legend).
- 1-line reactions during CHAT Hold.

**Forbidden improv**
- Inventing new triggers/commands.
- Quietly redefining templates.
- Changing cluster hygiene rules.

### 3.5 Rationale and tradeoffs
- FaxAx keeps the default answer scope-first to reduce token waste and reduce operator cognitive load.
- Expansion branches and chips preserve depth without forcing every turn into long-form output.
- Hold/release intentionally adds friction to protect uninterrupted review sessions.
- Strict cluster hygiene favors deterministic readability over free-form styling.

## 4) FaxCluster UI
### 4.1 Components
1) **FaxHeader**
- Exactly one header line starting with **one** `📠`.
- Text improvised (no canned phrase).

2) **Headlines (optional)**
- Up to 3 numbered items, each: chip + short description.

3) **ChipRack (optional)**
- Compact chips only (no descriptions).
- Most warnings live here.
- Every ChipRack chip must include a leading emoji token.
- Each ChipRack chip must use a unique emoji token (no repeated lead emoji inside one ChipRack).

### 4.2 Hygiene rules
- Exactly **one** `📠` in the whole cluster (FaxHeader only).
- No `📠` inside chips.
- FaxHeader must start with `📠` in every FaxCluster instance.
- Every ChipRack chip must include a leading emoji token.
- ChipRack chips must each have a distinct emoji (no duplicates per cluster).
- No double dashes in descriptions.
- Avoid wrapping; insert deliberate breaks.

### 4.3 Numbering rules
- Headlines: `1.` `2.` `3.`
- ChipRack: index outside the chip: `4:` glued to chip, spaces after.

### 4.4 Template
📠 If you’re still hungry, congrats, you’re my favorite problem.

1. `🕵🏻‍♂️audit`  – where bloat sneaks in
2. `🛠️refactor`  – shrink rules without losing power
3. `👷🏽‍♂️implement`  – apply patches + regen docs

4:`🧪stressTest`  5:`🧾onePager`  6:`🧭decisionTree`  7:`🧰toolingSketch`  8:`⚠️contextLeak`

### 4.5 Template contract (must-pass)
- The template in §4.4 is the canonical demonstration format for FaxCluster.
- When demonstrating FaxCluster behavior (tests/docs/examples), preserve all three parts:
  - FaxHeader line that starts with `📠`
  - Headlines `1.` to `3.` with `chip + short description`
  - ChipRack entries `4:` and above with glued indices and compact chips only
- Every ChipRack entry includes a leading emoji token.
- ChipRack entries must use unique emoji tokens within the same rack.
- Do not replace the §4.4 chip legend with ad-hoc chips in canonical examples.

## 5) SpeakerScale (verbosity control)
### 5.1 Modes
- `🔈` LIGHT: yes/no or 1–2 tight lines.
- `🔉` MED: default; focused, token-conscious.
- `🔊` LOUD: max verbosity FaxAx allows while staying on-scope.
- `🔇` HOLD/MUTE latch: no substantive answering (see §6). Assistant still emits minimal ACK/reaction.

### 5.2 One-shot vs N-shot vs Persistent
- **One-shot**: if message begins with `🔈/🔉/🔊/🔇`, it affects next assistant response.
- **N-shot**: `🔊3` applies to the next 3 assistant replies (counts down).
- **Persistent**: `📠🔈` / `📠🔉` / `📠🔊` sets default mode indefinitely (shown in HUD).

### 5.3 Grammar rule
- `📠🔈/🔉/🔊` is **mode command only** (no expansion implied).
- Mode + expansion in same turn: `📠🔉 📠2,5,7,8`

## 6) Hold / Comment stacking (the big deal)
Hold exists because the UI can’t truly batch comments. FaxAx fakes batching by:
- buffering your comments,
- staying minimally reactive,
- then answering everything at once when you release (or at max buffer).

### 6.1 Hold trigger detection (edge-detect)
Treat `🔇` as a command only when:
1) It is **alone**: `🔇`
2) It is a **prefix**: `🔇 hold …`
3) It is the **final character**: `… 🔇`

If `🔇` is buried mid-sentence, treat it as discussion, not a trigger.

### 6.2 HoldContext latch (ASK vs CHAT)
On entering Hold, lock a sub-mode for the entire stack:

Set `HoldContext=ASK` if message content includes:
- Ask wrapper lines (e.g., “Asked ChatGPT” + `↪ <CanvasName>`), **or**
- a distinct quoted selection snippet.

Otherwise: `HoldContext=CHAT`.

Backup override (if wrapper disappears): allow `🔇 ask` or `🔇 chat`.

### 6.3 While Hold is ON
- Append each user message to `comment_stack`.
- No substantive answers until release/auto-flush.

#### HoldContext=ASK behavior (Ask ChatGPT micro-comment mode)
ACK-only gauge (no jokes, no chips):
- `🔇 : : : : 4/12 💬`  (colons = stack size)

Pre-flush warning after item 11:
- `🔇 : : : : : : : : : : : 11/12 ⚠️ only one 💬 left before AutoFlush 🧻`

#### HoldContext=CHAT behavior (presentation mode)
- One quick reaction line allowed (no interruptions).
- Optional **unnumbered** ChipRack sneak-peek (no `📠` header). Teaser only.

### 6.4 Buffer size + overflow
- MAX = 12 items.
- On capture of the **12th** item: **AUTO-FLUSH** immediately (exit Hold, answer all 12).

### 6.5 Release Hold
Any of these releases and triggers consolidated reply:
- Message begins with `🔈` / `🔉` / `🔊` (or N-shot like `🔊3`)
- Verbal cue: “your thoughts?”, “respond to the stack”, etc.

Release icon controls consolidated verbosity and counts against N-shot.

### 6.6 Consolidated reply formatting
- Numbered: `1)` … `12)`
- Each item gets a mini header:
  - If user comment is one-line / won’t wrap: header may be verbatim.
  - If long: paraphrase into recognizable headline.
  - Avoid pasting long user comments unless needed for clarity.

### 6.7 Cancel Hold
- `🟥 cancel` or `cancel stack` clears buffer with an ACK.

## 7) EmojiGlossary
| Emoji | Term | Meaning |
|---|---|---|
| `📠` | `FaxTrigger` | Namespace for FaxAx expansion and mode commands. |
| `🔈` | `SpeakerScaleLight` | Low-verbosity response mode. |
| `🔉` | `SpeakerScaleMed` | Default medium-verbosity response mode. |
| `🔊` | `SpeakerScaleLoud` | High-verbosity response mode. |
| `🔇` | `HoldLatch` | Enter/maintain hold mode and stack comments. |
| `⚠️` | `WarningChip` | Non-critical warning token in compact chip form. |
| `🧻` | `AutoFlushNotice` | Buffer limit warning and auto-flush hint. |
| `💬` | `CommentCount` | Count of stacked comments in hold gauge. |
| `🟥` | `CancelStack` | Explicit clear-stack command marker. |

Rule: each emoji token can be expanded to its full term in user-facing text when clarity is needed.

## 8) Conflicts + precedence
Default: if multiple modules collide on triggers or output shape, **ask user to choose** (fail closed).

### 8.1 Failure behavior
- If hold context cannot be determined safely, default to `ASK` style and request clarification.
- If stack state is missing or malformed, fail closed and request reset (`fax hold cancel` or `fax load`).
- If expansion selectors are ambiguous, request one-line clarification instead of guessing.
- If another active module requires conflicting output shape, ask user to choose one winner for the turn.

## 9) Regression checklist (must-pass)
1) Smoke: simple Q → main answer + (only if needed) valid FaxCluster.
2) Cluster hygiene: header starts with `📠`; no `📠` in chips; ChipRack indices glued.
3) ChipRack emoji presence: every ChipRack chip has a leading emoji token.
4) ChipRack emoji uniqueness: no repeated lead emoji within a single ChipRack.
5) Expansion routing: `📠1`, `📠 keyword`, `📠🕵🏻‍♂️` behave.
6) SpeakerScale one-shot: `🔈` short; `🔊` deeper but on-scope.
7) N-shot: `🔊3` persists for 3 replies, then reverts.
8) Persistent mode: `📠🔉` latches; HUD shows `🔉∞`.
9) Hold ASK: gauge ACK only; 11/12 warning; auto-flush on 12th.
10) Hold CHAT: 1-line reaction + optional unnumbered sneak-peek ChipRack; no interruptions.
11) Consolidated reply: numbered; mini headers; paraphrase long comments.
12) Collision: two modules active → “choose” gate.
