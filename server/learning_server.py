"""FastMCP server for programming-learning capabilities."""

import json
from pathlib import Path

from fastmcp import FastMCP


# Create the MCP server instance.
mcp = FastMCP("Programming Learning Server")

# Build a reliable path to the local dataset.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "topics.json"
MAX_RESULTS = 3


def _load_topics() -> list[dict]:
    """Load and return all programming topics from the JSON dataset."""
    with DATA_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    return data["topics"]


@mcp.tool
def search_topics(query: str) -> list[dict]:
    """Search programming topics by title or key concept.

    Return up to three compact topic records so a client or agent can decide
    which topic is most relevant.
    """
    cleaned_query = query.strip().casefold()

    if not cleaned_query:
        return [{"message": "Please provide a non-empty search query."}]

    matches = []

    for topic in _load_topics():
        searchable_text = " ".join(
            [topic["title"], *topic["key_concepts"]]
        ).casefold()

        if cleaned_query in searchable_text:
            matches.append(
                {
                    "id": topic["id"],
                    "title": topic["title"],
                    "summary": topic["summary"],
                    "prerequisites": topic["prerequisites"],
                    "key_concepts": topic["key_concepts"],
                }
            )

        if len(matches) == MAX_RESULTS:
            break

    if not matches:
        return [
            {
                "message": (
                    f"No programming topics matched '{query.strip()}'."
                )
            }
        ]

    return matches


@mcp.tool
def get_topic_details(topic_id: str) -> dict:
    """Return full information for a programming topic by its id."""
    cleaned_topic_id = topic_id.strip().casefold()

    if not cleaned_topic_id:
        return {"message": "Please provide a non-empty topic id."}

    for topic in _load_topics():
        if topic["id"].casefold() == cleaned_topic_id:
            return topic

    return {
        "message": (
            f"No programming topic was found with id '{topic_id.strip()}'."
        )
    }


if __name__ == "__main__":
    # Start the server with FastMCP's default stdio transport.
    mcp.run()
