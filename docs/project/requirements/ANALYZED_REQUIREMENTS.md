# Analyzed Requirements

This document contains the rephrased, clarified, and structured requirements derived from `RAW_REQUIREMENTS.md`.

## Analysis Process

Requirements are analyzed to:
- **Clarify ambiguity** - Remove vague terms, add specifics
- **Identify dependencies** - Understand what needs to come first
- **Categorize** - Group related requirements
- **Prioritize** - Identify must-haves vs. nice-to-haves
- **Break down** - Separate complex requirements into smaller parts

---

## Requirements Overview

**Feature**: LinkedIn Post Automation V1
**Goal**: Automate posting a single LinkedIn post from Google Sheets at a scheduled date/time using browser automation.

**Key Components**:
1. Google Sheets integration (read post data)
2. Scheduling system (wait for scheduled time)
3. Browser automation (post to LinkedIn)
4. Status tracking (mark as posted in sheet)

---

## Categorized Requirements

### Functional Requirements

#### FR1: Google Sheets Data Reading
- **FR1.1**: Connect to Google Sheets using service account or OAuth
- **FR1.2**: Read post text from Column A ("post text" header)
- **FR1.3**: Read scheduled date from Column B ("date" header) - Format: DD/MM/YYYY
- **FR1.4**: Read scheduled hour from Column C ("heure" header) - Format: HH:MM (24-hour)
- **FR1.5**: Identify which post to process (V1: first row where Column D "posted" = "no")
- **FR1.6**: Parse date format DD/MM/YYYY and time format HH:MM correctly

#### FR2: Post Scheduling (via LinkedIn)
- **FR2.1**: Use LinkedIn's built-in "Schedule" feature (not wait for time)
- **FR2.2**: Script can run at any time - no need to wait
- **FR2.3**: Set scheduled date and time in LinkedIn's scheduling UI
- **FR2.4**: Handle timezone considerations when setting schedule in LinkedIn

#### FR3: LinkedIn Posting via Browser Automation
- **FR3.1**: Launch browser (headless or visible mode)
- **FR3.2**: Navigate to LinkedIn login page
- **FR3.3**: Authenticate with LinkedIn credentials (no 2FA)
- **FR3.4**: Navigate to LinkedIn post creation interface
- **FR3.5**: Enter post text content
- **FR3.6**: Click "Schedule" button (instead of "Post")
- **FR3.7**: Set scheduled date and time in LinkedIn's scheduling UI
- **FR3.8**: Confirm schedule in LinkedIn
- **FR3.9**: Verify post was scheduled successfully (appears in scheduled posts)

#### FR4: Status Tracking
- **FR4.1**: Update Google Sheet Column D ("posted") to "oui" after successful scheduling in LinkedIn
- **FR4.2**: Only update status if post was successfully scheduled
- **FR4.3**: Handle failed scheduling (keep status as "no" or mark with error indicator)

#### FR5: Error Handling & Logging
- **FR5.1**: Log all actions (reading sheet, connecting to LinkedIn, scheduling)
- **FR5.2**: Handle authentication failures
- **FR5.3**: Handle network errors
- **FR5.4**: Handle LinkedIn UI changes (element not found, especially Schedule button)
- **FR5.5**: Retry logic for transient failures

### Non-Functional Requirements

#### NFR1: Security
- **NFR1.1**: Store LinkedIn credentials securely (environment variables or encrypted config)
- **NFR1.2**: Store Google Sheets credentials securely
- **NFR1.3**: Never commit credentials to version control

#### NFR2: Reliability
- **NFR2.1**: Handle browser crashes gracefully
- **NFR2.2**: Recover from network interruptions
- **NFR2.3**: Validate data before attempting to post

#### NFR3: Usability
- **NFR3.1**: Clear logging output for debugging
- **NFR3.2**: Simple configuration setup
- **NFR3.3**: Easy to run manually for testing

#### NFR4: Performance
- **NFR4.1**: Browser automation should complete within reasonable time (2-5 minutes per post scheduling)
- **NFR4.2**: Efficient Google Sheets API usage
- **NFR4.3**: Script can run immediately - no waiting for scheduled time

### Constraints & Assumptions

#### Constraints
- **C1**: LinkedIn API is not available - must use browser automation
- **C2**: No 2FA on LinkedIn account (simplifies authentication)
- **C3**: V1 focuses on single post only (not batch processing)
- **C4**: Must work with provided Google Sheets structure

#### Assumptions
- **A1**: Google Sheets has headers in row 1: "post text", "date", "heure", "posted"
- **A2**: Date format is DD/MM/YYYY (e.g., 13/12/2025)
- **A3**: Hour format is 24-hour HH:MM (e.g., 08:00)
- **A4**: Status column uses "oui" (posted) or "no" (not posted)
- **A5**: V1 processes first row where status is "no"
- **A6**: LinkedIn account has permission to post
- **A7**: Browser automation won't be blocked by LinkedIn (may need to handle CAPTCHA in future)

---

## Requirements Breakdown

### Priority 1 (Must Have - MVP V1)

1. **Google Sheets Integration**
   - Read post text, date, and hour from specified columns
   - Connect to Google Sheets API

2. **LinkedIn Posting with Scheduling**
   - Browser automation to log in
   - Create post with text content
   - Use LinkedIn's "Schedule" feature to program post
   - Set date and time in LinkedIn's scheduling UI
   - Basic error handling

3. **Status Update**
   - Mark post as "posted" (scheduled) in Google Sheet

4. **Logging**
   - Basic logging of all operations

### Priority 2 (Should Have - V1 Enhancement)

1. **Better Error Handling**
   - Retry logic for failed posts
   - Detailed error messages

2. **Configuration Management**
   - Easy setup of credentials
   - Configurable sheet structure

3. **Validation**
   - Validate date/time formats
   - Validate post content before posting

### Priority 3 (Nice to Have - Future Versions)

1. **Multiple Posts Scheduler** (V2+)
2. **Post Analytics** (V3+)
3. **Image/Media Support** (V4+)
4. **Multiple LinkedIn Accounts** (V5+)
5. **Advanced Scheduling** (recurring posts, etc.) (V6+)

---

## Functionalities Identified

1. **LinkedIn Post Automation V1** - Core functionality to schedule and post a single LinkedIn post from Google Sheets
   - Google Sheets integration
   - Post scheduling
   - Browser automation for LinkedIn
   - Status tracking

---

## Technical Stack Additions

### New Dependencies
- **gspread** - Google Sheets API client
- **google-auth** - Google authentication
- **playwright** or **selenium** - Browser automation
- **python-dotenv** - Environment variable management

**Note**: No task scheduler needed (APScheduler/schedule) - LinkedIn handles the scheduling via its built-in Schedule feature

### Architecture Components
- Google Sheets reader module
- Date/time formatter module (convert DD/MM/YYYY and HH:MM to LinkedIn format)
- LinkedIn automation module (with scheduling)
- Status updater module
- Configuration manager

---

## Next Steps

1. ✅ Create feature file in `../features/LINKEDIN_AUTOMATION_V1.md` with detailed implementation plan
2. Break down functionality into implementation steps
3. Link features back to requirements for traceability
4. Get user approval before implementation

---

**Related Documents**:
- [Raw Requirements](./RAW_REQUIREMENTS.md)
- [Feature Template](./TEMPLATE.md)
- [Features Directory](../features/README.md)
