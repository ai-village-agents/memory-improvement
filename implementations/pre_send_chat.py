#!/usr/bin/env python3
"""
Pre-send-chat gate - Prevents duplicate messages and validates clarity.
Based on shared-gate-library standard, adapted for Sonnet 4.5 repo structure.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

REPO_PATH = Path("/home/computeruse/memory-improvement")
COMMS_FILE = REPO_PATH / "memory-artifacts" / "public_communications.md"

def load_recent_messages(limit=10):
    """Extract recent messages from public_communications.md"""
    if not COMMS_FILE.exists():
        return []
    
    try:
        with open(COMMS_FILE) as f:
            content = f.read()
        
        # Extract messages from markdown - look for lines with timestamps
        messages = []
        for line in content.split('\n'):
            # Look for session markers like "S1 [10:11 AM]:" or bullet points with content
            if '[' in line and ']' in line and (':' in line or 'AM' in line or 'PM' in line):
                messages.append(line.strip())
        
        return messages[-limit:] if messages else []
    except Exception as e:
        print(f"Warning: Could not load recent messages: {e}", file=sys.stderr)
        return []

def check_duplicate(message_text, recent_messages):
    """Check if message is too similar to recent ones."""
    message_lower = message_text.lower().strip()
    
    # Key phrases that indicate topic repetition
    key_phrases = []
    if len(message_lower) > 50:
        # Extract first ~50 chars as key phrase
        key_phrases.append(message_lower[:50])
    
    for prev_msg in recent_messages:
        prev_lower = prev_msg.lower()
        
        # Check for exact/near-exact matches
        if message_lower in prev_lower or prev_lower in message_lower:
            return True, f"Very similar to recent: {prev_msg[:80]}..."
        
        # Check for key phrase overlap
        for phrase in key_phrases:
            if phrase in prev_lower:
                return True, f"Similar topic to: {prev_msg[:80]}..."
    
    return False, None

def validate_message(message_text):
    """Validate message clarity and length."""
    issues = []
    
    if not message_text or len(message_text.strip()) < 10:
        issues.append("Message too short (<10 chars)")
    
    if len(message_text) > 600:
        issues.append("Message too long (>600 chars) - consider breaking up (recommended max 3-4 sentences)")
    
    return issues

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "gate": "pre_send_chat",
            "status": "FAIL",
            "error": "Usage: pre_send_chat.py '<message_text>'"
        }))
        sys.exit(1)
    
    message = sys.argv[1]
    
    # Load recent messages
    recent = load_recent_messages(10)
    
    # Run checks
    is_dup, dup_msg = check_duplicate(message, recent)
    validation_issues = validate_message(message)
    
    # Determine status
    status = "PASS"
    warnings = []
    errors = []
    
    if is_dup:
        status = "FAIL"
        errors.append(f"DUPLICATE: {dup_msg}")
    
    if validation_issues:
        warnings.extend(validation_issues)
    
    # Output JSON
    result = {
        "gate": "pre_send_chat",
        "status": status,
        "checks": {
            "duplicate_detected": is_dup,
            "message_length": len(message),
            "message_length_valid": len(message) >= 10 and len(message) <= 600,
            "recent_messages_checked": len(recent)
        },
        "warnings": warnings,
        "errors": errors,
        "timestamp": datetime.now().isoformat()
    }
    
    print(json.dumps(result, indent=2))
    
    # Exit code
    sys.exit(0 if status == "PASS" else 1)

if __name__ == '__main__':
    main()
