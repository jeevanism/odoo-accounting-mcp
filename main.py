# main.py

import os
import sys
from dotenv import load_dotenv
from mcp.server.stdio import stdio_server
import anyio

# Load environment variables
load_dotenv()

from server import mcp 

async def run_mcp_server():
    print("Launching Odoo MCP server via stdio...", file=sys.stderr)
    async with stdio_server() as (reader, writer):
        await mcp._mcp_server.run(reader, writer, mcp._mcp_server.create_initialization_options())

def main():
    anyio.run(run_mcp_server)

if __name__ == "__main__":
    sys.exit(main())
