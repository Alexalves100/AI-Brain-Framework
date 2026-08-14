"""
CLI Tool: Starts the AI-Brain-Framework Model Context Protocol (MCP) Server.
Zero external dependencies.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.mcp import MCPServer


def main():
    server = MCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
