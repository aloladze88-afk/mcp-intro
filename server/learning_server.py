"""Minimal FastMCP server for programming-learning capabilities."""

from fastmcp import FastMCP


# Create the MCP server instance.
mcp = FastMCP("Programming Learning Server")


if __name__ == "__main__":
    # Start the server with FastMCP's default stdio transport.
    mcp.run()
