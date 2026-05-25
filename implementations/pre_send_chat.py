#!/usr/bin/env python3
"""
Executable guard for send_message_to_chat tool.
Prevents duplicate announcements by checking public_communications.md.

Usage:
  python3 pre_send_chat.py

Prompts for 4 required fields before sending:
1. Purpose: Why sending this message?
2. Recipient: Who is it for? (@agent or general)
3. Content summary: What will you say?
4. Duplicate check: Have you said this before?

Then displays recent communications and asks for confirmation.
"""

import os
import sys
from datetime import datetime

REPO_PATH = "/home/computeruse/memory-improvement"
COMMS_FILE = f"{REPO_PATH}/memory-artifacts/public_communications.md"

def load_public_comms():
    """Load and parse public communications log."""
    if not os.path.exists(COMMS_FILE):
        return "⚠️  public_communications.md not found!"
    
    with open(COMMS_FILE, 'r') as f:
        return f.read()

def display_recent_comms(comms_text):
    """Display recent messages sent."""
    print("\n" + "="*60)
    print("RECENT COMMUNICATIONS (Last 20 lines):")
    print("="*60)
    lines = comms_text.split('\n')
    recent = lines[-20:] if len(lines) > 20 else lines
    for line in recent:
        if line.strip():
            print(line)
    print("="*60 + "\n")

def check_for_duplicates(comms_text, content_summary):
    """Simple keyword check for potential duplicates."""
    keywords = content_summary.lower().split()
    matches = []
    
    for line in comms_text.split('\n'):
        if '**DO NOT REPEAT**' in line:
            matches.append(f"⚠️  {line.strip()}")
        elif any(kw in line.lower() for kw in keywords if len(kw) > 4):
            if '- **[' in line or 'Content:' in line:
                matches.append(f"   {line.strip()}")
    
    return matches

def main():
    print("\n" + "="*60)
    print("PRE-SEND CHAT GUARD")
    print("="*60)
    print("This script helps prevent duplicate announcements.")
    print("Please answer the following questions:\n")
    
    # Required fields
    purpose = input("1. PURPOSE - Why are you sending this? ").strip()
    if not purpose:
        print("❌ Purpose required. Aborting.")
        sys.exit(1)
    
    recipient = input("2. RECIPIENT - Who is it for? (@agent or 'general') ").strip()
    if not recipient:
        print("❌ Recipient required. Aborting.")
        sys.exit(1)
    
    content_summary = input("3. CONTENT SUMMARY - What will you say? (brief) ").strip()
    if not content_summary:
        print("❌ Content summary required. Aborting.")
        sys.exit(1)
    
    # Load and display recent comms
    comms_text = load_public_comms()
    display_recent_comms(comms_text)
    
    # Check for potential duplicates
    print("DUPLICATE CHECK:")
    print("-" * 60)
    potential_duplicates = check_for_duplicates(comms_text, content_summary)
    
    if potential_duplicates:
        print("⚠️  POTENTIAL DUPLICATES FOUND:")
        for dup in potential_duplicates[:5]:  # Show max 5
            print(dup)
        print("-" * 60)
    else:
        print("✅ No obvious duplicates detected.")
        print("-" * 60)
    
    # Final confirmation
    print(f"\nYou are about to send:")
    print(f"  Purpose: {purpose}")
    print(f"  Recipient: {recipient}")
    print(f"  Content: {content_summary}")
    
    duplicate_check = input("\n4. DUPLICATE CHECK - Have you already sent similar message? (yes/no) ").strip().lower()
    
    if duplicate_check == 'yes':
        print("\n❌ BLOCKED: You confirmed this is a duplicate.")
        print("   Consider whether this message provides NEW value.")
        sys.exit(1)
    elif duplicate_check == 'no':
        print("\n✅ APPROVED: Proceed with sending message.")
        print("   Remember to log this in public_communications.md after sending!")
        sys.exit(0)
    else:
        print("\n❌ BLOCKED: Answer must be 'yes' or 'no'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
