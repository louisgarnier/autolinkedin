"""
Debug script to find date/time fields in schedule modal.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("DEBUG: FIND DATE/TIME FIELDS IN SCHEDULE MODAL")
print("="*60)

validate_settings()
settings = get_settings()
email, password = settings.get_linkedin_credentials()

automation = LinkedInAutomation(browser_mode="visible")
automation.start_browser()

try:
    # Login
    if not automation.login(email, password):
        exit(1)
    
    # Navigate and enter text
    automation.navigate_to_post_creation()
    automation.enter_post_text("vive la france")
    
    # Click Schedule
    automation.click_schedule_button()
    
    # Wait for modal
    print("\nWaiting for schedule modal...")
    time.sleep(3)
    automation.take_screenshot("debug_schedule_modal_full")
    
    # List ALL visible elements
    print("\n" + "="*60)
    print("ALL VISIBLE ELEMENTS IN MODAL")
    print("="*60)
    
    # All divs
    print("\n--- DIVs ---")
    divs = automation.page.locator('div').all()
    visible_divs = []
    for i, div in enumerate(divs[:50]):
        try:
            if div.is_visible():
                text = div.inner_text()[:100] if div.inner_text() else ""
                classes = div.get_attribute('class') or ""
                role = div.get_attribute('role') or ""
                if text or 'date' in (text + classes + role).lower() or 'time' in (text + classes + role).lower() or 'heure' in (text + classes + role).lower():
                    print(f"  Div {i}: role='{role}', text='{text[:50]}', class='{classes[:50]}'")
                    visible_divs.append((i, text, classes, role))
        except:
            pass
    
    # All buttons
    print("\n--- BUTTONs ---")
    buttons = automation.page.locator('button').all()
    for i, btn in enumerate(buttons[:20]):
        try:
            if btn.is_visible():
                text = btn.inner_text()[:50] if btn.inner_text() else ""
                aria = btn.get_attribute('aria-label') or ""
                print(f"  Button {i}: text='{text}', aria-label='{aria}'")
        except:
            pass
    
    # All inputs
    print("\n--- INPUTs ---")
    inputs = automation.page.locator('input').all()
    for i, inp in enumerate(inputs[:10]):
        try:
            if inp.is_visible():
                inp_type = inp.get_attribute('type') or ""
                placeholder = inp.get_attribute('placeholder') or ""
                aria = inp.get_attribute('aria-label') or ""
                value = inp.input_value() or ""
                print(f"  Input {i}: type='{inp_type}', placeholder='{placeholder}', aria-label='{aria}', value='{value}'")
        except:
            pass
    
    print("\n" + "="*60)
    print("Browser open for 10 seconds - check screenshot")
    print("="*60)
    time.sleep(10)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    automation.close_browser()

