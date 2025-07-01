"""Utility functions for WhatsApp MCP Server"""

import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def get_connection_credentials() -> Dict[str, Any]:
    """
    Get WhatsApp Business API credentials from Nango
    
    Returns:
        Dict containing access token credentials
        
    Raises:
        ValueError: If required Nango environment variables are not found
    """
    connection_id = os.environ.get("NANGO_CONNECTION_ID")
    integration_id = os.environ.get("NANGO_INTEGRATION_ID")
    base_url = os.environ.get("NANGO_BASE_URL")
    secret_key = os.environ.get("NANGO_SECRET_KEY")
    
    if not all([connection_id, integration_id, base_url, secret_key]):
        missing = [var for var, val in [
            ("NANGO_CONNECTION_ID", connection_id),
            ("NANGO_INTEGRATION_ID", integration_id), 
            ("NANGO_BASE_URL", base_url),
            ("NANGO_SECRET_KEY", secret_key)
        ] if not val]
        raise ValueError(f"Missing required Nango environment variables: {', '.join(missing)}")
    
    url = f"{base_url}/connection/{connection_id}"
    params = {
        "provider_config_key": integration_id,
        "refresh_token": "true",
    }
    headers = {"Authorization": f"Bearer {secret_key}"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Nango API response status: {response.status_code}")
        response.raise_for_status()
        
        credentials = response.json()
        print("Successfully retrieved credentials from Nango")
        return credentials
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Nango API: {str(e)}")
        raise ValueError(f"Failed to get credentials from Nango: {str(e)}")


def get_access_token() -> str:
    """
    Get WhatsApp Business API access token from Nango
    
    Returns:
        Access token string
        
    Raises:
        ValueError: If access token cannot be retrieved
    """
    credentials = get_connection_credentials()
    
    # Try different possible locations for the access token
    access_token = (
        credentials.get("apiKey") or 
        credentials.get("credentials", {}).get("apiKey") or
        credentials.get("credentials", {}).get("access_token")
    )
    
    if not access_token:
        print(f"Available credential keys: {list(credentials.keys())}")
        if "credentials" in credentials:
            print(f"Available credential.credentials keys: {list(credentials['credentials'].keys())}")
        raise ValueError("Access token not found in Nango credentials")
    
    return access_token


def validate_phone_number(phone_number: str) -> str:
    """
    Validate and clean phone number
    
    Args:
        phone_number: Phone number to validate
        
    Returns:
        Cleaned phone number with only digits
        
    Raises:
        ValueError: If phone number is empty or invalid
    """
    if not phone_number:
        raise ValueError("Phone number is required")
    
    # Remove all non-digit characters
    cleaned = "".join(filter(str.isdigit, phone_number))
    
    if not cleaned:
        raise ValueError("Invalid phone number format")
    
    return cleaned


def format_whatsapp_response(response_data: Dict[str, Any], error: str = None) -> Dict[str, Any]:
    """
    Format WhatsApp API response consistently
    
    Args:
        response_data: Response data from WhatsApp API
        error: Error message if any
        
    Returns:
        Formatted response dictionary
    """
    return {
        "result": response_data if not error else None,
        "error": error,
        "success": error is None
    }


def get_default_phone_number_id() -> str:
    """
    Get default WhatsApp phone number ID from environment variables
    
    Returns:
        Phone number ID string
        
    Raises:
        ValueError: If phone number ID is not found in environment
    """
    phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    if not phone_number_id or phone_number_id == "your_whatsapp_phone_number_id":
        raise ValueError("WHATSAPP_PHONE_NUMBER_ID environment variable is not set or still contains placeholder value")
    return phone_number_id


def get_default_business_account_id() -> str:
    """
    Get default WhatsApp business account ID from environment variables
    
    Returns:
        Business account ID string
        
    Raises:
        ValueError: If business account ID is not found in environment
    """
    business_account_id = os.environ.get("WHATSAPP_BUSINESS_ACCOUNT_ID")
    if not business_account_id or business_account_id == "your_whatsapp_business_account_id":
        raise ValueError("WHATSAPP_BUSINESS_ACCOUNT_ID environment variable is not set or still contains placeholder value")
    return business_account_id


def log_message(message: str, extra_data: Dict[str, Any] = None) -> None:
    """
    Simple logging function using print
    
    Args:
        message: Message to log
        extra_data: Additional data to include in log
    """
    if extra_data:
        print(f"{message} | Data: {extra_data}")
    else:
        print(message)
