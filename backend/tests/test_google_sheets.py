"""
Unit tests for Google Sheets service.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from backend.services.google_sheets import GoogleSheetsService


class TestGoogleSheetsService:
    """Test cases for GoogleSheetsService."""
    
    def test_parse_date_valid(self):
        """Test parsing valid date in DD/MM/YYYY format."""
        service = GoogleSheetsService("dummy_path", "dummy_id")
        result = service.parse_date("13/12/2025")
        assert result == datetime(2025, 12, 13)
    
    def test_parse_date_invalid(self):
        """Test parsing invalid date format."""
        service = GoogleSheetsService("dummy_path", "dummy_id")
        with pytest.raises(ValueError):
            service.parse_date("2025-12-13")
    
    def test_parse_time_valid(self):
        """Test parsing valid time in HH:MM format."""
        service = GoogleSheetsService("dummy_path", "dummy_id")
        hour, minute = service.parse_time("08:00")
        assert hour == 8
        assert minute == 0
    
    def test_parse_time_invalid(self):
        """Test parsing invalid time format."""
        service = GoogleSheetsService("dummy_path", "dummy_id")
        with pytest.raises(ValueError):
            service.parse_time("8:00 AM")
    
    def test_column_letter(self):
        """Test column number to letter conversion."""
        assert GoogleSheetsService._column_letter(1) == "A"
        assert GoogleSheetsService._column_letter(2) == "B"
        assert GoogleSheetsService._column_letter(4) == "D"
        assert GoogleSheetsService._column_letter(26) == "Z"
        assert GoogleSheetsService._column_letter(27) == "AA"
    
    @patch('backend.services.google_sheets.Credentials')
    @patch('backend.services.google_sheets.gspread')
    def test_connect_success(self, mock_gspread, mock_credentials):
        """Test successful connection to Google Sheets."""
        # Setup mocks
        mock_creds = Mock()
        mock_credentials.from_service_account_file.return_value = mock_creds
        
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        
        mock_sheet = Mock()
        mock_sheet.title = "Test Sheet"
        mock_client.open_by_key.return_value = mock_sheet
        
        mock_worksheet = Mock()
        mock_sheet.sheet1 = mock_worksheet
        
        # Test
        service = GoogleSheetsService("test_path.json", "test_id")
        service.connect()
        
        # Assertions
        assert service.client == mock_client
        assert service.sheet == mock_sheet
        assert service.worksheet == mock_worksheet
    
    @patch('backend.services.google_sheets.Credentials')
    @patch('backend.services.google_sheets.gspread')
    def test_find_first_unposted_row(self, mock_gspread, mock_credentials):
        """Test finding first unposted row."""
        # Setup mocks
        mock_worksheet = Mock()
        mock_worksheet.col_values.return_value = ["posted", "no", "oui", "no"]
        
        service = GoogleSheetsService("test_path.json", "test_id")
        service.worksheet = mock_worksheet
        
        # Test
        result = service.find_first_unposted_row()
        
        # Assertions
        assert result == 2  # Second row (first "no" after header)
    
    @patch('backend.services.google_sheets.Credentials')
    @patch('backend.services.google_sheets.gspread')
    def test_read_post_data(self, mock_gspread, mock_credentials):
        """Test reading post data from a row."""
        # Setup mocks
        mock_worksheet = Mock()
        mock_worksheet.row_values.return_value = [
            "Test post text",
            "13/12/2025",
            "08:00",
            "no"
        ]
        
        service = GoogleSheetsService("test_path.json", "test_id")
        service.worksheet = mock_worksheet
        
        # Test
        result = service.read_post_data(2)
        
        # Assertions
        assert result['post_text'] == "Test post text"
        assert result['date'] == "13/12/2025"
        assert result['heure'] == "08:00"
        assert result['posted'] == "no"
    
    @patch('backend.services.google_sheets.Credentials')
    @patch('backend.services.google_sheets.gspread')
    def test_update_post_status(self, mock_gspread, mock_credentials):
        """Test updating post status."""
        # Setup mocks
        mock_worksheet = Mock()
        
        service = GoogleSheetsService("test_path.json", "test_id")
        service.worksheet = mock_worksheet
        
        # Test
        service.update_post_status(2, "oui")
        
        # Assertions
        mock_worksheet.update.assert_called_once_with("D2", "oui")
    
    @patch('backend.services.google_sheets.Credentials')
    @patch('backend.services.google_sheets.gspread')
    def test_get_next_unposted_post(self, mock_gspread, mock_credentials):
        """Test getting next unposted post with parsed date/time."""
        # Setup mocks
        mock_worksheet = Mock()
        mock_worksheet.col_values.return_value = ["posted", "no"]  # Header + one row
        mock_worksheet.row_values.return_value = [
            "Test post",
            "13/12/2025",
            "08:00",
            "no"
        ]
        
        service = GoogleSheetsService("test_path.json", "test_id")
        service.worksheet = mock_worksheet
        
        # Test
        result = service.get_next_unposted_post()
        
        # Assertions
        assert result is not None
        assert result['row_num'] == 2
        assert result['post_text'] == "Test post"
        assert result['date'] == "13/12/2025"
        assert result['heure'] == "08:00"
        assert isinstance(result['scheduled_datetime'], datetime)
        assert result['scheduled_datetime'].year == 2025
        assert result['scheduled_datetime'].month == 12
        assert result['scheduled_datetime'].day == 13
        assert result['scheduled_datetime'].hour == 8
        assert result['scheduled_datetime'].minute == 0


