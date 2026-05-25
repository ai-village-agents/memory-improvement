#!/usr/bin/env python3
"""
Pre-consolidate gate - Validates memory system before consolidation.
Based on shared-gate-library standard, adapted for Sonnet 4.5 repo.
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

REPO_PATH = Path("/home/computeruse/memory-improvement")
INVENTORY_FILE = REPO_PATH / "inventory.yaml"

def validate_external_pointers():
    """Check that external memory repository is accessible."""
    required_files = [
        REPO_PATH / "memory-artifacts" / "goals" / "goal_002_improve_memory" / "active_state.md",
        REPO_PATH / "memory-artifacts" / "principles.md",
        INVENTORY_FILE
    ]
    
    missing = []
    for path in required_files:
        if not path.exists():
            missing.append(str(path.name))
    
    return len(missing) == 0, missing

def validate_inventory():
    """Check that inventory.yaml is valid."""
    if not INVENTORY_FILE.exists():
        return False, "inventory.yaml not found"
    
    try:
        # Run the validator
        result = subprocess.run(
            ["python3", str(REPO_PATH / "implementations" / "validate_inventory.py")],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True, "inventory valid"
        else:
            return False, f"inventory validation failed: {result.stdout}"
    except Exception as e:
        return False, f"inventory check error: {e}"

def validate_git_state():
    """Ensure repo is clean before consolidation."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout.strip():
            return False, f"Uncommitted changes: {len(result.stdout.strip().split(chr(10)))} files"
        return True, "git clean"
    except Exception as e:
        return False, f"git check failed: {e}"

def get_repo_stats():
    """Get basic repo statistics."""
    try:
        commit_result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=5
        )
        commits = len(commit_result.stdout.strip().split('\n'))
        
        files = len(list(REPO_PATH.rglob('*'))) - len(list((REPO_PATH / '.git').rglob('*')))
        
        return commits, files
    except:
        return None, None

def main():
    # Run all checks
    pointers_ok, pointers_msg = validate_external_pointers()
    inventory_ok, inventory_msg = validate_inventory()
    git_ok, git_msg = validate_git_state()
    commits, files = get_repo_stats()
    
    # Determine status
    status = "PASS" if all([pointers_ok, inventory_ok, git_ok]) else "FAIL"
    
    warnings = []
    errors = []
    
    if not pointers_ok:
        errors.append(f"Missing external pointers: {pointers_msg}")
    if not inventory_ok:
        errors.append(f"Inventory issue: {inventory_msg}")
    if not git_ok:
        warnings.append(f"Git state: {git_msg}")
    
    # Output JSON
    result = {
        "gate": "pre_consolidate",
        "status": status,
        "checks": {
            "external_pointers_present": pointers_ok,
            "inventory_valid": inventory_ok,
            "git_state_clean": git_ok,
            "total_commits": commits,
            "total_files": files
        },
        "warnings": warnings,
        "errors": errors,
        "timestamp": datetime.now().isoformat()
    }
    
    print(json.dumps(result, indent=2))
    
    # Exit code
    exit(0 if status == "PASS" else 1)

if __name__ == '__main__':
    main()
