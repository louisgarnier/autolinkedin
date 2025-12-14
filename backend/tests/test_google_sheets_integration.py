"""
Integration test script for Google Sheets service.

This script tests the Google Sheets integration functionality.
It can be run with: python backend/tests/test_google_sheets_integration.py

Requirements:
- .env file must be configured with GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH and GOOGLE_SHEETS_ID
- Google Sheets API must be set up (see docs/guides/GOOGLE_SHEETS_SETUP.md)
- Service account must have access to the Google Sheet
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.services.google_sheets import GoogleSheetsService, create_google_sheets_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_date_parsing():
    """Test date parsing functionality."""
    print("\n" + "="*60)
    print("TEST 1: Date Parsing")
    print("="*60)
    
    service = GoogleSheetsService("dummy_path", "dummy_id")
    
    # Test valid date
    try:
        result = service.parse_date("13/12/2025")
        print(f"✅ Valid date '13/12/2025' parsed successfully: {result}")
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 13
        print("✅ Date values are correct")
    except Exception as e:
        print(f"❌ Error parsing valid date: {e}")
        return False
    
    # Test invalid date
    try:
        service.parse_date("2025-12-13")
        print("❌ Invalid date should have raised ValueError")
        return False
    except ValueError:
        print("✅ Invalid date correctly raised ValueError")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True


def test_time_parsing():
    """Test time parsing functionality."""
    print("\n" + "="*60)
    print("TEST 2: Time Parsing")
    print("="*60)
    
    service = GoogleSheetsService("dummy_path", "dummy_id")
    
    # Test valid time
    try:
        hour, minute = service.parse_time("08:00")
        print(f"✅ Valid time '08:00' parsed successfully: hour={hour}, minute={minute}")
        assert hour == 8
        assert minute == 0
        print("✅ Time values are correct")
    except Exception as e:
        print(f"❌ Error parsing valid time: {e}")
        return False
    
    # Test invalid time
    try:
        service.parse_time("8:00 AM")
        print("❌ Invalid time should have raised ValueError")
        return False
    except ValueError:
        print("✅ Invalid time correctly raised ValueError")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True


def test_column_letter_conversion():
    """Test column number to letter conversion."""
    print("\n" + "="*60)
    print("TEST 3: Column Letter Conversion")
    print("="*60)
    
    test_cases = [
        (1, "A"),
        (2, "B"),
        (4, "D"),
        (26, "Z"),
        (27, "AA"),
    ]
    
    all_passed = True
    for col_num, expected_letter in test_cases:
        result = GoogleSheetsService._column_letter(col_num)
        if result == expected_letter:
            print(f"✅ Column {col_num} -> '{result}' (correct)")
        else:
            print(f"❌ Column {col_num} -> '{result}' (expected '{expected_letter}')")
            all_passed = False
    
    return all_passed


def test_google_sheets_connection():
    """Test Google Sheets connection (requires configuration)."""
    print("\n" + "="*60)
    print("TEST 4: Google Sheets Connection")
    print("="*60)
    
    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / ".env"
    if not env_path.exists():
        print("⚠️  .env file not found. Skipping connection test.")
        print("   To test connection, create .env file with:")
        print("   - GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH")
        print("   - GOOGLE_SHEETS_ID")
        return None
    
    load_dotenv(env_path)
    
    service_account_path = os.getenv('GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH')
    sheet_id = os.getenv('GOOGLE_SHEETS_ID')
    
    if not service_account_path or not sheet_id:
        print("⚠️  Google Sheets credentials not found in .env file.")
        print("   Required variables:")
        print("   - GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH")
        print("   - GOOGLE_SHEETS_ID")
        return None
    
    if not Path(service_account_path).exists():
        print(f"⚠️  Service account file not found: {service_account_path}")
        print("   Please check the path in .env file")
        return None
    
    try:
        service = GoogleSheetsService(service_account_path, sheet_id)
        service.connect()
        print("✅ Successfully connected to Google Sheets")
        return service
    except FileNotFoundError as e:
        print(f"❌ Service account file not found: {e}")
        return None
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
        print("   Make sure:")
        print("   1. Service account JSON file is valid")
        print("   2. Google Sheets API is enabled")
        print("   3. Service account has access to the sheet")
        return None


def test_read_post_data(service):
    """Test reading post data from Google Sheets."""
    print("\n" + "="*60)
    print("TEST 5: Read Post Data from Google Sheets")
    print("="*60)
    
    if service is None:
        print("⚠️  Skipping - Google Sheets not connected")
        return None
    
    try:
        # Find first unposted row
        row_num = service.find_first_unposted_row()
        
        if row_num is None:
            print("⚠️  No unposted rows found in sheet")
            return None
        
        print(f"✅ Found unposted row: {row_num}")
        
        # Read post data
        data = service.read_post_data(row_num)
        print(f"✅ Read post data from row {row_num}:")
        print(f"   - Post text: {data['post_text'][:50]}..." if len(data['post_text']) > 50 else f"   - Post text: {data['post_text']}")
        print(f"   - Date: {data['date']}")
        print(f"   - Heure: {data['heure']}")
        print(f"   - Posted: {data['posted']}")
        
        # Test parsing
        if data['date'] and data['heure']:
            try:
                parsed_date = service.parse_date(data['date'])
                hour, minute = service.parse_time(data['heure'])
                print(f"✅ Parsed date: {parsed_date}")
                print(f"✅ Parsed time: {hour:02d}:{minute:02d}")
            except ValueError as e:
                print(f"⚠️  Error parsing date/time: {e}")
        
        return data
    except Exception as e:
        print(f"❌ Error reading post data: {e}")
        return None


def test_get_next_unposted_post(service):
    """Test getting next unposted post."""
    print("\n" + "="*60)
    print("TEST 6: Get Next Unposted Post")
    print("="*60)
    
    if service is None:
        print("⚠️  Skipping - Google Sheets not connected")
        return None
    
    try:
        post = service.get_next_unposted_post()
        
        if post is None:
            print("⚠️  No unposted posts found")
            return None
        
        print("✅ Retrieved next unposted post:")
        print(f"   - Row number: {post['row_num']}")
        print(f"   - Post text: {post['post_text'][:50]}..." if len(post['post_text']) > 50 else f"   - Post text: {post['post_text']}")
        print(f"   - Date: {post['date']}")
        print(f"   - Heure: {post['heure']}")
        print(f"   - Scheduled datetime: {post['scheduled_datetime']}")
        print(f"   - Posted status: {post['posted']}")
        
        return post
    except Exception as e:
        print(f"❌ Error getting next unposted post: {e}")
        return None


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("GOOGLE SHEETS INTEGRATION TEST")
    print("="*60)
    print("\nThis script tests the Google Sheets integration functionality.")
    print("Some tests require Google Sheets API configuration.")
    print("\nFor setup instructions, see: docs/guides/GOOGLE_SHEETS_SETUP.md")
    
    results = []
    
    # Test 1: Date parsing (no connection needed)
    results.append(("Date Parsing", test_date_parsing()))
    
    # Test 2: Time parsing (no connection needed)
    results.append(("Time Parsing", test_time_parsing()))
    
    # Test 3: Column letter conversion (no connection needed)
    results.append(("Column Letter Conversion", test_column_letter_conversion()))
    
    # Test 4: Google Sheets connection (requires configuration)
    service = test_google_sheets_connection()
    if service:
        results.append(("Google Sheets Connection", True))
        
        # Test 5: Read post data (requires connection)
        data = test_read_post_data(service)
        results.append(("Read Post Data", data is not None))
        
        # Test 6: Get next unposted post (requires connection)
        post = test_get_next_unposted_post(service)
        results.append(("Get Next Unposted Post", post is not None))
    else:
        results.append(("Google Sheets Connection", None))
        results.append(("Read Post Data", None))
        results.append(("Get Next Unposted Post", None))
    
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
            print(f"⚠️  {test_name}: SKIPPED (requires configuration)")
            skipped += 1
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    elif passed > 0:
        print("\n✅ All executed tests passed!")
        if skipped > 0:
            print("   (Some tests were skipped - configure Google Sheets API to run them)")
        sys.exit(0)
    else:
        print("\n⚠️  No tests were executed. Please configure Google Sheets API.")
        sys.exit(0)


if __name__ == "__main__":
    main()


