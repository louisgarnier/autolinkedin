# Raw Requirements

This document captures the initial, unprocessed requirements for the project. Requirements can be provided in any format - bullet points, paragraphs, user stories, etc.

## How to Use

1. **Add your requirements below** - Write them as you think of them, in any format
2. **Don't worry about structure** - We'll analyze and rephrase them together
3. **Include context** - Add any relevant background information, constraints, or priorities

---

## Initial Requirements

### LinkedIn Post Automation - V1

**Goal**: Automate posting a single LinkedIn post from a Google Sheets spreadsheet.

**Data Source**:
- Google Sheets link: https://docs.google.com/spreadsheets/d/1E35yLjp_7p7UCjjInmeJUf0AwpkhZqOSvs57E2oIt7A/edit?usp=sharing
- Column A: Post text content
- Column B: Scheduled date
- Column C: Scheduled hour

**Constraints**:
- LinkedIn API is not available, must use browser automation
- No 2FA on LinkedIn account
- Focus on V1: Schedule and post ONE post (first iteration)
- Future versions (V2-V10) will add advanced features like scheduler for multiple posts

**Requirements**:
1. Read post data from Google Sheets (post text, date, hour)
2. Use browser automation to log into LinkedIn and create a post
3. Use LinkedIn's built-in "Schedule" feature to program the post for the specified date and time
4. The script can run at any time - it uses LinkedIn's scheduling, not waiting for the scheduled time
5. Mark the post as "posted" in the Google Sheet after successful scheduling in LinkedIn
6. Handle errors gracefully with logging

---

## Notes & Context

- This is V1 - focusing on a single post automation
- Browser automation will be used (Playwright or Selenium)
- Google Sheets integration needed (gspread library)
- **Important**: Script uses LinkedIn's built-in "Schedule" feature - no need for external scheduler (APScheduler)
- Script can run at any time - LinkedIn handles the actual scheduling
- Authentication: LinkedIn credentials will be stored securely (no 2FA)
- Post status tracking: Update Google Sheet to mark posts as scheduled/completed

---

**Next Step**: Once requirements are added, we'll analyze and rephrase them in `ANALYZED_REQUIREMENTS.md`

