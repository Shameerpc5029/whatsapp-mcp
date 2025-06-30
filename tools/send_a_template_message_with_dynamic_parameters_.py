import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import requests

from connections import get_connection_credentials


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")

class WhatsAppError(Exception):
    """Custom exception for WhatsApp-related errors."""

    pass


class TemplateLanguage(Enum):
    """Supported template languages."""

    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"


class WhatsAppClient:
    def __init__(self,phone_number_id: str):
        """Initialize WhatsApp API client with credentials from Nango."""
        try:
            credentials = get_connection_credentials(
            )

            self.access_token = credentials.get(
                "apiKey", credentials.get("credentials", {}).get("apiKey")
            )
            if not self.access_token:
                raise ValueError("API key is missing from credentials")

            self.base_url = (
                f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
            )
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }

            logger.info(
                "WhatsAppClient initialized",
                extra={
                    "phone_number_id": phone_number_id,
                    "path": os.getenv("WM_JOB_PATH"),
                },
            )
        except Exception as e:
            logger.error(
                f"Error initializing WhatsAppClient: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "path": os.getenv("WM_JOB_PATH"),
                },
            )
            raise WhatsAppError(f"Failed to initialize WhatsApp client: {str(e)}")

    def send_template_message(
        self,
        to: str,
        template_name: str,
        parameters: List[Dict[str, str]],
        language: TemplateLanguage = TemplateLanguage.ENGLISH,
    ) -> Dict[str, Any]:
        try:
            # Format parameters if they're not already in the correct format
            formatted_parameters = []
            for param in parameters:
                if isinstance(param, dict) and "type" in param and "text" in param:
                    formatted_parameters.append(param)
                else:
                    # Convert simple values to properly formatted parameter dictionaries
                    formatted_parameters.append({"type": "text", "text": str(param)})

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language.value},
                    "components": [
                        {"type": "body", "parameters": formatted_parameters}
                    ],
                },
            }

            logger.info(
                f"Sending template message to {to}",
                extra={"payload": payload, "path": os.getenv("WM_JOB_PATH")},
            )

            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                logger.info(
                    "Template message sent successfully",
                    extra={"response": response_data, "path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to send template message: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                f"Error sending template message: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "path": os.getenv("WM_JOB_PATH"),
                },
            )
            return {"result": None, "error": str(e)}


def main(
    connection_id: str,
    phone_number_id: str,
    to: str,
    template_name: str,
    parameters: List[Dict[str, Any]],
    language: str = "en",
) -> Dict[str, Any]:
    """
    Args:
        connection_id (str): Nango connection ID
        phone_number_id (str): WhatsApp Business phone number ID
        to (str): Recipient's phone number with country code
        template_name (str): Name of the approved template
        parameters (List[Dict[str, Any]]): List of template parameters
        language (str): Template language code (default: "en")

    """
    try:
        whatsapp_client = WhatsAppClient(connection_id, phone_number_id)

        try:
            template_language = TemplateLanguage(language)
        except ValueError:
            logger.warning(
                f"Invalid language code: {language}, using English",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            template_language = TemplateLanguage.ENGLISH

        result = whatsapp_client.send_template_message(
            to=to,
            template_name=template_name,
            parameters=parameters,
            language=template_language,
        )

        logger.info(
            "Message sending attempt completed",
            extra={"result": result, "path": os.getenv("WM_JOB_PATH")},
        )

        return result

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={
                "error_type": type(e).__name__,
                "path": os.getenv("WM_JOB_PATH"),
            },
        )
        return {"result": None, "error": str(e)}

    # Example template parameters
    # template_parameters = [
    #     {"type": "text", "text": "John Smith"},
    #     {"type": "text", "text": datetime.now().strftime("%B %d, %Y at %I:%M %p")},
    #     {"type": "text", "text": "Dr. Sarah Wilson"},
    # ]
