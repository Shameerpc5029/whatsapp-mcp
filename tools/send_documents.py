import logging
import requests
import os
from typing import Dict, Any

from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


class WhatsAppClient:
    def __init__(self,  phone_number_id: str):
        credentials = get_connection_credentials(
        )

        # self.phone_number_id = "587392797785338"  # Update with your phone number ID
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

        logger.info(
            "WhatsAppClient initialized",
            extra={
                "phone_number_id": phone_number_id,
                "path": os.getenv("WM_JOB_PATH"),
            },
        )

    def send_document(
        self,
        to: str,
        document_url: str,
        caption: str = "",
    ) -> Dict[str, Any]:
        try:
            if not to:
                raise ValueError("Recipient phone number is required")

            if not document_url:
                raise ValueError("Document URL is required")

            # Prepare the payload for sending the document
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "document",
                "document": {
                    "link": document_url,
                },
            }

            if caption:
                # Add caption if provided
                payload["document"]["caption"] = caption
                log_msg = f"Sending document with caption to {to} - {document_url} with caption: {caption}"
            else:
                log_msg = f"Sending document without caption to {to} - {document_url}"

            logger.info(
                log_msg, extra={"payload": payload, "path": os.getenv("WM_JOB_PATH")}
            )

            # Send the document via WhatsApp
            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                logger.info(
                    "Document message sent successfully",
                    extra={"response": response_data, "path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to send document message: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                f"Error sending document message: {str(e)}",
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
    document_url: str,
    caption: str = "",
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(connection_id, phone_number_id)
        logger.info(
            whatsapp_client,
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return whatsapp_client.send_document(to, document_url, caption)

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}
