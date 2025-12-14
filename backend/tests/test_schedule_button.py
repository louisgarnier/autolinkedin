"""
Test script for Schedule button functionality.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("TEST: CLICK SCHEDULE BUTTON")
print("="*60)

validate_settings()
settings = get_settings()
email, password = settings.get_linkedin_credentials()

automation = LinkedInAutomation(browser_mode="visible")
automation.start_browser()

try:
    # Login
    print("\n1. Logging in...")
    if not automation.login(email, password):
        print("❌ Login failed")
        exit(1)
    print("✅ Login successful")
    
    # Navigate to post creation
    print("\n2. Navigating to post creation...")
    if not automation.navigate_to_post_creation():
        print("❌ Failed to navigate to post creation")
        exit(1)
    print("✅ Composer opened")
    
    # Enter test text
    print("\n3. Entering test text...")
    test_text = "Test post for scheduling - please ignore"
    if not automation.enter_post_text(test_text):
        print("❌ Failed to enter text")
        exit(1)
    print("✅ Text entered")
    
    # Click Schedule button
    print("\n4. Clicking Schedule button...")
    if not automation.click_schedule_button():
        print("❌ Failed to click Schedule button")
        exit(1)
    print("✅ Schedule button clicked!")
    
    print("\n" + "="*60)
    print("✅ ALL STEPS COMPLETED")
    print("="*60)
    print("\nBrowser will stay open for 10 seconds to verify...")
    time.sleep(10)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    automation.close_browser()

