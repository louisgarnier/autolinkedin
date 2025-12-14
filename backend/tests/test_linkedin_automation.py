"""
Integration test script for LinkedIn automation.

This script tests the LinkedIn browser automation functionality.
It can be run with: python backend/tests/test_linkedin_automation.py

WARNING: This test requires real LinkedIn credentials and will perform actual actions.
Make sure you have valid credentials in .env file.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import logging

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.linkedin_automation import LinkedInAutomation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_browser_startup():
    """Test browser startup and shutdown."""
    print("\n" + "="*60)
    print("TEST 1: Browser Startup")
    print("="*60)
    
    try:
        automation = LinkedInAutomation(browser_mode="visible")
        automation.start_browser()
        print("✅ Browser started successfully")
        
        # Take a test screenshot
        screenshot = automation.take_screenshot("test_startup")
        print(f"✅ Screenshot taken: {screenshot}")
        
        automation.close_browser()
        print("✅ Browser closed successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_linkedin_login():
    """Test LinkedIn login (requires real credentials)."""
    print("\n" + "="*60)
    print("TEST 2: LinkedIn Login")
    print("="*60)
    
    automation = None
    try:
        settings = get_settings()
        email, password = settings.get_linkedin_credentials()
        
        automation = LinkedInAutomation(browser_mode="visible")
        automation.start_browser()
        
        print(f"Attempting to login with email: {email[:3]}***")
        success = automation.login(email, password)
        
        if success:
            print("✅ Login successful")
            # Keep browser open for a few seconds to see the result
            import time
            time.sleep(5)
        else:
            print("❌ Login failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if automation:
            try:
                automation.close_browser()
            except:
                pass


def test_navigate_to_post_creation():
    """Test navigating to post creation interface."""
    print("\n" + "="*60)
    print("TEST 3: Navigate to Post Creation")
    print("="*60)
    
    automation = None
    try:
        settings = get_settings()
        email, password = settings.get_linkedin_credentials()
        
        automation = LinkedInAutomation(browser_mode="visible")
        automation.start_browser()
        
        # Login first
        if not automation.login(email, password):
            print("❌ Login failed, cannot test post creation")
            return False
        
        # Navigate to post creation
        success = automation.navigate_to_post_creation()
        
        if success:
            print("✅ Successfully navigated to post creation")
            import time
            time.sleep(5)  # Keep browser open to see
        else:
            print("❌ Failed to navigate to post creation")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if automation:
            try:
                automation.close_browser()
            except:
                pass


def test_enter_post_text():
    """Test entering post text."""
    print("\n" + "="*60)
    print("TEST 4: Enter Post Text")
    print("="*60)
    
    automation = None
    try:
        settings = get_settings()
        email, password = settings.get_linkedin_credentials()
        
        automation = LinkedInAutomation(browser_mode="visible")
        automation.start_browser()
        
        # Login
        if not automation.login(email, password):
            print("❌ Login failed")
            return False
        
        # Navigate to post creation
        if not automation.navigate_to_post_creation():
            print("❌ Failed to navigate to post creation")
            return False
        
        # Enter test post text
        test_text = "Test post from automation - please ignore"
        success = automation.enter_post_text(test_text)
        
        if success:
            print("✅ Successfully entered post text")
            import time
            time.sleep(5)  # Keep browser open to see
        else:
            print("❌ Failed to enter post text")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if automation:
            try:
                automation.close_browser()
            except:
                pass


def test_full_schedule_flow():
    """Test the complete scheduling flow (requires real credentials and will schedule a real post)."""
    print("\n" + "="*60)
    print("TEST 5: Full Schedule Flow")
    print("="*60)
    print("⚠️  WARNING: This will schedule a REAL post on LinkedIn!")
    print("   Make sure you want to proceed.")
    
    response = input("Continue with full schedule test? (yes/no): ")
    if response.lower() != 'yes':
        print("⚠️  Test skipped")
        return None
    
    try:
        settings = get_settings()
        email, password = settings.get_linkedin_credentials()
        
        # Schedule for tomorrow at 8:00 AM
        scheduled_datetime = datetime.now() + timedelta(days=1)
        scheduled_datetime = scheduled_datetime.replace(hour=8, minute=0, second=0, microsecond=0)
        
        automation = LinkedInAutomation(browser_mode="visible")
        
        test_text = "Test scheduled post from automation - please ignore"
        
        print(f"Scheduling post for: {scheduled_datetime}")
        print(f"Post text: {test_text[:50]}...")
        
        success = automation.schedule_post(
            post_text=test_text,
            scheduled_datetime=scheduled_datetime,
            email=email,
            password=password
        )
        
        if success:
            print("✅ Post scheduled successfully")
            print("   Check your LinkedIn scheduled posts to verify")
        else:
            print("❌ Failed to schedule post")
        
        # Keep browser open for user to verify
        print("\nBrowser will stay open for 10 seconds for verification...")
        import time
        time.sleep(10)
        automation.close_browser()
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test LinkedIn automation')
    parser.add_argument('--skip-login', action='store_true', help='Skip login tests (only test browser startup)')
    parser.add_argument('--full-test', action='store_true', help='Run full test including schedule (requires confirmation)')
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("LINKEDIN AUTOMATION TEST")
    print("="*60)
    print("\n⚠️  WARNING: These tests require real LinkedIn credentials")
    print("   and will perform actual actions on LinkedIn.")
    print("\nMake sure:")
    print("  1. LinkedIn credentials are set in .env file")
    print("  2. You have a stable internet connection")
    print("  3. You're ready to see browser automation in action")
    
    # Validate settings first
    try:
        validate_settings()
        print("\n✅ Configuration validated")
    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        print("   Please check your .env file")
        sys.exit(1)
    
    results = []
    
    # Test 1: Browser startup (safe, no login)
    print("\n" + "-"*60)
    print("Starting with safe tests (no login required)...")
    results.append(("Browser Startup", test_browser_startup()))
    
    # Skip login tests if requested
    if args.skip_login:
        print("\n⚠️  Login tests skipped (--skip-login flag)")
        results.append(("LinkedIn Login", None))
        results.append(("Navigate to Post Creation", None))
        results.append(("Enter Post Text", None))
        results.append(("Full Schedule Flow", None))
    else:
        # Test 2: Login
        print("\n" + "-"*60)
        print("Running login tests...")
        results.append(("LinkedIn Login", test_linkedin_login()))
        
        # Test 3: Navigate to post creation
        results.append(("Navigate to Post Creation", test_navigate_to_post_creation()))
        
        # Test 4: Enter post text
        results.append(("Enter Post Text", test_enter_post_text()))
        
        # Test 5: Full schedule flow (only if --full-test flag)
        if args.full_test:
            results.append(("Full Schedule Flow", test_full_schedule_flow()))
        else:
            print("\n⚠️  Full schedule flow skipped (use --full-test to run)")
            results.append(("Full Schedule Flow", None))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results:
        if result is True:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        elif result is False:
            print(f"❌ {test_name}: FAILED")
            failed += 1
        else:
            print(f"⚠️  {test_name}: SKIPPED")
            skipped += 1
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
    elif passed > 0:
        print("\n✅ All executed tests passed!")
        if skipped > 0:
            print("   (Some tests were skipped)")
        sys.exit(0)
    else:
        print("\n⚠️  No tests were executed.")
        sys.exit(0)


if __name__ == "__main__":
    main()

