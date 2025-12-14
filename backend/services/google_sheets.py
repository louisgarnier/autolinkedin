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
        self.worksheet2 = None  # Sheet2 for V2
        
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
    
    # V2 Methods for Sheet2
    def connect_sheet2(self) -> None:
        """
        Connect to Sheet2 for V2 functionality.
        Must call connect() first to initialize client.
        
        Raises:
            ValueError: If not connected to Google Sheets
            Exception: If Sheet2 doesn't exist
        """
        if not self.client or not self.sheet:
            raise ValueError("Not connected to Google Sheets. Call connect() first.")
        
        try:
            # Get Sheet2 by name
            self.worksheet2 = self.sheet.worksheet("Sheet2")
            logger.info("✅ Connected to Sheet2")
            
        except gspread.exceptions.WorksheetNotFound:
            logger.error("Sheet2 not found in Google Sheet")
            raise ValueError("Sheet2 not found in Google Sheet")
        except Exception as e:
            logger.error(f"Error connecting to Sheet2: {e}")
            raise
    
    def read_subject_from_sheet2(self) -> Optional[str]:
        """
        Read subject from Sheet2, Row 2, Column A.
        
        Returns:
            Subject string, or None if empty/not found
            
        Raises:
            ValueError: If not connected to Sheet2
        """
        if not self.worksheet2:
            raise ValueError("Not connected to Sheet2. Call connect_sheet2() first.")
        
        try:
            # Row 2, Column A (1-based indexing)
            cell_value = self.worksheet2.cell(2, 1).value
            
            if not cell_value or not cell_value.strip():
                logger.warning("Row 2, Column A is empty")
                return None
            
            subject = cell_value.strip()
            logger.info(f"✅ Read subject from Sheet2, Row 2: '{subject[:50]}...'")
            return subject
            
        except Exception as e:
            logger.error(f"Error reading subject from Sheet2: {e}")
            raise
    
    def write_post_to_sheet2(self, post: str) -> None:
        """
        Write generated post to Sheet2, Row 2, Column B.
        Overwrites existing value if present (regeneration support).
        
        Args:
            post: Generated post text to write
            
        Raises:
            ValueError: If not connected to Sheet2
        """
        if not self.worksheet2:
            raise ValueError("Not connected to Sheet2. Call connect_sheet2() first.")
        
        if not post or not post.strip():
            raise ValueError("Post cannot be empty")
        
        try:
            # Row 2, Column B (1-based indexing)
            cell_address = "B2"
            self.worksheet2.update(cell_address, [[post.strip()]])
            
            logger.info(f"✅ Wrote post to Sheet2, Row 2, Column B ({len(post)} characters)")
            
        except Exception as e:
            logger.error(f"Error writing post to Sheet2: {e}")
            raise
    
    def set_post_generated_status(self, status: str = "yes") -> None:
        """
        Set post generated status in Sheet2, Row 2, Column C.
        
        Args:
            status: Status to set (default: "yes")
            
        Raises:
            ValueError: If not connected to Sheet2
        """
        if not self.worksheet2:
            raise ValueError("Not connected to Sheet2. Call connect_sheet2() first.")
        
        try:
            # Row 2, Column C (1-based indexing)
            cell_address = "C2"
            self.worksheet2.update(cell_address, [[status]])
            
            logger.info(f"✅ Set post generated status to '{status}' in Sheet2, Row 2, Column C")
            
        except Exception as e:
            logger.error(f"Error setting post generated status: {e}")
            raise
    
    def read_post_from_sheet2(self) -> Optional[str]:
        """
        Read generated post from Sheet2, Row 2, Column B.
        
        Returns:
            Post text, or None if empty/not found
            
        Raises:
            ValueError: If not connected to Sheet2
        """
        if not self.worksheet2:
            raise ValueError("Not connected to Sheet2. Call connect_sheet2() first.")
        
        try:
            # Row 2, Column B (1-based indexing)
            cell_value = self.worksheet2.cell(2, 2).value
            
            if not cell_value or not cell_value.strip():
                logger.warning("Row 2, Column B is empty")
                return None
            
            post = cell_value.strip()
            logger.info(f"✅ Read post from Sheet2, Row 2, Column B ({len(post)} characters)")
            return post
            
        except Exception as e:
            logger.error(f"Error reading post from Sheet2: {e}")
            raise
    
    def get_post_generated_status(self) -> Optional[str]:
        """
        Get post generated status from Sheet2, Row 2, Column C.
        
        Returns:
            Status string ("yes" or "no"), or None if empty
            
        Raises:
            ValueError: If not connected to Sheet2
        """
        if not self.worksheet2:
            raise ValueError("Not connected to Sheet2. Call connect_sheet2() first.")
        
        try:
            # Row 2, Column C (1-based indexing)
            cell_value = self.worksheet2.cell(2, 3).value
            
            if not cell_value:
                logger.warning("Row 2, Column C is empty")
                return None
            
            status = cell_value.strip().lower()
            logger.info(f"✅ Read post generated status from Sheet2, Row 2, Column C: '{status}'")
            return status
            
        except Exception as e:
            logger.error(f"Error reading post generated status from Sheet2: {e}")
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


