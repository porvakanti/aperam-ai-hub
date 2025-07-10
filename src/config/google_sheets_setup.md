# Google Sheets Integration Setup

## Overview
The AI Hub supports two methods for integrating with Google Sheets to automatically store use case submissions:

1. **Google Sheets API** (Recommended for production)
2. **Google Forms Webhook** (Simpler setup for testing)

## Method 1: Google Sheets API

### Prerequisites
- Google Cloud Project with Sheets API enabled
- Service Account with appropriate permissions
- Google Sheet with proper headers

### Setup Steps

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing one
   - Enable Google Sheets API

2. **Create Service Account**
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Download JSON credentials file
   - Place credentials file in `src/config/google_credentials.json`

3. **Create Google Sheet**
   - Create new Google Sheet
   - Add headers in first row:
     ```
     Timestamp | Name | Email | Department | Business Unit | Title | Problem | Solution | Benefits | Priority | Timeline | Data Availability | Complexity | Integration | Budget | Stakeholders | Notes
     ```
   - Share sheet with service account email (Editor permissions)
   - Copy sheet ID from URL

4. **Update Configuration**
   Add to your `.env` file:
   ```env
   GOOGLE_SHEETS_URL=https://sheets.googleapis.com/v4/spreadsheets/YOUR_SHEET_ID/values/Sheet1:append?valueInputOption=RAW
   GOOGLE_CREDENTIALS_PATH=src/config/google_credentials.json
   ```

### Code Integration
```python
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_CREDENTIALS_PATH'),
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Build service
service = build('sheets', 'v4', credentials=credentials)
```

## Method 2: Google Forms Webhook

### Setup Steps

1. **Create Google Form**
   - Go to [Google Forms](https://forms.google.com)
   - Create new form with fields matching use case submission
   - Get form ID from URL

2. **Set up Webhook**
   - Use Google Apps Script or third-party service
   - Create webhook endpoint that posts to Google Sheets
   - Configure webhook URL in application

3. **Update Configuration**
   Add to your `.env` file:
   ```env
   WEBHOOK_URL=https://your-webhook-endpoint.com/submit
   ```

## Method 3: Fallback (Default)

If no external integration is configured, the system will:
- Save submissions to local JSON files in `static/data/`
- Log submission events for tracking
- Send email notifications (if email service is configured)

## Testing Integration

Use the "Test Connection" button in the Use Case Intake page to verify your setup.

## Security Considerations

- Never commit credentials to version control
- Use environment variables for sensitive configuration
- Implement proper error handling and logging
- Consider rate limiting for API calls
- Validate all input data before submission

## Troubleshooting

### Common Issues
1. **Authentication Error**: Check service account permissions
2. **API Quota Exceeded**: Implement retry logic with exponential backoff
3. **Sheet Not Found**: Verify sheet ID and sharing permissions
4. **Invalid Data Format**: Ensure data matches expected schema

### Debug Mode
Enable debug mode in `src/config/settings.py` to see detailed error messages.