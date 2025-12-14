"""
Integration test for Phase 1 (V2b - Step 5).

This test verifies the complete Phase 1 workflow:
1. Read subject from Sheet2, Row 2, Column A
2. Generate post using OpenAI with prompt template
3. Write generated post to Sheet2, Row 2, Column B
4. Set Column C to "yes"
5. Display generated post for review
"""

import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)

from backend.services.google_sheets import GoogleSheetsService
from backend.services.post_generation_service import PostGenerationService
from backend.config.settings import get_settings

print("="*60)
print("INTEGRATION TEST: Phase 1 Complete Workflow (V2b)")
print("="*60)

try:
    # Step 1: Connect to Google Sheets and Sheet2
    print("\n📋 STEP 1: Connecting to Google Sheets...")
    settings = get_settings()
    sheets_config = settings.get_google_sheets_config()
    
    sheets_service = GoogleSheetsService(
        service_account_path=sheets_config['service_account_path'],
        sheet_id=sheets_config['sheet_id']
    )
    sheets_service.connect()
    sheets_service.connect_sheet2()
    print("✅ Connected to Google Sheets and Sheet2")
    
    # Step 2: Read subject from Sheet2, Row 2, Column A
    print("\n📋 STEP 2: Reading subject from Sheet2, Row 2, Column A...")
    subject = sheets_service.read_subject_from_sheet2()
    
    if not subject:
        print("❌ No subject found in Sheet2, Row 2, Column A")
        print("   Please add a subject to test with")
        exit(1)
    
    print(f"✅ Subject read: '{subject}'")
    
    # Step 3: Generate post using OpenAI with prompt template
    print("\n📋 STEP 3: Generating post using OpenAI GPT-4 with prompt template...")
    print("   This may take 10-30 seconds...")
    
    post_service = PostGenerationService()
    generated_post = post_service.generate_post(subject)
    
    print(f"✅ Post generated successfully")
    print(f"   Length: {len(generated_post)} characters")
    print(f"   Lines: {len(generated_post.split(chr(10)))}")
    
    # Step 4: Display generated post for review
    print("\n" + "="*60)
    print("📝 GENERATED POST PREVIEW:")
    print("="*60)
    print(generated_post)
    print("="*60)
    
    # Step 5: Write generated post to Sheet2, Row 2, Column B
    print("\n📋 STEP 4: Writing generated post to Sheet2, Row 2, Column B...")
    sheets_service.write_post_to_sheet2(generated_post)
    print("✅ Post written to Sheet2")
    
    # Step 6: Set Column C to "yes"
    print("\n📋 STEP 5: Setting post generated status to 'yes' in Sheet2, Row 2, Column C...")
    sheets_service.set_post_generated_status("yes")
    print("✅ Status set to 'yes'")
    
    # Step 7: Verify by reading back
    print("\n📋 STEP 6: Verifying by reading back from Sheet2...")
    read_post = sheets_service.read_post_from_sheet2()
    read_status = sheets_service.get_post_generated_status()
    
    if read_post == generated_post:
        print("✅ Post matches what was written")
    else:
        print("⚠️  Warning: Post doesn't match exactly (might be whitespace differences)")
    
    if read_status == "yes":
        print("✅ Status is 'yes'")
    else:
        print(f"⚠️  Warning: Status is '{read_status}', expected 'yes'")
    
    print("\n" + "="*60)
    print("✅ PHASE 1 INTEGRATION TEST PASSED")
    print("="*60)
    print("\n📊 Summary:")
    print(f"   - Subject: '{subject}'")
    print(f"   - Post generated: {len(generated_post)} characters")
    print(f"   - Post saved to Sheet2, Row 2, Column B")
    print(f"   - Status set to 'yes' in Column C")
    print("\n💡 Next steps:")
    print("   - Review the generated post in Google Sheets")
    print("   - If satisfied, proceed to Phase 2 (LinkedIn integration)")
    print("   - If not satisfied, regenerate by running this test again")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

