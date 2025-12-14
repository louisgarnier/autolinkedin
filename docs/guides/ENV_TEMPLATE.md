# Environment Variables Template

Copy this content to a `.env` file in the project root directory.

```bash
# LinkedIn Automation V1 - Environment Variables
# Copy this content to .env file in project root
# NEVER commit .env to version control

# LinkedIn Credentials
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password

# Google Sheets Configuration
# Option 1: Service Account (Recommended for automation)
GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH=backend/config/service-account-key.json
GOOGLE_SHEETS_ID=1E35yLjp_7p7UCjjInmeJUf0AwpkhZqOSvs57E2oIt7A

# Option 2: OAuth (Alternative - requires manual authentication)
# GOOGLE_SHEETS_OAUTH_CREDENTIALS_PATH=path/to/oauth-credentials.json
# GOOGLE_SHEETS_TOKEN_PATH=path/to/token.json

# Browser Configuration
BROWSER_MODE=visible
# Options: "visible" (see browser) or "headless" (background)

# Logging
LOG_LEVEL=INFO
# Options: DEBUG, INFO, WARNING, ERROR

# LinkedIn Automation V2 - OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
# Optional: Model selection (default: gpt-3.5-turbo for testing, use gpt-4 for production)
# OPENAI_MODEL=gpt-3.5-turbo
# OPENAI_MODEL=gpt-4
```

## Instructions

1. Create a `.env` file in the project root: `/Users/louisgarnier/Library/Mobile Documents/com~apple~CloudDocs/Python/DEV/autolinkedin/.env`
2. Copy the content above into the file
3. Replace placeholder values with your actual credentials
4. Make sure `.env` is in `.gitignore` (should be by default)

## Security

- **Never commit `.env` to Git**
- Keep credentials secure
- Use environment variables, not hardcoded values

