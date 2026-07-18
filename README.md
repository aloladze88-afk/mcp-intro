# Programming Learning MCP Server

A beginner Python project demonstrating how an MCP server can expose programming-study capabilities to a client or AI agent.

## Project status

Completed:

- Task 0: project structure
- Task 1: MCP architecture explanation
- Task 2: basic FastMCP server

## Project structure

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

## What each part is for

- `server/`: the MCP server, tools and resources.
- `client/`: the MCP client and agent.
- `data/`: local programming-topic data.
- `output/`: generated example responses.
- `requirements.txt`: Python dependencies.
- `.env.example`: example environment variables.
- `.gitignore`: files Git must not commit.

## MCP Architecture Summary

MCP, or the Model Context Protocol, is a standard way for an AI application to connect to external tools and information.

- **MCP host:** the main AI application. It manages the conversation, model, permissions and server connections.
- **MCP client:** the connection between the host and one MCP server. A host normally creates one client for each server.
- **MCP server:** a separate program that exposes focused capabilities.
- **Tools:** functions that perform an operation, such as searching programming topics.
- **Resources:** read-only information, such as a catalogue of available topics.

Simple flow:

```text
Student → MCP host → MCP client → MCP server → tool or resource
```

A server should expose only the capabilities it genuinely needs. This keeps it easier to understand and reduces unnecessary access and risk.

### Task 1 self-validation

- [x] I explained what MCP is.
- [x] I explained the role of an MCP host.
- [x] I explained the role of an MCP client.
- [x] I explained the role of an MCP server.
- [x] I explained the difference between tools and resources.
- [x] I used my own words.

## Basic FastMCP server

`server/learning_server.py` creates a minimal server named `Programming Learning Server`.

```python
from fastmcp import FastMCP

mcp = FastMCP("Programming Learning Server")

if __name__ == "__main__":
    mcp.run()
```

`FastMCP(...)` creates the server. `mcp.run()` starts it. The `__main__` condition means it starts when the file is run directly.

The server does not contain tools or resources yet. Those belong to later tasks.

## Setup

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Start the server

```bash
python server/learning_server.py
```

FastMCP uses stdio by default. The process may appear to wait because it is expecting an MCP client. Stop it with `Ctrl+C`.

Avoid ordinary `print()` debugging in a stdio server because stdout is used for MCP communication.

### Task 2 self-validation

- [x] I created a FastMCP server instance.
- [x] The server has the name `Programming Learning Server`.
- [x] The server can run as a Python script.
- [x] The server starts without errors after installing the requirements.
- [x] I documented how to start the server.

## Task 0 self-validation

- [x] I created the required project directories.
- [x] I created the MCP server file.
- [x] I created the client and agent files.
- [x] I created the data directory.
- [x] I created `README.md`.
- [x] I created `requirements.txt`.
- [x] I created `.env.example`.
- [x] I created `.gitignore`.

## Real-world example

A learning assistant could connect to this server and ask it to search a catalogue of Python topics. Later tasks will add the tool that performs the search and the resource that provides the catalogue.
