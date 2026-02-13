#!/usr/bin/env python3
"""
ModuleMill Compiler v0.7.2
- lint: validate metadata, role hygiene, and ModuleManifest contract checks
- extract: print a requested section by heading
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

DOC_ROLES = {"Install", "QuickRefCard", "MachineManual", "UserGuide"}
FRAMEWORK_MODULE_IDS = {"ModuleMill", "KitRegistry"}
ENGAGE_POLICIES = {"AUTO", "OFFER", "MANUAL"}
INTENT_POLICIES = {"explicit_only", "infer_high_confidence"}
GLOBAL_INSTRUCTION_FILENAMES = {
    "ChatGPT_GlobalInstructions.md",
    "ChatGPT_GlobalInstructions_Enterprise.md",
}
CHATGPT_CUSTOM_INSTRUCTIONS_MAX_CHARS = 1500
GLOBAL_INSTRUCTION_RESERVED_PERSONALIZATION_CHARS = 100
GLOBAL_INSTRUCTION_CODEBLOCK_MAX_CHARS = (
    CHATGPT_CUSTOM_INSTRUCTIONS_MAX_CHARS - GLOBAL_INSTRUCTION_RESERVED_PERSONALIZATION_CHARS
)
GLOBAL_INSTRUCTION_CODEBLOCK_SOFT_TARGET = 1350
REQUIRED_MANIFEST_KEYS = {
    "module",
    "module_emoji",
    "module_aliases",
    "version",
    "mission",
    "must_preserve",
    "engage_policy",
    "intent_policy",
    "single_emoji_activate",
    "use_when",
    "do_not_use_when",
    "required_inputs",
    "response_envelope",
    "failure_mode",
    "docs",
}
REQUIRED_MANIFEST_DOC_KEYS = {"install", "quickref", "machinemanual", "userguide"}
REQUIRED_COMMAND_MARKERS = {"Command", "Canon", "Aliases", "Inputs", "Output shape", "State effects"}
CANONICAL_MODULEKIT_DOC_FILENAMES = {"Install.md", "QuickRefCard.md", "MachineManual.md", "UserGuide.md"}
REQUIRED_USERGUIDE_SECTION_GROUPS = {
    "context/mission depth": {"what this is", "mission", "scope", "context"},
    "rationale/why": {"rationale", "why", "tradeoff", "trade-off"},
    "failure behavior": {"failure behavior", "fail-closed", "fail closed", "guardrail", "error"},
    "examples": {"example", "template", "sample", "walkthrough"},
}
USERGUIDE_MIN_NONEMPTY_LINES = 120
USERGUIDE_MIN_HEADINGS = 8
LIFECYCLE_VERBS = ("load", "activate", "sleep", "unload", "status")
STATE_KEY_RE = re.compile(r"`([a-z][a-z0-9_]*\.[a-z0-9_.]+)`")

META_PATTERNS = {
    "ModuleID": re.compile(r"\bModuleID\s*[:=]\s*(\S+)", re.IGNORECASE),
    "Version": re.compile(r"\bVersion\s*[:=]\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    "DocRole": re.compile(r"\bDocRole\s*[:=]\s*(\w+)", re.IGNORECASE),
    "Audience": re.compile(r"\bAudience\s*[:=]\s*(.+)", re.IGNORECASE),
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
EMOJI_RE = re.compile(r"[\u2600-\u27bf\U0001F300-\U0001FAFF]")
VARIATION_SELECTOR_RE = re.compile(r"[\ufe0e\ufe0f]")
PASCAL_CASE_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
INTENT_SIGNAL_KEYWORDS = {
    "natural-language intent handling": {"natural-language", "natural language", "intent inference", "inferred"},
    "confidence gating": {"high confidence", "low confidence", "clarif"},
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_meta(text: str, scan_lines: int = 40) -> Dict[str, str]:
    lines = text.splitlines()[:scan_lines]
    blob = "\n".join(lines)
    meta: Dict[str, str] = {}
    for key, pat in META_PATTERNS.items():
        m = pat.search(blob)
        if m:
            meta[key] = m.group(1).strip()
    return meta


def strip_inline_comment(raw: str) -> str:
    """
    Remove trailing comments for simple YAML-like lines while preserving # inside quotes.
    """
    in_single = False
    in_double = False
    out: List[str] = []
    for ch in raw:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            break
        out.append(ch)
    return "".join(out).rstrip()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].strip()
    return value


def parse_inline_list(value: str) -> List[str]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [unquote(x.strip()) for x in inner.split(",") if x.strip()]


def parse_manifest(text: str) -> Dict[str, object]:
    """
    Parse a constrained YAML subset used by ModuleManifest.yaml.
    Supports:
    - key: scalar
    - key: [a, b]
    - key:\n    - item
    - docs:\n  subkey: value
    """
    manifest: Dict[str, object] = {}
    list_key = ""
    in_docs = False

    for raw in text.splitlines():
        line = strip_inline_comment(raw)
        if not line.strip():
            continue

        if line.startswith("  - "):
            if list_key:
                cast_list = manifest.setdefault(list_key, [])
                if isinstance(cast_list, list):
                    cast_list.append(unquote(line[4:]))
            continue

        if line.startswith("  "):
            if in_docs and ":" in line.strip():
                subkey, subval = line.strip().split(":", 1)
                docs = manifest.setdefault("docs", {})
                if isinstance(docs, dict):
                    docs[subkey.strip()] = unquote(subval.strip())
            continue

        list_key = ""
        in_docs = False

        if ":" not in line:
            continue

        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()

        if key in {
            "module_aliases",
            "use_when",
            "do_not_use_when",
            "required_inputs",
            "must_preserve",
            "must_preserve_runtime",
        }:
            inline_items = parse_inline_list(val)
            if inline_items:
                manifest[key] = inline_items
            else:
                manifest[key] = []
                list_key = key
            continue

        if key == "docs":
            manifest[key] = {}
            in_docs = True
            continue

        manifest[key] = unquote(val)

    return manifest


def route_issue(msg: str, strict: bool, errs: List[str], warns: List[str]) -> None:
    if strict:
        errs.append(msg)
    else:
        warns.append(msg)


def heading_titles_lower(text: str) -> List[str]:
    return [title.lower() for _, title, _ in build_heading_index(text)]


def find_heading_section_lines(text: str, needle: str) -> List[str]:
    lines = text.splitlines()
    headings = build_heading_index(text)
    match = None
    for level, title, li in headings:
        if needle.lower() in title.lower():
            match = (level, li)
            break
    if not match:
        return []

    level, start = match
    end = len(lines)
    for lvl, _, li in headings:
        if li > start and lvl <= level:
            end = li
            break
    return lines[start:end]


def normalize_emoji_tokens(raw: str) -> str:
    # Ignore text/emoji variation selectors so aliases like `🖨️` and `🖨`
    # are treated as the same emoji token across renderers.
    normalized = VARIATION_SELECTOR_RE.sub("", raw)
    return "".join(EMOJI_RE.findall(normalized))


def is_pascal_case_term(raw: str) -> bool:
    term = raw.replace("`", "").strip()
    if not PASCAL_CASE_RE.match(term):
        return False
    # Avoid matching all-uppercase labels that are not PascalCase feature names.
    return any(ch.islower() for ch in term)


def extract_emoji_glossary_entries(text: str) -> List[Tuple[str, str, str]]:
    entries: List[Tuple[str, str, str]] = []
    section_lines = find_heading_section_lines(text, "EmojiGlossary")
    if not section_lines:
        return entries

    for raw in section_lines:
        line = raw.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 3:
            continue
        emoji_cell = cells[0].replace("`", "").strip()
        term_cell = cells[1].replace("`", "").strip()
        meaning_cell = cells[2].replace("`", "").strip()
        emoji_tokens = normalize_emoji_tokens(emoji_cell)
        if not emoji_tokens:
            continue
        entries.append((emoji_tokens, term_cell, meaning_cell))

    return entries


def parse_emoji_pascal_token(raw: str) -> Tuple[str, str]:
    token = raw.replace("`", "").strip()
    if not token:
        return "", ""
    emoji_tokens = normalize_emoji_tokens(token)
    if not emoji_tokens:
        return "", ""
    # Remove emoji and variation selector marks to isolate a possible PascalCase term.
    term = EMOJI_RE.sub("", token)
    term = re.sub(r"[\ufe0e\ufe0f\s]+", "", term)
    if not is_pascal_case_term(term):
        return "", ""
    return emoji_tokens, term


def must_preserve_item_matches_pair(item: str, emoji_token: str, pascal_term: str) -> bool:
    cleaned = item.replace("`", "").strip()
    item_emoji_tokens = normalize_emoji_tokens(cleaned)
    return bool(emoji_token) and (emoji_token in item_emoji_tokens) and (pascal_term in cleaned)


def lint_userguide_completeness(path: Path, text: str, strict: bool, errs: List[str], warns: List[str]) -> None:
    titles = heading_titles_lower(text)
    nonempty_lines = [line for line in text.splitlines() if line.strip()]

    if len(nonempty_lines) < USERGUIDE_MIN_NONEMPTY_LINES:
        route_issue(
            f"{path.name}: UserGuide appears over-compressed ({len(nonempty_lines)} non-empty lines; expected >= {USERGUIDE_MIN_NONEMPTY_LINES})",
            strict,
            errs,
            warns,
        )

    if len(titles) < USERGUIDE_MIN_HEADINGS:
        route_issue(
            f"{path.name}: UserGuide appears over-compressed ({len(titles)} headings; expected >= {USERGUIDE_MIN_HEADINGS})",
            strict,
            errs,
            warns,
        )

    for label, keywords in REQUIRED_USERGUIDE_SECTION_GROUPS.items():
        if not any(any(key in title for key in keywords) for title in titles):
            route_issue(
                f"{path.name}: UserGuide missing required section signal for {label}",
                strict,
                errs,
                warns,
            )


def lint_emoji_glossary_contract(path: Path, text: str, strict: bool, errs: List[str], warns: List[str]) -> None:
    if not EMOJI_RE.search(text):
        return

    if "EmojiGlossary" not in text:
        errs.append(f"{path.name}: UserGuide contains emoji but no 'EmojiGlossary' section.")
        return

    section_lines = find_heading_section_lines(text, "EmojiGlossary")
    if not section_lines:
        errs.append(f"{path.name}: UserGuide contains emoji but 'EmojiGlossary' section could not be parsed.")
        return

    seen: Set[str] = set()
    entries = extract_emoji_glossary_entries(text)

    for emoji_tokens, term_cell, meaning_cell in entries:
        if emoji_tokens in seen:
            route_issue(
                f"{path.name}: EmojiGlossary contains duplicate emoji mapping for '{emoji_tokens}'",
                strict,
                errs,
                warns,
            )
        else:
            seen.add(emoji_tokens)

        if not term_cell or not meaning_cell:
            route_issue(
                f"{path.name}: EmojiGlossary must map emoji aliases to non-empty term and meaning fields.",
                strict,
                errs,
                warns,
            )

    if not entries:
        route_issue(
            f"{path.name}: EmojiGlossary exists but no valid emoji mapping rows were found.",
            strict,
            errs,
            warns,
        )


def lint_inline_code_emoji_render_safety(path: Path, text: str, strict: bool, errs: List[str], warns: List[str]) -> None:
    # Variation-selector-leading spans can indicate dropped emoji bases.
    # If no emoji can be recovered after normalization, treat the span as
    # corrupted render noise and ignore it.
    for m in re.finditer(r"`([^`]+)`", text):
        token = m.group(1)
        if token and token[0] in ("\ufe0e", "\ufe0f"):
            if not normalize_emoji_tokens(token):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            route_issue(
                f"{path.name}:{line_no}: inline code span starts with variation selector; likely missing emoji base token",
                strict,
                errs,
                warns,
            )


def extract_first_text_codeblock(text: str) -> str:
    m = re.search(r"```text\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not m:
        return ""
    return m.group(1)


def lint_global_instruction_codeblock_size(
    path: Path, text: str, strict: bool, errs: List[str], warns: List[str]
) -> None:
    block = extract_first_text_codeblock(text)
    if not block:
        route_issue(
            f"{path.name}: missing ```text fenced block for copy/paste instructions",
            strict,
            errs,
            warns,
        )
        return

    # Align with how users copy/paste the block as plain text (final newline included).
    char_count = len(block) + 1

    if char_count > GLOBAL_INSTRUCTION_CODEBLOCK_MAX_CHARS:
        errs.append(
            f"{path.name}: instruction code block length {char_count} exceeds ModuleMill budget {GLOBAL_INSTRUCTION_CODEBLOCK_MAX_CHARS} "
            f"(ChatGPT limit {CHATGPT_CUSTOM_INSTRUCTIONS_MAX_CHARS} minus reserved {GLOBAL_INSTRUCTION_RESERVED_PERSONALIZATION_CHARS})"
        )
        return

    if char_count > GLOBAL_INSTRUCTION_CODEBLOCK_SOFT_TARGET:
        route_issue(
            f"{path.name}: instruction code block length {char_count} exceeds soft target {GLOBAL_INSTRUCTION_CODEBLOCK_SOFT_TARGET}",
            strict,
            errs,
            warns,
        )


def normalize_canon_command(raw: str) -> str:
    token = raw.replace("`", "").strip()
    token = re.sub(r"<[^>]+>", "", token)
    token = re.sub(r"\[[^\]]+\]", "", token)
    token = re.sub(r"\s+", " ", token).strip()
    return token


def extract_userguide_canon_commands(text: str) -> List[str]:
    commands: List[str] = []
    in_command_table = False

    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            if in_command_table and line:
                in_command_table = False
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 2:
            continue

        if cells[0].lower() == "command" and cells[1].lower() == "canon":
            in_command_table = True
            continue

        if not in_command_table:
            continue

        if set("".join(cells)) <= {"-", " "}:
            continue

        canon_cell = cells[1]
        m = re.search(r"`([^`]+)`", canon_cell)
        canon = normalize_canon_command(m.group(1) if m else canon_cell)
        if canon and canon not in commands:
            commands.append(canon)

    return commands


def extract_userguide_command_alias_emoji_map(text: str) -> List[Tuple[str, str]]:
    aliases: List[Tuple[str, str]] = []
    in_command_table = False

    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            if in_command_table and line:
                in_command_table = False
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 3:
            continue

        if cells[0].lower() == "command" and cells[1].lower() == "canon":
            in_command_table = True
            continue

        if not in_command_table:
            continue

        if set("".join(cells)) <= {"-", " "}:
            continue

        command_label = cells[0].replace("`", "").strip()
        alias_cell = cells[2].replace("`", "").strip()
        emoji_tokens = normalize_emoji_tokens(alias_cell)
        if not command_label or not emoji_tokens:
            continue

        # Preserve appearance order while removing duplicates.
        dedup_tokens = "".join(dict.fromkeys(emoji_tokens))
        aliases.append((command_label, dedup_tokens))

    return aliases


def extract_namespaced_state_keys(text: str, module: str) -> List[str]:
    keys: List[str] = []
    module_prefix = f"{module.lower()}."
    sections: List[str] = []
    headings = build_heading_index(text)
    lines = text.splitlines()

    for idx, (level, title, start) in enumerate(headings):
        if "state" not in title.lower():
            continue
        end = len(lines)
        for lvl, _, li in headings[idx + 1 :]:
            if li > start and lvl <= level:
                end = li
                break
        sections.append("\n".join(lines[start:end]))

    scan_text = "\n".join(sections) if sections else text
    for m in STATE_KEY_RE.finditer(scan_text):
        key = m.group(1)
        if key.startswith(module_prefix) and key.count(".") == 1 and key not in keys:
            keys.append(key)
    return keys


def lint_manifest_contract_parity(
    path: Path,
    manifest: Dict[str, object],
    doc_texts: Dict[str, str],
    strict: bool,
    errs: List[str],
    warns: List[str],
) -> None:
    module = str(manifest.get("module", "")).strip()
    userguide_text = doc_texts.get("userguide", "")
    machinemanual_text = doc_texts.get("machinemanual", "")
    quickref_text = doc_texts.get("quickref", "")
    intent_policy = str(manifest.get("intent_policy", "")).strip()

    must_preserve = manifest.get("must_preserve", [])
    if not isinstance(must_preserve, list):
        errs.append(f"{path.name}: 'must_preserve' must be a list")
        must_preserve = []

    for i, item in enumerate(must_preserve, start=1):
        if not isinstance(item, str) or not item.strip():
            errs.append(f"{path.name}: must_preserve item #{i} must be a non-empty string")

    glossary_entries: List[Tuple[str, str, str]] = []
    if userguide_text:
        glossary_entries = extract_emoji_glossary_entries(userguide_text)

    if userguide_text and isinstance(must_preserve, list):
        userguide_lower = userguide_text.lower()
        for item in must_preserve:
            if isinstance(item, str) and item.strip():
                raw_item = item.strip()
                if raw_item.lower() in userguide_lower:
                    continue
                emoji_token, pascal_term = parse_emoji_pascal_token(raw_item)
                if emoji_token and pascal_term:
                    if any(
                        g_emoji == emoji_token and g_term == pascal_term
                        for g_emoji, g_term, _ in glossary_entries
                    ):
                        continue
                if raw_item.lower() not in userguide_lower:
                    errs.append(
                        f"{path.name}: must_preserve term missing from UserGuide: '{item}'"
                    )

    must_preserve_runtime = manifest.get("must_preserve_runtime", [])
    if must_preserve_runtime and not isinstance(must_preserve_runtime, list):
        errs.append(f"{path.name}: 'must_preserve_runtime' must be a list when provided")
        must_preserve_runtime = []

    for i, item in enumerate(must_preserve_runtime, start=1):
        if not isinstance(item, str) or not item.strip():
            errs.append(f"{path.name}: must_preserve_runtime item #{i} must be a non-empty string")

    if isinstance(must_preserve_runtime, list) and must_preserve_runtime:
        runtime_docs = {
            "UserGuide": userguide_text,
            "MachineManual": machinemanual_text,
            "QuickRefCard": quickref_text,
        }
        for item in must_preserve_runtime:
            if not isinstance(item, str) or not item.strip():
                continue
            needle = item.strip().lower()
            for role, role_text in runtime_docs.items():
                if not role_text:
                    errs.append(
                        f"{path.name}: must_preserve_runtime requires docs.{role.lower()} text for term '{item}'"
                    )
                    continue
                if needle not in role_text.lower():
                    errs.append(
                        f"{path.name}: must_preserve_runtime term missing from {role}: '{item}'"
                    )

    if intent_policy == "infer_high_confidence" and userguide_text:
        userguide_lower = userguide_text.lower()
        missing_signals: List[str] = []
        for label, keywords in INTENT_SIGNAL_KEYWORDS.items():
            if not any(key in userguide_lower for key in keywords):
                missing_signals.append(label)
        if missing_signals:
            warns.append(
                f"{path.name}: intent_policy=infer_high_confidence but UserGuide is missing signal(s): {', '.join(missing_signals)}"
            )

    if not strict or not module:
        return

    # Global anti-drift rule: any Emoji + PascalCase feature token defined in EmojiGlossary
    # must be protected in must_preserve.
    for emoji_token, term_cell, _ in glossary_entries:
        if not is_pascal_case_term(term_cell):
            continue
        if not any(
            isinstance(item, str) and item.strip() and must_preserve_item_matches_pair(item, emoji_token, term_cell)
            for item in must_preserve
        ):
            errs.append(
                f"{path.name}: missing must_preserve anti-drift entry for Emoji+PascalCase token '{emoji_token}{term_cell}'"
            )

    command_alias_emoji = extract_userguide_command_alias_emoji_map(userguide_text)
    for command_label, emoji_tokens in command_alias_emoji:
        missing_mm = [token for token in emoji_tokens if token not in machinemanual_text]
        if missing_mm:
            errs.append(
                f"{path.name}: MachineManual missing emoji alias token(s) for command '{command_label}': {''.join(missing_mm)}"
            )
        if quickref_text:
            missing_qr = [token for token in emoji_tokens if token not in quickref_text]
            if missing_qr:
                errs.append(
                    f"{path.name}: QuickRefCard missing emoji alias token(s) for command '{command_label}': {''.join(missing_qr)}"
                )

    if userguide_text and machinemanual_text:
        ug_state_keys = extract_namespaced_state_keys(userguide_text, module)
        mm_lower = machinemanual_text.lower()
        missing_state = [k for k in ug_state_keys if k.lower() not in mm_lower]
        if missing_state:
            errs.append(
                f"{path.name}: MachineManual missing namespaced state key(s) from UserGuide: {', '.join(missing_state)}"
            )

        canon_commands = extract_userguide_canon_commands(userguide_text)
        lifecycle_commands = [
            cmd
            for cmd in canon_commands
            if any(cmd.lower().endswith(f" {verb}") for verb in LIFECYCLE_VERBS)
        ]
        missing_lifecycle = [cmd for cmd in lifecycle_commands if cmd.lower() not in mm_lower]
        if missing_lifecycle:
            errs.append(
                f"{path.name}: MachineManual missing lifecycle canon command(s): {', '.join(missing_lifecycle)}"
            )

        if quickref_text:
            qr_lower = quickref_text.lower()
            missing_qr_lifecycle = [cmd for cmd in lifecycle_commands if cmd.lower() not in qr_lower]
            if missing_qr_lifecycle:
                warns.append(
                    f"{path.name}: QuickRefCard missing lifecycle canon command text for: {', '.join(missing_qr_lifecycle)}"
                )


def lint_markdown_file(path: Path, strict: bool = False, require_manifest: bool = False) -> Tuple[List[str], List[str]]:
    text = read_text(path)
    meta = parse_meta(text)
    errs: List[str] = []
    warns: List[str] = []

    if path.name in GLOBAL_INSTRUCTION_FILENAMES:
        lint_global_instruction_codeblock_size(path, text, strict, errs, warns)
        return errs, warns

    # Bundle files intentionally aggregate multiple docs and do not map to one DocRole.
    if path.name.upper().endswith("_BUNDLE.MD"):
        return errs, warns

    # Default mode: only lint docs that opt into ModuleKit metadata.
    # Use --strict to enforce metadata on every markdown file.
    if not strict and "DocRole" not in meta:
        return errs, warns

    for req in ("ModuleID", "Version", "DocRole", "Audience"):
        if req not in meta:
            errs.append(f"{path.name}: missing {req} in first ~40 lines")

    role = meta.get("DocRole", "")
    if role and role not in DOC_ROLES:
        errs.append(f"{path.name}: DocRole '{role}' not in {sorted(DOC_ROLES)}")

    # Basic role hygiene (lightweight heuristics, not a full classifier)
    if role == "QuickRefCard":
        if "rationale" in text.lower()[:2000]:
            errs.append(f"{path.name}: QuickRefCard contains 'rationale' near top (role bleed risk)")
        if len(text.splitlines()) > 220:
            errs.append(f"{path.name}: QuickRefCard is very long (>220 lines). Consider slimming.")

    module_id = meta.get("ModuleID", "")
    lint_inline_code_emoji_render_safety(path, text, strict, errs, warns)

    # Encourage canon command table markers in runtime UserGuides.
    if role == "UserGuide" and module_id not in FRAMEWORK_MODULE_IDS:
        lint_userguide_completeness(path, text, strict, errs, warns)
        lint_emoji_glossary_contract(path, text, strict, errs, warns)

        missing_markers = [m for m in sorted(REQUIRED_COMMAND_MARKERS) if m not in text]
        if missing_markers:
            msg = f"{path.name}: UserGuide missing canon command markers: {', '.join(missing_markers)}"
            route_issue(msg, strict, errs, warns)

        manifest_path = path.parent / "ModuleManifest.yaml"
        if not manifest_path.exists():
            msg = f"{path.name}: missing sibling ModuleManifest.yaml in {path.parent}"
            if require_manifest or strict:
                errs.append(msg)
            else:
                warns.append(msg)

    return errs, warns


def lint_manifest_file(path: Path, strict: bool = False) -> Tuple[List[str], List[str]]:
    text = read_text(path)
    manifest = parse_manifest(text)
    errs: List[str] = []
    warns: List[str] = []

    missing_keys = [k for k in sorted(REQUIRED_MANIFEST_KEYS) if k not in manifest]
    if missing_keys:
        errs.append(f"{path.name}: missing required key(s): {', '.join(missing_keys)}")

    engage_policy = str(manifest.get("engage_policy", "")).strip()
    if engage_policy and engage_policy not in ENGAGE_POLICIES:
        errs.append(f"{path.name}: engage_policy '{engage_policy}' not in {sorted(ENGAGE_POLICIES)}")

    intent_policy = str(manifest.get("intent_policy", "")).strip()
    if intent_policy and intent_policy not in INTENT_POLICIES:
        errs.append(f"{path.name}: intent_policy '{intent_policy}' not in {sorted(INTENT_POLICIES)}")

    version = str(manifest.get("version", "")).strip()
    if version and not re.match(r"^[0-9]+\.[0-9]+(?:\.[0-9]+)?$", version):
        errs.append(f"{path.name}: version '{version}' is not SemVer-like (MAJOR.MINOR[.PATCH])")

    for list_key in (
        "module_aliases",
        "use_when",
        "do_not_use_when",
        "required_inputs",
        "must_preserve",
        "must_preserve_runtime",
    ):
        if list_key in manifest and not isinstance(manifest.get(list_key), list):
            errs.append(f"{path.name}: '{list_key}' must be a list")

    module_emoji = str(manifest.get("module_emoji", "")).strip()
    if module_emoji and not EMOJI_RE.search(module_emoji):
        errs.append(f"{path.name}: module_emoji must contain an emoji token")

    docs = manifest.get("docs", {})
    if not isinstance(docs, dict):
        errs.append(f"{path.name}: 'docs' must be a mapping")
        docs = {}

    missing_doc_keys = [k for k in sorted(REQUIRED_MANIFEST_DOC_KEYS) if k not in docs]
    if missing_doc_keys:
        errs.append(f"{path.name}: docs missing key(s): {', '.join(missing_doc_keys)}")

    role_expectations = {
        "install": "Install",
        "quickref": "QuickRefCard",
        "machinemanual": "MachineManual",
        "userguide": "UserGuide",
    }

    module = str(manifest.get("module", "")).strip()
    is_template_manifest = any(part.lower() == "templates" for part in path.parts) or "<" in module or ">" in module

    doc_texts: Dict[str, str] = {}

    for doc_key, expected_role in role_expectations.items():
        rel = str(docs.get(doc_key, "")).strip()
        if not rel:
            continue

        if is_template_manifest:
            continue

        doc_path = path.parent / rel
        if not doc_path.exists():
            errs.append(f"{path.name}: docs.{doc_key} points to missing file '{rel}'")
            continue

        if doc_path.suffix.lower() != ".md":
            warns.append(f"{path.name}: docs.{doc_key} expected markdown file, got '{rel}'")
            continue

        doc_text = read_text(doc_path)
        doc_texts[doc_key] = doc_text
        doc_meta = parse_meta(doc_text)
        doc_role = doc_meta.get("DocRole", "")
        if doc_role and doc_role != expected_role:
            errs.append(
                f"{path.name}: docs.{doc_key} points to {doc_path.name} with DocRole '{doc_role}', expected '{expected_role}'"
            )

        doc_module = doc_meta.get("ModuleID", "")
        if module and doc_module and doc_module != module:
            errs.append(
                f"{path.name}: docs.{doc_key} module mismatch ({doc_module} != {module})"
            )

        doc_version = doc_meta.get("Version", "")
        if version and doc_version and doc_version != version:
            msg = f"{path.name}: docs.{doc_key} version mismatch ({doc_version} != {version})"
            if strict:
                errs.append(msg)
            else:
                warns.append(msg)

    failure_mode = str(manifest.get("failure_mode", "")).strip()
    if failure_mode and not failure_mode.startswith("fail_closed"):
        warns.append(f"{path.name}: failure_mode '{failure_mode}' should start with 'fail_closed' for safety")

    if not is_template_manifest:
        lint_manifest_contract_parity(path, manifest, doc_texts, strict, errs, warns)

    return errs, warns


def build_heading_index(text: str) -> List[Tuple[int, str, int]]:
    """
    Returns list of (level, title, line_index)
    """
    idx = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            idx.append((level, title, i))
    return idx


def extract_section(text: str, want: str) -> str:
    lines = text.splitlines()
    headings = build_heading_index(text)

    # Find the first heading whose title starts with want (case-insensitive)
    target = None
    for level, title, li in headings:
        if title.lower().startswith(want.lower()):
            target = (level, li)
            break
    if not target:
        raise SystemExit(f"Section not found: '{want}'")

    level, start = target
    end = len(lines)
    for lvl, _, li in headings:
        if li > start and lvl <= level:
            end = li
            break
    return "\n".join(lines[start:end]).rstrip() + "\n"


def is_canonical_modulekit_markdown(path: Path) -> bool:
    return path.name in CANONICAL_MODULEKIT_DOC_FILENAMES and "_CURRENT" in path.parts


def is_modulemill_lint_markdown(path: Path, modulekit_only: bool) -> bool:
    if path.name in GLOBAL_INSTRUCTION_FILENAMES:
        return True
    if not modulekit_only:
        return True
    return is_canonical_modulekit_markdown(path)


def collect_files(paths: List[Path], modulekit_only: bool = False) -> Tuple[List[Path], List[Path]]:
    md_files: Set[Path] = set()
    manifest_files: Set[Path] = set()

    for p in paths:
        if p.is_dir():
            if modulekit_only:
                for md in p.rglob("*.md"):
                    if is_modulemill_lint_markdown(md, modulekit_only=True):
                        md_files.add(md)
                for mf in p.rglob("ModuleManifest.yaml"):
                    if "_CURRENT" in mf.parts:
                        manifest_files.add(mf)
            else:
                md_files.update(p.rglob("*.md"))
                manifest_files.update(p.rglob("ModuleManifest.yaml"))
        else:
            if p.suffix.lower() == ".md":
                if is_modulemill_lint_markdown(p, modulekit_only=modulekit_only):
                    md_files.add(p)
            if p.name == "ModuleManifest.yaml":
                if not modulekit_only or "_CURRENT" in p.parts:
                    manifest_files.add(p)

    return sorted(md_files), sorted(manifest_files)


def cmd_lint(paths: List[Path], strict: bool = False, require_manifest: bool = False, modulekit_only: bool = False) -> int:
    all_errs: List[str] = []
    all_warns: List[str] = []

    md_files, manifest_files = collect_files(paths, modulekit_only=modulekit_only)

    for md in md_files:
        errs, warns = lint_markdown_file(md, strict=strict, require_manifest=require_manifest)
        all_errs.extend(errs)
        all_warns.extend(warns)

    for mf in manifest_files:
        errs, warns = lint_manifest_file(mf, strict=strict)
        all_errs.extend(errs)
        all_warns.extend(warns)

    if all_warns:
        print("\n".join([f"WARN: {w}" for w in all_warns]))

    if all_errs:
        print("\n".join(all_errs))
        return 1

    print("OK: no lint errors.")
    return 0


def cmd_extract(path: Path, section: str) -> int:
    text = read_text(path)
    print(extract_section(text, section), end="")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="modulemill")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_lint = sub.add_parser("lint", help="lint ModuleKit docs")
    ap_lint.add_argument("paths", nargs="+", help="file(s) or folder(s)")
    ap_lint.add_argument(
        "--strict",
        action="store_true",
        help="enforce metadata and stronger checks, including warning escalations",
    )
    ap_lint.add_argument(
        "--require-manifest",
        action="store_true",
        help="treat missing ModuleManifest.yaml beside runtime UserGuide as an error",
    )
    ap_lint.add_argument(
        "--modulekit-only",
        action="store_true",
        help="lint only canonical ModuleKit artifacts under *_CURRENT (Install/QuickRefCard/MachineManual/UserGuide/ModuleManifest)",
    )

    ap_ext = sub.add_parser("extract", help="extract section by heading prefix")
    ap_ext.add_argument("path", help="markdown file")
    ap_ext.add_argument("--section", required=True, help="heading title prefix, e.g. '3.2'")

    args = ap.parse_args()

    if args.cmd == "lint":
        return cmd_lint(
            [Path(x) for x in args.paths],
            strict=args.strict,
            require_manifest=args.require_manifest,
            modulekit_only=args.modulekit_only,
        )
    if args.cmd == "extract":
        return cmd_extract(Path(args.path), args.section)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
