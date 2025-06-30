# WhatsApp MCP Server

A comprehensive Model Context Protocol (MCP) server for WhatsApp Business API integration. This server provides powerful tools for sending various types of messages, managing templates, and handling interactive communications through WhatsApp Business API.

## 🚀 Features

### Message Types
- **Text Messages** - Send plain text and template messages
- **Media Messages** - Send images, videos, documents, and audio files
- **Interactive Messages** - Send lists and button menus
- **Template Messages** - Send approved templates with dynamic parameters

### Template Management
- **Create Templates** - Design new message templates
- **Check Status** - Monitor template approval status
- **List Templates** - View all available templates

### Enterprise Ready
- **Clean Architecture** - Modular, maintainable codebase
- **Error Handling** - Robust error handling and logging
- **Type Safety** - Full type hints for better development experience
- **Environment Based** - Secure credential management

## 📦 Installation

### Option 1: Direct Installation
```bash
git clone <repository-url>
cd whatsapp-mcp
uv sync
```

## ⚙️ Configuration

### Environment Setup
Create a `.env` file in your project root:

```env
# Nango Configuration for WhatsApp Business API
NANGO_CONNECTION_ID=your_nango_connection_id
NANGO_INTEGRATION_ID=whatsapp-business
NANGO_BASE_URL=https://api.nango.dev
NANGO_SECRET_KEY=your_nango_secret_key
```

### Getting Nango Credentials
1. Set up a [Nango account](https://www.nango.dev/)
2. Create a WhatsApp Business integration in Nango
3. Set up your WhatsApp Business API connection
4. Get your Nango connection ID and secret key

### Getting WhatsApp Credentials
1. Set up a [WhatsApp Business Account](https://business.whatsapp.com/)
2. Create a [Meta Developer App](https://developers.facebook.com/)
3. Add WhatsApp Business API to your app
4. Configure the integration in Nango with your WhatsApp credentials

### Running the Server

```bash
# Run using the installed command
whatsapp-mcp

# Or run directly from source
python main.py

# Or as a module
python -m whatsapp_mcp.server

# Show help
python main.py --help
```

**Note:** This server uses the MCP stdio transport protocol and is designed to be run by MCP clients like Claude Desktop. It communicates via stdin/stdout and should not be run directly in interactive mode.

## 🤖 Claude Desktop Integration

Add this configuration to your Claude Desktop config file:

### macOS
`~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows  
`%APPDATA%/Claude/claude_desktop_config.json`

### Linux
`~/.config/Claude/claude_desktop_config.json`



```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "uvx",
      "args": ["git+https://github.com/Shameerpc5029/whatsapp-mcp.git"],
      "env": {
        "NANGO_CONNECTION_ID": "your_nango_connection_id",
        "NANGO_INTEGRATION_ID": "whatsapp-business",
        "NANGO_BASE_URL": "https://api.nango.dev",
        "NANGO_SECRET_KEY": "your_nango_secret_key"
      }
    }
  }
}
```

## 🛠️ Available Tools

### Message Tools

#### `send_text_message`
Send text messages or templates to WhatsApp users.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number with country code
- `message` (str, optional): Text message content
- `template_name` (str, optional): Template name to use
- `language_code` (str): Language code for templates (default: "en_US")

**Example Usage:**
```python
# Send text message
send_text_message(
    phone_number_id="1234567890",
    to="+1234567890", 
    message="Hello! How can I help you today?"
)

# Send template message
send_text_message(
    phone_number_id="1234567890",
    to="+1234567890",
    template_name="welcome_message",
    language_code="en_US"
)
```

#### `send_image_message`
Send images with optional captions.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `image_url` (str): Public URL of the image
- `caption` (str, optional): Image caption

#### `send_video_message`
Send videos with optional captions.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `video_url` (str): Public URL of the video
- `caption` (str, optional): Video caption

#### `send_document_message`
Send documents like PDFs, Word files, etc.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `document_url` (str): Public URL of the document
- `caption` (str, optional): Document caption
- `filename` (str, optional): Filename for the document

#### `send_audio_message`
Send audio files and voice messages.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `audio_url` (str): Public URL of the audio file

### Interactive Tools

#### `send_list_message`
Send interactive list messages with selectable options.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `sections` (list): List of sections with options
- `header_text` (str): Header text (default: "Available Options")
- `body_text` (str): Body text
- `footer_text` (str): Footer text
- `button_text` (str): Button text (default: "Options")

**Example Usage:**
```python
sections = [
    {
        "title": "Main Menu",
        "rows": [
            {
                "id": "option_1",
                "title": "Product Info",
                "description": "Get information about our products"
            },
            {
                "id": "option_2",
                "title": "Support",
                "description": "Contact customer support"
            }
        ]
    }
]

