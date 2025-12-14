# Google Sheets API Setup Guide

This guide explains how to set up Google Sheets API access for the LinkedIn Automation V1 project.

## Overview

The LinkedIn Automation V1 project needs to read and write data from a Google Sheet. There are two main approaches:

1. **Service Account** (Recommended for automation) - Best for server/automated scripts
2. **OAuth 2.0** - Best for user-facing applications

For this automation project, we recommend using a **Service Account**.

---

## Option 1: Service Account (Recommended)

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project name/ID

### Step 2: Enable Google Sheets API

1. In Google Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Google Sheets API"
3. Click on it and click **Enable**

### Step 3: Create a Service Account

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Fill in:
   - **Service account name**: `linkedin-automation` (or any name)
   - **Service account ID**: Auto-generated (or customize)
   - Click **Create and Continue**
4. Skip the optional steps (Grant access, Grant users access) and click **Done**

### Step 4: Create and Download Service Account Key

1. In the **Credentials** page, find your service account
2. Click on the service account email
3. Go to the **Keys** tab
4. Click **Add Key** > **Create new key**
5. Choose **JSON** format
6. Click **Create** - the JSON file will download automatically
7. **Save this file securely** - you'll need it for the project

### Step 5: Share Google Sheet with Service Account

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1E35yLjp_7p7UCjjInmeJUf0AwpkhZqOSvs57E2oIt7A/edit?usp=sharing
2. Click the **Share** button (top right)
3. Copy the **Service Account Email** from the JSON file (it looks like: `your-service-account@project-id.iam.gserviceaccount.com`)
4. Paste it in the "Add people and groups" field
5. Give it **Editor** permissions (so it can read and write)
6. Click **Send** (you can uncheck "Notify people" since it's a service account)

### Step 6: Configure the Project

1. Place the downloaded JSON file in a secure location (e.g., `backend/config/service-account-key.json`)
2. Add the path to your `.env` file:
   ```
   GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH=backend/config/service-account-key.json
   GOOGLE_SHEETS_ID=1E35yLjp_7p7UCjjInmeJUf0AwpkhZqOSvs57E2oIt7A
   ```
3. **Important**: Add `service-account-key.json` to `.gitignore` to never commit it!

---

## Option 2: OAuth 2.0 (Alternative)

If you prefer OAuth 2.0 (requires manual authentication flow):

### Step 1: Create OAuth 2.0 Credentials

1. In Google Cloud Console, go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen first
4. Choose **Desktop app** as application type
5. Name it (e.g., "LinkedIn Automation")
6. Click **Create**
7. Download the JSON credentials file

### Step 2: Configure the Project

1. Place the credentials file in a secure location
2. Add to `.env`:
   ```
   GOOGLE_SHEETS_OAUTH_CREDENTIALS_PATH=path/to/oauth-credentials.json
   GOOGLE_SHEETS_TOKEN_PATH=path/to/token.json
   ```

### Step 3: Authenticate (First Time Only)

The first time you run the script, it will open a browser for you to authenticate. The token will be saved for future use.

---

## Environment Variables

Add these to your `.env` file:

```bash
# Service Account (Recommended)
GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH=backend/config/service-account-key.json
GOOGLE_SHEETS_ID=1E35yLjp_7p7UCjjInmeJUf0AwpkhZqOSvs57E2oIt7A

# OR OAuth (Alternative)
# GOOGLE_SHEETS_OAUTH_CREDENTIALS_PATH=path/to/oauth-credentials.json
# GOOGLE_SHEETS_TOKEN_PATH=path/to/token.json
```

---

## Security Best Practices

1. **Never commit credentials to Git**
   - Add `*.json` (service account keys) to `.gitignore`
   - Add `.env` to `.gitignore`
   - Use `.env.example` as a template

2. **Store credentials securely**
   - Keep service account keys in a secure location
   - Use environment variables, not hardcoded paths

3. **Limit permissions**
   - Service account only needs access to the specific sheet
   - Use "Editor" permission (not "Owner")

---

## Troubleshooting

### Error: "Access denied" or "Permission denied"
- Make sure you shared the Google Sheet with the service account email
- Check that the service account has "Editor" permissions

### Error: "API not enabled"
- Make sure Google Sheets API is enabled in Google Cloud Console

### Error: "Invalid credentials"
- Check that the JSON file path is correct
- Verify the JSON file is valid and not corrupted

### Error: "File not found"
- Check the path in `.env` is correct
- Use absolute path if relative path doesn't work

---

## Testing the Setup

Once configured, you can test the connection with a simple script:

```python
import gspread
from google.oauth2.service_account import Credentials

# Load credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(
    'path/to/service-account-key.json',
    scopes=scopes
)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open_by_key('1E35yLjp_7p7UCjjInmeJUf0AwpkhZqOSvs57E2oIt7A')
worksheet = sheet.sheet1

# Test read
print(worksheet.get('A1'))
```

---

## Next Steps

Once Google Sheets API is configured:
1. Proceed to Step 2: Google Sheets Integration
2. Test reading data from the sheet
3. Test writing status updates

---

**Related Documents**:
- [LinkedIn Automation V1 Feature](../project/features/LINKEDIN_AUTOMATION_V1.md)
- [Best Practices](../../workflow/BEST_PRACTICES.md)

