"""
Test script for main application integration (Step 5).

This script tests the full flow:
1. Read Google Sheets
2. Find post for today
3. Post to LinkedIn
4. Update status
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.main import main

print("="*60)
print("TEST: MAIN APPLICATION INTEGRATION (STEP 5)")
print("="*60)
print("\nThis will:")
print("1. Connect to Google Sheets")
print("2. Find post with today's date")
print("3. Post to LinkedIn")
print("4. Update status to 'yes'")
print("\n" + "="*60)

if __name__ == "__main__":
    exit_code = main()
    if exit_code == 0:
        print("\n✅ TEST PASSED")
    else:
        print("\n❌ TEST FAILED")
    sys.exit(exit_code)

