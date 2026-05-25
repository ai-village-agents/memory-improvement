#!/usr/bin/env python3
"""
Validate inventory.yaml conforming to expected memory inventory schema.

Usage:
    python implementations/validate_inventory.py
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependent on environment
    print(
        "Error: PyYAML is required to validate the inventory. "
        "Install it with `pip install PyYAML` and retry.",
        file=sys.stderr,
    )
    sys.exit(1)


REQUIRED_FIELDS = {
    "id",
    "status",
    "kind",
    "summary",
    "source",
    "last_verified",
    "retrieval_cue",
    "internal_memory_policy",
}


def load_inventory(path: Path) -> dict:
    """Load inventory.yaml from disk."""
    try:
        with path.open("r", encoding="utf-8") as stream:
            return yaml.safe_load(stream) or {}
    except FileNotFoundError:
        print(f"Error: inventory file not found at {path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error: failed to parse YAML: {exc}", file=sys.stderr)
        sys.exit(1)


def validate_entries(data: dict) -> list[str]:
    """Validate structure and content of inventory entries."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append("Top-level YAML structure must be a mapping.")
        return errors

    entries = data.get("entries")
    if entries is None:
        errors.append("Missing top-level `entries` key.")
        return errors

    if not isinstance(entries, list):
        errors.append("`entries` must be a list.")
        return errors

    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()

    for index, entry in enumerate(entries):
        location = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{location} must be a mapping.")
            continue

        missing_fields = sorted(REQUIRED_FIELDS - entry.keys())
        if missing_fields:
            errors.append(
                f"{location} missing required fields: {', '.join(missing_fields)}"
            )

        entry_id = entry.get("id")
        if entry_id is None:
            continue

        if entry_id in seen_ids:
            duplicate_ids.add(entry_id)
        else:
            seen_ids.add(entry_id)

    if duplicate_ids:
        duplicates_list = ", ".join(sorted(duplicate_ids))
        errors.append(f"Duplicate entry ids found: {duplicates_list}")

    return errors


def main() -> int:
    inventory_path = Path("inventory.yaml")
    data = load_inventory(inventory_path)
    errors = validate_entries(data)

    if errors:
        print("Inventory validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Inventory validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
