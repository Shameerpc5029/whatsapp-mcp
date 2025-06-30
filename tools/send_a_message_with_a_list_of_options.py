import logging
import requests
import os
from typing import Dict, Any, List

from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


class WhatsAppClient:
    def __init__(self,phone_number_id: str):
        """Initialize WhatsApp API client with credentials from Nango."""
        try:
            credentials = get_connection_credentials(
            )

            # self.phone_number_id = 587392797785338
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
                "WhatsAppClient initialized successfully",
                extra={
                    "phone_number_id": phone_number_id,
                    "path": os.getenv("WM_JOB_PATH"),
                },
            )
        except Exception as e:
            logger.error(
                "Error initializing WhatsAppClient",
                exc_info=True,  # Provides detailed traceback
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            raise

    def send_list_message(
        self, to: str, sections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Send a WhatsApp interactive list message."""
        try:
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
                    },  # Fixed formatting
                },
            }

            logger.info(
                f"Sending interactive list message to {to}",
                extra={"payload": payload, "path": os.getenv("WM_JOB_PATH")},
            )

            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                logger.info(
                    "Message sent successfully",
                    extra={"response": response_data, "path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to send message: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                "Error sending list message",
                exc_info=True,
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": str(e)}


def main(
    connection_id: str, phone_number_id: str, to: str, sections: List[Dict[str, Any]]
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(connection_id, phone_number_id)
        result = whatsapp_client.send_list_message(to=to, sections=sections)

        logger.info(
            "Message sending attempt completed",
            extra={"result": result, "path": os.getenv("WM_JOB_PATH")},
        )

        return result

    except Exception as e:
        logger.error(
            "Error in main function",
            exc_info=True,
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}


# {
#                 "title": "Section 1",
#                 "rows": [
#                     {
#                         "id": "option1",
#                         "title": "First Option",
#                         "description": "Description for first option",
#                     },
#                     {
#                         "id": "option2",
#                         "title": "Second Option",
#                         "description": "Description for second option",
#                     },
#                 ],
#             }
