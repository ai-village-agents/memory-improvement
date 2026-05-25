#!/usr/bin/env python3
"""
Non-interactive public communications checker.
Displays recent messages and DO NOT REPEAT items.
Use this for quick reference before sending messages.
"""

import os
import sys

REPO_PATH = "/home/computeruse/memory-improvement"
COMMS_FILE = f"{REPO_PATH}/memory-artifacts/public_communications.md"

def main():
    if not os.path.exists(COMMS_FILE):
        print("⚠️  public_communications.md not found!")
        sys.exit(1)
    
    with open(COMMS_FILE, 'r') as f:
        content = f.read()
    
    print("="*70)
    print("PUBLIC COMMUNICATIONS LOG - QUICK REFERENCE")
    print("="*70)
    print()
    
    # Extract DO NOT REPEAT items
    do_not_repeat = []
    in_dnr_section = False
    for line in content.split('\n'):
        if '## Key Messages NOT to Repeat' in line:
            in_dnr_section = True
            continue
        if in_dnr_section:
            if line.startswith('##'):
                break
            if line.strip() and line.strip().startswith(('❌', '-', '*')):
                do_not_repeat.append(line.strip())
    
    if do_not_repeat:
        print("🚫 DO NOT REPEAT:")
        for item in do_not_repeat:
            print(f"  {item}")
        print()
    
    # Show last session's messages
    print("📝 RECENT MESSAGES (last 30 lines):")
    print("-" * 70)
    lines = content.split('\n')
    for line in lines[-30:]:
        if line.strip():
            print(line)
    
    print("="*70)
    print()
    print("✅ Before sending: Does your message repeat any of the above?")
    print("✅ Does it provide NEW value to the conversation?")
    print()

if __name__ == '__main__':
    main()
