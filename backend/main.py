"""
Main application entry point for LinkedIn Automation V1.

This script:
1. Reads Google Sheets
2. Finds post with date matching today
3. Posts to LinkedIn
4. Updates status in Google Sheets
"""

import sys
import logging
from pathlib import Path
from datetime import date

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.google_sheets import GoogleSheetsService
from backend.services.linkedin_automation import LinkedInAutomation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application function."""
    try:
        logger.info("="*60)
        logger.info("LINKEDIN AUTOMATION V1 - MAIN APPLICATION")
        logger.info("="*60)
        
        # Step 1: Validate and load settings
        logger.info("\nSTEP 1: Loading configuration...")
        validate_settings()
        settings = get_settings()
        logger.info("✅ Configuration loaded")
        
        # Step 2: Connect to Google Sheets
        logger.info("\nSTEP 2: Connecting to Google Sheets...")
        sheets_config = settings.get_google_sheets_config()
        sheets_service = GoogleSheetsService(
            service_account_path=sheets_config['service_account_path'],
            sheet_id=sheets_config['sheet_id']
        )
        sheets_service.connect()
        logger.info("✅ Connected to Google Sheets")
        
        # Step 3: Find post for today
        logger.info("\nSTEP 3: Looking for post with today's date...")
        today_str = date.today().strftime('%d/%m/%Y')
        logger.info(f"Today's date: {today_str}")
        
        post_data = sheets_service.find_post_for_today()
        
        if not post_data:
            logger.info("ℹ️  No post found for today. Exiting.")
            return 0
        
        logger.info(f"✅ Found post at row {post_data['row_num']}")
        logger.info(f"   Post text: {post_data['post_text'][:50]}...")
        logger.info(f"   Date: {post_data['date']}")
        logger.info(f"   Posted status: {post_data['posted']}")
        
        # Step 4: Post to LinkedIn
        logger.info("\nSTEP 4: Posting to LinkedIn...")
        linkedin_credentials = settings.get_linkedin_credentials()
        browser_mode = settings.get_browser_mode()
        
        automation = LinkedInAutomation(browser_mode=browser_mode)
        automation.start_browser()
        
        try:
            # Login
            logger.info("   Logging in to LinkedIn...")
            if not automation.login(linkedin_credentials[0], linkedin_credentials[1]):
                logger.error("❌ Failed to login to LinkedIn")
                return 1
            logger.info("   ✅ Logged in successfully")
            
            # Navigate to post creation
            logger.info("   Navigating to post creation...")
            if not automation.navigate_to_post_creation():
                logger.error("❌ Failed to navigate to post creation")
                return 1
            logger.info("   ✅ Composer opened")
            
            # Enter post text
            logger.info("   Entering post text...")
            if not automation.enter_post_text(post_data['post_text']):
                logger.error("❌ Failed to enter post text")
                return 1
            logger.info("   ✅ Post text entered")
            
            # Click Post button
            logger.info("   Clicking Post button...")
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
                            post_btn.click(timeout=5000)
                            import time
                            time.sleep(3)
                            posted = True
                            logger.info("   ✅ Post button clicked!")
                            break
                    except:
                        continue
                
                if not posted:
                    logger.error("   ❌ Could not find Post button")
                    return 1
                    
            except Exception as e:
                logger.error(f"   ❌ Error clicking Post button: {e}")
                return 1
            
            logger.info("   ✅ Post published successfully!")
            
        finally:
            automation.close_browser()
        
        # Step 5: Update status in Google Sheets
        logger.info("\nSTEP 5: Updating status in Google Sheets...")
        try:
            sheets_service.update_post_status(post_data['row_num'], "yes")
            logger.info(f"✅ Updated row {post_data['row_num']} status to 'yes'")
        except Exception as e:
            logger.error(f"❌ Failed to update status: {e}")
            return 1
        
        logger.info("\n" + "="*60)
        logger.info("✅ SUCCESS - Post published and status updated!")
        logger.info("="*60)
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Error in main application: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

