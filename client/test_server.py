"""Run direct integration checks against the local FastMCP server."""

import asyncio
import json
from pathlib import Path

from fastmcp import Client


SERVER_FILE = (
    Path(__file__).resolve().parent.parent / "server" / "learning_server.py"
)
EXPECTED_TOOLS = {"search_topics", "get_topic_details"}
CATALOG_URI = "topics://catalog"


async def main() -> None:
    """Connect through stdio and verify the server's public capabilities."""
    client = Client(str(SERVER_FILE))

    async with client:
        await client.ping()
        print("[PASS] Server started and responded to ping.")

        tools = await client.list_tools()
        tool_names = {tool.name for tool in tools}
        assert EXPECTED_TOOLS.issubset(tool_names)
        print(f"[PASS] Tools are visible: {sorted(tool_names)}")

        search_result = await client.call_tool(
            "search_topics",
            {"query": "functions"},
        )
        assert isinstance(search_result.data, list)
        assert search_result.data[0]["id"] == "python-functions"
        print(
            "[PASS] search_topics returned: "
            f"{search_result.data[0]['title']}"
        )

        details_result = await client.call_tool(
            "get_topic_details",
            {"topic_id": "python-functions"},
        )
        assert details_result.data["id"] == "python-functions"
        assert "common_mistakes" in details_result.data
        print(
            "[PASS] get_topic_details returned the full record for: "
            f"{details_result.data['title']}"
        )

        blank_search = await client.call_tool(
            "search_topics",
            {"query": "   "},
        )
        assert "message" in blank_search.data[0]
        print(f"[PASS] Blank search error: {blank_search.data[0]['message']}")

        unknown_topic = await client.call_tool(
            "get_topic_details",
            {"topic_id": "unknown-topic"},
        )
        assert "message" in unknown_topic.data
        print(f"[PASS] Unknown id error: {unknown_topic.data['message']}")

        resources = await client.list_resources()
        resource_uris = {str(resource.uri) for resource in resources}
        assert CATALOG_URI in resource_uris
        print(f"[PASS] Resource is visible: {CATALOG_URI}")

        resource_contents = await client.read_resource(CATALOG_URI)
        catalog = json.loads(resource_contents[0].text)
        assert len(catalog) == 5
        assert all(set(item) == {"id", "title"} for item in catalog)
        print(f"[PASS] Catalogue resource returned {len(catalog)} topics.")

    print("All MCP server tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
