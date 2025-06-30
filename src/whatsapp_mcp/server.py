"""
WhatsApp MCP Server - A Model Context Protocol server for WhatsApp Business API integration.

This server provides tools for sending messages, managing templates, and handling interactive communications
via WhatsApp Business API. It implements the MCP stdio transport protocol for seamless integration with MCP clients.
"""

import json
from typing import Any, Dict, List
import asyncio
import sys

from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import (
    TextContent,
    Tool,
)

# Import tool functions
from whatsapp_mcp.tools.messages import (
    send_text_message, send_image_message, send_video_message,
    send_document_message, send_audio_message,
)
from whatsapp_mcp.tools.interactive import (
    send_list_message, send_button_message,
)
from whatsapp_mcp.tools.templates import (
    send_template_message, check_template_status, list_templates, create_template,
)


class WhatsAppMCPServer:
    """MCP Server for WhatsApp Business API integration using proper MCP patterns."""
    
    def __init__(self):
        """Initialize the WhatsApp MCP server with all tools."""
        self.server = Server("whatsapp-mcp")
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup all available tools with their schemas."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available tools."""
            return [
                # Message Tools
                Tool(
                    name="send_text_message",
                    description="Send a text message or template message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "message": {"type": "string", "description": "Text message to send (optional if template_name is provided)"},
                            "template_name": {"type": "string", "description": "Template name to use (optional if message is provided)"},
                            "language_code": {"type": "string", "default": "en_US", "description": "Language code for template"}
                        },
                        "required": ["phone_number_id", "to"]
                    }
                ),
                Tool(
                    name="send_image_message",
                    description="Send an image message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "image_url": {"type": "string", "description": "Public URL of the image to send"},
                            "caption": {"type": "string", "description": "Optional caption for the image"}
                        },
                        "required": ["phone_number_id", "to", "image_url"]
                    }
                ),
                Tool(
                    name="send_video_message",
                    description="Send a video message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "video_url": {"type": "string", "description": "Public URL of the video to send"},
                            "caption": {"type": "string", "description": "Optional caption for the video"}
                        },
                        "required": ["phone_number_id", "to", "video_url"]
                    }
                ),
                Tool(
                    name="send_document_message",
                    description="Send a document message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "document_url": {"type": "string", "description": "Public URL of the document to send"},
                            "caption": {"type": "string", "description": "Optional caption for the document"},
                            "filename": {"type": "string", "description": "Optional filename for the document"}
                        },
                        "required": ["phone_number_id", "to", "document_url"]
                    }
                ),
                Tool(
                    name="send_audio_message",
                    description="Send an audio/voice message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "audio_url": {"type": "string", "description": "Public URL of the audio file to send"}
                        },
                        "required": ["phone_number_id", "to", "audio_url"]
                    }
                ),
                
                # Interactive Tools
                Tool(
                    name="send_list_message",
                    description="Send an interactive list message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "sections": {
                                "type": "array",
                                "description": "List of sections with options",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "rows": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "title": {"type": "string"},
                                                    "description": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "header_text": {"type": "string", "default": "Available Options", "description": "Header text for the message"},
                            "body_text": {"type": "string", "default": "Please select from the following options:", "description": "Body text for the message"},
                            "footer_text": {"type": "string", "default": "Select an option to proceed", "description": "Footer text for the message"},
                            "button_text": {"type": "string", "default": "Options", "description": "Button text for the list"}
                        },
                        "required": ["phone_number_id", "to", "sections"]
                    }
                ),
                Tool(
                    name="send_button_message",
                    description="Send an interactive button message via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "body_text": {"type": "string", "description": "Main message text"},
                            "buttons": {
                                "type": "array",
                                "description": "List of buttons (max 3)",
                                "maxItems": 3,
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "enum": ["reply"]},
                                        "reply": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "title": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            },
                            "header_text": {"type": "string", "description": "Optional header text"},
                            "footer_text": {"type": "string", "description": "Optional footer text"}
                        },
                        "required": ["phone_number_id", "to", "body_text", "buttons"]
                    }
                ),
                
                # Template Tools
                Tool(
                    name="send_template_message",
                    description="Send a template message with dynamic parameters via WhatsApp Business API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number_id": {"type": "string", "description": "WhatsApp Business phone number ID"},
                            "to": {"type": "string", "description": "Recipient phone number with country code"},
                            "template_name": {"type": "string", "description": "Name of the approved template"},
                            "parameters": {
                                "type": "array",
                                "description": "List of template parameters",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "enum": ["text"]},
                                        "text": {"type": "string"}
                                    }
                                }
                            },
                            "language": {"type": "string", "default": "en", "description": "Template language code"}
                        },
                        "required": ["phone_number_id", "to", "template_name"]
                    }
                ),
                Tool(
                    name="check_template_status",
                    description="Check the approval status of a WhatsApp template",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "business_account_id": {"type": "string", "description": "WhatsApp Business Account ID"},
                            "template_name": {"type": "string", "description": "Name of the template to check"}
                        },
                        "required": ["business_account_id", "template_name"]
                    }
                ),
                Tool(
                    name="list_templates",
                    description="List all templates for a WhatsApp Business Account",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "business_account_id": {"type": "string", "description": "WhatsApp Business Account ID"},
                            "status_filter": {"type": "string", "description": "Optional status filter (APPROVED, PENDING, REJECTED)"}
                        },
                        "required": ["business_account_id"]
                    }
                ),
                Tool(
                    name="create_template",
                    description="Create a new WhatsApp message template",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "business_account_id": {"type": "string", "description": "WhatsApp Business Account ID"},
                            "template_name": {"type": "string", "description": "Name for the new template"},
                            "language": {"type": "string", "description": "Language code for the template"},
                            "category": {"type": "string", "enum": ["MARKETING", "UTILITY", "AUTHENTICATION"], "description": "Template category"},
                            "components": {
                                "type": "array",
                                "description": "List of template components",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "enum": ["HEADER", "BODY", "FOOTER"]},
                                        "format": {"type": "string"},
                                        "text": {"type": "string"}
                                    }
                                }
                            }
                        },
                        "required": ["business_account_id", "template_name", "language", "category", "components"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute a tool with the given arguments."""
            try:
                # Route the tool call to the appropriate function
                if name == "send_text_message":
                    result = send_text_message(**arguments)
                elif name == "send_image_message":
                    result = send_image_message(**arguments)
                elif name == "send_video_message":
                    result = send_video_message(**arguments)
                elif name == "send_document_message":
                    result = send_document_message(**arguments)
                elif name == "send_audio_message":
                    result = send_audio_message(**arguments)
                elif name == "send_list_message":
                    result = send_list_message(**arguments)
                elif name == "send_button_message":
                    result = send_button_message(**arguments)
                elif name == "send_template_message":
                    result = send_template_message(**arguments)
                elif name == "check_template_status":
                    result = check_template_status(**arguments)
                elif name == "list_templates":
                    result = list_templates(**arguments)
                elif name == "create_template":
                    result = create_template(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                # Return the result as TextContent
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
                
            except Exception as e:
                # Return error information
                error_result = {
                    "error": str(e),
                    "tool": name,
                    "arguments": arguments
                }
                return [TextContent(type="text", text=json.dumps(error_result, indent=2))]
    
    async def run(self):
        """Run the MCP server using stdio transport."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream, 
                self.server.create_initialization_options()
            )


def main():
    """Main entry point for the MCP server."""
    
    # Check if we're being run directly or as a module
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("WhatsApp MCP Server")
        print("A Model Context Protocol server for WhatsApp Business API integration.")
        print("")
        print("Usage:")
        print("  python -m whatsapp_mcp.server")
        print("  or")
        print("  whatsapp-mcp")
        print("")
        print("This server provides 11 tools for managing:")
        print("  • Messages (text, image, video, document, audio)")
        print("  • Interactive Messages (lists, buttons)")
        print("  • Templates (send, check status, list, create)")
        print("")
        print("The server communicates via stdin/stdout using the MCP protocol.")
        print("")
        print("Required environment variables:")
        print("  NANGO_CONNECTION_ID - Nango connection ID for WhatsApp Business")
        print("  NANGO_INTEGRATION_ID - Nango integration ID (usually 'whatsapp-business')")
        print("  NANGO_BASE_URL - Nango API base URL (usually 'https://api.nango.dev')")
        print("  NANGO_SECRET_KEY - Nango secret key for authentication")
        return
    
    # Create and run the server
    server = WhatsAppMCPServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\\nServer shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
