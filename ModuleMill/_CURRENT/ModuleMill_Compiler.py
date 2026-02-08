#!/usr/bin/env python3
"""
ModuleMill Compiler v0.2
- lint: validate required metadata + basic role hygiene
- extract: print a requested section by heading
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

DOC_ROLES = {"Install", "QuickRefCard", "MachineManual", "UserGuide"}

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

def lint_file(path: Path, strict: bool = False) -> List[str]:
    text = read_text(path)
    meta = parse_meta(text)
    errs: List[str] = []

    # Bundle files intentionally aggregate multiple docs and don't map to one DocRole.
    if path.name.upper().endswith("_BUNDLE.MD"):
        return errs

    # Default mode: only lint docs that opt into ModuleKit metadata.
    # Use --strict to enforce metadata on every markdown file.
    if not strict and "DocRole" not in meta:
        return errs

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

    # If user-facing emoji aliases are present, the glossary must exist in canon docs.
    module_id = meta.get("ModuleID", "")
    if (
        role == "UserGuide"
        and module_id not in {"ModuleMill", "KitRegistry"}
        and EMOJI_RE.search(text)
        and "EmojiGlossary" not in text
    ):
        errs.append(f"{path.name}: UserGuide contains emoji but no 'EmojiGlossary' section.")
    return errs

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

def cmd_lint(paths: List[Path], strict: bool = False) -> int:
    all_errs: List[str] = []
    for p in paths:
        if p.is_dir():
            for md in p.rglob("*.md"):
                all_errs.extend(lint_file(md, strict=strict))
        else:
            all_errs.extend(lint_file(p, strict=strict))
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
        help="require metadata in all markdown files (including framework/support docs)",
    )

    ap_ext = sub.add_parser("extract", help="extract section by heading prefix")
    ap_ext.add_argument("path", help="markdown file")
    ap_ext.add_argument("--section", required=True, help="heading title prefix, e.g. '3.2'")

    args = ap.parse_args()

    if args.cmd == "lint":
        return cmd_lint([Path(x) for x in args.paths], strict=args.strict)
    if args.cmd == "extract":
        return cmd_extract(Path(args.path), args.section)

    return 2

if __name__ == "__main__":
    raise SystemExit(main())
