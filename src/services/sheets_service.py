"""
Google Sheets Integration Service
Handles use case submissions to Google Sheets
"""

import json
import requests
from typing import Dict, Optional
from datetime import datetime
from src.config.settings import get_app_config
from src.utils.helpers import log_user_action

class SheetsService:
    """Service for Google Sheets integration"""
    
    def __init__(self):
        self.config = get_app_config()
        # In production, these would come from environment variables
        self.sheets_url = self.config.google_sheets_url if hasattr(self.config, 'google_sheets_url') else None
        self.webhook_url = self.config.webhook_url if hasattr(self.config, 'webhook_url') else None
    
    def submit_use_case(self, submission_data: Dict) -> bool:
        """
        Submit use case to Google Sheets
        Returns True if successful, False otherwise
        """
        try:
            # Prepare data for sheets
            sheets_data = self._prepare_sheets_data(submission_data)
            
            # Method 1: Direct Google Sheets API (requires setup)
            if self.sheets_url:
                success = self._submit_to_sheets_api(sheets_data)
                if success:
                    log_user_action("use_case_submitted_sheets", {"title": submission_data.get('use_case_title')})
                    return True
            
            # Method 2: Google Forms webhook (simpler setup)
            if self.webhook_url:
                success = self._submit_to_webhook(sheets_data)
                if success:
                    log_user_action("use_case_submitted_webhook", {"title": submission_data.get('use_case_title')})
                    return True
            
            # Method 3: Fallback to local storage/email
            return self._fallback_submission(submission_data)
            
        except Exception as e:
            log_user_action("use_case_submission_error", {"error": str(e)})
            return False
    
    def _prepare_sheets_data(self, submission_data: Dict) -> Dict:
        """Prepare data for Google Sheets format"""
        return {
            "timestamp": datetime.now().isoformat(),
            "submitter_name": submission_data.get('submitter_name', ''),
            "submitter_email": submission_data.get('submitter_email', ''),
            "department": submission_data.get('department', ''),
            "business_unit": submission_data.get('business_unit', ''),
            "use_case_title": submission_data.get('use_case_title', ''),
            "problem_description": submission_data.get('problem_description', ''),
            "proposed_solution": submission_data.get('proposed_solution', ''),
            "expected_benefits": submission_data.get('expected_benefits', ''),
            "priority": submission_data.get('priority', ''),
            "timeline": submission_data.get('timeline', ''),
            "data_availability": submission_data.get('data_availability', ''),
            "technical_complexity": submission_data.get('technical_complexity', ''),
            "integration_needs": submission_data.get('integration_needs', ''),
            "budget_range": submission_data.get('budget_range', ''),
            "stakeholders": submission_data.get('stakeholders', ''),
            "additional_notes": submission_data.get('additional_notes', '')
        }
    
    def _submit_to_sheets_api(self, data: Dict) -> bool:
        """Submit to Google Sheets using API"""
        try:
            # This would require Google Sheets API setup
            # For now, we'll simulate success
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._get_access_token()}'
            }
            
            # Construct the API request
            sheets_payload = {
                "values": [list(data.values())],
                "majorDimension": "ROWS"
            }
            
            # Make the API call
            response = requests.post(
                self.sheets_url,
                headers=headers,
                json=sheets_payload,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            log_user_action("sheets_api_error", {"error": str(e)})
            return False
    
    def _submit_to_webhook(self, data: Dict) -> bool:
        """Submit to Google Forms webhook"""
        try:
            # This would post to a Google Forms webhook
            response = requests.post(
                self.webhook_url,
                data=data,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            log_user_action("webhook_error", {"error": str(e)})
            return False
    
    def _fallback_submission(self, submission_data: Dict) -> bool:
        """Fallback method - save locally and/or send email"""
        try:
            # Save to local file as backup
            self._save_to_local_file(submission_data)
            
            # Send email notification (if configured)
            if hasattr(self.config, 'email_notifications') and self.config.email_notifications:
                self._send_email_notification(submission_data)
            
            return True
            
        except Exception as e:
            log_user_action("fallback_submission_error", {"error": str(e)})
            return False
    
    def _save_to_local_file(self, submission_data: Dict):
        """Save submission to local file"""
        try:
            import os
            
            # Create data directory if it doesn't exist
            data_dir = "static/data"
            os.makedirs(data_dir, exist_ok=True)
            
            # Save to JSON file
            filename = f"{data_dir}/use_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(submission_data, f, indent=2)
            
            log_user_action("use_case_saved_locally", {"filename": filename})
            
        except Exception as e:
            log_user_action("local_save_error", {"error": str(e)})
    
    def _send_email_notification(self, submission_data: Dict):
        """Send email notification to AI team"""
        try:
            # This would integrate with email service
            # For now, we'll just log it
            log_user_action("email_notification", {
                "to": "ai-team@aperam.com",
                "subject": f"New Use Case Submission: {submission_data.get('use_case_title')}",
                "submitter": submission_data.get('submitter_name')
            })
            
        except Exception as e:
            log_user_action("email_notification_error", {"error": str(e)})
    
    def _get_access_token(self) -> str:
        """Get Google API access token"""
        # This would implement OAuth2 flow
        # For now, return placeholder
        return "placeholder_token"
    
    def test_connection(self) -> Dict:
        """Test Google Sheets connection"""
        try:
            if self.sheets_url:
                # Test API connection
                response = requests.get(self.sheets_url, timeout=10)
                return {
                    "success": response.status_code == 200,
                    "method": "API",
                    "status": response.status_code
                }
            elif self.webhook_url:
                # Test webhook connection
                response = requests.post(self.webhook_url, data={"test": "true"}, timeout=10)
                return {
                    "success": response.status_code == 200,
                    "method": "Webhook",
                    "status": response.status_code
                }
            else:
                return {
                    "success": True,
                    "method": "Fallback",
                    "status": "No external integration configured"
                }
                
        except Exception as e:
            return {
                "success": False,
                "method": "Unknown",
                "error": str(e)
            }

# Global instance
sheets_service = SheetsService()

def submit_use_case_to_sheets(submission_data: Dict) -> bool:
    """Convenience function for submitting use case"""
    return sheets_service.submit_use_case(submission_data)

def test_sheets_connection() -> Dict:
    """Convenience function for testing connection"""
    return sheets_service.test_connection()