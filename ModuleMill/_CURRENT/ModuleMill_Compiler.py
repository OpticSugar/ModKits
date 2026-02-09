#!/usr/bin/env python3
"""
ModuleMill Compiler v0.4
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
REQUIRED_MANIFEST_KEYS = {
    "module",
    "version",
    "mission",
    "engage_policy",
    "use_when",
    "do_not_use_when",
    "required_inputs",
    "response_envelope",
    "failure_mode",
    "docs",
}
REQUIRED_MANIFEST_DOC_KEYS = {"install", "quickref", "machinemanual", "userguide"}
REQUIRED_COMMAND_MARKERS = {"Command", "Canon", "Aliases", "Inputs", "Output shape", "State effects"}
REQUIRED_USERGUIDE_SECTION_GROUPS = {
    "context/mission depth": {"what this is", "mission", "scope", "context"},
    "rationale/why": {"rationale", "why", "tradeoff", "trade-off"},
    "failure behavior": {"failure behavior", "fail-closed", "fail closed", "guardrail", "error"},
    "examples": {"example", "template", "sample", "walkthrough"},
}
USERGUIDE_MIN_NONEMPTY_LINES = 120
USERGUIDE_MIN_HEADINGS = 8

META_PATTERNS = {
    "ModuleID": re.compile(r"\bModuleID\s*[:=]\s*(\S+)", re.IGNORECASE),
    "Version": re.compile(r"\bVersion\s*[:=]\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    "DocRole": re.compile(r"\bDocRole\s*[:=]\s*(\w+)", re.IGNORECASE),
    "Audience": re.compile(r"\bAudience\s*[:=]\s*(.+)", re.IGNORECASE),
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
EMOJI_RE = re.compile(r"[\u2600-\u27bf\U0001F300-\U0001FAFF]")


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

        if key in {"use_when", "do_not_use_when", "required_inputs"}:
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
    glossary_rows = 0

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

        if not EMOJI_RE.search(emoji_cell):
            continue

        glossary_rows += 1
        emoji_tokens = "".join(EMOJI_RE.findall(emoji_cell))
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

    if glossary_rows == 0:
        route_issue(
            f"{path.name}: EmojiGlossary exists but no valid emoji mapping rows were found.",
            strict,
            errs,
            warns,
        )


def lint_markdown_file(path: Path, strict: bool = False, require_manifest: bool = False) -> Tuple[List[str], List[str]]:
    text = read_text(path)
    meta = parse_meta(text)
    errs: List[str] = []
    warns: List[str] = []

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

    version = str(manifest.get("version", "")).strip()
    if version and not re.match(r"^[0-9]+\.[0-9]+(?:\.[0-9]+)?$", version):
        errs.append(f"{path.name}: version '{version}' is not SemVer-like (MAJOR.MINOR[.PATCH])")

    for list_key in ("use_when", "do_not_use_when", "required_inputs"):
        if list_key in manifest and not isinstance(manifest.get(list_key), list):
            errs.append(f"{path.name}: '{list_key}' must be a list")

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

        doc_meta = parse_meta(read_text(doc_path))
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


def collect_files(paths: List[Path]) -> Tuple[List[Path], List[Path]]:
    md_files: Set[Path] = set()
    manifest_files: Set[Path] = set()

    for p in paths:
        if p.is_dir():
            md_files.update(p.rglob("*.md"))
            manifest_files.update(p.rglob("ModuleManifest.yaml"))
        else:
            if p.suffix.lower() == ".md":
                md_files.add(p)
            if p.name == "ModuleManifest.yaml":
                manifest_files.add(p)

    return sorted(md_files), sorted(manifest_files)


def cmd_lint(paths: List[Path], strict: bool = False, require_manifest: bool = False) -> int:
    all_errs: List[str] = []
    all_warns: List[str] = []

    md_files, manifest_files = collect_files(paths)

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

    ap_ext = sub.add_parser("extract", help="extract section by heading prefix")
    ap_ext.add_argument("path", help="markdown file")
    ap_ext.add_argument("--section", required=True, help="heading title prefix, e.g. '3.2'")

    args = ap.parse_args()

    if args.cmd == "lint":
        return cmd_lint([Path(x) for x in args.paths], strict=args.strict, require_manifest=args.require_manifest)
    if args.cmd == "extract":
        return cmd_extract(Path(args.path), args.section)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
