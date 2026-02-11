# agents.override.md
# Repo override for Codex behavior in /Users/stu/git/ModKits

Version: 0.1.0
LastUpdated: 2026-02-11
Scope: Entire repository

Intent
- This repository is for LLM module engineering, not traditional software-only specification work.
- Treat modules as behavior scaffolding for an intelligent model, not as rigid script engines.
- Preserve assistant judgment, contextual inference, and guided improvisation inside clear guardrails.

Operating Model
- Prioritize intent + constraints + outcomes over exhaustive micrologic.
- Keep deterministic contracts explicit where needed: commands, state keys, output envelopes, safety limits.
- Keep language behavior flexible where needed: tone, phrasing, invitation copy, ordering, and presentation choices.
- Do not flatten behavior-critical style guidance into repetitive boilerplate.

Inference-First Rule
- When user input is messy, infer structure from context before asking questions.
- Convert loose "rambles" into organized outputs using best-fit interpretation.
- Ask clarifying questions only when ambiguity is material and blocks a reliable response.
- If proceeding under uncertainty, state assumptions briefly and continue.

Clarification Threshold
Ask only if at least one is true:
- Multiple plausible interpretations would produce materially different results.
- Required information is missing and cannot be inferred with acceptable confidence.
- The action is high-risk and a wrong assumption would create meaningful harm.
- Otherwise proceed with best judgment.

Module Authoring Expectations
- UserGuide is canonical module DNA: preserve rationale, tradeoffs, examples, and operating intent.
- MachineManual/QuickRef/Install are derived operational layers and must not invent new policy.
- Modules should guide model behavior, not suppress model reasoning.
- Prefer "bounded improvisation": clear invariants plus freedom inside those boundaries.

Codex Collaboration Defaults For This Repo
- Discussion requests are analysis-first: read, reason, propose, and align before implementation.
- Do not run lint, regenerate docs, or patch module files unless user explicitly asks.
- When editing module docs, preserve module identity terms and behavior-critical named features.

LogKit-Specific Interpretation Pattern (applies as a general example)
- Treat unstructured user notes as candidate log material.
- Infer likely lane/category, key entries, and normalized structure from context.
- Produce a clean structured draft directly.
- Request clarification only for genuinely ambiguous fields that change meaning.

Success Criteria
- Outputs feel like a strong human collaborator: adaptive, context-aware, and concise.
- Modules remain robust and predictable without becoming brittle or over-specified.
- User effort stays low: fewer back-and-forth clarifications for obvious context.
