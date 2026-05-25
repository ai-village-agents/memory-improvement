#!/usr/bin/env python3
"""
Pre-goal transition gate.

Validates that the repository is ready to incorporate a new goal announcement
by ensuring required artifacts are present, the inventory is valid, and the
repository state is safe to modify. Emits shared-gate-library compliant JSON.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
GOALS_DIR = REPO_ROOT / "memory-artifacts" / "goals"
ARCHIVE_CANDIDATES = (
    REPO_ROOT / "memory-artifacts" / "archives",
    REPO_ROOT / "archives",
)
PUBLIC_COMMS_FILE = REPO_ROOT / "memory-artifacts" / "public_communications.md"
INVENTORY_VALIDATOR = REPO_ROOT / "implementations" / "validate_inventory.py"


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS" or "FAIL"
    details: str

    def as_dict(self) -> dict:
        return {"name": self.name, "status": self.status, "details": self.details}


@dataclass
class GoalInfo:
    directory: Path
    goal_id: str
    goal_name: Optional[str]
    day: Optional[str]
    active_state: Path


def run_subprocess(args: Iterable[str], *, cwd: Path, timeout: int = 15) -> subprocess.CompletedProcess:
    """Execute a subprocess command with sane defaults."""
    return subprocess.run(
        list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def determine_current_goal() -> Optional[GoalInfo]:
    """Identify the current goal by selecting the highest-numbered goal directory with an active_state."""
    if not GOALS_DIR.exists():
        return None

    goal_candidates: List[Tuple[int, GoalInfo]] = []

    for path in GOALS_DIR.iterdir():
        if not path.is_dir():
            continue
        active_state = path / "active_state.md"
        if not active_state.exists():
            continue

        match = re.match(r"(goal_(\d+))", path.name)
        if match:
            goal_id = match.group(1)
            numeric_id = int(match.group(2))
        else:
            goal_id = path.name
            numeric_id = -1

        try:
            contents = active_state.read_text(encoding="utf-8")
        except OSError:
            contents = ""

        goal_name = None
        for line in contents.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                header_text = stripped.lstrip("#").strip()
                goal_name = re.sub(r"^(GOAL(?:\s+[A-Z]+)?\:?)\s*", "", header_text, flags=re.IGNORECASE)
                goal_name = goal_name.strip('" ')
                break

        day_match = re.search(r"Day\s+(\d+)", contents)
        day = day_match.group(1) if day_match else None

        goal_candidates.append(
            (
                numeric_id,
                GoalInfo(
                    directory=path,
                    goal_id=goal_id,
                    goal_name=goal_name or None,
                    day=day,
                    active_state=active_state,
                ),
            )
        )

    if not goal_candidates:
        return None

    goal_candidates.sort(key=lambda item: item[0])
    return goal_candidates[-1][1]


def check_current_goal_archived(goal: Optional[GoalInfo]) -> Tuple[CheckResult, List[str]]:
    """Verify that the current goal has a corresponding archive entry."""
    if goal is None:
        return CheckResult("current_goal_archived", "FAIL", "No active goal directory with active_state.md was found."), []

    archive_dirs = [path for path in ARCHIVE_CANDIDATES if path.exists()]
    if not archive_dirs:
        return CheckResult("current_goal_archived", "FAIL", "No archives directory present (looked for memory-artifacts/archives or archives/)."), []

    expected_tokens = (goal.directory.name, goal.goal_id)
    matched_archive: Optional[Path] = None
    for archive_dir in archive_dirs:
        for candidate in archive_dir.iterdir():
            if not candidate.is_file():
                continue
            filename = candidate.name
            if any(token in filename for token in expected_tokens):
                matched_archive = candidate
                break
        if matched_archive:
            break

    if matched_archive is None:
        searched = ", ".join(str(path) for path in archive_dirs)
        message = (
            f"No archive entry found for {goal.goal_id!r}. "
            f"Searched directories: {searched}."
        )
        return CheckResult("current_goal_archived", "FAIL", message), []

    warnings: List[str] = []
    try:
        if matched_archive.stat().st_size == 0:
            warnings.append(f"Archive file {matched_archive.name} is empty; confirm contents before proceeding.")
    except OSError:
        warnings.append(f"Could not verify size of archive file {matched_archive.name}.")

    detail = f"Archive located: {matched_archive.relative_to(REPO_ROOT)}"
    return CheckResult("current_goal_archived", "PASS", detail), warnings


def check_active_state_documented(goal: Optional[GoalInfo]) -> Tuple[CheckResult, List[str]]:
    """Ensure the active state's documentation exists and is populated."""
    if goal is None:
        return CheckResult("active_state_documented", "FAIL", "Unable to locate a current goal active_state.md."), []

    active_state = goal.active_state
    if not active_state.exists():
        return CheckResult("active_state_documented", "FAIL", f"Expected active_state.md at {active_state} but file is missing."), []

    try:
        contents = active_state.read_text(encoding="utf-8")
    except OSError as exc:
        return CheckResult("active_state_documented", "FAIL", f"Error reading {active_state.name}: {exc}"), []

    line_count = sum(1 for line in contents.splitlines() if line.strip())
    if line_count == 0:
        return CheckResult("active_state_documented", "FAIL", f"{active_state.name} is empty; document current goal state before transitioning."), []

    detail = f"{active_state.relative_to(REPO_ROOT)} contains {line_count} non-blank lines."
    return CheckResult("active_state_documented", "PASS", detail), []


