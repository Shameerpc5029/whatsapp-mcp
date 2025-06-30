import logging
import requests
import os
from typing import Dict, Any

from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


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

        logger.info(
            "WhatsAppClient initialized",
            extra={
                "phone_number_id": phone_number_id,
                "path": os.getenv("WM_JOB_PATH"),
            },
        )

    def send_audio_message(
        self,
        to: str,
        audio_url: str,
    ) -> Dict[str, Any]:
        try:
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

            logger.info(
                log_msg, extra={"payload": payload, "path": os.getenv("WM_JOB_PATH")}
            )

            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            
            response_data = response.json()
            logger.info(
                f"Response from WhatsApp API: {response_data}",
                extra={"status_code": response.status_code, "path": os.getenv("WM_JOB_PATH")},
            )

            if response.status_code == 200:
                logger.info(
                    "Audio sent successfully",
                    extra={"response": response_data, "path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to send audio: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error( 
                f"Error sending audio: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "path": os.getenv("WM_JOB_PATH"),
                },
            )
            return {"result": None, "error": str(e)}


def main(
    phone_number_id: str,
    to: str,
    audio_url: str,
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(phone_number_id)
        return whatsapp_client.send_audio_message(to, audio_url)

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}


if __name__ == "__main__":
    result=main(
        phone_number_id="719875087856282",
        to="918136938259",
        audio_url="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"
    )

    print(result)
# This code is a standalone script that initializes a WhatsApp client and sends an audio message.