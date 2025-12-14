"""
Google Sheets integration for LinkedIn Automation V1.

This module handles reading and writing post data from Google Sheets.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Tuple
import gspread
from google.oauth2.service_account import Credentials
import logging

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Service for interacting with Google Sheets."""
    
    # Column indices (1-based for gspread)
    COL_POST_TEXT = 1  # Column A
    COL_DATE = 2       # Column B
    COL_POSTED = 3     # Column C
    
    # Header row
    HEADER_ROW = 1
    
    def __init__(self, service_account_path: str, sheet_id: str):
        """
        Initialize Google Sheets service.
        
        Args:
            service_account_path: Path to service account JSON key file
            sheet_id: Google Sheets ID
        """
        self.service_account_path = service_account_path
        self.sheet_id = sheet_id
        self.client = None
        self.sheet = None
        self.worksheet = None
        
    def connect(self) -> None:
        """Connect to Google Sheets and open the worksheet."""
        try:
            # Define scopes
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                self.service_account_path,
                scopes=scopes
            )
            
            # Authorize client
            self.client = gspread.authorize(creds)
            
            # Open the sheet
            self.sheet = self.client.open_by_key(self.sheet_id)
            
            # Get the first worksheet
            self.worksheet = self.sheet.sheet1
            
            logger.info(f"Successfully connected to Google Sheet: {self.sheet.title}")
            
        except FileNotFoundError:
            logger.error(f"Service account file not found: {self.service_account_path}")
            raise
        except gspread.exceptions.APIError as e:
            logger.error(f"Google Sheets API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error connecting to Google Sheets: {e}")
            raise
    
    def find_first_unposted_row(self) -> Optional[int]:
        """
        Find the first row where posted status is "no".
        
        Returns:
            Row number (1-based) if found, None otherwise
        """
        if not self.worksheet:
            raise ValueError("Not connected to Google Sheets. Call connect() first.")
        
        try:
            # Get all values in the posted column (Column C)
            posted_column = self.worksheet.col_values(self.COL_POSTED)
            
            # Start from row 2 (skip header)
            for row_num in range(2, len(posted_column) + 1):
                status = posted_column[row_num - 1].strip().lower()
                if status == "no":
                    logger.info(f"Found unposted row: {row_num}")
                    return row_num
            
            logger.info("No unposted rows found")
            return None
            
        except Exception as e:
            logger.error(f"Error finding unposted row: {e}")
            raise
    
    def read_post_data(self, row_num: int) -> Dict[str, str]:
        """
        Read post data from a specific row.
        
        Args:
            row_num: Row number (1-based)
            
        Returns:
            Dictionary with keys: 'post_text', 'date', 'posted'
        """
        if not self.worksheet:
            raise ValueError("Not connected to Google Sheets. Call connect() first.")
        
        try:
            # Read all columns for this row
            row_values = self.worksheet.row_values(row_num)
            
            # Extract values (handle missing columns)
            post_text = row_values[self.COL_POST_TEXT - 1] if len(row_values) >= self.COL_POST_TEXT else ""
            date = row_values[self.COL_DATE - 1] if len(row_values) >= self.COL_DATE else ""
            posted = row_values[self.COL_POSTED - 1] if len(row_values) >= self.COL_POSTED else ""
            
            data = {
                'post_text': post_text.strip(),
                'date': date.strip(),
                'posted': posted.strip().lower()
            }
            
            logger.info(f"Read post data from row {row_num}: {data}")
            return data
            
        except Exception as e:
            logger.error(f"Error reading post data from row {row_num}: {e}")
            raise
    
    def parse_date(self, date_str: str) -> datetime:
        """
        Parse date string in DD/MM/YYYY format.
        
        Args:
            date_str: Date string in DD/MM/YYYY format (e.g., "13/12/2025")
            
        Returns:
            datetime object
        """
        try:
            return datetime.strptime(date_str.strip(), "%d/%m/%Y")
        except ValueError as e:
            logger.error(f"Error parsing date '{date_str}': {e}")
            raise ValueError(f"Invalid date format. Expected DD/MM/YYYY, got: {date_str}")
    
    def parse_time(self, time_str: str) -> Tuple[int, int]:
        """
        Parse time string in HH:MM format.
        
        Args:
            time_str: Time string in HH:MM format (e.g., "08:00")
            
        Returns:
            Tuple of (hour, minute)
        """
        try:
            time_obj = datetime.strptime(time_str.strip(), "%H:%M").time()
            return (time_obj.hour, time_obj.minute)
        except ValueError as e:
            logger.error(f"Error parsing time '{time_str}': {e}")
            raise ValueError(f"Invalid time format. Expected HH:MM, got: {time_str}")
    
    def update_post_status(self, row_num: int, status: str = "yes") -> None:
        """
        Update the posted status for a row.
        
        Args:
            row_num: Row number (1-based)
            status: Status to set (default: "yes")
        """
        if not self.worksheet:
            raise ValueError("Not connected to Google Sheets. Call connect() first.")
        
        try:
            # Update the posted column (Column C)
            # gspread.update() expects a list of lists
            cell_address = f"{self._column_letter(self.COL_POSTED)}{row_num}"
            self.worksheet.update(cell_address, [[status]])
            
            logger.info(f"Updated row {row_num} status to '{status}'")
            
        except Exception as e:
            logger.error(f"Error updating post status for row {row_num}: {e}")
            raise
    
    def find_post_for_today(self) -> Optional[Dict]:
        """
        Find the first post where date matches today's date and posted = "no".
        If multiple posts have the same date, returns the first one in the file.
        
        Returns:
            Dictionary with post data including row_num, or None if no post found for today
        """
        if not self.worksheet:
            raise ValueError("Not connected to Google Sheets. Call connect() first.")
        
        try:
            from datetime import date
            
            today = date.today()
            logger.info(f"Looking for post with date: {today.strftime('%d/%m/%Y')}")
            
            # Get all rows (starting from row 2, skip header)
            all_rows = self.worksheet.get_all_values()
            
            # Start from row 2 (skip header)
            for row_idx, row_values in enumerate(all_rows[1:], start=2):
                try:
                    # Extract values
                    if len(row_values) < self.COL_POSTED:
                        continue
                    
                    post_text = row_values[self.COL_POST_TEXT - 1].strip() if len(row_values) >= self.COL_POST_TEXT else ""
                    date_str = row_values[self.COL_DATE - 1].strip() if len(row_values) >= self.COL_DATE else ""
                    posted = row_values[self.COL_POSTED - 1].strip().lower() if len(row_values) >= self.COL_POSTED else ""
                    
                    # Skip if already posted
                    if posted == "yes":
                        continue
                    
                    # Skip if no date
                    if not date_str:
                        continue
                    
                    # Parse date and compare with today
                    try:
                        parsed_date = self.parse_date(date_str)
                        if parsed_date.date() == today:
                            logger.info(f"✅ Found post for today at row {row_idx}")
                            return {
                                'row_num': row_idx,
                                'post_text': post_text,
                                'date': date_str,
                                'posted': posted
                            }
                    except ValueError:
                        # Invalid date format, skip
                        logger.debug(f"Row {row_idx} has invalid date format: {date_str}")
                        continue
                        
                except Exception as e:
                    logger.debug(f"Error processing row {row_idx}: {e}")
                    continue
            
            logger.info("No post found for today")
            return None
            
        except Exception as e:
            logger.error(f"Error finding post for today: {e}")
            raise
    
    def get_next_unposted_post(self) -> Optional[Dict]:
        """
        Get the next unposted post data.
        
        Returns:
            Dictionary with post data including parsed date/time, or None if no unposted posts
        """
        try:
            # Find first unposted row
            row_num = self.find_first_unposted_row()
            
            if row_num is None:
                return None
            
            # Read post data
            data = self.read_post_data(row_num)
            
            # Validate required fields
            if not data['post_text']:
                logger.warning(f"Row {row_num} has empty post text")
                return None
            
            if not data['date']:
                logger.warning(f"Row {row_num} has empty date")
                return None
            
            if not data['heure']:
                logger.warning(f"Row {row_num} has empty heure")
                return None
            
            # Parse date and time
            try:
                parsed_date = self.parse_date(data['date'])
                hour, minute = self.parse_time(data['heure'])
                
                # Combine date and time
                scheduled_datetime = datetime.combine(parsed_date.date(), datetime.min.time().replace(hour=hour, minute=minute))
                
                return {
                    'row_num': row_num,
                    'post_text': data['post_text'],
                    'date': data['date'],
                    'heure': data['heure'],
                    'scheduled_datetime': scheduled_datetime,
                    'posted': data['posted']
                }
                
            except ValueError as e:
                logger.error(f"Error parsing date/time for row {row_num}: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting next unposted post: {e}")
            raise
    
    @staticmethod
    def _column_letter(col_num: int) -> str:
        """
        Convert column number to letter (1 = A, 2 = B, etc.).
        
        Args:
            col_num: Column number (1-based)
            
        Returns:
            Column letter (A, B, C, etc.)
        """
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(65 + (col_num % 26)) + result
            col_num //= 26
        return result


def create_google_sheets_service() -> GoogleSheetsService:
    """
    Factory function to create GoogleSheetsService from environment variables.
    
    Returns:
        GoogleSheetsService instance
    """
    service_account_path = os.getenv('GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH')
    sheet_id = os.getenv('GOOGLE_SHEETS_ID')
    
    if not service_account_path:
        raise ValueError("GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH environment variable not set")
    
    if not sheet_id:
        raise ValueError("GOOGLE_SHEETS_ID environment variable not set")
    
    return GoogleSheetsService(service_account_path, sheet_id)