def check_public_comms_logged(goal: Optional[GoalInfo]) -> Tuple[CheckResult, List[str]]:
    """Confirm that public communications include an entry for the current goal/day."""
    if not PUBLIC_COMMS_FILE.exists():
        return CheckResult("public_communications_logged", "FAIL", f"Missing log file at {PUBLIC_COMMS_FILE}."), []

    try:
        contents = PUBLIC_COMMS_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        return CheckResult("public_communications_logged", "FAIL", f"Unable to read public communications log: {exc}"), []

    if goal is None:
        # Without a goal, we cannot cross-reference; treat as failure so operator investigates.
        return CheckResult("public_communications_logged", "FAIL", "Cannot confirm public communications without a current goal context."), []

    search_terms: List[str] = []
    if goal.day:
        search_terms.append(f"Day {goal.day}")
    if goal.goal_name:
        search_terms.append(goal.goal_name)
    search_terms.append(goal.goal_id)

    for term in filter(None, search_terms):
        if term in contents:
            detail = f"Public communications include reference to '{term}'."
            return CheckResult("public_communications_logged", "PASS", detail), []

    preview = " ".join(contents.splitlines()[:5])
    detail = (
        f"No reference to current goal ({goal.goal_id}) found in public communications. "
        f"Searched for terms: {', '.join(search_terms)}. "
        f"Preview: {preview[:120]}..."
    )
    return CheckResult("public_communications_logged", "FAIL", detail), []


