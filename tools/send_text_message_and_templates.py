import logging
import requests
import os
from typing import Dict, Any, Optional


from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


class WhatsAppClient:
    def __init__(self,phone_number_id: str):
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

    def send_message(
        self,
        to: str,
        message: str = "",
        template_name: str = "",
        language_code: str = "en_US",
    ) -> Dict[str, Any]:
        try:
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
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                logger.info(
                    f"Message sent successfully {response}",
                    extra={"path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to send message {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                f"Error sending message: {str(e)}",
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
    message: str = "",
    template_name: str = "",
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(connection_id, phone_number_id)
        return whatsapp_client.send_message(to, message, template_name)

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}
