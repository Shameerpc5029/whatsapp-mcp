"""Interactive tools for WhatsApp MCP Server"""

from typing import Dict, Any, List
from ..utils.client import WhatsAppClient
from ..utils import validate_phone_number, log_message


def send_list_message(
    phone_number_id: str,
    to: str,
    sections: List[Dict[str, Any]],
    header_text: str = "Available Options",
    body_text: str = "Please select from the following options:",
    footer_text: str = "Select an option to proceed",
    button_text: str = "Options"
) -> Dict[str, Any]:
    """
    Send an interactive list message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        sections: List of sections with options
        header_text: Header text for the message
        body_text: Body text for the message
        footer_text: Footer text for the message
        button_text: Button text for the list
        
    Example sections format:
    [
        {
            "title": "Section 1",
            "rows": [
                {
                    "id": "option1",
                    "title": "First Option",
                    "description": "Description for first option",
                },
                {
                    "id": "option2", 
                    "title": "Second Option",
                    "description": "Description for second option",
                },
            ],
        }
    ]
    """
    try:
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if not sections:
            raise ValueError("Sections are required for list message")

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_clean,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": header_text},
                "body": {"text": body_text},
                "footer": {"text": footer_text},
                "action": {
                    "button": button_text,
                    "sections": sections,
                },
            },
        }

        log_message(f"Sending interactive list message to {to_clean}", {
            "sections_count": len(sections),
            "header": header_text
        })
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_list_message: {str(e)}")
        return {"result": None, "error": str(e)}


def send_button_message(
    phone_number_id: str,
    to: str,
    body_text: str,
    buttons: List[Dict[str, Any]],
    header_text: str = "",
    footer_text: str = ""
) -> Dict[str, Any]:
    """
    Send an interactive button message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        body_text: Main message text
        buttons: List of buttons (max 3)
        header_text: Optional header text
        footer_text: Optional footer text
        
    Example buttons format:
    [
        {
            "type": "reply",
            "reply": {
                "id": "button_1",
                "title": "Yes"
            }
        },
        {
            "type": "reply", 
            "reply": {
                "id": "button_2",
                "title": "No"
            }
        }
    ]
    """
    try:
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if not buttons or len(buttons) > 3:
            raise ValueError("Must provide 1-3 buttons for button message")

        interactive_data = {
            "type": "button",
            "body": {"text": body_text},
            "action": {"buttons": buttons}
        }

        if header_text:
            interactive_data["header"] = {"type": "text", "text": header_text}
        
        if footer_text:
            interactive_data["footer"] = {"text": footer_text}

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_clean,
            "type": "interactive",
            "interactive": interactive_data,
        }

        log_message(f"Sending interactive button message to {to_clean}", {
            "buttons_count": len(buttons),
            "has_header": bool(header_text),
            "has_footer": bool(footer_text)
        })
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_button_message: {str(e)}")
        return {"result": None, "error": str(e)}
