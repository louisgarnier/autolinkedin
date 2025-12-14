"""
Integration test script for configuration settings.

This script tests the configuration management functionality.
It can be run with: python backend/tests/test_config_settings.py
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch
import tempfile

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import Settings, ConfigError, get_settings, validate_settings


def test_settings_loading():
    """Test loading settings from environment variables."""
    print("\n" + "="*60)
    print("TEST 1: Settings Loading")
    print("="*60)
    
    # Test with mock environment variables
    with patch.dict(os.environ, {
        'LINKEDIN_EMAIL': 'test@example.com',
        'LINKEDIN_PASSWORD': 'test_password',
        'GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH': 'backend/config/service-account-key.json',
        'GOOGLE_SHEETS_ID': 'test_sheet_id',
        'BROWSER_MODE': 'visible',
        'LOG_LEVEL': 'INFO'
    }):
        settings = Settings.load()
        
        assert settings.LINKEDIN_EMAIL == 'test@example.com'
        assert settings.LINKEDIN_PASSWORD == 'test_password'
        assert settings.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH == 'backend/config/service-account-key.json'
        assert settings.GOOGLE_SHEETS_ID == 'test_sheet_id'
        assert settings.BROWSER_MODE == 'visible'
        assert settings.LOG_LEVEL == 'INFO'
        
        print("✅ Settings loaded correctly from environment variables")
        return True


def test_settings_validation_success():
    """Test settings validation with all required fields."""
    print("\n" + "="*60)
    print("TEST 2: Settings Validation (Success)")
    print("="*60)
    
    # Create a temporary file for service account
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"test": "data"}')
        temp_path = f.name
    
    try:
        settings = Settings()
        settings.LINKEDIN_EMAIL = 'test@example.com'
        settings.LINKEDIN_PASSWORD = 'test_password'
        settings.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH = temp_path
        settings.GOOGLE_SHEETS_ID = 'test_sheet_id'
        
        # Should not raise an error
        settings.validate()
        print("✅ Settings validation passed with all required fields")
        return True
    except ConfigError as e:
        print(f"❌ Unexpected validation error: {e}")
        return False
    finally:
        # Clean up temp file
        Path(temp_path).unlink()


def test_settings_validation_missing_fields():
    """Test settings validation with missing required fields."""
    print("\n" + "="*60)
    print("TEST 3: Settings Validation (Missing Fields)")
    print("="*60)
    
    settings = Settings()
    
    # Test missing LinkedIn email
    try:
        settings.validate()
        print("❌ Should have raised ConfigError for missing fields")
        return False
    except ConfigError as e:
        print("✅ Correctly raised ConfigError for missing fields")
        print(f"   Error message: {str(e)[:100]}...")
        return True


def test_get_linkedin_credentials():
    """Test getting LinkedIn credentials."""
    print("\n" + "="*60)
    print("TEST 4: Get LinkedIn Credentials")
    print("="*60)
    
    settings = Settings()
    settings.LINKEDIN_EMAIL = 'test@example.com'
    settings.LINKEDIN_PASSWORD = 'test_password'
    
    email, password = settings.get_linkedin_credentials()
    
    assert email == 'test@example.com'
    assert password == 'test_password'
    print("✅ LinkedIn credentials retrieved correctly")
    
    # Test missing credentials
    settings.LINKEDIN_EMAIL = None
    try:
        settings.get_linkedin_credentials()
        print("❌ Should have raised ConfigError for missing credentials")
        return False
    except ConfigError:
        print("✅ Correctly raised ConfigError for missing credentials")
        return True


def test_get_google_sheets_config():
    """Test getting Google Sheets configuration."""
    print("\n" + "="*60)
    print("TEST 5: Get Google Sheets Config")
    print("="*60)
    
    # Create a temporary file for service account
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"test": "data"}')
        temp_path = f.name
    
    try:
        settings = Settings()
        settings.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH = temp_path
        settings.GOOGLE_SHEETS_ID = 'test_sheet_id'
        
        config = settings.get_google_sheets_config()
        
        assert config['service_account_path'] == temp_path
        assert config['sheet_id'] == 'test_sheet_id'
        print("✅ Google Sheets config retrieved correctly")
        
        # Test missing config
        settings.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH = None
        try:
            settings.get_google_sheets_config()
            print("❌ Should have raised ConfigError for missing config")
            return False
        except ConfigError:
            print("✅ Correctly raised ConfigError for missing config")
            return True
    finally:
        # Clean up temp file
        Path(temp_path).unlink()


def test_browser_mode_validation():
    """Test browser mode validation."""
    print("\n" + "="*60)
    print("TEST 6: Browser Mode Validation")
    print("="*60)
    
    with patch.dict(os.environ, {'BROWSER_MODE': 'headless'}):
        settings = Settings.load()
        assert settings.BROWSER_MODE == 'headless'
        print("✅ Browser mode 'headless' loaded correctly")
    
    with patch.dict(os.environ, {'BROWSER_MODE': 'invalid'}):
        settings = Settings.load()
        assert settings.BROWSER_MODE == 'visible'  # Should default to visible
        print("✅ Invalid browser mode defaulted to 'visible'")
    
    return True


def test_log_level_validation():
    """Test log level validation."""
    print("\n" + "="*60)
    print("TEST 7: Log Level Validation")
    print("="*60)
    
    with patch.dict(os.environ, {'LOG_LEVEL': 'DEBUG'}):
        settings = Settings.load()
        assert settings.LOG_LEVEL == 'DEBUG'
        print("✅ Log level 'DEBUG' loaded correctly")
    
    with patch.dict(os.environ, {'LOG_LEVEL': 'invalid'}):
        settings = Settings.load()
        assert settings.LOG_LEVEL == 'INFO'  # Should default to INFO
        print("✅ Invalid log level defaulted to 'INFO'")
    
    return True


def test_real_env_file():
    """Test loading from real .env file if it exists."""
    print("\n" + "="*60)
    print("TEST 8: Real .env File Loading")
    print("="*60)
    
    env_path = Path(__file__).parent.parent.parent / ".env"
    
    if env_path.exists():
        # Reset global settings to force reload
        import backend.config.settings as settings_module
        settings_module._settings = None
        
        settings = get_settings()
        
        print(f"✅ Loaded settings from {env_path}")
        print(f"   LinkedIn email: {'***' if settings.LINKEDIN_EMAIL else 'Not set'}")
        print(f"   Google Sheets ID: {settings.GOOGLE_SHEETS_ID or 'Not set'}")
        print(f"   Browser mode: {settings.BROWSER_MODE}")
        print(f"   Log level: {settings.LOG_LEVEL}")
        
        # Try validation (might fail if credentials not set, that's OK)
        try:
            settings.validate()
            print("✅ Settings validation passed")
        except ConfigError as e:
            print(f"⚠️  Settings validation failed (expected if credentials not set): {str(e)[:100]}...")
        
        return True
    else:
        print(f"⚠️  .env file not found at {env_path}, skipping real file test")
        return None


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("CONFIGURATION SETTINGS TEST")
    print("="*60)
    print("\nThis script tests the configuration management functionality.")
    
    results = []
    
    # Test 1: Settings loading
    results.append(("Settings Loading", test_settings_loading()))
    
    # Test 2: Validation success
    results.append(("Settings Validation (Success)", test_settings_validation_success()))
    
    # Test 3: Validation missing fields
    results.append(("Settings Validation (Missing Fields)", test_settings_validation_missing_fields()))
    
    # Test 4: Get LinkedIn credentials
    results.append(("Get LinkedIn Credentials", test_get_linkedin_credentials()))
    
    # Test 5: Get Google Sheets config
    results.append(("Get Google Sheets Config", test_get_google_sheets_config()))
    
    # Test 6: Browser mode validation
    results.append(("Browser Mode Validation", test_browser_mode_validation()))
    
    # Test 7: Log level validation
    results.append(("Log Level Validation", test_log_level_validation()))
    
    # Test 8: Real .env file
    result = test_real_env_file()
    results.append(("Real .env File Loading", result))
    
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
        print("\n❌ Some tests failed. Please check the errors above.")
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

