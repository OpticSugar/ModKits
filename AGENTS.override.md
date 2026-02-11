# AGENTS.override.md
# Repo override for Codex behavior in ModKits

Version: 0.2.0
LastUpdated: 2026-02-11
Scope: Entire repository

## Intent
- This repository is for LLM module engineering (prompt programs), not conventional software-only specification work.
- Treat modules as behavior scaffolding for an intelligent model, not rigid script engines.
- Preserve assistant judgment, contextual inference, and guided improvisation inside clear guardrails.

## HARD PRESERVATION RULES (default)
- Emojis are **syntax tokens / command handles / reference anchors**. Never remove, replace, rename, or “simplify” emojis.
- Unicode is **allowed and expected**. Do not convert content to ASCII-only.
- UserGuide is canonical module DNA: preserve context, rationale, tradeoffs, examples, operating intent, and voice.
- Never delete “improvisation slots” or intentionally open-ended sections. Preserve them verbatim unless asked.

## Operating model
- Prioritize intent + constraints + outcomes over exhaustive micrologic.
- Keep deterministic contracts explicit where needed: commands, state keys, output envelopes, safety limits.
- Keep language behavior flexible where needed: tone, phrasing, invitation copy, ordering, and presentation choices.
- Do not flatten behavior-critical style guidance into repetitive boilerplate.

## Inference-first rule (with a guardrail)
- When user input is messy, infer structure from context before asking questions.
- Ask clarifying questions only when ambiguity is material and blocks a reliable response.
- If proceeding under uncertainty, state assumptions briefly and continue.
- Never “resolve” or remove intentional ambiguity in module design docs.

## Clarification threshold
Ask only if at least one is true:
- Multiple plausible interpretations would produce materially different results.
- Required information is missing and cannot be inferred with acceptable confidence.
- The action is high-risk and a wrong assumption would create meaningful harm.

## Collaboration defaults
- Do not run lint, regenerate docs, or patch module files unless user explicitly asks.
- When editing module docs, preserve module identity terms and behavior-critical named features.
- If you think something should be removed/shortened: propose an optional diff and ask before applying.

## Quality control (treat modules like software)
- Maintain a small “golden prompts” regression set per module (emoji retention, formatting, tone, fail-closed behavior).
- Any prompt/module change should be checked against that set to detect regressions.
