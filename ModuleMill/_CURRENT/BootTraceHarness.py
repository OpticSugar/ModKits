#!/usr/bin/env python3
"""
BootTraceHarness

Deterministic diagnostics for ModuleKit bootstrapping docs:
- compares boot warning text across registry + global instruction files
- validates DefaultLoad module doc pointers for Manifest + QuickRef
- prints a traceable boot decision flow
- optionally checks remote URL reachability
"""

from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class ModuleEntry:
    name: str
    emoji: str = ""
    default_load: str = "no"
    single_emoji_activate: str = "no"
    docs: Dict[str, str] = field(default_factory=dict)


DOC_KEYS = ("Manifest", "Install", "QuickRef", "MachineManual", "UserGuide")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_boot_warning_from_global(text: str) -> str:
    patterns = (
        r'Reply 1:\s*"([^"]+)"',
        r'Reply #1 includes:\s*"([^"]+)"',
        r"Reply 1:\s*`([^`]+)`",
    )
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""


def extract_boot_warning_from_registry(text: str) -> str:
    m = re.search(
        r"first assistant message must include a one-line boot warning:\s*\n\s*-\s*`([^`]+)`",
        text,
        flags=re.IGNORECASE,
    )
    if m:
        return m.group(1).strip()
    return ""


def extract_supported_modules(global_text: str) -> List[str]:
    m = re.search(
        r"-\s*(?:Supported modules|Modules):\s*`([^`]+)`",
        global_text,
        flags=re.IGNORECASE,
    )
    if not m:
        return []
    raw = m.group(1)
    modules = [part.strip() for part in raw.split("|")]
    return [m for m in modules if m]


def parse_registry_modules(text: str) -> List[ModuleEntry]:
    parts = re.split(r"^###\s+Module:\s*", text, flags=re.MULTILINE)
    entries: List[ModuleEntry] = []
    if len(parts) <= 1:
        return entries

    for block in parts[1:]:
        lines = block.splitlines()
        if not lines:
            continue

        name = lines[0].strip()
        entry = ModuleEntry(name=name)
        in_docs = False

        for raw in lines[1:]:
            if raw.startswith("## "):
                break

            line = raw.strip()
            if not line:
                continue

            if line.startswith("- Docs:"):
                in_docs = True
                continue

            if in_docs:
                m_doc = re.match(r"^\s*-\s*(\w+):\s*`([^`]+)`\s*$", line)
                if m_doc and m_doc.group(1) in DOC_KEYS:
                    entry.docs[m_doc.group(1)] = m_doc.group(2).strip()
                    continue

                if line.startswith("- ") and not line.startswith("- Version:"):
                    in_docs = False
                elif line.startswith("- Version:"):
                    in_docs = False

            if line.startswith("- ModuleEmoji:"):
                entry.emoji = extract_backtick_value(line)
            elif line.startswith("- DefaultLoad:"):
                entry.default_load = extract_backtick_value(line).lower()
            elif line.startswith("- SingleEmojiActivate:"):
                entry.single_emoji_activate = extract_backtick_value(line).lower()

        entries.append(entry)

    return entries


def extract_backtick_value(line: str) -> str:
    m = re.search(r"`([^`]+)`", line)
    return m.group(1).strip() if m else ""


def check_url(url: str, timeout: int) -> Tuple[bool, str]:
    req = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, str(resp.status)
    except urllib.error.HTTPError as err:
        return False, f"HTTP {err.code}"
    except Exception as err:  # pragma: no cover
        return False, f"{type(err).__name__}: {err}"


def collect_all_doc_urls(entries: List[ModuleEntry]) -> List[str]:
    urls: List[str] = []
    for entry in entries:
        for key in DOC_KEYS:
            url = entry.docs.get(key, "").strip()
            if url and url not in urls:
                urls.append(url)
    return urls


