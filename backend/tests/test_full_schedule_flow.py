"""
Test script for full schedule flow: login -> post -> schedule -> date/time -> confirm.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("TEST: FULL SCHEDULE FLOW")
print("="*60)

validate_settings()
settings = get_settings()
email, password = settings.get_linkedin_credentials()

# Set date/time for tomorrow at 08:00
tomorrow = datetime.now() + timedelta(days=1)
scheduled_datetime = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)

print(f"\nScheduled date/time: {scheduled_datetime}")
print(f"Date: {scheduled_datetime.strftime('%Y-%m-%d')}")
print(f"Time: {scheduled_datetime.strftime('%H:%M')}")

automation = LinkedInAutomation(browser_mode="visible")
automation.start_browser()

try:
    # Step 1: Login
    print("\n" + "="*60)
    print("STEP 1: LOGIN")
    print("="*60)
    if not automation.login(email, password):
        print("❌ Login failed")
        exit(1)
    print("✅ Login successful")
    
    # Step 2: Navigate to post creation
    print("\n" + "="*60)
    print("STEP 2: NAVIGATE TO POST CREATION")
    print("="*60)
    if not automation.navigate_to_post_creation():
        print("❌ Failed to navigate to post creation")
        exit(1)
    print("✅ Composer opened")
    
    # Step 3: Enter post text
    print("\n" + "="*60)
    print("STEP 3: ENTER POST TEXT")
    print("="*60)
    test_text = "vive la france"
    if not automation.enter_post_text(test_text):
        print("❌ Failed to enter text")
        exit(1)
    print("✅ Text entered")
    
    # Step 4: Click Schedule button
    print("\n" + "="*60)
    print("STEP 4: CLICK SCHEDULE BUTTON")
    print("="*60)
    if not automation.click_schedule_button():
        print("❌ Failed to click Schedule button")
        exit(1)
    print("✅ Schedule button clicked!")
    
    # Step 5: Set date and time
    print("\n" + "="*60)
    print("STEP 5: SET DATE AND TIME")
    print("="*60)
    if not automation.set_scheduled_date_time(scheduled_datetime):
        print("⚠️  Failed to set date/time (may need manual check)")
        # Continue anyway to see what happens
    else:
        print("✅ Date and time set")
    
    # Step 6: Confirm schedule
    print("\n" + "="*60)
    print("STEP 6: CONFIRM SCHEDULE")
    print("="*60)
    if not automation.confirm_schedule():
        print("⚠️  Failed to confirm schedule (may need manual check)")
    else:
        print("✅ Schedule confirmed!")
    
    print("\n" + "="*60)
    print("✅ ALL STEPS COMPLETED")
    print("="*60)
    print("\nBrowser will stay open for 10 seconds to verify...")
    print("Check if the post was scheduled successfully in LinkedIn")
    time.sleep(10)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    automation.close_browser()

