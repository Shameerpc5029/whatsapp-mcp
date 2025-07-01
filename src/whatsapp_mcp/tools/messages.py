"""Message tools for WhatsApp MCP Server"""

from typing import Dict, Any, Optional
from ..utils.client import WhatsAppClient
from ..utils import validate_phone_number, log_message, get_default_phone_number_id


def send_text_message(
    to: str,
    message: str = "",
    template_name: str = "",
    language_code: str = "en_US",
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a text message or template message via WhatsApp
    
    Args:
        to: Recipient phone number
        message: Text message to send (optional if template_name is provided)
        template_name: Template name to use (optional if message is provided)
        language_code: Language code for template (default: en_US)
        phone_number_id: WhatsApp Business phone number ID (optional, uses env var if not provided)
    """
    try:
        if phone_number_id is None:
            phone_number_id = get_default_phone_number_id()
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if message:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_clean,
                "type": "text",
                "text": {"body": message},
            }
        elif template_name:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_clean,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language_code},
                },
            }
        else:
            raise ValueError("Either 'message' or 'template_name' must be provided")

        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_text_message: {str(e)}")
        return {"result": None, "error": str(e)}


def send_image_message(
    to: str,
    image_url: str,
    caption: str = "",
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send an image message via WhatsApp
    
    Args:
        to: Recipient phone number  
        image_url: URL of the image to send
        caption: Optional caption for the image
        phone_number_id: WhatsApp Business phone number ID (optional, uses env var if not provided)
    """
    try:
        if phone_number_id is None:
            phone_number_id = get_default_phone_number_id()
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if not image_url:
            raise ValueError("Image URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to_clean,
            "type": "image",
            "image": {"link": image_url},
        }

        if caption:
            payload["image"]["caption"] = caption

        log_message(f"Sending image to {to_clean}", {"image_url": image_url, "has_caption": bool(caption)})
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_image_message: {str(e)}")
        return {"result": None, "error": str(e)}


def send_video_message(
    to: str,
    video_url: str,
    caption: str = "",
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a video message via WhatsApp
    
    Args:
        to: Recipient phone number
        video_url: URL of the video to send
        caption: Optional caption for the video
        phone_number_id: WhatsApp Business phone number ID (optional, uses env var if not provided)
    """
    try:
        if phone_number_id is None:
            phone_number_id = get_default_phone_number_id()
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if not video_url:
            raise ValueError("Video URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to_clean,
            "type": "video",
            "video": {"link": video_url},
        }

        if caption:
            payload["video"]["caption"] = caption

        log_message(f"Sending video to {to_clean}", {"video_url": video_url, "has_caption": bool(caption)})
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_video_message: {str(e)}")
        return {"result": None, "error": str(e)}


def send_document_message(
    to: str,
    document_url: str,
    caption: str = "",
    filename: str = "",
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a document message via WhatsApp
    
    Args:
        to: Recipient phone number
        document_url: URL of the document to send
        caption: Optional caption for the document
        filename: Optional filename for the document
        phone_number_id: WhatsApp Business phone number ID (optional, uses env var if not provided)
    """
    try:
        if phone_number_id is None:
            phone_number_id = get_default_phone_number_id()
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if not document_url:
            raise ValueError("Document URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to_clean,
            "type": "document",
            "document": {"link": document_url},
        }

        if caption:
            payload["document"]["caption"] = caption
        
        if filename:
            payload["document"]["filename"] = filename

        log_message(f"Sending document to {to_clean}", {
            "document_url": document_url, 
            "has_caption": bool(caption),
            "filename": filename
        })
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_document_message: {str(e)}")
        return {"result": None, "error": str(e)}


def send_audio_message(
    to: str,
    audio_url: str,
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send an audio/voice message via WhatsApp
    
    Args:
        to: Recipient phone number
        audio_url: URL of the audio file to send
        phone_number_id: WhatsApp Business phone number ID (optional, uses env var if not provided)
    """
    try:
        if phone_number_id is None:
            phone_number_id = get_default_phone_number_id()
        client = WhatsAppClient(phone_number_id)
        to_clean = validate_phone_number(to)

        if not audio_url:
            raise ValueError("Audio URL is required")

        payload = {
            "messaging_product": "whatsapp",
            "to": to_clean,
            "type": "audio",
            "audio": {"link": audio_url},
        }

        log_message(f"Sending audio to {to_clean}", {"audio_url": audio_url})
        return client.send_request(payload)

    except Exception as e:
        log_message(f"Error in send_audio_message: {str(e)}")
        return {"result": None, "error": str(e)}