def main() -> int:
    ap = argparse.ArgumentParser(prog="boottrace")
    ap.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[3]),
        help="Path to repository root (default: inferred from script location)",
    )
    ap.add_argument(
        "--check-urls",
        action="store_true",
        help="Check remote reachability for module doc URLs in KitRegistry",
    )
    ap.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="URL check timeout seconds (default: 10)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    kitregistry_path = repo_root / "ModKits" / "KitRegistry" / "_CURRENT" / "KitRegistry.md"
    global_path = repo_root / "ModKits" / "KitRegistry" / "_CURRENT" / "ChatGPT_GlobalInstructions.md"
    enterprise_path = (
        repo_root / "ModKits" / "KitRegistry" / "_CURRENT" / "ChatGPT_GlobalInstructions_Enterprise.md"
    )

    missing = [p for p in (kitregistry_path, global_path, enterprise_path) if not p.exists()]
    if missing:
        for path in missing:
            print(f"ERROR missing file: {path}")
        return 1

    kitregistry_text = read_text(kitregistry_path)
    global_text = read_text(global_path)
    enterprise_text = read_text(enterprise_path)

    registry_boot = extract_boot_warning_from_registry(kitregistry_text)
    standard_boot = extract_boot_warning_from_global(global_text)
    enterprise_boot = extract_boot_warning_from_global(enterprise_text)

    modules = parse_registry_modules(kitregistry_text)
    module_names = [m.name for m in modules]
    default_modules = [m for m in modules if m.default_load == "yes"]
    emoji_map = {m.emoji: m.name for m in modules if m.emoji}

    standard_supported = extract_supported_modules(global_text)
    enterprise_supported = extract_supported_modules(enterprise_text)

    issues: List[str] = []
    if not registry_boot:
        issues.append("Could not parse boot warning from KitRegistry.md")
    if not standard_boot:
        issues.append("Could not parse boot warning from ChatGPT_GlobalInstructions.md")
    if not enterprise_boot:
        issues.append("Could not parse boot warning from ChatGPT_GlobalInstructions_Enterprise.md")

    if registry_boot and standard_boot and registry_boot != standard_boot:
        issues.append("Boot warning mismatch: KitRegistry vs ChatGPT_GlobalInstructions")
    if registry_boot and enterprise_boot and registry_boot != enterprise_boot:
        issues.append("Boot warning mismatch: KitRegistry vs ChatGPT_GlobalInstructions_Enterprise")

    if not default_modules:
        issues.append("No DefaultLoad=yes modules found in KitRegistry")

    for entry in default_modules:
        if "Manifest" not in entry.docs:
            issues.append(f"DefaultLoad module '{entry.name}' is missing Docs.Manifest")
        if "QuickRef" not in entry.docs:
            issues.append(f"DefaultLoad module '{entry.name}' is missing Docs.QuickRef")

    if standard_supported:
        registry_set = set(module_names)
        supported_set = set(standard_supported)
        if supported_set != registry_set:
            issues.append(
                "Supported module list mismatch in ChatGPT_GlobalInstructions.md "
                f"(global={sorted(supported_set)} registry={sorted(registry_set)})"
            )

    if enterprise_supported:
        registry_set = set(module_names)
        supported_set = set(enterprise_supported)
        if supported_set != registry_set:
            issues.append(
                "Supported module list mismatch in ChatGPT_GlobalInstructions_Enterprise.md "
                f"(enterprise={sorted(supported_set)} registry={sorted(registry_set)})"
            )

    print("BootTrace decision flow")
    print("-----------------------")
    print("1) Reply #1 boot warning:")
    print(f"   \"{standard_boot or '<missing>'}\"")
    print("2) Pre-reply #2 gate:")
    print("   If user sends HALT/cancel/skip modules, suppress auto-boot for this chat.")
    print("3) Reply #2 auto-boot path:")
    if default_modules:
        print("   Load DefaultLoad=yes modules in this order:")
        for idx, entry in enumerate(default_modules, start=1):
            manifest = entry.docs.get("Manifest", "<missing>")
            quickref = entry.docs.get("QuickRef", "<missing>")
            print(f"   {idx}. {entry.name}")
            print(f"      - Manifest: {manifest}")
            print(f"      - QuickRef: {quickref}")
    else:
        print("   <none>")
    print("4) Single-emoji activation map:")
    if emoji_map:
        for emoji, module in emoji_map.items():
            print(f"   - {emoji} -> {module}")
    else:
        print("   <none>")

    if args.check_urls:
        print("5) URL reachability:")
        for url in collect_all_doc_urls(modules):
            ok, status = check_url(url, timeout=args.timeout)
            label = "OK" if ok else "FAIL"
            print(f"   - {label} {status} {url}")
            if not ok:
                issues.append(f"Unreachable doc URL: {url} ({status})")

    print("")
    if issues:
        print("BootTrace checks: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("BootTrace checks: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
