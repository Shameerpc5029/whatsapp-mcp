"""Template tools for WhatsApp MCP Server"""

from typing import Dict, Any, List, Optional
from enum import Enum
from ..utils.client import WhatsAppClient, WhatsAppTemplateClient
from ..utils import validate_phone_number, log_message, get_default_phone_number_id, get_default_business_account_id


class TemplateLanguage(Enum):
    """Supported template languages"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    ARABIC = "ar"
    HINDI = "hi"


def send_template_message(
    to: str,
    template_name: str,
    parameters: List[Dict[str, str]] = None,
    language: str = "en",
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a template message with dynamic parameters via WhatsApp
    
    Args:
        to: Recipient phone number with country code
        template_name: Name of the approved template
        parameters: List of template parameters (optional)
        language: Template language code (default: "en")
        phone_number_id: WhatsApp Business phone number ID (optional, uses env var if not provided)
        
    Example parameters format:
    [
        {"type": "text", "text": "John Smith"},
        {"type": "text", "text": "2024-01-15"},
    ]
    """
    try:
        if phone_number_id is None:
            phone_number_id = get_default_phone_number_id()
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        # Validate language
        try:
            template_language = TemplateLanguage(language)
        except ValueError:
            log_message(f"Invalid language code: {language}, using English")
            template_language = TemplateLanguage.ENGLISH

        # Format parameters if provided
        formatted_parameters = []
        if parameters:
            for param in parameters:
                if isinstance(param, dict) and "type" in param and "text" in param:
                    formatted_parameters.append(param)
                else:
                    # Convert simple values to properly formatted parameter dictionaries
                    formatted_parameters.append({"type": "text", "text": str(param)})

        # Build template payload
        template_data = {
            "name": template_name,
            "language": {"code": template_language.value},
        }

        # Add components if parameters are provided
        if formatted_parameters:
            template_data["components"] = [
                {"type": "body", "parameters": formatted_parameters}
            ]

        payload = {
            "messaging_product": "whatsapp",
            "to": to_clean,
            "type": "template",
            "template": template_data,
        }

        log_message(f"Sending template message to {to_clean}", {
            "template_name": template_name,
            "language": template_language.value,
            "parameters_count": len(formatted_parameters)
        })
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_template_message: {str(e)}")
        return {"result": None, "error": str(e)}


def check_template_status(
    template_name: str,
    business_account_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check the approval status of a WhatsApp template
    
    Args:
        template_name: Name of the template to check
        business_account_id: WhatsApp Business Account ID (optional, uses env var if not provided)
    """
    try:
        if business_account_id is None:
            business_account_id = get_default_business_account_id()
        client = WhatsAppTemplateClient(business_account_id)
        
        log_message(f"Checking status for template: {template_name}")
        
        response = client.get_templates()
        
        if response["error"]:
            return response
        
        templates = response["result"].get("data", [])
        for template in templates:
            if template.get("name") == template_name:
                log_message(f"Template found", {
                    "name": template.get("name"),
                    "status": template.get("status"),
                    "id": template.get("id")
                })
                return {"result": template, "error": None}

        return {"result": None, "error": "Template not found"}

    except Exception as e:
        log_message(f"Error in check_template_status: {str(e)}")
        return {"result": None, "error": str(e)}


def list_templates(
    status_filter: str = "",
    business_account_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List all templates for a WhatsApp Business Account
    
    Args:
        status_filter: Optional status filter (APPROVED, PENDING, REJECTED)
        business_account_id: WhatsApp Business Account ID (optional, uses env var if not provided)
    """
    try:
        if business_account_id is None:
            business_account_id = get_default_business_account_id()
        client = WhatsAppTemplateClient(business_account_id)
        
        log_message(f"Listing templates for business account: {business_account_id}")
        
        response = client.get_templates()
        
        if response["error"]:
            return response
        
        templates = response["result"].get("data", [])
        
        # Filter by status if provided
        if status_filter:
            templates = [t for t in templates if t.get("status", "").upper() == status_filter.upper()]
        
        log_message(f"Found {len(templates)} templates", {
            "status_filter": status_filter,
            "total_count": len(templates)
        })
        
        return {"result": {"templates": templates, "count": len(templates)}, "error": None}

    except Exception as e:
        log_message(f"Error in list_templates: {str(e)}")
        return {"result": None, "error": str(e)}


def create_template(
    template_name: str,
    language: str,
    category: str,
    components: List[Dict[str, Any]],
    business_account_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new WhatsApp message template
    
    Args:
        template_name: Name for the new template
        language: Language code for the template
        category: Template category (MARKETING, UTILITY, AUTHENTICATION)
        components: List of template components
        business_account_id: WhatsApp Business Account ID (optional, uses env var if not provided)
        
    Example components format:
    [
        {
            "type": "HEADER",
            "format": "TEXT",
            "text": "Hello {{1}}"
        },
        {
            "type": "BODY", 
            "text": "Welcome {{1}}, your appointment is on {{2}}"
        },
        {
            "type": "FOOTER",
            "text": "Thank you for choosing us"
        }
    ]
    """
    try:
        if business_account_id is None:
            business_account_id = get_default_business_account_id()
        client = WhatsAppTemplateClient(business_account_id)

        # Validate category
        valid_categories = ["MARKETING", "UTILITY", "AUTHENTICATION"]
        if category.upper() not in valid_categories:
            raise ValueError(f"Invalid category. Must be one of: {valid_categories}")

        payload = {
            "name": template_name,
            "language": language,
            "category": category.upper(),
            "components": components,
        }

        log_message(f"Creating template: {template_name}", {
            "language": language,
            "category": category.upper(),
            "components_count": len(components)
        })
        
        return client.create_template(payload)

    except Exception as e:
        log_message(f"Error in create_template: {str(e)}")
        return {"result": None, "error": str(e)}
