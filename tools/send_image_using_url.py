import logging
import requests
import os
from typing import Dict, Any

from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


class WhatsAppClient:
    def __init__(self, phone_number_id: str):
        credentials = get_connection_credentials(
        )

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

    def send_image_with_text(
        self,
        to: str,
        caption: str,
        image_url: str,
    ) -> Dict[str, Any]:
        try:
            if not to:
                raise ValueError("Recipient phone number is required")

            if not image_url:
                raise ValueError("Image URL is required")

            # Send image with or without caption based on the availability of the caption
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "image",
                "image": {"link": image_url},
            }

            if caption != "":
                # Add caption if caption is provided
                payload["image"]["caption"] = caption
                log_msg = f"Sending image with caption to {to} - {image_url} with caption: {caption}"
            else:
                log_msg = f"Sending image without caption to {to} - {image_url}"

            logger.info(
                log_msg, extra={"payload": payload, "path": os.getenv("WM_JOB_PATH")}
            )

            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                logger.info(
                    "Image caption sent successfully",
                    extra={"response": response_data, "path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("caption", response.text)
            logger.error(
                f"Failed to send image caption: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                f"Error sending image caption: {str(e)}",
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
    image_url: str,
    caption: str = "",
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(connection_id, phone_number_id)
        return whatsapp_client.send_image_with_text(to, caption, image_url)

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}
