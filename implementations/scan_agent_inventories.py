#!/usr/bin/env python3
"""
Usage:
    python implementations/scan_agent_inventories.py

Fetches inventory.yaml files from a curated list of agent repositories and
prints a per-agent summary of memory items and their kinds.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from collections import Counter
from typing import Dict, Iterable, List, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/{repo}/master/inventory.yaml"
KNOWN_REPOS: Tuple[str, ...] = (
    "ai-village-agents/claude-opus-memory",
    "ai-village-agents/gpt-5-4-memory-kit",
    "ai-village-agents/gemini-3.1-pro-memory",
    "ai-village-agents/deepseek-v3.2-memory-system",
    "ai-village-agents/gpt-5-5-memory-improvement",
    "ai-village-agents/gpt-5-2-memory-improvement",
    "ai-village-agents/claude-opus-4-7-memory",
    "ai-village-agents/haiku-memory-system",
    "ai-village-agents/opus-46-memory",
    "ai-village-agents/gpt-5-1-memory",
)
COLLECTION_KEYS: Tuple[str, ...] = ("entries", "items", "inventory")


def fetch_text(url: str, timeout: float = 15.0) -> str:
    """Fetch raw text from a URL, returning a UTF-8 decoded string."""
    request = urllib.request.Request(url, headers={"User-Agent": "inventory-scanner/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_inventory(text: str) -> List[Dict[str, object]]:
    """Parse inventory content using PyYAML when available, else JSON."""
    if yaml is not None:
        data = yaml.safe_load(text)  # type: ignore[no-untyped-call]
    else:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return parse_simple_inventory(text)

    if isinstance(data, dict):
        entries_source = None
        for key in COLLECTION_KEYS:
            if key in data:
                entries_source = data[key]
                break
        if entries_source is None:
            if all(isinstance(value, dict) for value in data.values()):
                entries_source = list(data.values())
            else:
                entries_source = data
    else:
        entries_source = data

    if isinstance(entries_source, dict):
        entries_iter: Iterable[Dict[str, object]] = (
            entry for entry in entries_source.values() if isinstance(entry, dict)
        )
    elif isinstance(entries_source, list):
        entries_iter = (entry for entry in entries_source if isinstance(entry, dict))
    elif entries_source is None:
        entries_iter = ()
    else:
        raise ValueError("Inventory does not contain a list or mapping of entries")

    return list(entries_iter)


def parse_simple_inventory(text: str) -> List[Dict[str, object]]:
    """Minimal YAML fallback parser for inventory files without PyYAML."""
    entries: List[Dict[str, object]] = []
    current: Dict[str, object] | None = None
    in_entries = False
    entry_indent: int | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        if raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if not in_entries and stripped.startswith("- "):
            in_entries = True
            current = {}
            entry_indent = indent
            inline = stripped[2:].strip()
            if inline:
                key, sep, value = inline.partition(":")
                if sep:
                    current[key.strip()] = _coerce_value(value.strip())
            continue

        if not in_entries:
            matched_key = None
            for key in COLLECTION_KEYS:
                if stripped.startswith(f"{key}:"):
                    matched_key = key
                    break
            if matched_key is None:
                continue

            inline_value = stripped[len(matched_key) + 1 :].strip()
            inline_value = _strip_inline_comment(inline_value)

            if not inline_value:
                in_entries = True
                continue

            if inline_value.startswith("[") and inline_value.endswith("]"):
                try:
                    inline_list = json.loads(inline_value.replace("'", '"'))
                except json.JSONDecodeError:
                    inline_list = []
                if isinstance(inline_list, list):
                    for item in inline_list:
                        if isinstance(item, dict):
                            entries.append(item)
                return entries

            # Treat any other inline content as the beginning of the entries section.
            in_entries = True
            continue

        if indent <= 0 and not stripped.startswith("- "):
            if current is not None:
                entries.append(current)
            break

        if stripped.startswith("- "):
            if current is not None:
                entries.append(current)
            current = {}
            entry_indent = indent
            inline = stripped[2:].strip()
            if inline:
                key, sep, value = inline.partition(":")
                if sep:
                    current[key.strip()] = _coerce_value(value.strip())
            continue

        if current is None:
            continue

        if entry_indent is not None and indent <= entry_indent and not stripped.startswith("- "):
            entries.append(current)
            current = None
            in_entries = False
            entry_indent = None
            continue

        key, sep, value = stripped.partition(":")
        if not sep:
            continue
        current[key.strip()] = _coerce_value(value.strip())

    if current is not None:
        entries.append(current)

    if not entries:
        raise ValueError("Unable to parse inventory entries without PyYAML")

    return entries


def _coerce_value(value: str) -> object:
    """Trim quotes and inline comments from scalar values."""
    clean = _strip_inline_comment(value.strip())
    if clean.startswith(("'", '"')) and clean.endswith(("'", '"')) and len(clean) >= 2:
        clean = clean[1:-1]
    lowered = clean.lower()
    if lowered in {"null", "none", "~"}:
        return None
    if lowered in {"true", "false"}:
        return lowered == "true"
    return clean


def _strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False
    result_chars = []
    for char in value:
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            break
        result_chars.append(char)
    return "".join(result_chars).strip()


def summarise_entries(entries: List[Dict[str, object]]) -> Tuple[int, Counter[str]]:
    """Return total items and counts grouped by the 'kind' field."""
    kind_totals: Counter[str] = Counter()
    for entry in entries:
        raw_kind = entry.get("kind", "unknown")
        kind = str(raw_kind).strip().lower() if isinstance(raw_kind, str) else str(raw_kind)
        if not kind:
            kind = "unknown"
        kind_totals[kind] += 1
    return len(entries), kind_totals


def format_kind_summary(counter: Counter) -> str:
    """Create a compact 'kind:count' summary string."""
    if not counter:
        return "-"
    parts = [f"{kind}:{counter[kind]}" for kind in sorted(counter)]
    return " | ".join(parts)


def main() -> int:
    results = []
    aggregate_items = 0
    functional_repos = 0
    aggregate_kind_counts: Counter[str] = Counter()

    for repo in KNOWN_REPOS:
        agent_name = repo.rsplit("/", 1)[-1]
        url = RAW_URL_TEMPLATE.format(repo=repo)

        try:
            text = fetch_text(url)
        except urllib.error.HTTPError as exc:
            results.append((agent_name, None, None, f"HTTP {exc.code}"))
            continue
        except urllib.error.URLError as exc:
            results.append((agent_name, None, None, f"Network error: {exc.reason}"))
            continue
        except Exception as exc:
            results.append((agent_name, None, None, f"Fetch error: {exc}"))
            continue

        try:
            entries = parse_inventory(text)
        except Exception as exc:
            results.append((agent_name, None, None, f"Parse error: {exc}"))
            continue

        total, kind_counts = summarise_entries(entries)
        results.append((agent_name, total, kind_counts, None))
        aggregate_items += total
        functional_repos += 1
        aggregate_kind_counts.update(kind_counts)

    agent_header = "Agent"
    total_header = "Items"
    kinds_header = "Kinds"

    agent_width = max(len(agent_header), max((len(item[0]) for item in results), default=0))
    total_width = len(total_header)
    print(f"{agent_header:<{agent_width}}  {total_header:>{total_width}}  {kinds_header}")
    print(f"{'-' * agent_width}  {'-' * total_width}  {'-' * len(kinds_header)}")

    for agent_name, total, kind_counts, error in results:
        if error is not None:
            kind_text = f"ERROR: {error}"
            total_text = "-"
        else:
            kind_text = format_kind_summary(kind_counts)
            total_text = str(total)
        print(f"{agent_name:<{agent_width}}  {total_text:>{total_width}}  {kind_text}")

    total_repos = len(results)
    print()
    print(f"Total items across all repos: {aggregate_items}")
    print(f"Total functional repos: {functional_repos}/{total_repos}")
    print(f"Total kinds distribution: {format_kind_summary(aggregate_kind_counts)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
