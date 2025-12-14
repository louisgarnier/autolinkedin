"""
Main application entry point for LinkedIn Automation V2 - Phase 1.

This script:
1. Reads subject from Sheet2, Row 2, Column A
2. Generates post using OpenAI GPT-4 with prompt template
3. Saves generated post to Sheet2, Row 2, Column B
4. Sets Column C to "yes"
5. Displays generated post for review
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config.settings import get_settings, validate_settings
from backend.services.google_sheets import GoogleSheetsService
from backend.services.post_generation_service import PostGenerationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application function for Phase 1."""
    try:
        logger.info("="*60)
        logger.info("LINKEDIN AUTOMATION V2 - PHASE 1: POST GENERATION")
        logger.info("="*60)
        
        # Step 1: Validate and load settings
        logger.info("\n📋 STEP 1: Loading configuration...")
        validate_settings()
        settings = get_settings()
        logger.info("✅ Configuration loaded")
        
        # Step 2: Connect to Google Sheets and Sheet2
        logger.info("\n📋 STEP 2: Connecting to Google Sheets...")
        sheets_config = settings.get_google_sheets_config()
        sheets_service = GoogleSheetsService(
            service_account_path=sheets_config['service_account_path'],
            sheet_id=sheets_config['sheet_id']
        )
        sheets_service.connect()
        sheets_service.connect_sheet2()
        logger.info("✅ Connected to Google Sheets and Sheet2")
        
        # Step 3: Read subject from Sheet2, Row 2, Column A
        logger.info("\n📋 STEP 3: Reading subject from Sheet2, Row 2, Column A...")
        subject = sheets_service.read_subject_from_sheet2()
        
        if not subject:
            logger.error("❌ No subject found in Sheet2, Row 2, Column A")
            logger.info("   Please add a subject to generate a post")
            return 1
        
        logger.info(f"✅ Subject read: '{subject}'")
        
        # Step 4: Generate post using OpenAI
        logger.info("\n📋 STEP 4: Generating post using OpenAI...")
        logger.info("   This may take a few seconds...")
        
        post_service = PostGenerationService()
        generated_post = post_service.generate_post(subject)
        
        logger.info(f"✅ Post generated successfully")
        logger.info(f"   Length: {len(generated_post)} characters")
        logger.info(f"   Lines: {len(generated_post.split(chr(10)))}")
        
        # Step 5: Display generated post for review
        logger.info("\n" + "="*60)
        logger.info("📝 GENERATED POST:")
        logger.info("="*60)
        print("\n" + generated_post + "\n")
        logger.info("="*60)
        
        # Step 6: Write generated post to Sheet2, Row 2, Column B
        logger.info("\n📋 STEP 5: Writing generated post to Sheet2, Row 2, Column B...")
        sheets_service.write_post_to_sheet2(generated_post)
        logger.info("✅ Post written to Sheet2")
        
        # Step 7: Set Column C to "yes"
        logger.info("\n📋 STEP 6: Setting post generated status to 'yes' in Sheet2, Row 2, Column C...")
        sheets_service.set_post_generated_status("yes")
        logger.info("✅ Status set to 'yes'")
        
        # Step 8: Verify by reading back
        logger.info("\n📋 STEP 7: Verifying by reading back from Sheet2...")
        read_post = sheets_service.read_post_from_sheet2()
        read_status = sheets_service.get_post_generated_status()
        
        if read_post == generated_post:
            logger.info("✅ Post matches what was written")
        else:
            logger.warning("⚠️  Warning: Post doesn't match exactly (might be whitespace differences)")
        
        if read_status == "yes":
            logger.info("✅ Status is 'yes'")
        else:
            logger.warning(f"⚠️  Warning: Status is '{read_status}', expected 'yes'")
        
        logger.info("\n" + "="*60)
        logger.info("✅ PHASE 1 COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        logger.info("\n📊 Summary:")
        logger.info(f"   - Subject: '{subject}'")
        logger.info(f"   - Post generated: {len(generated_post)} characters")
        logger.info(f"   - Post saved to Sheet2, Row 2, Column B")
        logger.info(f"   - Status set to 'yes' in Column C")
        logger.info("\n💡 Next steps:")
        logger.info("   - Review the generated post in Google Sheets")
        logger.info("   - If satisfied, proceed to Phase 2 (LinkedIn integration)")
        logger.info("   - If not satisfied, regenerate by running this script again")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

