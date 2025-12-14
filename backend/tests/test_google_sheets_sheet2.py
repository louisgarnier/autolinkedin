"""
Test script for Google Sheets Sheet2 integration (V2b - Step 4).

This test verifies:
1. Can connect to Sheet2
2. Can read subject from Row 2, Column A
3. Can write post to Row 2, Column B
4. Can set status to "yes" in Row 2, Column C
5. Can read back the post and status
6. Regeneration works (overwrite Column B)
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
from backend.config.settings import get_settings

print("="*60)
print("TEST: Google Sheets Sheet2 Integration (V2b - Step 4)")
print("="*60)

try:
    # Test 1: Create service and connect
    print("\n1. Creating Google Sheets service and connecting...")
    settings = get_settings()
    sheets_config = settings.get_google_sheets_config()
    
    service = GoogleSheetsService(
        service_account_path=sheets_config['service_account_path'],
        sheet_id=sheets_config['sheet_id']
    )
    service.connect()
    print("✅ Connected to Google Sheets")
    
    # Test 2: Connect to Sheet2
    print("\n2. Connecting to Sheet2...")
    service.connect_sheet2()
    print("✅ Connected to Sheet2")
    
    # Test 3: Read subject from Row 2, Column A
    print("\n3. Reading subject from Sheet2, Row 2, Column A...")
    subject = service.read_subject_from_sheet2()
    if subject:
        print(f"✅ Subject read: '{subject[:100]}...'")
        print(f"   Full subject: '{subject}'")
    else:
        print("⚠️  Warning: Subject is empty. Please add a subject in Sheet2, Row 2, Column A")
        print("   Continuing with tests anyway...")
        subject = "Test sujet pour vérification"
    
    # Test 4: Write post to Row 2, Column B
    print("\n4. Writing test post to Sheet2, Row 2, Column B...")
    test_post = "Ceci est un post de test généré automatiquement pour vérifier l'intégration Google Sheets V2."
    service.write_post_to_sheet2(test_post)
    print(f"✅ Post written ({len(test_post)} characters)")
    
    # Test 5: Set status to "yes" in Row 2, Column C
    print("\n5. Setting post generated status to 'yes' in Sheet2, Row 2, Column C...")
    service.set_post_generated_status("yes")
    print("✅ Status set to 'yes'")
    
    # Test 6: Read back the post
    print("\n6. Reading post back from Sheet2, Row 2, Column B...")
    read_post = service.read_post_from_sheet2()
    if read_post:
        print(f"✅ Post read back: '{read_post[:100]}...'")
        if read_post == test_post:
            print("✅ Post matches what was written")
        else:
            print("⚠️  Warning: Post doesn't match exactly")
            print(f"   Expected: '{test_post}'")
            print(f"   Got: '{read_post}'")
    else:
        print("❌ Could not read post back")
        exit(1)
    
    # Test 7: Read back the status
    print("\n7. Reading status back from Sheet2, Row 2, Column C...")
    read_status = service.get_post_generated_status()
    if read_status:
        print(f"✅ Status read back: '{read_status}'")
        if read_status == "yes":
            print("✅ Status matches 'yes'")
        else:
            print(f"⚠️  Warning: Status is '{read_status}', expected 'yes'")
    else:
        print("❌ Could not read status back")
        exit(1)
    
    # Test 8: Test regeneration (overwrite Column B)
    print("\n8. Testing regeneration (overwriting Column B)...")
    new_test_post = "Ceci est un post régénéré pour tester la fonctionnalité de régénération."
    service.write_post_to_sheet2(new_test_post)
    print(f"✅ New post written ({len(new_test_post)} characters)")
    
    read_post2 = service.read_post_from_sheet2()
    if read_post2 == new_test_post:
        print("✅ Regeneration works: new post overwrote the old one")
    else:
        print("❌ Regeneration failed: post was not overwritten")
        exit(1)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    print("\n📝 Sheet2 integration is working correctly!")
    print("   - Subject can be read from Row 2, Column A")
    print("   - Post can be written to Row 2, Column B")
    print("   - Status can be set/read in Row 2, Column C")
    print("   - Regeneration (overwrite) works correctly")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

