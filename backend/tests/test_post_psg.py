"""
Test script to post "vive le psg" with reduced latency.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("TEST: POST 'vive le psg'")
print("="*60)

validate_settings()
settings = get_settings()
email, password = settings.get_linkedin_credentials()

automation = LinkedInAutomation(browser_mode="visible")
automation.start_browser()

try:
    # Step 1: Login
    print("\n1. Logging in...")
    if not automation.login(email, password):
        print("❌ Login failed")
        exit(1)
    print("✅ Login successful")
    
    # Step 2: Navigate to post creation
    print("\n2. Navigating to post creation...")
    if not automation.navigate_to_post_creation():
        print("❌ Failed")
        exit(1)
    print("✅ Composer opened")
    
    # Step 3: Enter post text
    print("\n3. Entering post text...")
    post_text = "vive le psg"
    if not automation.enter_post_text(post_text):
        print("❌ Failed")
        exit(1)
    print("✅ Text entered")
    
    # Step 4: Click Post button
    print("\n4. Clicking Post button...")
    try:
        post_selectors = [
            'button:has-text("Post")',
            'button:has-text("Publier")',
            'button[aria-label*="Post" i]',
            'button[aria-label*="Publier" i]',
        ]
        
        posted = False
        for selector in post_selectors:
            try:
                post_btn = automation.page.locator(selector).first
                if post_btn.is_visible():
                    print(f"  ✅ Found Post button")
                    post_btn.click(timeout=5000)
                    time.sleep(3)
                    print("  ✅ Post button clicked!")
                    posted = True
                    break
            except:
                continue
        
        if posted:
            print("✅ Post published!")
        else:
            print("❌ Could not find Post button")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETED")
    print("="*60)
    print("\nBrowser open for 5 seconds to verify...")
    time.sleep(5)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    automation.close_browser()

