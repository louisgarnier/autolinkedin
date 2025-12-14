"""
Configuration management for LinkedIn Automation V1.

This module handles loading and validating environment variables from .env file.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"Loaded environment variables from {env_path}")
else:
    logger.warning(f".env file not found at {env_path}")


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class Settings:
    """Application settings loaded from environment variables."""
    
    # LinkedIn credentials
    LINKEDIN_EMAIL: Optional[str] = None
    LINKEDIN_PASSWORD: Optional[str] = None
    
    # Google Sheets configuration
    GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH: Optional[str] = None
    GOOGLE_SHEETS_ID: Optional[str] = None
    
    # Browser configuration
    BROWSER_MODE: str = "visible"  # Default: visible
    
    # Logging
    LOG_LEVEL: str = "INFO"  # Default: INFO
    
    @classmethod
    def load(cls) -> 'Settings':
        """
        Load all settings from environment variables.
        
        Returns:
            Settings instance with loaded values
        """
        settings = cls()
        
        # LinkedIn credentials
        settings.LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
        settings.LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
        
        # Google Sheets configuration
        settings.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH = os.getenv('GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH')
        settings.GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
        
        # Browser configuration
        browser_mode = os.getenv('BROWSER_MODE', 'visible').lower()
        if browser_mode in ['visible', 'headless']:
            settings.BROWSER_MODE = browser_mode
        else:
            logger.warning(f"Invalid BROWSER_MODE '{browser_mode}', using default 'visible'")
            settings.BROWSER_MODE = "visible"
        
        # Logging
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        if log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            settings.LOG_LEVEL = log_level
        else:
            logger.warning(f"Invalid LOG_LEVEL '{log_level}', using default 'INFO'")
            settings.LOG_LEVEL = "INFO"
        
        return settings
    
    def validate(self) -> None:
        """
        Validate that all required configuration is present.
        
        Raises:
            ConfigError: If required configuration is missing
        """
        errors = []
        
        # Validate LinkedIn credentials
        if not self.LINKEDIN_EMAIL:
            errors.append("LINKEDIN_EMAIL is required but not set")
        if not self.LINKEDIN_PASSWORD:
            errors.append("LINKEDIN_PASSWORD is required but not set")
        
        # Validate Google Sheets configuration
        if not self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH:
            errors.append("GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH is required but not set")
        elif not Path(self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH).exists():
            errors.append(f"Service account file not found: {self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH}")
        
        if not self.GOOGLE_SHEETS_ID:
            errors.append("GOOGLE_SHEETS_ID is required but not set")
        
        if errors:
            error_msg = "Configuration errors:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ConfigError(error_msg)
    
    def get_linkedin_credentials(self) -> Tuple[str, str]:
        """
        Get LinkedIn credentials.
        
        Returns:
            Tuple of (email, password)
            
        Raises:
            ConfigError: If credentials are not set
        """
        if not self.LINKEDIN_EMAIL or not self.LINKEDIN_PASSWORD:
            raise ConfigError("LinkedIn credentials are not configured")
        return (self.LINKEDIN_EMAIL, self.LINKEDIN_PASSWORD)
    
    def get_google_sheets_config(self) -> Dict[str, str]:
        """
        Get Google Sheets configuration.
        
        Returns:
            Dictionary with 'service_account_path' and 'sheet_id'
            
        Raises:
            ConfigError: If configuration is not set
        """
        if not self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH or not self.GOOGLE_SHEETS_ID:
            raise ConfigError("Google Sheets configuration is not set")
        
        if not Path(self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH).exists():
            raise ConfigError(f"Service account file not found: {self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH}")
        
        return {
            'service_account_path': self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH,
            'sheet_id': self.GOOGLE_SHEETS_ID
        }
    
    def get_browser_mode(self) -> str:
        """
        Get browser mode (visible or headless).
        
        Returns:
            Browser mode string
        """
        return self.BROWSER_MODE
    
    def get_log_level(self) -> str:
        """
        Get log level.
        
        Returns:
            Log level string
        """
        return self.LOG_LEVEL
    
    def __repr__(self) -> str:
        """String representation of settings (hides sensitive data)."""
        return (
            f"Settings("
            f"linkedin_email={'***' if self.LINKEDIN_EMAIL else None}, "
            f"linkedin_password={'***' if self.LINKEDIN_PASSWORD else None}, "
            f"google_sheets_service_account_path={self.GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH}, "
            f"google_sheets_id={self.GOOGLE_SHEETS_ID}, "
            f"browser_mode={self.BROWSER_MODE}, "
            f"log_level={self.LOG_LEVEL}"
            f")"
        )


# Global settings instance (loaded on import)
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    Loads settings if not already loaded.
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings


def validate_settings() -> None:
    """
    Validate the global settings.
    
    Raises:
        ConfigError: If settings are invalid
    """
    settings = get_settings()
    settings.validate()