def check_inventory_valid() -> Tuple[CheckResult, List[str]]:
    """Run the inventory validator script."""
    if not INVENTORY_VALIDATOR.exists():
        return CheckResult("inventory_valid", "FAIL", f"Validator missing at {INVENTORY_VALIDATOR}."), []

    try:
        result = run_subprocess(
            (sys.executable, str(INVENTORY_VALIDATOR)),
            cwd=REPO_ROOT,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return CheckResult("inventory_valid", "FAIL", "Inventory validation timed out after 30 seconds."), []
    except OSError as exc:
        return CheckResult("inventory_valid", "FAIL", f"Failed to execute inventory validator: {exc}"), []

    if result.returncode != 0:
        detail = result.stdout.strip() or result.stderr.strip() or "Unknown validation error."
        return CheckResult("inventory_valid", "FAIL", detail), []

    message = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "Inventory validator reported success."
    return CheckResult("inventory_valid", "PASS", message), []


def check_git_clean() -> Tuple[CheckResult, List[str]]:
    """Ensure there are no uncommitted changes."""
    try:
        result = run_subprocess(("git", "status", "--porcelain"), cwd=REPO_ROOT, timeout=10)
    except OSError as exc:
        return CheckResult("git_state_clean", "FAIL", f"Failed to invoke git: {exc}"), []

    if result.returncode != 0:
        detail = result.stderr.strip() or "git status --porcelain failed."
        return CheckResult("git_state_clean", "FAIL", detail), []

    output = result.stdout.strip()
    if output:
        changed_files = len(output.splitlines())
        return CheckResult("git_state_clean", "FAIL", f"Repository has {changed_files} uncommitted change(s)."), []

    return CheckResult("git_state_clean", "PASS", "Working tree is clean."), []


def check_repository_pushed() -> Tuple[CheckResult, List[str]]:
    """Ensure local commits have been pushed to the tracked upstream branch."""
    try:
        upstream = run_subprocess(
            ("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"),
            cwd=REPO_ROOT,
            timeout=5,
        )
    except OSError as exc:
        return CheckResult("repository_pushed", "FAIL", f"Failed to query git upstream: {exc}"), []

    if upstream.returncode != 0:
        detail = upstream.stderr.strip() or "No upstream branch configured; push to remote before transitioning goals."
        return CheckResult("repository_pushed", "FAIL", detail), []

    upstream_ref = upstream.stdout.strip()
    try:
        ahead_behind = run_subprocess(
            ("git", "rev-list", "--count", "--left-right", "@{u}...HEAD"),
            cwd=REPO_ROOT,
            timeout=5,
        )
    except OSError as exc:
        return CheckResult("repository_pushed", "FAIL", f"Failed to compare with upstream {upstream_ref}: {exc}"), []

    if ahead_behind.returncode != 0:
        detail = ahead_behind.stderr.strip() or f"git rev-list comparison with {upstream_ref} failed."
        return CheckResult("repository_pushed", "FAIL", detail), []

    counts = ahead_behind.stdout.strip().split()
    if len(counts) != 2:
        return CheckResult("repository_pushed", "FAIL", f"Unexpected rev-list output: {ahead_behind.stdout.strip()}"), []

    behind_count, ahead_count = map(int, counts)
    warnings: List[str] = []

    if ahead_count > 0:
        detail = f"HEAD is ahead of {upstream_ref} by {ahead_count} commit(s); push before proceeding."
        return CheckResult("repository_pushed", "FAIL", detail), []

    if behind_count > 0:
        warnings.append(f"Local branch is behind {upstream_ref} by {behind_count} commit(s); pull latest changes after transition tasks.")

    return CheckResult("repository_pushed", "PASS", f"Local branch is in sync with {upstream_ref}."), warnings


def main() -> None:
    warnings: List[str] = []
    errors: List[str] = []
    checks: List[dict] = []

    goal = determine_current_goal()

    def run_inventory_check(_: Optional[GoalInfo]) -> Tuple[CheckResult, List[str]]:
        return check_inventory_valid()

    def run_git_clean_check(_: Optional[GoalInfo]) -> Tuple[CheckResult, List[str]]:
        return check_git_clean()

    def run_git_pushed_check(_: Optional[GoalInfo]) -> Tuple[CheckResult, List[str]]:
        return check_repository_pushed()

    check_functions = (
        (check_current_goal_archived, "current_goal_archived"),
        (check_active_state_documented, "active_state_documented"),
        (check_public_comms_logged, "public_communications_logged"),
        (run_inventory_check, "inventory_valid"),
        (run_git_clean_check, "git_state_clean"),
        (run_git_pushed_check, "repository_pushed"),
    )

    for fn, fallback_name in check_functions:
        try:
            result, check_warnings = fn(goal)
        except Exception as exc:  # noqa: BLE001
            result = CheckResult(fallback_name, "FAIL", f"Unexpected error: {exc}")
            check_warnings = []

        checks.append(result.as_dict())

        if result.status != "PASS":
            errors.append(result.details)

        warnings.extend(check_warnings)

    status = "PASS" if not errors else "FAIL"

    payload = {
        "gate": "pre_goal_transition",
        "status": status,
        "checks": checks,
        "warnings": warnings,
        "errors": errors,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(payload, indent=2))
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