send_list_message(
    phone_number_id="1234567890",
    to="+1234567890",
    sections=sections,
    body_text="How can we help you today?"
)
```

#### `send_button_message`
Send interactive messages with up to 3 buttons.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `body_text` (str): Main message text
- `buttons` (list): List of buttons (max 3)
- `header_text` (str, optional): Header text
- `footer_text` (str, optional): Footer text

### Template Tools

#### `send_template_message`
Send approved template messages with dynamic parameters.

**Parameters:**
- `phone_number_id` (str): Your WhatsApp Business phone number ID
- `to` (str): Recipient's phone number
- `template_name` (str): Name of approved template
- `parameters` (list, optional): List of parameters for template variables
- `language` (str): Template language code (default: "en")

**Example Usage:**
```python
parameters = [
    {"type": "text", "text": "John Smith"},
    {"type": "text", "text": "December 25, 2024"}
]

send_template_message(
    phone_number_id="1234567890",
    to="+1234567890",
    template_name="appointment_reminder",
    parameters=parameters,
    language="en"
)
```

#### `check_template_status`
Check the approval status of a template.

**Parameters:**
- `business_account_id` (str): WhatsApp Business Account ID
- `template_name` (str): Name of the template to check

#### `list_templates`
List all templates for your business account.

**Parameters:**
- `business_account_id` (str): WhatsApp Business Account ID
- `status_filter` (str, optional): Filter by status (APPROVED, PENDING, REJECTED)

#### `create_template`
Create a new message template.

**Parameters:**
- `business_account_id` (str): WhatsApp Business Account ID
- `template_name` (str): Name for the new template
- `language` (str): Language code
- `category` (str): Template category (MARKETING, UTILITY, AUTHENTICATION)
- `components` (list): List of template components

## 📁 Project Structure

```
whatsapp-mcp/
├── src/
│   └── whatsapp_mcp/
│       ├── __init__.py
│       ├── server.py          # Main server entry point
│       ├── tools/            # MCP tools
│       │   ├── __init__.py
│       │   ├── messages.py   # Message sending tools
│       │   ├── interactive.py # Interactive message tools
│       │   └── templates.py  # Template management tools
│       └── utils/            # Utilities
│           ├── __init__.py   # Core utilities
│           └── client.py     # WhatsApp API client
├── .env.example              # Environment template
├── pyproject.toml           # Project configuration
└── README.md               # This file
```


## 📝 Usage Examples

### Basic Text Message
```python
# Send a simple text message
result = send_text_message(
    phone_number_id="1234567890",
    to="+1234567890",
    message="Hello! Welcome to our service."
)
```

### Image with Caption
```python
# Send an image with caption
result = send_image_message(
    phone_number_id="1234567890",
    to="+1234567890", 
    image_url="https://example.com/image.jpg",
    caption="Check out our new product!"
)
```

### Interactive List
```python
# Send an interactive list
sections = [
    {
        "title": "Services",
        "rows": [
            {
                "id": "service_1",
                "title": "Web Development", 
                "description": "Custom website development"
            },
            {
                "id": "service_2",
                "title": "Mobile Apps",
                "description": "iOS and Android app development"
            }
        ]
    }
]

result = send_list_message(
    phone_number_id="1234567890",
    to="+1234567890",
    sections=sections,
    body_text="What service are you interested in?"
)
```

### Template with Parameters
```python
# Send template with dynamic content
parameters = [
    {"type": "text", "text": "Alice Johnson"},
    {"type": "text", "text": "Premium"},
    {"type": "text", "text": "January 15, 2025"}
]

result = send_template_message(
    phone_number_id="1234567890",
    to="+1234567890",
    template_name="subscription_confirmation",
    parameters=parameters
)
```

## 🔒 Security

- **Environment Variables**: Store sensitive data like access tokens in environment variables
- **Input Validation**: All inputs are validated before API calls
- **Error Handling**: Secure error messages that don't expose sensitive information
- **Rate Limiting**: Respect WhatsApp API rate limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and request features via GitHub Issues
- **WhatsApp API**: Refer to [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)

## 🔄 Changelog

### v0.1.0
- Initial release
- Basic message sending capabilities
- Template management
- Interactive messages
- Claude Desktop integration
- Clean modular architecture

---

**Note**: This MCP server requires a WhatsApp Business API account and valid access tokens. Make sure to comply with WhatsApp's terms of service and messaging policies.
