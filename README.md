# WhatsApp MCP Server

A Model Context Protocol (MCP) server for WhatsApp Business API integration. This server provides tools for sending various types of messages through WhatsApp Business API.

## Features

- Send text messages and templates
- Send images with optional captions
- Send videos with optional captions  
- Send documents with optional captions
- Send audio/voice messages
- Send interactive list messages
- Send template messages with dynamic parameters
- Check template approval status
- Create new message templates

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

Set the following environment variable in your `.env` file:

```env
WHATSAPP_ACCESS_TOKEN=your_whatsapp_business_api_access_token
```

## Usage

### Running the MCP Server

```bash
python server.py
```

### Available Tools

#### send_text_message
Send a text message or template message via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number
- `message`: Text message to send (optional if template_name is provided)
- `template_name`: Template name to use (optional if message is provided)
- `language_code`: Language code for template (default: en_US)

#### send_image_message
Send an image message via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number
- `image_url`: URL of the image to send
- `caption`: Optional caption for the image

#### send_video_message
Send a video message via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number
- `video_url`: URL of the video to send
- `caption`: Optional caption for the video

#### send_document_message
Send a document message via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number
- `document_url`: URL of the document to send
- `caption`: Optional caption for the document

#### send_audio_message
Send an audio/voice message via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number
- `audio_url`: URL of the audio file to send

#### send_list_message
Send an interactive list message via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number
- `sections`: List of sections with options

**Example sections format:**
```json
[
    {
        "title": "Section 1",
        "rows": [
            {
                "id": "option1",
                "title": "First Option",
                "description": "Description for first option"
            },
            {
                "id": "option2",
                "title": "Second Option", 
                "description": "Description for second option"
            }
        ]
    }
]
```

#### send_template_message
Send a template message with dynamic parameters via WhatsApp.

**Parameters:**
- `phone_number_id`: WhatsApp Business phone number ID
- `to`: Recipient phone number with country code
- `template_name`: Name of the approved template
- `parameters`: List of template parameters
- `language`: Template language code (default: "en")

**Example parameters format:**
```json
[
    {"type": "text", "text": "John Smith"},
    {"type": "text", "text": "2024-01-15"}
]
```

#### check_template_status
Check the approval status of a WhatsApp template.

**Parameters:**
- `business_account_id`: WhatsApp Business Account ID
- `template_name`: Name of the template to check

#### create_template
Create a new WhatsApp message template.

**Parameters:**
- `whatsapp_business_account_id`: WhatsApp Business Account ID
- `template_name`: Name for the new template
- `language`: Language code for the template
- `body`: Main body text of the template
- `header`: Optional header text
- `footer`: Optional footer text
- `button`: Optional button configuration

## Changes Made

This project has been updated with the following changes:

1. **Replaced logger with print statements** - All logging calls have been replaced with simple print statements for easier debugging
2. **Replaced Nango connection function** - Updated to use a custom connection function that reads from environment variables
3. **Removed connection arguments** - All functions no longer require connection_id parameters as credentials are read from environment
4. **Converted to MCP tools** - All main functions have been converted to MCP tools using FastMCP decorators

## Requirements

- Python 3.13+
- WhatsApp Business API access token
- Valid WhatsApp Business phone number ID
- Valid WhatsApp Business Account ID (for template operations)

## License

This project is licensed under the MIT License.
