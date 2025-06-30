#!/usr/bin/env python3
"""
WhatsApp MCP Server entry point
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from whatsapp_mcp.server import main

if __name__ == "__main__":
    main()
