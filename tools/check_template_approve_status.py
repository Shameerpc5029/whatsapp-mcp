import logging
import requests
import os
from typing import Dict, Any

from connections import get_connection_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsApp mcp logger")


class WhatsAppClient:
    def __init__(self,  business_account_id: str):
        credentials = get_connection_credentials(
        )

        self.access_token = credentials.get(
            "apiKey", credentials.get("credentials", {}).get("apiKey")
        )
        if not self.access_token:
            raise ValueError("API key is missing from credentials")

        self.base_url = f"https://graph.facebook.com/v21.0/{business_account_id}/message_templates"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        logger.info(
            "WhatsAppClient initialized",
            extra={
                "business_account_id": business_account_id,
                "path": os.getenv("WM_JOB_PATH"),
            },
        )

    def check_template_status(self, template_name: str) -> Dict[str, Any]:
        try:
            logger.info(
                f"Checking status for template: {template_name}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )

            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response_data = response.json()

            if response.status_code == 200:
                templates = response_data.get("data", [])
                for template in templates:
                    if template.get("name") == template_name:
                        logger.info(
                            f"Template status retrieved: {template}",
                            extra={"path": os.getenv("WM_JOB_PATH")},
                        )
                        return {"result": template, "error": None}

                return {"result": None, "error": "Template not found"}

            error_message = response_data.get("error", {}).get("message", response.text)
            logger.error(
                f"Failed to retrieve template status: {error_message}",
                extra={"path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": error_message}

        except Exception as e:
            logger.error(
                f"Error checking template status: {str(e)}",
                extra={"error_type": type(e).__name__, "path": os.getenv("WM_JOB_PATH")},
            )
            return {"result": None, "error": str(e)}


def main(
    connection_id: str,
    business_account_id: str,
    template_name: str,
) -> Dict[str, Any]:
    try:
        whatsapp_client = WhatsAppClient(connection_id, business_account_id)
        return whatsapp_client.check_template_status(template_name)

    except Exception as e:
        logger.error(
            f"Error in main function: {str(e)}",
            extra={"path": os.getenv("WM_JOB_PATH")},
        )
        return {"result": None, "error": str(e)}
