"""
Simple debug script - just login and inspect the page.
NO modifications, just inspection.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

print("="*60)
print("SIMPLE DEBUG - INSPECT PAGE ONLY")
print("="*60)

validate_settings()
settings = get_settings()
email, password = settings.get_linkedin_credentials()

automation = LinkedInAutomation(browser_mode="visible")
automation.start_browser()

print("\n1. Logging in...")
if automation.login(email, password):
    print("✅ Login OK")
else:
    print("❌ Login failed")
    automation.close_browser()
    exit(1)

print("\n2. Going to feed...")
automation.page.goto("https://www.linkedin.com/feed/")
time.sleep(5)

print("\n3. Looking for 'Start a post' encadré...")
print("-" * 60)

# Strategy 1: Find divs that contain BOTH "Start a post" AND "Video" or "Photo"
print("\nLooking for divs with 'Start a post' AND 'Video'...")
combined = automation.page.locator('div:has-text("Start a post"):has-text("Video")').all()
print(f"Found {len(combined)} divs with both")

for i, div in enumerate(combined[:3]):
    try:
        if div.is_visible():
            text = div.inner_text()[:300]
            classes = div.get_attribute('class') or ""
            print(f"\n✅ Div {i} (has both):")
            print(f"  Text preview: {text}")
            print(f"  Classes: {classes[:150]}")
    except Exception as e:
        print(f"  Error: {e}")

# Strategy 2: Find the text "Start a post" and get its parent
print("\n\nLooking for 'Start a post' text element and its parents...")
start_post_text = automation.page.locator('text="Start a post"').first
if start_post_text.is_visible():
    print("✅ Found 'Start a post' text element")
    
    # Get parent
    try:
        parent = start_post_text.locator('xpath=..').first
        if parent.is_visible():
            parent_text = parent.inner_text()[:300]
            parent_classes = parent.get_attribute('class') or ""
            print(f"  Parent text: {parent_text}")
            print(f"  Parent classes: {parent_classes[:150]}")
            print(f"  Parent has Video/Photo/Write? {('Video' in parent_text or 'Photo' in parent_text or 'Write' in parent_text)}")
    except:
        pass
    
    # Get grandparent
    try:
        grandparent = start_post_text.locator('xpath=../..').first
        if grandparent.is_visible():
            gp_text = grandparent.inner_text()[:300]
            gp_classes = grandparent.get_attribute('class') or ""
            print(f"  Grandparent text: {gp_text}")
            print(f"  Grandparent classes: {gp_classes[:150]}")
            print(f"  Grandparent has Video/Photo/Write? {('Video' in gp_text or 'Photo' in gp_text or 'Write' in gp_text)}")
    except:
        pass
else:
    print("❌ 'Start a post' text not found")

# Strategy 3: Look for common LinkedIn composer selectors
print("\n\nLooking for common composer/share-box selectors...")
selectors_to_try = [
    'div[data-control-name="composer"]',
    'div.share-box',
    'div[class*="share-box"]',
    'div[class*="composer"]',
]

for selector in selectors_to_try:
    try:
        elements = automation.page.locator(selector)
        count = elements.count()
        if count > 0:
            print(f"\n✅ Found {count} elements with: {selector}")
            for i in range(min(count, 2)):
                try:
                    elem = elements.nth(i)
                    if elem.is_visible():
                        text = elem.inner_text()[:200]
                        classes = elem.get_attribute('class') or ""
                        print(f"  Element {i}:")
                        print(f"    Text: {text}")
                        print(f"    Has 'Start a post'? {'Start a post' in text}")
                        print(f"    Has Video/Photo/Write? {('Video' in text or 'Photo' in text or 'Write' in text)}")
                except:
                    pass
    except:
        pass

print("\n" + "="*60)
print("Browser will stay open 60 seconds for manual inspection")
print("Look at the page and tell me which element to click")
print("="*60)

time.sleep(60)
automation.close_browser()

