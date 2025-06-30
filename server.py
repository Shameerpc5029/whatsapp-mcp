"""WhatsApp MCP Server"""
from typing import Dict, Any, List
from enum import Enum
import requests
from mcp.server.fastmcp import FastMCP
from connections import get_connection_credentials

# Initialize FastMCP
mcp = FastMCP("WhatsApp")


class WhatsAppError(Exception):
    """Custom exception for WhatsApp-related errors."""
    pass


class TemplateLanguage(Enum):
    """Supported template languages."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"


class WhatsAppClient:
    def __init__(self, phone_number_id: str):
        credentials = get_connection_credentials()
        
        self.access_token = credentials.get(
            "apiKey", credentials.get("credentials", {}).get("apiKey")
        )
        if not self.access_token:
            raise ValueError("API key is missing from credentials")

        self.base_url = f"https://graph.facebook.com/v21.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        print(f"WhatsAppClient initialized for phone_number_id: {phone_number_id}")


@mcp.tool()
def send_text_message(
    phone_number_id: str,
    to: str,
    message: str = "",
    template_name: str = "",
    language_code: str = "en_US",
) -> Dict[str, Any]:
    """
    Send a text message or template message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        message: Text message to send (optional if template_name is provided)
        template_name: Template name to use (optional if message is provided)
        language_code: Language code for template (default: en_US)
    """
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        if not to:
            raise ValueError("Recipient phone number is required")

        to = "".join(filter(str.isdigit, to))  # Ensure phone number is numeric

        if message:
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message},
            }
        elif template_name:
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language_code},
                },
            }
        else:
            raise ValueError("Either 'message' or 'template_name' must be provided")

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print(f"Message sent successfully: {response_data}")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send message: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def send_image_message(
    phone_number_id: str,
    to: str,
    image_url: str,
    caption: str = "",
) -> Dict[str, Any]:
    """
    Send an image message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number  
        image_url: URL of the image to send
        caption: Optional caption for the image
    """
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        if not to:
            raise ValueError("Recipient phone number is required")

        if not image_url:
            raise ValueError("Image URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {"link": image_url},
        }

        if caption:
            payload["image"]["caption"] = caption
            log_msg = f"Sending image with caption to {to} - {image_url} with caption: {caption}"
        else:
            log_msg = f"Sending image without caption to {to} - {image_url}"

        print(log_msg)

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print("Image sent successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send image: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending image: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def send_video_message(
    phone_number_id: str,
    to: str,
    video_url: str,
    caption: str = "",
) -> Dict[str, Any]:
    """
    Send a video message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        video_url: URL of the video to send
        caption: Optional caption for the video
    """
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        if not to:
            raise ValueError("Recipient phone number is required")

        if not video_url:
            raise ValueError("Video URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "video",
            "video": {"link": video_url},
        }

        if caption:
            payload["video"]["caption"] = caption
            log_msg = f"Sending video with caption to {to} - {video_url} with caption: {caption}"
        else:
            log_msg = f"Sending video without caption to {to} - {video_url}"

        print(log_msg)

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print("Video sent successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send video: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending video: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def send_document_message(
    phone_number_id: str,
    to: str,
    document_url: str,
    caption: str = "",
) -> Dict[str, Any]:
    """
    Send a document message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        document_url: URL of the document to send
        caption: Optional caption for the document
    """
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        if not to:
            raise ValueError("Recipient phone number is required")

        if not document_url:
            raise ValueError("Document URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "document",
            "document": {
                "link": document_url,
            },
        }

        if caption:
            payload["document"]["caption"] = caption
            log_msg = f"Sending document with caption to {to} - {document_url} with caption: {caption}"
        else:
            log_msg = f"Sending document without caption to {to} - {document_url}"

        print(log_msg)

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print("Document sent successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send document: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending document: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def send_audio_message(
    phone_number_id: str,
    to: str,
    audio_url: str,
) -> Dict[str, Any]:
    """
    Send an audio/voice message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        audio_url: URL of the audio file to send
    """
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        if not to:
            raise ValueError("Recipient phone number is required")

        if not audio_url:
            raise ValueError("Audio URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "audio",
            "audio": {"link": audio_url},
        }

        log_msg = f"Sending audio message to {to} - {audio_url}"
        print(log_msg)

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        
        response_data = response.json()
        print(f"Response from WhatsApp API: {response_data}")

        if response.status_code == 200:
            print("Audio sent successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send audio: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending audio: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def send_list_message(
    phone_number_id: str,
    to: str,
    sections: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Send an interactive list message via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number
        sections: List of sections with options
        
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
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": "Available Options"},
                "body": {"text": "Please select from the following options:"},
                "footer": {"text": "Select an option to proceed"},
                "action": {
                    "button": "Options",
                    "sections": sections,
                },
            },
        }

        print(f"Sending interactive list message to {to}")

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print("List message sent successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send list message: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending list message: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def send_template_message(
    phone_number_id: str,
    to: str,
    template_name: str,
    parameters: List[Dict[str, str]],
    language: str = "en",
) -> Dict[str, Any]:
    """
    Send a template message with dynamic parameters via WhatsApp
    
    Args:
        phone_number_id: WhatsApp Business phone number ID
        to: Recipient phone number with country code
        template_name: Name of the approved template
        parameters: List of template parameters
        language: Template language code (default: "en")
        
    Example parameters format:
    [
        {"type": "text", "text": "John Smith"},
        {"type": "text", "text": "2024-01-15"},
    ]
    """
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        
        # Format parameters if they're not already in the correct format
        formatted_parameters = []
        for param in parameters:
            if isinstance(param, dict) and "type" in param and "text" in param:
                formatted_parameters.append(param)
            else:
                # Convert simple values to properly formatted parameter dictionaries
                formatted_parameters.append({"type": "text", "text": str(param)})

        try:
            template_language = TemplateLanguage(language)
        except ValueError:
            print(f"Invalid language code: {language}, using English")
            template_language = TemplateLanguage.ENGLISH

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": template_language.value},
                "components": [
                    {"type": "body", "parameters": formatted_parameters}
                ],
            },
        }

        print(f"Sending template message to {to}")

        response = requests.post(
            whatsapp_client.base_url, headers=whatsapp_client.headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print("Template message sent successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to send template message: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error sending template message: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def check_template_status(
    business_account_id: str,
    template_name: str,
) -> Dict[str, Any]:
    """
    Check the approval status of a WhatsApp template
    
    Args:
        business_account_id: WhatsApp Business Account ID
        template_name: Name of the template to check
    """
    try:
        credentials = get_connection_credentials()
        access_token = credentials.get(
            "apiKey", credentials.get("credentials", {}).get("apiKey")
        )
        
        if not access_token:
            raise ValueError("API key is missing from credentials")

        base_url = f"https://graph.facebook.com/v21.0/{business_account_id}/message_templates"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        print(f"Checking status for template: {template_name}")

        response = requests.get(base_url, headers=headers, timeout=10)
        response_data = response.json()

        if response.status_code == 200:
            templates = response_data.get("data", [])
            for template in templates:
                if template.get("name") == template_name:
                    print(f"Template status retrieved: {template}")
                    return {"result": template, "error": None}

            return {"result": None, "error": "Template not found"}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to retrieve template status: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error checking template status: {str(e)}")
        return {"result": None, "error": str(e)}


@mcp.tool()
def create_template(
    whatsapp_business_account_id: str,
    template_name: str,
    language: str,
    body: str,
    header: str = "",
    footer: str = "",
    button: str = "",
) -> Dict[str, Any]:
    """
    Create a new WhatsApp message template
    
    Args:
        whatsapp_business_account_id: WhatsApp Business Account ID
        template_name: Name for the new template
        language: Language code for the template
        body: Main body text of the template
        header: Optional header text
        footer: Optional footer text
        button: Optional button configuration
    """
    try:
        credentials = get_connection_credentials()
        access_token = credentials.get(
            "apiKey", credentials.get("credentials", {}).get("apiKey")
        )
        
        if not access_token:
            raise ValueError("API key is missing from credentials")

        base_url = f"https://graph.facebook.com/v21.0/{whatsapp_business_account_id}/message_templates"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "name": template_name,
            "language": language,
            "category": "MARKETING",
            "components": [
                header,
                body,
                footer,
                button,
            ],
        }

        print(f"Creating template {template_name} with language {language}")

        response = requests.post(
            base_url, headers=headers, json=payload, timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            print("Template created successfully")
            return {"result": response_data, "error": None}

        error_message = response_data.get("error", {}).get("message", response.text)
        print(f"Failed to create template: {error_message}")
        return {"result": None, "error": error_message}

    except Exception as e:
        print(f"Error creating template: {str(e)}")
        return {"result": None, "error": str(e)}


if __name__ == "__main__":
    mcp.run()
