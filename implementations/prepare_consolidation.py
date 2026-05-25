#!/usr/bin/env python3
"""
Generate a consolidation worksheet based on the consolidation runbook.

Usage:
    python implementations/prepare_consolidation.py

Run this from anywhere inside the repository. The worksheet is printed to
stdout and includes git state details plus prompts that align with the
consolidation procedure.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List


def run_git_command(repo_root: Path, *args: str) -> str:
    """Run a git command in the repository and return stdout (stripped)."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed with code {result.returncode}: {result.stderr.strip()}"
        )
    return result.stdout.rstrip()


def extract_checklist(runbook_text: str) -> List[str]:
    """Extract checklist items (- [ ]) under the Consolidation Checklist section."""
    heading = "## Consolidation Checklist"
    try:
        section_start = runbook_text.index(heading) + len(heading)
    except ValueError:
        return []

    remainder = runbook_text[section_start:]
    next_heading_index = remainder.find("\n## ")
    if next_heading_index != -1:
        section_text = remainder[:next_heading_index]
    else:
        section_text = remainder

    checklist = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ["):
            checklist.append(stripped)
    return checklist


def format_repository_state(status_summary: str) -> str:
    """Indent each line of the repository state summary for readability."""
    if not status_summary:
        return "  (no status output)"
    return "\n".join(f"  {line}" for line in status_summary.splitlines())


def build_stays_moves_deletes_template() -> str:
    """Return the STAYS/MOVES/DELETES template block."""
    sections = ["STAYS", "MOVES", "DELETES"]
    lines = ["STAYS/MOVES/DELETES:"]
    for section in sections:
        lines.append(f"  {section}:")
        lines.append("    - ")
    return "\n".join(lines)


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    runbook_path = repo_root / "runbooks" / "consolidation.md"

    try:
        runbook_text = runbook_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Runbook not found at {runbook_path}")

    checklist_items = extract_checklist(runbook_text)

    porcelain_status = run_git_command(repo_root, "status", "--porcelain")
    is_clean = porcelain_status == ""
    status_label = "Clean" if is_clean else "Dirty"
    if not is_clean:
        print(
            "Warning: working tree is not clean. Resolve before consolidating.",
            file=sys.stderr,
        )

    status_summary = run_git_command(repo_root, "status", "-sb")

    try:
        commit_output = run_git_command(
            repo_root,
            "log",
            "-1",
            "--pretty=format:%H%n%an%n%ad%n%s",
        )
        commit_lines = commit_output.splitlines()
        commit_hash = commit_lines[0] if commit_lines else "N/A"
        commit_author = commit_lines[1] if len(commit_lines) > 1 else "N/A"
        commit_date = commit_lines[2] if len(commit_lines) > 2 else "N/A"
        commit_subject = commit_lines[3] if len(commit_lines) > 3 else "N/A"
    except RuntimeError:
        commit_hash = "N/A"
        commit_author = "N/A"
        commit_date = "N/A"
        commit_subject = "No commits yet"

    worksheet_lines = [
        "=== Consolidation Worksheet ===",
        f"Repository: {repo_root}",
        "",
        f"Git Status: {status_label}",
        "",
        "Latest Commit:",
        f"  Hash:    {commit_hash}",
        f"  Author:  {commit_author}",
        f"  Date:    {commit_date}",
        f"  Message: {commit_subject}",
        "",
        "Repository State Summary:",
        format_repository_state(status_summary),
        "",
        "Checklist:",
    ]

    if checklist_items:
        worksheet_lines.extend(f"  {item}" for item in checklist_items)
    else:
        worksheet_lines.append("  (No checklist items found in runbook.)")

    worksheet_lines.extend(
        [
            "",
            "What changed this session?",
            "  - ",
            "",
            "What should be updated in external memory?",
            "  - ",
            "",
            build_stays_moves_deletes_template(),
            "",
            "Next session goal:",
            "  - ",
        ]
    )

    print("\n".join(worksheet_lines))


if __name__ == "__main__":
    main()
