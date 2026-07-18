# MCP Servers in Python: Tools, Resources, and Agent Integration

## Description

This beginner project demonstrates how to build a small Model Context Protocol (MCP) server in Python, expose local learning data, connect through an MCP client, and later integrate the server with an AI agent.

## Project Status

- Task 0 — Project structure: complete
- Task 1 — MCP architecture explanation: complete
- Task 2 — Basic FastMCP server: complete
- Task 3 — Local topic dataset: complete

## Project Structure

```text
mcp-intro/
├── server/
│   ├── __init__.py
│   └── learning_server.py
├── client/
│   ├── __init__.py
│   ├── mcp_client.py
│   └── agent.py
├── data/
│   └── topics.json
├── output/
│   └── sample_agent_response.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## MCP Architecture Summary

MCP is a standard way for AI applications to connect to external capabilities.

- The MCP host manages the AI application and the overall interaction.
- The MCP client connects the host to one MCP server.
- A host can create one client for each server it uses.
- The MCP server exposes focused capabilities.
- Tools perform operations.
- Resources provide read-only information.
- A server should expose only the capabilities that are necessary.

Basic flow:

```text
Student → MCP host → MCP client → MCP server → tool or resource
```

## Basic FastMCP Server

The server is created in `server/learning_server.py`:

```python
"""Minimal FastMCP server for programming-learning capabilities."""

from fastmcp import FastMCP


# Create the MCP server instance.
mcp = FastMCP("Programming Learning Server")


if __name__ == "__main__":
    # Start the server with FastMCP's default stdio transport.
    mcp.run()
```

`FastMCP(...)` creates the server, while `mcp.run()` starts it. The `if __name__ == "__main__":` condition means the server starts when this file is run directly. FastMCP uses standard input and output, called stdio, by default. Ordinary debug messages should not be printed to stdout because they can interfere with MCP communication.

## Local Topic Dataset

`data/topics.json` contains five small programming-learning records:

- Python Functions
- Python Lists
- Python Dictionaries
- Python Exception Handling
- Python Classes

Each topic contains:

- `id`
- `title`
- `summary`
- `prerequisites`
- `key_concepts`
- `common_mistakes`
- `practice_idea`

The file uses a top-level `topics` list so the MCP server can load and search the records in later tasks.

## Requirements

- Python 3.10 or newer
- A Python virtual environment
- Packages listed in `requirements.txt`

## Setup

```bash
cd ~/mcp-intro

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## How to Run the Server

```bash
cd ~/mcp-intro
source .venv/bin/activate
python server/learning_server.py
```

The server waits for MCP communication through stdio. Stop it with `Ctrl+C`.

## Validate the JSON Dataset

```bash
cd ~/mcp-intro
python -m json.tool data/topics.json
```

If the JSON is valid, Python prints the formatted data. If it is invalid, Python reports the location of the syntax error.

You can also check the number of topics:

```bash
python -c "import json; data=json.load(open('data/topics.json')); print(len(data['topics']))"
```

Expected result:

```text
5
```

## Real-World Use Case

A programming tutor agent could ask the MCP server for the topic `python-functions`. The server could return its summary, prerequisites, common mistakes and practice idea without putting all learning content directly inside the agent prompt.

## Self-Validation

### Task 0 — Project Structure

- [x] I created the required project directories.
- [x] I created the server, client and agent files.
- [x] I created `data/topics.json`.
- [x] I created `output/sample_agent_response.md`.
- [x] I created `README.md`.
- [x] I created `requirements.txt`.
- [x] I created `.env.example`.
- [x] I created `.gitignore`.
- [x] Secrets, virtual environments, caches and editor files are excluded from Git.
- [x] Server code is separate from client and agent code.

### Task 1 — MCP Architecture

- [x] I explained what MCP is.
- [x] I explained the MCP host.
- [x] I explained the MCP client.
- [x] I explained the MCP server.
- [x] I explained tools.
- [x] I explained resources.
- [x] I included the basic interaction flow.
- [x] I explained why servers should expose only necessary capabilities.

### Task 2 — Basic FastMCP Server

- [x] I imported `FastMCP`.
- [x] I created a server named `Programming Learning Server`.
- [x] I stored the server in `mcp`.
- [x] I added a script entry point.
- [x] The entry point calls `mcp.run()`.
- [x] The server can use FastMCP's default stdio transport.
- [x] I avoided ordinary debug output on stdout.

### Task 3 — Local Topic Dataset

- [x] I created `data/topics.json`.
- [x] The dataset contains at least five topics.
- [x] Each topic has an `id`.
- [x] Each topic has a `title`.
- [x] Each topic has a `summary`.
- [x] Each topic has `prerequisites`.
- [x] Each topic has `key_concepts`.
- [x] Each topic has `common_mistakes`.
- [x] Each topic has a `practice_idea`.
- [x] The JSON file is valid.
