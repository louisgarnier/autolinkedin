"""
Debug script to inspect LinkedIn page after login.

This script logs into LinkedIn and then inspects the page to find
the post creation area (encadré/box) instead of a button.
"""

import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def debug_linkedin_feed_page():
    """Debug: Inspect the LinkedIn feed page to find post creation area."""
    print("\n" + "="*60)
    print("DEBUG: LINKEDIN FEED PAGE INSPECTION")
    print("="*60)
    
    automation = None
    try:
        # Validate settings
        validate_settings()
        settings = get_settings()
        email, password = settings.get_linkedin_credentials()
        
        # Start browser and login
        automation = LinkedInAutomation(browser_mode="visible")
        automation.start_browser()
        
        print("\n🔐 Logging into LinkedIn...")
        login_success = automation.login(email, password)
        
        if not login_success:
            print("⚠️  Login returned False, but checking if we're actually logged in...")
            # Check if page is still open and we're on feed
            try:
                if not automation.page.is_closed():
                    current_url = automation.page.url
                    print(f"Current URL: {current_url}")
                    if "feed" in current_url or "linkedin.com/in/" in current_url:
                        print("✅ Actually logged in! (URL shows feed/profile)")
                        login_success = True
                    else:
                        print("❌ Not on feed page, trying to navigate...")
                        automation.page.goto("https://www.linkedin.com/feed/")
                        import time
                        time.sleep(5)
                        if "feed" in automation.page.url:
                            login_success = True
                else:
                    print("❌ Page is closed, cannot continue")
                    return
            except Exception as e:
                print(f"❌ Error checking login status: {e}")
                return
        
        if not login_success:
            print("❌ Login failed, cannot continue")
            return
        
        print("✅ Login successful")
        
        # Make sure we're on feed page
        print("\n📄 Ensuring we're on feed page...")
        try:
            if automation.page.is_closed():
                print("❌ Page is closed!")
                return
            
            current_url = automation.page.url
            if "feed" not in current_url:
                print(f"Not on feed (current: {current_url}), navigating...")
                automation.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            
            import time
            time.sleep(5)
            print(f"✅ On feed page: {automation.page.url}")
        except Exception as e:
            print(f"❌ Error navigating to feed: {e}")
            return
        
        print("\n" + "="*60)
        print("INSPECTING PAGE ELEMENTS")
        print("="*60)
        
        # Take screenshot
        automation.take_screenshot("debug_feed_page")
        print(f"\n📸 Screenshot saved")
        
        # Look for all divs that might be the post creation box
        print("\n🔍 Looking for post creation boxes/encadrés...")
        
        # Common selectors for post creation boxes
        box_selectors = [
            'div[data-control-name="composer"]',
            'div.share-box',
            'div.share-box__inner',
            'div[class*="share-box"]',
            'div[class*="composer"]',
            'div[class*="post"]',
            'div[role="textbox"]',
            'div[contenteditable="true"]',
            'div[data-placeholder]',
        ]
        
        print("\n--- Checking box selectors ---")
        for selector in box_selectors:
            try:
                elements = automation.page.locator(selector)
                count = elements.count()
                if count > 0:
                    print(f"\n✅ Found {count} elements with: {selector}")
                    for i in range(min(count, 3)):
                        try:
                            elem = elements.nth(i)
                            is_visible = elem.is_visible()
                            text = elem.inner_text()[:100] if elem.inner_text() else "N/A"
                            classes = elem.get_attribute('class') or "N/A"
                            print(f"  Element {i}: visible={is_visible}, text='{text}', class='{classes[:50]}'")
                        except Exception as e:
                            print(f"  Element {i}: Error - {e}")
            except Exception as e:
                print(f"❌ Selector {selector}: Error - {e}")
        
        # Look for all clickable divs in the top area
        print("\n--- Looking for clickable divs in top area ---")
        try:
            # Get all divs
            all_divs = automation.page.locator('div').all()
            print(f"Found {len(all_divs)} divs on page")
            
            # Check first 20 divs for clickable/visible ones
            clickable_found = 0
            for i, div in enumerate(all_divs[:20]):
                try:
                    if div.is_visible():
                        text = div.inner_text()[:80] if div.inner_text() else ""
                        classes = div.get_attribute('class') or ""
                        placeholder = div.get_attribute('data-placeholder') or ""
                        role = div.get_attribute('role') or ""
                        
                        # Check if it looks like a post creation area
                        if any(keyword in (text + classes + placeholder).lower() for keyword in ['post', 'share', 'what', 'talk', 'mind']):
                            print(f"\n  🎯 Potential post box {clickable_found}:")
                            print(f"    Text: '{text}'")
                            print(f"    Class: '{classes[:80]}'")
                            print(f"    Placeholder: '{placeholder}'")
                            print(f"    Role: '{role}'")
                            clickable_found += 1
                except:
                    pass
        except Exception as e:
            print(f"Error inspecting divs: {e}")
        
        # Look for all buttons
        print("\n--- Looking for buttons with 'post' or 'share' ---")
        try:
            buttons = automation.page.locator('button').all()
            print(f"Found {len(buttons)} buttons")
            for i, button in enumerate(buttons[:15]):
                try:
                    if button.is_visible():
                        text = button.inner_text()[:50] if button.inner_text() else ""
                        aria_label = button.get_attribute('aria-label') or ""
                        if 'post' in (text + aria_label).lower() or 'share' in (text + aria_label).lower():
                            print(f"  Button {i}: text='{text}', aria-label='{aria_label}'")
                except:
                    pass
        except Exception as e:
            print(f"Error inspecting buttons: {e}")
        
        # Look for spans with "Start a post" or similar
        print("\n--- Looking for text 'Start a post' or similar ---")
        try:
            text_selectors = [
                '*:has-text("Start a post")',
                '*:has-text("start a post" i)',
                '*:has-text("What do you want to talk about")',
                '*:has-text("What\'s on your mind")',
            ]
            for selector in text_selectors:
                try:
                    elements = automation.page.locator(selector)
                    count = elements.count()
                    if count > 0:
                        print(f"  ✅ Found {count} elements with text selector: {selector}")
                        for i in range(min(count, 3)):
                            try:
                                elem = elements.nth(i)
                                tag = elem.evaluate("el => el.tagName")
                                text = elem.inner_text()[:80]
                                print(f"    {i}: <{tag}> '{text}'")
                            except:
                                pass
                except:
                    pass
        except Exception as e:
            print(f"Error finding text: {e}")
        
        print("\n" + "="*60)
        print("DEBUG COMPLETE")
        print("="*60)
        print("\nBrowser will stay open for 30 seconds for manual inspection...")
        print("Look at the page and identify the post creation encadré/box")
        time.sleep(30)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if automation:
            try:
                automation.close_browser()
            except:
                pass


if __name__ == "__main__":
    debug_linkedin_feed_page()

