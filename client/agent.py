"""Run a simple study assistant that uses the MCP server through stdio."""

import argparse
import asyncio
import re
from pathlib import Path

from fastmcp import Client


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_FILE = PROJECT_ROOT / "server" / "learning_server.py"
OUTPUT_FILE = PROJECT_ROOT / "output" / "sample_agent_response.md"

STOP_WORDS = {
    "a",
    "about",
    "and",
    "first",
    "for",
    "how",
    "i",
    "is",
    "learn",
    "me",
    "my",
    "of",
    "please",
    "python",
    "review",
    "should",
    "study",
    "the",
    "to",
    "want",
    "what",
    "with",
}


def _search_candidates(question: str) -> list[str]:
    """Return useful search terms extracted from a student's question."""
    words = [
        word.replace("-", " ")
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]*", question)
        if word.casefold() not in STOP_WORDS
    ]

    candidates = []

    if 1 <= len(question.split()) <= 4:
        candidates.append(question.strip())

    for index in range(len(words) - 1):
        candidates.append(f"{words[index]} {words[index + 1]}")

    candidates.extend(words)

    unique_candidates = []
    seen = set()

    for candidate in candidates:
        cleaned_candidate = candidate.strip()
        key = cleaned_candidate.casefold()

        if cleaned_candidate and key not in seen:
            seen.add(key)
            unique_candidates.append(cleaned_candidate)

    return unique_candidates or [""]


def _format_list(items: list[str]) -> str:
    """Format a list as short Markdown bullet points."""
    return "\n".join(f"- {item}" for item in items)


def _format_success(question: str, topic: dict) -> str:
    """Create a student-facing Markdown answer from one topic record."""
    return f"""# Programming Study Recommendation

**Student question:** {question}

## Recommended topic

**{topic['title']}**

## Why it is relevant

{topic['summary']}

## Prerequisites

{_format_list(topic['prerequisites'])}

## Key concepts

{_format_list(topic['key_concepts'])}

## Practice idea

{topic['practice_idea']}

## Common mistakes to avoid

{_format_list(topic['common_mistakes'])}
"""


def _format_no_match(question: str, message: str) -> str:
    """Create a clear Markdown answer when no topic matches."""
    return f"""# Programming Study Recommendation

**Student question:** {question or '(blank question)'}

No matching topic was found in the local MCP topic dataset.

Server response: {message}
"""


async def create_answer(question: str) -> str:
    """Call the MCP tools and build a short answer from their returned data."""
    client = Client(str(SERVER_FILE))
    last_message = "No matching topic was found."

    async with client:
        selected_topic = None

        for query in _search_candidates(question):
            search_result = await client.call_tool(
                "search_topics",
                {"query": query},
            )
            matches = search_result.data

            if matches and "message" not in matches[0]:
                selected_topic = matches[0]
                break

            if matches and "message" in matches[0]:
                last_message = matches[0]["message"]

        if selected_topic is None:
            return _format_no_match(question, last_message)

        details_result = await client.call_tool(
            "get_topic_details",
            {"topic_id": selected_topic["id"]},
        )
        topic = details_result.data

        if "message" in topic:
            return _format_no_match(question, topic["message"])

        return _format_success(question, topic)


async def run(question: str) -> str:
    """Generate, save and return one MCP-backed study response."""
    answer = await create_answer(question)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(answer, encoding="utf-8")
    return answer


def main() -> None:
    """Read a question from the command line and run the agent-like client."""
    parser = argparse.ArgumentParser(
        description=(
            "Ask the MCP-backed programming study assistant a question."
        )
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="A programming topic or student question.",
    )
    args = parser.parse_args()

    question = " ".join(args.question).strip()

    if not question:
        question = input(
            "What programming topic do you want to study? "
        ).strip()

    answer = asyncio.run(run(question))
    print(answer)
    print(f"Saved response to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
