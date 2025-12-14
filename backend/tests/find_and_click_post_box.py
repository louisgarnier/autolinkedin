"""
Simple script: login, find the "Start a post" box, click it.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("FIND AND CLICK POST BOX")
print("="*60)

validate_settings()
settings = get_settings()
email, password = settings.get_linkedin_credentials()

automation = LinkedInAutomation(browser_mode="visible")
automation.start_browser()

print("\n1. Logging in...")
success = automation.login(email, password)
if not success:
    print("⚠️  Login returned False, but continuing anyway...")
    time.sleep(2)

print("\n2. Going to feed...")
automation.page.goto("https://www.linkedin.com/feed/")
time.sleep(5)

print("\n3. Looking for 'Start a post' box...")
print("-" * 60)

# Try to find the box that contains "Start a post" text
# We'll try clicking on the text itself first
try:
    start_post = automation.page.locator('text="Start a post"').first
    if start_post.is_visible():
        print("✅ Found 'Start a post' text")
        print("   Clicking...")
        start_post.click()
        time.sleep(3)
        print("✅ Clicked!")
        
        # Check if composer opened
        composer = automation.page.locator('div[contenteditable="true"]').first
        if composer.is_visible():
            print("✅ Composer is open!")
        else:
            print("⚠️  Composer not visible yet")
    else:
        print("❌ 'Start a post' text not visible")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Browser open for 30 seconds - check if composer opened")
print("="*60)
time.sleep(30)

automation.close_browser()

