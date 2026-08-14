"""
Entrypoint for starting the MCP server via `python -m framework.mcp`
"""

from .server import MCPServer


def main():
    server = MCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
