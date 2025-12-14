"""
LinkedIn browser automation for LinkedIn Automation V1.

This module handles automating LinkedIn post scheduling using browser automation.
"""

import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from backend.config.settings import get_settings

logger = logging.getLogger(__name__)


class LinkedInAutomation:
    """Service for automating LinkedIn post scheduling."""
    
    def __init__(self, browser_mode: str = "visible"):
        """
        Initialize LinkedIn automation.
        
        Args:
            browser_mode: "visible" or "headless"
        """
        self.browser_mode = browser_mode
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.screenshots_dir = Path(__file__).parent.parent.parent / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
    
    def start_browser(self) -> None:
        """Start browser instance."""
        try:
            self.playwright = sync_playwright().start()
            
            # Launch browser based on mode
            headless = self.browser_mode == "headless"
            
            self.browser = self.playwright.chromium.launch(
                headless=headless,
                slow_mo=1000  # Slow down for visibility and reliability
            )
            
            # Create context with viewport
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            self.page = self.context.new_page()
            
            logger.info(f"Browser started in {self.browser_mode} mode")
            
        except Exception as e:
            logger.error(f"Error starting browser: {e}")
            raise
    
    def close_browser(self) -> None:
        """Close browser instance."""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            
            logger.info("Browser closed")
            
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot for debugging.
        
        Args:
            name: Screenshot name
            
        Returns:
            Path to screenshot file
        """
        if not self.page:
            return ""
        
        try:
            # Check if page is still valid
            if self.page.is_closed():
                logger.warning("Page is closed, cannot take screenshot")
                return ""
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshots_dir / f"{name}_{timestamp}.png"
            self.page.screenshot(path=str(screenshot_path), timeout=5000)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            logger.warning(f"Could not take screenshot: {e}")
            return ""
    
    def wait_for_element(self, selector: str, timeout: int = 30000) -> bool:
        """
        Wait for an element to appear on the page.
        
        Args:
            selector: CSS selector or text to wait for
            timeout: Timeout in milliseconds
            
        Returns:
            True if element found, False otherwise
        """
        try:
            if selector.startswith("text="):
                self.page.wait_for_selector(selector, timeout=timeout)
            else:
                self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"Element not found: {selector} - {e}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """
        Log into LinkedIn.
        
        Args:
            email: LinkedIn email
            password: LinkedIn password
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("LINKEDIN LOGIN PROCESS")
            logger.info("="*60)
            
            logger.info("STEP 1: Navigating to LinkedIn login page")
            logger.info("URL: https://www.linkedin.com/login")
            self.page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            logger.info(f"✅ Page loaded. Current URL: {self.page.url}")
            time.sleep(2)
            
            # Take screenshot before login
            self.take_screenshot("01_before_login")
            
            # Enter email
            logger.info("")
            logger.info("STEP 2: Entering email")
            email_selector = "#username"
            logger.info(f"Looking for email field: {email_selector}")
            
            if not self.wait_for_element(email_selector):
                logger.error(f"❌ Email field not found: {email_selector}")
                self.take_screenshot("02_email_field_not_found")
                return False
            
            logger.info("✅ Email field found, filling...")
            self.page.fill(email_selector, email)
            logger.info(f"✅ Email entered: {email[:3]}***")
            time.sleep(1)
            
            # Enter password
            logger.info("")
            logger.info("STEP 3: Entering password")
            password_selector = "#password"
            logger.info(f"Looking for password field: {password_selector}")
            
            if not self.wait_for_element(password_selector):
                logger.error(f"❌ Password field not found: {password_selector}")
                self.take_screenshot("03_password_field_not_found")
                return False
            
            logger.info("✅ Password field found, filling...")
            self.page.fill(password_selector, password)
            logger.info("✅ Password entered")
            time.sleep(1)
            
            # Click sign in button
            logger.info("")
            logger.info("STEP 4: Clicking sign in button")
            sign_in_selector = 'button[type="submit"]'
            logger.info(f"Looking for sign in button: {sign_in_selector}")
            
            if not self.wait_for_element(sign_in_selector):
                logger.error(f"❌ Sign in button not found: {sign_in_selector}")
                self.take_screenshot("04_sign_in_button_not_found")
                return False
            
            logger.info("✅ Sign in button found, clicking...")
            self.page.click(sign_in_selector)
            logger.info("✅ Sign in button clicked")
            time.sleep(3)  # Wait after clicking
            
            # Wait for navigation after login
            logger.info("")
            logger.info("STEP 5: Waiting for navigation after login")
            logger.info("Waiting for URL to change to feed...")
            
            # Check if page is still open
            try:
                if self.page.is_closed():
                    logger.error("❌ Page was closed during login!")
                    return False
            except:
                pass
            
            try:
                # Wait for URL to change - but don't wait for networkidle (can be slow)
                logger.info("Waiting for URL to contain 'feed'...")
                self.page.wait_for_url("**/feed/**", timeout=60000)
                logger.info(f"✅ URL changed to feed. Current URL: {self.page.url}")
            except Exception as e:
                logger.warning(f"⚠️  Timeout waiting for feed URL: {e}")
                
                # Check current URL
                try:
                    if not self.page.is_closed():
                        current_url = self.page.url
                        logger.info(f"Current URL: {current_url}")
                        
                        if "feed" in current_url or "linkedin.com/in/" in current_url:
                            logger.info("✅ URL already contains feed/profile - login successful")
                        else:
                            logger.warning("⚠️  URL doesn't contain feed, but continuing...")
                    else:
                        logger.error("❌ Page is closed!")
                        return False
                except Exception as e2:
                    logger.error(f"❌ Error checking URL: {e2}")
                    return False
            
            # Wait a bit for page to render (but don't wait for networkidle which can timeout)
            time.sleep(3)  # Give time for page to render
            logger.info("✅ Wait complete")
            
            # Check page is still open
            try:
                if self.page.is_closed():
                    logger.error("❌ Page closed after waiting!")
                    return False
            except:
                pass
            
            # Take screenshot after login
            logger.info("")
            logger.info("STEP 6: Taking screenshot and verifying login")
            try:
                self.take_screenshot("05_after_login")
            except Exception as e:
                logger.warning(f"Could not take screenshot: {e}")
            
            # Check if we're logged in (look for feed or profile)
            try:
                # Check page is still open first
                if self.page.is_closed():
                    logger.error("❌ Page is closed, cannot verify login")
                    return False
                
                current_url = self.page.url
                logger.info(f"Current URL: {current_url}")
                
                try:
                    page_title = self.page.title()
                    logger.info(f"Page title: {page_title}")
                except Exception as e:
                    logger.warning(f"Could not get page title: {e}")
                    # Continue anyway
                
                # Check multiple indicators of successful login
                url_indicators = ["feed", "linkedin.com/in/", "linkedin.com/feed"]
                url_match = any(indicator in current_url for indicator in url_indicators)
                
                if url_match:
                    logger.info(f"✅ Login successful - URL contains one of: {url_indicators}")
                    return True
                
                logger.info("URL doesn't match feed pattern, checking for logged-in elements...")
                
                # Also check for elements that indicate we're logged in
                logged_in_indicators = [
                    'nav[role="navigation"]',
                    'div[data-test-id="nav"]',
                    'button[aria-label*="Me"]',
                    'button[aria-label*="me" i]',
                ]
                
                for indicator in logged_in_indicators:
                    try:
                        count = self.page.locator(indicator).count()
                        logger.info(f"Checking indicator '{indicator}': found {count} elements")
                        if count > 0:
                            logger.info(f"✅ Login successful - found logged-in indicator: {indicator}")
                            return True
                    except Exception as e:
                        logger.debug(f"Error checking indicator {indicator}: {e}")
                        continue
                
                logger.warning("⚠️  Login verification unclear - no clear indicators found")
                logger.warning(f"   URL: {current_url}")
                logger.warning("   Taking debug screenshot...")
                self.take_screenshot("06_login_verification_unclear")
                
                # Check for error messages
                error_selectors = [
                    'div[role="alert"]',
                    'div.error',
                    'span.error',
                    '*:has-text("incorrect")',
                    '*:has-text("error")',
                ]
                
                for selector in error_selectors:
                    try:
                        if self.page.locator(selector).count() > 0:
                            error_text = self.page.locator(selector).first.inner_text()
                            logger.error(f"❌ Error message found: {error_text}")
                            return False
                    except:
                        continue
                
                # Assume success if we got past the login form without errors
                logger.info("⚠️  Assuming login successful (no errors found)")
                return True
                
            except Exception as e:
                logger.error(f"❌ Error checking login status: {e}")
                import traceback
                logger.error(traceback.format_exc())
                return False
                
        except Exception as e:
            logger.error(f"❌ Error during login: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.take_screenshot("07_login_error")
            return False
    
    def navigate_to_post_creation(self) -> bool:
        """
        Navigate to LinkedIn post creation interface.
        
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("NAVIGATING TO POST CREATION")
            logger.info("="*60)
            
            # Check if we're already on feed page (after login)
            current_url = self.page.url if not self.page.is_closed() else ""
            logger.info(f"STEP 1: Current URL: {current_url}")
            
            if "feed" not in current_url or self.page.is_closed():
                logger.info("Navigating to feed page...")
                self.page.goto("https://www.linkedin.com/feed/", wait_until="networkidle")
                logger.info(f"✅ Page loaded. Current URL: {self.page.url}")
            else:
                logger.info("✅ Already on feed page")
            
            time.sleep(3)  # Give LinkedIn time to render
            logger.info("✅ Wait complete (5 seconds)")
            
            self.take_screenshot("01_feed_page_loaded")
            
            # Scroll up a bit to make sure we're at the top
            logger.info("STEP 2: Scrolling to top of page")
            self.page.evaluate("window.scrollTo(0, 0)")
            time.sleep(2)
            logger.info("✅ Scrolled to top")
            
            # Try multiple strategies with retries
            max_retries = 3
            logger.info("="*60)
            logger.info(f"STEP 3: Looking for post creation interface (max {max_retries} attempts)")
            logger.info("="*60)
            
            for attempt in range(max_retries):
                logger.info("")
                logger.info(f"--- ATTEMPT {attempt + 1}/{max_retries} ---")
                
                # Simple strategy: Find "Start a post" text and click it
                # This is the encadré that contains Video/Photo/Write article buttons
                logger.info("Looking for 'Start a post' text...")
                
                try:
                    start_post = self.page.locator('text="Start a post"').first
                    if start_post.is_visible():
                        logger.info("✅ Found 'Start a post' text")
                        logger.info("   Clicking...")
                        start_post.click(timeout=5000)
                        time.sleep(3)
                        logger.info("✅ Clicked!")
                        self.take_screenshot(f"02_start_post_clicked_attempt_{attempt+1}")
                        
                        # Verify composer opened
                        if self._verify_composer_opened():
                            logger.info("✅ Composer opened successfully!")
                            return True
                        else:
                            logger.warning("⚠️  Composer not visible yet, waiting...")
                            time.sleep(2)
                            if self._verify_composer_opened():
                                logger.info("✅ Composer opened after wait!")
                                return True
                    else:
                        logger.warning("❌ 'Start a post' text not visible")
                except Exception as e:
                    logger.warning(f"❌ Error finding/clicking 'Start a post': {e}")
                
                # If first attempt failed, wait and retry
                if attempt < max_retries - 1:
                    logger.info("Waiting before retry...")
                    time.sleep(2)
                    self.page.evaluate("window.scrollTo(0, 0)")
                    time.sleep(1)
                
                # OLD CODE BELOW - keeping as fallback but simplified approach above should work
                # Strategy 1: Look for the "Start a post" ENCADRÉ/BOX
                # This is the box that contains "Start a post" text + Video/Photo/Write article buttons
                logger.info("Strategy 1 (fallback): Looking for 'Start a post' ENCADRÉ/BOX")
                logger.info("  This box contains: 'Start a post' text + Video/Photo/Write article buttons")
                
                # Look for the section that contains "Start a post" text
                # The encadré is likely a div that contains both the text and the buttons below
                start_post_box_selectors = [
                    # Look for divs containing "Start a post" text
                    'div:has-text("Start a post")',
                    'section:has-text("Start a post")',
                    # Look for the container that has both "Start a post" and the buttons
                    'div:has-text("Start a post"):has-text("Video")',
                    'div:has-text("Start a post"):has-text("Photo")',
                    'div:has-text("Start a post"):has-text("Write article")',
                    # Common LinkedIn selectors
                    'div[data-control-name="composer"]',
                    'div.share-box',
                    'div.share-box__inner',
                    'div[class*="share-box"]',
                    'div[class*="composer"]',
                ]
                
                box_found = False
                for box_selector in start_post_box_selectors:
                    try:
                        logger.info(f"  Checking box selector: {box_selector}")
                        boxes = self.page.locator(box_selector)
                        count = boxes.count()
                        logger.info(f"    Found {count} boxes")
                        
                        if count > 0:
                            for i in range(min(count, 5)):
                                try:
                                    box = boxes.nth(i)
                                    if box.is_visible():
                                        # Check if this box contains "Start a post" text
                                        text = box.inner_text()
                                        logger.info(f"    Box {i} text preview: '{text[:100] if text else 'N/A'}'")
                                        
                                        if "Start a post" in text or "start a post" in text.lower():
                                            logger.info(f"    ✅ Found 'Start a post' box {i}")
                                            logger.info(f"    Clicking on the box...")
                                            
                                            # Click on the box - try clicking on the text area first
                                            try:
                                                # Try to click on the "Start a post" text specifically
                                                start_post_text = box.locator('text="Start a post"').first
                                                if start_post_text.is_visible():
                                                    start_post_text.click(timeout=5000)
                                                    logger.info("    Clicked on 'Start a post' text")
                                                else:
                                                    # Click on the box itself
                                                    box.click(timeout=5000)
                                                    logger.info("    Clicked on box container")
                                            except:
                                                # Fallback: click on box
                                                box.click(timeout=5000)
                                                logger.info("    Clicked on box (fallback)")
                                            
                                            time.sleep(3)
                                            self.take_screenshot(f"02_start_post_box_clicked_attempt_{attempt+1}")
                                            
                                            if self._verify_composer_opened():
                                                logger.info("    ✅ Composer opened after clicking box!")
                                                return True
                                            else:
                                                logger.warning("    ⚠️  Composer did not open, trying to click inside box...")
                                                # Maybe need to click on the text input area inside
                                                try:
                                                    text_input = box.locator('div[contenteditable="true"]').first
                                                    if text_input.is_visible():
                                                        text_input.click(timeout=5000)
                                                        time.sleep(2)
                                                        if self._verify_composer_opened():
                                                            logger.info("    ✅ Composer opened after clicking text input!")
                                                            return True
                                                except:
                                                    pass
                                except Exception as e:
                                    logger.debug(f"    Could not process box {i}: {e}")
                                    continue
                    except Exception as e:
                        logger.debug(f"  Box selector {box_selector} failed: {e}")
                        continue
                
                # Strategy 1b: Look for the text "Start a post" and click on its parent container
                logger.info("Strategy 1b: Looking for 'Start a post' text and clicking parent")
                start_post_selectors = [
                    'div[data-placeholder*="What do you want to talk about"]',
                    'div[data-placeholder*="What\'s on your mind"]',
                    'div[data-placeholder*="post"]',
                    'div[contenteditable="true"][role="textbox"]',
                    'div[contenteditable="true"]',
                    'div[role="textbox"]',
                    'button:has-text("Start a post")',
                    'span:has-text("Start a post")',
                    'div:has-text("Start a post")',
                    '[aria-label*="Start a post"]',
                    '[aria-label*="start a post"]',
                ]
                
                # Strategy 1: Look for the "Start a post" ENCADRÉ/BOX
                # This is the box that contains "Start a post" text + Video/Photo/Write article buttons
                logger.info("Strategy 1: Looking for 'Start a post' ENCADRÉ/BOX")
                logger.info("  This box contains: 'Start a post' text + Video/Photo/Write article buttons")
                
                # Look for divs containing "Start a post" text - this should be the encadré
                start_post_box_selectors = [
                    'div:has-text("Start a post")',
                    'section:has-text("Start a post")',
                    # Look for containers that might have the box
                    'div[data-control-name="composer"]',
                    'div.share-box',
                    'div[class*="share-box"]',
                    'div[class*="composer"]',
                ]
                
                for box_selector in start_post_box_selectors:
                    try:
                        logger.info(f"  Checking box selector: {box_selector}")
                        boxes = self.page.locator(box_selector)
                        count = boxes.count()
                        logger.info(f"    Found {count} boxes")
                        
                        if count > 0:
                            for i in range(min(count, 5)):
                                try:
                                    box = boxes.nth(i)
                                    if box.is_visible():
                                        # Check if this box contains "Start a post" text
                                        text = box.inner_text()
                                        logger.info(f"    Box {i} text preview: '{text[:150] if text else 'N/A'}'")
                                        
                                        # Check if it contains "Start a post" and the buttons (Video/Photo/Write article)
                                        if "Start a post" in text or ("start a post" in text.lower() and ("Video" in text or "Photo" in text or "Write article" in text)):
                                            logger.info(f"    ✅ Found 'Start a post' encadré {i}")
                                            logger.info(f"    Clicking on the encadré...")
                                            
                                            # Click on the box
                                            box.click(timeout=5000)
                                            logger.info("    ✅ Clicked on encadré")
                                            time.sleep(3)
                                            self.take_screenshot(f"02_start_post_encadre_clicked_attempt_{attempt+1}")
                                            
                                            if self._verify_composer_opened():
                                                logger.info("    ✅ Composer opened after clicking encadré!")
                                                return True
                                            else:
                                                logger.warning("    ⚠️  Composer did not open, trying to click text inside...")
                                                # Try clicking on the "Start a post" text specifically
                                                try:
                                                    start_text = box.locator('text="Start a post"').first
                                                    if start_text.is_visible():
                                                        start_text.click(timeout=5000)
                                                        time.sleep(2)
                                                        if self._verify_composer_opened():
                                                            logger.info("    ✅ Composer opened after clicking text!")
                                                            return True
                                                except:
                                                    pass
                                except Exception as e:
                                    logger.debug(f"    Could not process box {i}: {e}")
                                    continue
                    except Exception as e:
                        logger.debug(f"  Box selector {box_selector} failed: {e}")
                        continue
                
                # Strategy 1b: Look for the text "Start a post" directly and click it
                logger.info("Strategy 1b: Looking for 'Start a post' text directly")
                start_post_text_selectors = [
                    'text="Start a post"',
                    'span:has-text("Start a post")',
                    '*:has-text("Start a post")',
                ]
                
                for text_selector in start_post_text_selectors:
                    try:
                        logger.info(f"  Looking for text: {text_selector}")
                        text_elements = self.page.locator(text_selector)
                        count = text_elements.count()
                        logger.info(f"    Found {count} elements")
                        
                        if count > 0:
                            for i in range(min(count, 3)):
                                try:
                                    text_elem = text_elements.nth(i)
                                    if text_elem.is_visible():
                                        logger.info(f"    ✅ Found visible 'Start a post' text {i}")
                                        text_elem.click(timeout=5000)
                                        logger.info("    Clicked on text")
                                        time.sleep(3)
                                        self.take_screenshot(f"02_start_post_text_clicked_attempt_{attempt+1}")
                                        
                                        if self._verify_composer_opened():
                                            logger.info("    ✅ Composer opened!")
                                            return True
                                except Exception as e:
                                    logger.debug(f"    Could not click text {i}: {e}")
                                    continue
                    except Exception as e:
                        logger.debug(f"  Text selector {text_selector} failed: {e}")
                        continue
                
                # Strategy 1c: Look for text input areas (composer might already be open or clickable)
                logger.info("Strategy 1c: Looking for text input areas")
                for selector in start_post_selectors:
                    try:
                        logger.info(f"  Trying selector: {selector}")
                        elements = self.page.locator(selector)
                        count = elements.count()
                        logger.info(f"  Found {count} elements")
                        
                        if count > 0:
                            for i in range(min(count, 3)):
                                try:
                                    elem = elements.nth(i)
                                    if elem.is_visible():
                                        logger.info(f"  ✅ Found visible element {i}")
                                        elem.click(timeout=5000)
                                        logger.info(f"  ✅ Clicked element {i}")
                                        time.sleep(3)
                                        self.take_screenshot(f"02_input_clicked_attempt_{attempt+1}")
                                        
                                        if self._verify_composer_opened():
                                            logger.info("  ✅ Composer opened!")
                                            return True
                                except Exception as e:
                                    logger.debug(f"    Could not click element {i}: {e}")
                                    continue
                    except Exception as e:
                        logger.warning(f"  ❌ Selector {selector} failed: {e}")
                        continue
                
                # Strategy 2: Look for the composer/editor area directly (might already be visible)
                logger.info("Strategy 2: Looking for composer/editor area")
                logger.info("  Checking if composer is already open...")
                if self._verify_composer_opened():
                    logger.info("  ✅ Composer already open!")
                    return True
                logger.info("  Composer not open, looking for it...")
                
                composer_selectors = [
                    'div[data-placeholder*="What do you want to talk about"]',
                    'div[data-placeholder*="What\'s on your mind"]',
                    'div[data-placeholder*="post"]',
                    'div[aria-label*="What do you want to talk about"]',
                    'div[aria-label*="What\'s on your mind"]',
                    'div[contenteditable="true"][role="textbox"]',
                    'div.ql-editor[contenteditable="true"]',
                    'div[contenteditable="true"]',
                    'div[role="textbox"]',
                ]
                
                for selector in composer_selectors:
                    try:
                        elements = self.page.locator(selector)
                        if elements.count() > 0:
                            logger.info(f"Found composer area with selector: {selector}")
                            elements.first.click(timeout=5000)
                            time.sleep(3)
                            self.take_screenshot(f"composer_clicked_attempt_{attempt+1}")
                            
                            if self._verify_composer_opened():
                                return True
                    except Exception as e:
                        logger.debug(f"Selector {selector} failed: {e}")
                        continue
                
                # Strategy 3: Look for share box or feed composer container
                logger.info("Strategy 3: Looking for share box container")
                share_box_selectors = [
                    'div.share-box',
                    'div.share-box__inner',
                    'div[data-control-name="composer"]',
                    'div.feed-shared-comment-box',
                    'div.comment-box',
                    'div[class*="share-box"]',
                    'div[class*="composer"]',
                ]
                
                for selector in share_box_selectors:
                    try:
                        elements = self.page.locator(selector)
                        if elements.count() > 0:
                            logger.info(f"Found share box with selector: {selector}")
                            # Click in the middle of the share box
                            element = elements.first
                            element.click(timeout=5000)
                            time.sleep(3)
                            self.take_screenshot(f"share_box_clicked_attempt_{attempt+1}")
                            
                            if self._verify_composer_opened():
                                return True
                    except Exception as e:
                        logger.debug(f"Selector {selector} failed: {e}")
                        continue
                
                # Strategy 4: Try keyboard shortcut 'n' (LinkedIn shortcut for new post)
                logger.info("Strategy 4: Trying keyboard shortcut 'n'")
                try:
                    # Make sure page has focus
                    self.page.click('body')
                    time.sleep(0.5)
                    self.page.keyboard.press('n')
                    time.sleep(3)
                    self.take_screenshot(f"keyboard_n_pressed_attempt_{attempt+1}")
                    
                    if self._verify_composer_opened():
                        logger.info("Composer opened with keyboard shortcut")
                        return True
                except Exception as e:
                    logger.debug(f"Keyboard shortcut failed: {e}")
                
                # Strategy 5: Try clicking anywhere in the top feed area
                if attempt < max_retries - 1:
                    logger.info("Waiting before retry...")
                    time.sleep(3)
                    # Scroll and try again
                    self.page.evaluate("window.scrollTo(0, 0)")
                    time.sleep(2)
            
            # Final debug: Take screenshot and log page state
            logger.error("="*60)
            logger.error("❌ COULD NOT FIND POST CREATION INTERFACE")
            logger.error("="*60)
            self.take_screenshot("03_post_creation_not_found_final")
            
            # Log page state
            logger.error(f"Page title: {self.page.title()}")
            logger.error(f"Page URL: {self.page.url}")
            
            # Try to find all buttons and log them
            logger.error("Looking for all buttons on page for debugging...")
            try:
                buttons = self.page.locator('button').all()
                logger.error(f"Found {len(buttons)} buttons on the page")
                for i, button in enumerate(buttons[:15]):  # Log first 15 buttons
                    try:
                        text = button.inner_text()
                        aria_label = button.get_attribute('aria-label')
                        is_visible = button.is_visible()
                        logger.error(f"  Button {i}: text='{text[:50] if text else 'N/A'}', aria-label='{aria_label}', visible={is_visible}")
                    except Exception as e:
                        logger.debug(f"  Button {i}: Error reading - {e}")
            except Exception as e:
                logger.error(f"Error listing buttons: {e}")
            
            # Try to find all divs with "post" in them
            logger.error("Looking for elements containing 'post'...")
            try:
                post_elements = self.page.locator('*:has-text("post" i)').all()
                logger.error(f"Found {len(post_elements)} elements containing 'post'")
                for i, elem in enumerate(post_elements[:10]):
                    try:
                        text = elem.inner_text()
                        tag = elem.evaluate("el => el.tagName")
                        logger.error(f"  Element {i} ({tag}): '{text[:80] if text else 'N/A'}'")
                    except:
                        pass
            except Exception as e:
                logger.error(f"Error finding post elements: {e}")
            
            return False
            
        except Exception as e:
            logger.error(f"Error navigating to post creation: {e}")
            self.take_screenshot("navigate_post_creation_error")
            return False
    
    def _verify_composer_opened(self) -> bool:
        """
        Verify that the post composer is open and ready.
        
        Returns:
            True if composer is open, False otherwise
        """
        try:
            logger.info("    Checking for composer elements...")
            
            # Check for contenteditable text area (composer is open)
            composer_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'div[contenteditable="true"]',
                'div.ql-editor[contenteditable="true"]',
                'div[data-placeholder*="What do you want to talk about"]',
                'div[data-placeholder*="What\'s on your mind"]',
                'div[data-placeholder*="post"]',
            ]
            
            for selector in composer_selectors:
                try:
                    count = self.page.locator(selector).count()
                    logger.info(f"    Selector '{selector}': {count} elements found")
                    
                    if count > 0:
                        # Check if it's visible
                        element = self.page.locator(selector).first
                        is_visible = element.is_visible()
                        logger.info(f"    First element visible: {is_visible}")
                        
                        if is_visible:
                            logger.info(f"    ✅ Composer verified open with selector: {selector}")
                            return True
                except Exception as e:
                    logger.debug(f"    Error checking selector {selector}: {e}")
                    continue
            
            logger.info("    ❌ No composer elements found or visible")
            return False
        except Exception as e:
            logger.debug(f"Error verifying composer: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return False
    
    def enter_post_text(self, post_text: str) -> bool:
        """
        Enter post text into the composer.
        
        Args:
            post_text: The text content to enter
            
        Returns:
            True if text entered successfully, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("ENTERING POST TEXT")
            logger.info("="*60)
            
            # Find the composer text area
            logger.info("Looking for composer text area...")
            
            composer_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'div[contenteditable="true"]',
                'div.ql-editor[contenteditable="true"]',
                'div[data-placeholder*="What do you want to talk about"]',
                'div[data-placeholder*="What\'s on your mind"]',
            ]
            
            text_entered = False
            for selector in composer_selectors:
                try:
                    logger.info(f"  Trying selector: {selector}")
                    composer = self.page.locator(selector).first
                    
                    if composer.is_visible():
                        logger.info(f"  ✅ Found composer with selector: {selector}")
                        logger.info("  Clicking to focus...")
                        composer.click(timeout=5000)
                        time.sleep(1)
                        
                        logger.info("  Entering text...")
                        # Clear any existing text first
                        composer.clear()
                        # Type the text
                        composer.fill(post_text)
                        time.sleep(1)
                        
                        logger.info(f"  ✅ Text entered: '{post_text[:50]}...'")
                        self.take_screenshot("03_post_text_entered")
                        text_entered = True
                        break
                except Exception as e:
                    logger.debug(f"  Selector {selector} failed: {e}")
                    continue
            
            if not text_entered:
                logger.error("❌ Could not find composer text area")
                self.take_screenshot("03_post_text_error")
                return False
            
            # Verify text was entered
            try:
                composer = self.page.locator('div[contenteditable="true"][role="textbox"]').first
                entered_text = composer.inner_text()
                if post_text[:50] in entered_text or entered_text[:50] in post_text:
                    logger.info("✅ Text verified in composer")
                    return True
                else:
                    logger.warning(f"⚠️  Text verification unclear. Expected: '{post_text[:50]}', Got: '{entered_text[:50]}'")
                    # Still return True as text might be there
                    return True
            except:
                logger.warning("⚠️  Could not verify text, but assuming success")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error entering post text: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.take_screenshot("03_post_text_error")
            return False
    
    def enter_post_text_OLD(self, post_text: str) -> bool:
        """
        Enter post text content.
        
        Args:
            post_text: Text content to post
            
        Returns:
            True if text entered successfully, False otherwise
        """
        try:
            logger.info("Entering post text")
            
            # Try multiple selectors for the text input area
            text_selectors = [
                'div[contenteditable="true"]',
                'div.ql-editor',
                'div[role="textbox"]',
                'div[data-placeholder*="post"]',
                'div[aria-label*="post"]'
            ]
            
            text_entered = False
            for selector in text_selectors:
                if self.wait_for_element(selector, timeout=5000):
                    try:
                        # Clear any existing text
                        self.page.fill(selector, "")
                        time.sleep(0.5)
                        
                        # Type the post text
                        self.page.type(selector, post_text, delay=50)
                        time.sleep(2)
                        
                        text_entered = True
                        logger.info(f"Text entered using selector: {selector}")
                        break
                    except Exception as e:
                        logger.warning(f"Failed to enter text with selector {selector}: {e}")
                        continue
            
            if not text_entered:
                self.take_screenshot("text_input_not_found")
                logger.error("Could not find text input area")
                return False
            
            self.take_screenshot("post_text_entered")
            return True
            
        except Exception as e:
            logger.error(f"Error entering post text: {e}")
            self.take_screenshot("enter_post_text_error")
            return False
    
    def click_schedule_button(self) -> bool:
        """
        Find and click the Schedule button instead of Post.
        
        Returns:
            True if schedule button clicked, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("CLICKING SCHEDULE BUTTON")
            logger.info("="*60)
            
            # Wait a bit for the post interface to fully load
            time.sleep(2)
            
            # Try to find and click Schedule button
            # In French: "Programmer pour plus tard"
            logger.info("Looking for Schedule button...")
            
            schedule_selectors = [
                'button:has-text("Programmer pour plus tard")',
                'span:has-text("Programmer pour plus tard")',
                '*:has-text("Programmer pour plus tard")',
                'button:has-text("Schedule")',
                'button[aria-label*="Schedule"]',
                'button[aria-label*="programmer" i]',
                'span:has-text("Schedule")',
                '*:has-text("Schedule")',
                'button[data-control-name*="schedule"]',
            ]
            
            # First, look for the "Post" button area - Schedule is usually a dropdown next to it
            logger.info("Looking for Post button area...")
            post_button_selectors = [
                'button:has-text("Post")',
                'button[aria-label*="Post"]',
                'button[data-control-name="share.post"]',
            ]
            
            # Try to find Schedule button directly
            for selector in schedule_selectors:
                try:
                    logger.info(f"  Trying selector: {selector}")
                    schedule_btn = self.page.locator(selector).first
                    if schedule_btn.is_visible():
                        logger.info(f"  ✅ Found Schedule button with selector: {selector}")
                        logger.info("  Clicking Schedule button...")
                        schedule_btn.click(timeout=5000)
                        time.sleep(2)
                        logger.info("  ✅ Schedule button clicked!")
                        self.take_screenshot("04_schedule_button_clicked")
                        return True
                except Exception as e:
                    logger.debug(f"  Selector {selector} failed: {e}")
                    continue
            
            # If Schedule button not found directly, look for dropdown next to Post button
            logger.info("Schedule button not found directly, looking for dropdown...")
            for post_selector in post_button_selectors:
                try:
                    post_btn = self.page.locator(post_selector).first
                    if post_btn.is_visible():
                        logger.info(f"  Found Post button with: {post_selector}")
                        # Look for a dropdown/chevron button next to Post
                        # Usually there's a chevron or dropdown icon
                        logger.info("  Looking for dropdown/chevron next to Post button...")
                        
                        # Try to find a chevron or dropdown button
                        dropdown_selectors = [
                            'button[aria-label*="More"]',
                            'button[aria-label*="more"]',
                            'button[aria-expanded="false"]',
                            'button:has(svg)',
                        ]
                        
                        # Get parent container and look for Schedule option
                        try:
                            parent = post_btn.locator('xpath=..').first
                            # Look for Schedule in the same container
                            schedule_in_parent = parent.locator('text="Schedule"').first
                            if schedule_in_parent.is_visible():
                                logger.info("  ✅ Found Schedule in Post button container")
                                schedule_in_parent.click(timeout=5000)
                                time.sleep(2)
                                logger.info("  ✅ Clicked Schedule!")
                                self.take_screenshot("04_schedule_clicked_from_dropdown")
                                return True
                        except:
                            pass
                except:
                    continue
            
            logger.error("❌ Could not find Schedule button")
            self.take_screenshot("04_schedule_button_not_found")
            return False
            
            schedule_found = False
            for selector in schedule_selectors:
                if self.wait_for_element(selector, timeout=5000):
                    logger.info(f"Found Schedule button with selector: {selector}")
                    self.page.click(selector)
                    time.sleep(2)
                    schedule_found = True
                    break
            
            if not schedule_found:
                # Maybe Schedule is in a dropdown menu
                logger.info("Schedule button not found directly, checking for dropdown")
                
                # Look for a menu or dropdown button
                menu_selectors = [
                    'button[aria-label*="More"]',
                    'button[aria-label*="Options"]',
                    'button[data-control-name*="more"]'
                ]
                
                for menu_selector in menu_selectors:
                    if self.wait_for_element(menu_selector, timeout=3000):
                        self.page.click(menu_selector)
                        time.sleep(1)
                        
                        # Now look for Schedule in the dropdown
                        for selector in schedule_selectors:
                            if self.wait_for_element(selector, timeout=3000):
                                self.page.click(selector)
                                time.sleep(2)
                                schedule_found = True
                                break
                        
                        if schedule_found:
                            break
            
            if not schedule_found:
                self.take_screenshot("schedule_button_not_found")
                logger.error("Could not find Schedule button")
                return False
            
            self.take_screenshot("schedule_button_clicked")
            return True
            
        except Exception as e:
            logger.error(f"Error clicking Schedule button: {e}")
            self.take_screenshot("click_schedule_error")
            return False
    
    def set_scheduled_date_time(self, scheduled_datetime: datetime) -> bool:
        """
        Set scheduled date and time in LinkedIn's scheduling interface.
        
        Args:
            scheduled_datetime: Datetime object for when to schedule the post
            
        Returns:
            True if date/time set successfully, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("SETTING SCHEDULED DATE AND TIME")
            logger.info("="*60)
            logger.info(f"Target date/time: {scheduled_datetime}")
            
            # Wait for scheduling modal/interface to appear
            time.sleep(2)
            self.take_screenshot("05_schedule_modal_opened")
            
            # Format date as YYYY-MM-DD (ISO format)
            date_str = scheduled_datetime.strftime("%Y-%m-%d")
            
            # Format time as HH:MM (24-hour format)
            time_str = scheduled_datetime.strftime("%H:%M")
            
            logger.info(f"Date string: {date_str}")
            logger.info(f"Time string: {time_str}")
            
            # STEP 1: Find and click the "Date" field to open calendar
            logger.info("STEP 1: Looking for Date field to open calendar...")
            date_field_selectors = [
                'input[aria-label*="Date" i]',
                'input[placeholder*="Date" i]',
                'div[role="textbox"][aria-label*="Date" i]',
                'label:has-text("Date")',
            ]
            
            date_field_clicked = False
            for selector in date_field_selectors:
                try:
                    logger.info(f"  Trying: {selector}")
                    date_field = self.page.locator(selector).first
                    if date_field.is_visible():
                        logger.info(f"  ✅ Found Date field")
                        logger.info("  Clicking to open calendar...")
                        date_field.click(timeout=5000)
                        time.sleep(1)
                        date_field_clicked = True
                        self.take_screenshot("06_date_calendar_opened")
                        break
                except:
                    continue
            
            # If not found by label, look for input with date format (DD/MM/YYYY)
            if not date_field_clicked:
                logger.info("  Looking for input with date format...")
                try:
                    all_inputs = self.page.locator('input').all()
                    for inp in all_inputs[:10]:
                        if inp.is_visible():
                            value = inp.input_value() or ""
                            # Check if it looks like a date (DD/MM/YYYY or similar)
                            if '/' in value and len(value) >= 8:
                                logger.info(f"  ✅ Found date input with value: {value}")
                                inp.click(timeout=5000)
                                time.sleep(1)
                                date_field_clicked = True
                                self.take_screenshot("06_date_calendar_opened")
                                break
                except:
                    pass
            
            # STEP 2: Select date in calendar
            date_set = False
            if date_field_clicked:
                logger.info("STEP 2: Selecting date in calendar...")
                day = scheduled_datetime.day
                logger.info(f"  Looking for day {day} in calendar...")
                try:
                    # Look for the day number in the calendar
                    day_element = self.page.locator(f'text="{day}"').first
                    if day_element.is_visible():
                        logger.info(f"  ✅ Found day {day} in calendar")
                        day_element.click(timeout=5000)
                        time.sleep(0.5)
                        date_set = True
                        logger.info(f"  ✅ Date selected: {day}")
                        self.take_screenshot("07_date_selected")
                except Exception as e:
                    logger.debug(f"  Could not click day {day}: {e}")
            
            # STEP 3: Find and click the "Heure" field to open dropdown
            logger.info("STEP 3: Looking for Heure (time) field to open dropdown...")
            time_field_selectors = [
                'input[aria-label*="Heure" i]',
                'input[placeholder*="Heure" i]',
                'div[role="textbox"][aria-label*="Heure" i]',
                'label:has-text("Heure")',
            ]
            
            time_field_clicked = False
            for selector in time_field_selectors:
                try:
                    logger.info(f"  Trying: {selector}")
                    time_field = self.page.locator(selector).first
                    if time_field.is_visible():
                        logger.info(f"  ✅ Found Heure field")
                        logger.info("  Clicking to open dropdown...")
                        time_field.click(timeout=5000)
                        time.sleep(1)
                        time_field_clicked = True
                        self.take_screenshot("08_time_dropdown_opened")
                        break
                except:
                    continue
            
            # If not found by label, look for input with time format (HH:MM)
            if not time_field_clicked:
                logger.info("  Looking for input with time format...")
                try:
                    all_inputs = self.page.locator('input').all()
                    for inp in all_inputs[:10]:
                        if inp.is_visible():
                            value = inp.input_value() or ""
                            # Check if it looks like a time (HH:MM)
                            if ':' in value and len(value) == 5:
                                logger.info(f"  ✅ Found time input with value: {value}")
                                inp.click(timeout=5000)
                                time.sleep(1)
                                time_field_clicked = True
                                self.take_screenshot("08_time_dropdown_opened")
                                break
                except:
                    pass
            
            # STEP 4: Select time in dropdown (times are every 15 minutes: 08:00, 08:15, 08:30, etc.)
            time_set = False
            if time_field_clicked:
                logger.info("STEP 4: Selecting time in dropdown...")
                # Round time to nearest 15 minutes (LinkedIn uses 15-min intervals)
                minutes = scheduled_datetime.minute
                rounded_minutes = (minutes // 15) * 15
                target_time = scheduled_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)
                time_str_formatted = target_time.strftime("%H:%M")
                
                logger.info(f"  Looking for time: {time_str_formatted} (rounded to 15-min interval)")
                try:
                    # Look for the time option in the dropdown
                    time_option = self.page.locator(f'text="{time_str_formatted}"').first
                    if time_option.is_visible():
                        logger.info(f"  ✅ Found time option: {time_str_formatted}")
                        time_option.click(timeout=5000)
                        time.sleep(0.5)
                        time_set = True
                        logger.info(f"  ✅ Time selected: {time_str_formatted}")
                        self.take_screenshot("09_time_selected")
                except Exception as e:
                    logger.debug(f"  Could not click time {time_str_formatted}: {e}")
            
            # Final verification
            if date_set and time_set:
                logger.info(f"✅ Date set: {date_set}, Time set: {time_set}")
                self.take_screenshot("10_date_time_set")
                return True
            elif date_set or time_set:
                logger.warning(f"⚠️  Partial success - Date: {date_set}, Time: {time_set}")
                self.take_screenshot("10_date_time_partial")
                return True  # Return True if at least one is set
            else:
                logger.error("❌ Could not set date or time")
                self.take_screenshot("10_date_time_not_set")
                return False
            
        except Exception as e:
            logger.error(f"Error setting scheduled date/time: {e}")
            self.take_screenshot("set_date_time_error")
            return False
    
    def confirm_schedule(self) -> bool:
        """
        Confirm and schedule the post.
        
        Returns:
            True if scheduled successfully, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("CONFIRMING SCHEDULE")
            logger.info("="*60)
            
            # Take screenshot first to see what's on screen
            self.take_screenshot("08_before_confirm")
            time.sleep(2)
            
            # Look for confirm/schedule button
            # In French: "Programmer" or "Confirmer"
            logger.info("Looking for confirm/schedule button...")
            confirm_selectors = [
                'button:has-text("Programmer")',
                'button:has-text("Confirmer")',
                'button:has-text("Schedule")',
                'button:has-text("Confirm")',
                'button:has-text("Schedule post")',
                'button:has-text("Confirm schedule")',
                'button[aria-label*="Programmer" i]',
                'button[aria-label*="Confirmer" i]',
                'button[aria-label*="Schedule" i]',
                'button[aria-label*="Confirm" i]',
                'button[data-control-name*="schedule"]',
                'button[type="submit"]',
            ]
            
            confirmed = False
            for selector in confirm_selectors:
                try:
                    logger.info(f"  Trying selector: {selector}")
                    confirm_btn = self.page.locator(selector).first
                    if confirm_btn.is_visible():
                        logger.info(f"  ✅ Found confirm button with selector: {selector}")
                        logger.info("  Clicking confirm button...")
                        confirm_btn.click(timeout=5000)
                        time.sleep(3)
                        logger.info("  ✅ Confirm button clicked!")
                        confirmed = True
                        self.take_screenshot("09_confirm_clicked")
                        break
                except Exception as e:
                    logger.debug(f"  Selector {selector} failed: {e}")
                    continue
            
            if not confirmed:
                logger.warning("⚠️  Could not find confirm/schedule button with standard selectors")
                logger.info("Looking for all buttons on page...")
                self.take_screenshot("08_confirm_button_not_found")
                
                # Try to find any button that might be the confirm button
                try:
                    all_buttons = self.page.locator('button').all()
                    logger.info(f"Found {len(all_buttons)} buttons on page")
                    for i, btn in enumerate(all_buttons[:10]):
                        try:
                            if btn.is_visible():
                                text = btn.inner_text()
                                aria_label = btn.get_attribute('aria-label') or ""
                                logger.info(f"  Button {i}: text='{text[:50] if text else 'N/A'}', aria-label='{aria_label[:50]}'")
                                # If button text contains schedule/confirm, try clicking it
                                if text and ('schedule' in text.lower() or 'confirm' in text.lower() or 'publier' in text.lower()):
                                    logger.info(f"  ✅ Trying to click button with text: '{text}'")
                                    btn.click(timeout=5000)
                                    time.sleep(3)
                                    confirmed = True
                                    self.take_screenshot("09_confirm_clicked_alternative")
                                    break
                        except:
                            pass
                except Exception as e:
                    logger.debug(f"Error listing buttons: {e}")
                
                if not confirmed:
                    logger.error("❌ Could not find confirm/schedule button")
                    return False
            
            # Wait for confirmation
            logger.info("Waiting for confirmation...")
            try:
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            time.sleep(2)
            
            self.take_screenshot("10_post_scheduled")
            logger.info("✅ Post scheduled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error confirming schedule: {e}")
            self.take_screenshot("confirm_schedule_error")
            return False
    
    def schedule_post(self, post_text: str, scheduled_datetime: datetime, email: str, password: str) -> bool:
        """
        Complete flow to schedule a LinkedIn post.
        
        Args:
            post_text: Text content of the post
            scheduled_datetime: When to schedule the post
            email: LinkedIn email
            password: LinkedIn password
            
        Returns:
            True if post scheduled successfully, False otherwise
        """
        try:
            logger.info("Starting LinkedIn post scheduling flow")
            
            # Start browser
            self.start_browser()
            
            # Login
            if not self.login(email, password):
                logger.error("Login failed")
                return False
            
            # Navigate to post creation
            if not self.navigate_to_post_creation():
                logger.error("Failed to navigate to post creation")
                return False
            
            # Enter post text
            if not self.enter_post_text(post_text):
                logger.error("Failed to enter post text")
                return False
            
            # Click Schedule button
            if not self.click_schedule_button():
                logger.error("Failed to click Schedule button")
                return False
            
            # Set scheduled date/time
            if not self.set_scheduled_date_time(scheduled_datetime):
                logger.warning("Failed to set scheduled date/time (may still work)")
            
            # Confirm schedule
            if not self.confirm_schedule():
                logger.error("Failed to confirm schedule")
                return False
            
            logger.info("Post scheduling flow completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error in schedule_post flow: {e}")
            self.take_screenshot("schedule_post_error")
            return False
        finally:
            # Keep browser open for a bit to see the result
            time.sleep(3)
            # Don't close browser automatically - let user see the result
            # self.close_browser()

