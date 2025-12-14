"""
Debug script to inspect the schedule modal and find date/time fields.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("DEBUG: INSPECT SCHEDULE MODAL")
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
        print("❌ Failed")
        exit(1)
    print("✅ Composer opened")
    
    # Enter text
    print("\n3. Entering text...")
    if not automation.enter_post_text("vive la france"):
        print("❌ Failed")
        exit(1)
    print("✅ Text entered")
    
    # Click Schedule
    print("\n4. Clicking Schedule...")
    if not automation.click_schedule_button():
        print("❌ Failed")
        exit(1)
    print("✅ Schedule clicked")
    
    # Wait for modal
    print("\n5. Waiting for schedule modal...")
    time.sleep(5)
    automation.take_screenshot("debug_schedule_modal")
    
    # Inspect all inputs
    print("\n6. Looking for input fields...")
    inputs = automation.page.locator('input').all()
    print(f"Found {len(inputs)} input elements")
    
    for i, inp in enumerate(inputs[:10]):
        try:
            if inp.is_visible():
                input_type = inp.get_attribute('type') or "N/A"
                placeholder = inp.get_attribute('placeholder') or "N/A"
                aria_label = inp.get_attribute('aria-label') or "N/A"
                value = inp.input_value() or "N/A"
                print(f"\n  Input {i}:")
                print(f"    Type: {input_type}")
                print(f"    Placeholder: {placeholder}")
                print(f"    Aria-label: {aria_label}")
                print(f"    Value: {value}")
        except:
            pass
    
    # Look for divs that might be date/time pickers
    print("\n7. Looking for date/time related elements...")
    date_time_selectors = [
        '*:has-text("date" i)',
        '*:has-text("time" i)',
        '*:has-text("heure" i)',
        'div[role="textbox"]',
        'div[contenteditable="true"]',
    ]
    
    for selector in date_time_selectors:
        try:
            elements = automation.page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"\n  Found {count} elements with: {selector}")
                for i in range(min(count, 5)):
                    try:
                        elem = elements.nth(i)
                        if elem.is_visible():
                            text = elem.inner_text()[:100]
                            print(f"    Element {i}: '{text}'")
                    except:
                        pass
        except:
            pass
    
    print("\n" + "="*60)
    print("Browser open for 60 seconds - inspect the modal manually")
    print("="*60)
    time.sleep(60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    automation.close_browser()

