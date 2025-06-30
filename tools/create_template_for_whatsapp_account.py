import logging
import requests
import os
from typing import Dict, Any

from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


class WhatsAppClient:
    def __init__(self,whatsapp_business_account_id: str):
        credentials = get_connection_credentials(
        )

        self.access_token = credentials.get(
            "apiKey", credentials.get("credentials", {}).get("apiKey")
        )
        if not self.access_token:
            raise ValueError("API key is missing from credentials")

        self.base_url = f"https://graph.facebook.com/v21.0/{whatsapp_business_account_id}/message_templates"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        logger.info(
            "WhatsAppClient initialized",
            extra={
                "whatsapp_business_account_id": whatsapp_business_account_id,
                "path": os.getenv("WM_JOB_PATH"),
            },
        )

    def create_template(
        self,
        template_name: str,
        language: str,
        body: str,
        header: str = "",
        footer: str = "",
        button: str = "",
    ) -> Dict[str, Any]:
        try:
            payload = {
                "name": template_name,
                "language": language,
                "category": "MARKETING",  # You might want to make this configurable
                "components": [
                    header,
                    body,
                    footer,
                    button,
                ],
            }

            logger.info(
                f"Creating template {template_name} with language {language}",
                extra={"payload": payload, "path": os.getenv("WM_JOB_PATH")},
            )

            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=10
            )
            response_data = response.json()

            if response.status_code == 200:
                logger.info(
                    "Template created successfully",
                    extra={"response": response_data, "path": os.getenv("WM_JOB_PATH")},
                )
                return {"result": response_data, "error": None}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to create template: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                f"Error creating template: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "path": os.getenv("WM_JOB_PATH"),
                },
            )
            return {"result": None, "error": str(e)}


def main(
    connection_id: str,
    whatsapp_business_account_id: str,
    template_name: str,
    body: str,
    language: str,
    header: str = "",
    footer: str = "",
    button: str = "",
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(connection_id, whatsapp_business_account_id)
        return whatsapp_client.create_template(
            template_name=template_name,
            language=language,
            header=header,
            body=body,
            footer=footer,
            button=button,
        )

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}
