"""WhatsApp API client"""

from typing import Dict, Any
import requests
from ..utils import get_connection_credentials, log_message


class WhatsAppClient:
    """WhatsApp Business API client using Nango for authentication"""
    
    def __init__(self, phone_number_id: str):
        """
        Initialize WhatsApp client with Nango credentials
        
        Args:
            phone_number_id: WhatsApp Business phone number ID
        """
        credentials = get_connection_credentials()
        
        # Try different possible locations for the access token
        self.access_token = (
            credentials.get("apiKey") or 
            credentials.get("credentials", {}).get("apiKey") or
            credentials.get("credentials", {}).get("access_token")
        )
        
        if not self.access_token:
            raise ValueError("API key is missing from Nango credentials")

        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v21.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        log_message(f"WhatsAppClient initialized for phone_number_id: {phone_number_id}")

    def send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send request to WhatsApp API
        
        Args:
            payload: Request payload
            
        Returns:
            Response dictionary with result and error
        """
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload, 
                timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                log_message("Message sent successfully", {"response": response_data})
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            log_message(f"Failed to send message: {error_message}")
            return {"result": None, "error": error_message}

        except Exception as e:
            log_message(f"Error sending request: {str(e)}")
            return {"result": None, "error": str(e)}


class WhatsAppTemplateClient:
    """WhatsApp Business API client for template operations using Nango"""
    
    def __init__(self, business_account_id: str):
        """
        Initialize WhatsApp template client with Nango credentials
        
        Args:
            business_account_id: WhatsApp Business Account ID
        """
        credentials = get_connection_credentials()
        
        # Try different possible locations for the access token
        self.access_token = (
            credentials.get("apiKey") or 
            credentials.get("credentials", {}).get("apiKey") or
            credentials.get("credentials", {}).get("access_token")
        )
        
        if not self.access_token:
            raise ValueError("API key is missing from Nango credentials")

        self.business_account_id = business_account_id
        self.base_url = f"https://graph.facebook.com/v21.0/{business_account_id}/message_templates"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        log_message(f"WhatsAppTemplateClient initialized for business_account_id: {business_account_id}")

    def get_templates(self) -> Dict[str, Any]:
        """Get all templates for the business account"""
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response_data = response.json()

            if response.status_code == 200:
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            return {"result": None, "error": error_message}

        except Exception as e:
            return {"result": None, "error": str(e)}

    def create_template(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new template"""
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload, 
                timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                log_message("Template created successfully", {"response": response_data})
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            log_message(f"Failed to create template: {error_message}")
            return {"result": None, "error": error_message}

        except Exception as e:
            log_message(f"Error creating template: {str(e)}")
            return {"result": None, "error": str(e)}
