# MCP Servers in Python

## Description

This beginner project demonstrates how to build, test and consume a local Model Context Protocol (MCP) server with Python and FastMCP.

The server exposes a small programming-topic dataset through two tools and one read-only resource. A deterministic agent-like client connects to the server through MCP, searches for a relevant topic, retrieves its complete details and creates a short study recommendation.

Completed tasks:

- Task 0 — Project structure
- Task 1 — MCP architecture explanation
- Task 2 — Basic FastMCP server
- Task 3 — Local topic dataset
- Task 4 — `search_topics` tool
- Task 5 — `get_topic_details` tool
- Task 6 — Read-only catalogue resource
- Task 7 — Direct MCP server testing
- Task 8 — MCP-connected agent-like client
- Task 9 — Third-party MCP server review
- Task 10 — Complete documentation and reflection

Project structure:

```text
mcp-intro/
├── server/
│   ├── __init__.py
│   └── learning_server.py
├── client/
│   ├── __init__.py
│   ├── mcp_client.py
│   ├── agent.py
│   └── test_server.py
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

MCP gives an AI application a standard way to connect to external tools and data sources.

```text
Student
   ↓
Agent-like application
   ↓
FastMCP client
   ↓
Programming Learning Server
   ↓
Tools or resource
   ↓
data/topics.json
```

The main parts are:

- **MCP host:** the application that manages the overall interaction.
- **MCP client:** the connection between the host or application and one MCP server.
- **MCP server:** the program that publishes focused capabilities.
- **Tool:** a callable operation that accepts input and returns a result.
- **Resource:** readable data exposed through a stable URI.

The server should expose only the capabilities and data that the client needs.

## Requirements

- Python 3.10 or newer
- A Python virtual environment
- Packages listed in `requirements.txt`

The current Python dependencies are:

```text
fastmcp
python-dotenv
```

## Setup

```bash
cd ~/mcp-intro

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Validate the local dataset:

```bash
python -m json.tool data/topics.json > /dev/null
```

Compile the Python files:

```bash
python -m py_compile \
    server/learning_server.py \
    client/mcp_client.py \
    client/test_server.py \
    client/agent.py
```

No output from these validation commands means they completed successfully.

## How to Run the Server

The server uses FastMCP's default stdio transport.

```bash
cd ~/mcp-intro
source .venv/bin/activate
python server/learning_server.py
```

The process waits for an MCP client to communicate through standard input and output. Stop it with `Ctrl+C`.

Do not add ordinary debug `print()` calls to the server's standard output because they can interfere with stdio MCP messages.

## How to Test the Server

Run the cumulative FastMCP integration test:

```bash
cd ~/mcp-intro
source .venv/bin/activate
python client/test_server.py
```

The test client starts the server through stdio and verifies that:

- the server responds to a ping;
- both tools are listed;
- `search_topics` returns a valid match;
- `get_topic_details` returns a complete topic;
- blank and unknown inputs return understandable messages;
- `topics://catalog` is listed and can be read;
- the catalogue contains five topic ids and titles.

Expected final line:

```text
All MCP server tests passed.
```

The server can also be inspected manually:

```bash
fastmcp dev server/learning_server.py
```

Useful manual inputs are:

```text
search_topics: functions
search_topics: methods
search_topics: networking
get_topic_details: python-functions
get_topic_details: unknown-topic
resource: topics://catalog
```

## How to Run the Agent

Run the agent-like client with a student question:

```bash
cd ~/mcp-intro
source .venv/bin/activate
python client/agent.py "I want to study Python functions. What should I review first?"
```

It can also prompt for a question interactively:

```bash
python client/agent.py
```

The agent:

1. receives the student's question;
2. connects to `server/learning_server.py` through a FastMCP client;
3. calls `search_topics` through MCP;
4. calls `get_topic_details` through MCP;
5. formats the returned data as a student-facing answer;
6. saves the answer to `output/sample_agent_response.md`.

It does not import the server's tool functions directly.

## Available Tools

### `search_topics`

Searches topic titles and key concepts.

Input:

```json
{"query": "functions"}
```

It returns up to three compact matches containing:

- `id`
- `title`
- `summary`
- `prerequisites`
- `key_concepts`

A blank query or a query with no match returns a clear message.

### `get_topic_details`

Retrieves one complete topic by its stable id.

Input:

```json
{"topic_id": "python-functions"}
```

A successful result contains:

- `id`
- `title`
- `summary`
- `prerequisites`
- `key_concepts`
- `common_mistakes`
- `practice_idea`

A blank or unknown id returns a clear message.

## Available Resources

### `topics://catalog`

This read-only resource returns a JSON string containing only the available topic ids and titles.

Example:

```json
[
  {"id": "python-functions", "title": "Python Functions"},
  {"id": "python-lists", "title": "Python Lists"}
]
```

The resource reads the existing dataset and does not create, edit or delete files or topic records.

## Third-Party MCP Server Review

The reviewed third-party server is the official reference **Filesystem MCP Server** from the `modelcontextprotocol/servers` repository.

**Purpose:** It allows an MCP client to read files, inspect directories and metadata, search files, create directories, write or edit files, and move files or directories.

**Where it runs:** It runs locally as a Node.js process and normally communicates through stdio. It can be started with `npx` or Docker.

**Exposed tools:** Its documented tools include file reading, directory listing, directory trees, file search, file information, directory creation, file writing, file editing, moving files and listing allowed directories. The reviewed documentation describes tools rather than MCP resources.

**Permissions and credentials:** It does not require an API key or personal account. It requires explicit filesystem directory access and runs with the current user's permissions inside the allowed directories.

Restricted configuration example:

```json
{
  "mcpServers": {
    "filesystem-review": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/tmp/mcp-filesystem-review"
      ]
    }
  }
}
```

**Risk:** Broad access could expose private files or allow important files to be overwritten, edited or moved.

**Safety measure:** Grant access only to a dedicated test directory containing disposable files. Never expose the complete home directory, SSH keys, browser profiles, password stores or project secrets. Prefer a read-only mount when write access is unnecessary.

Documentation reviewed:

- `https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem`
- `https://modelcontextprotocol.io/docs/develop/connect-local-servers`

## Example Output

A real generated example is saved in `output/sample_agent_response.md`.

```text
Recommended topic: Python Functions

Why it is relevant:
Functions group reusable instructions under a name so that code can be organised and called when needed.

Prerequisites:
- Variables
- Basic Python syntax

Key concepts:
- Defining functions
- Parameters and arguments
- Return values

Practice idea:
Create a function that receives two numbers and returns their total.

Common mistakes to avoid:
- Calling a function before defining it
- Using print when a return value is needed
```

## Known Limitations

- The local dataset contains only five topics.
- Search uses simple case-insensitive substring matching rather than semantic search.
- The agent chooses the first matching topic rather than ranking several possibilities intelligently.
- The agent is deterministic and does not use an LLM.
- A question about a missing topic, such as Python decorators, cannot produce a detailed recommendation.
- The server currently uses local stdio only; it does not expose an authenticated HTTP endpoint.
- The dataset is loaded from disk on every tool or resource call.
- The agent overwrites `output/sample_agent_response.md` each time it runs.
- The project has no database, user accounts, authentication, rate limiting or persistent conversation memory.
- Expected invalid searches return result messages rather than formal MCP error objects.

During development, the most important errors to check were an incorrect path to `data/topics.json`, accidentally bypassing MCP by importing server functions directly, and writing debug output to stdout while using stdio.

## Reflection

### What problem does MCP solve?

MCP provides a standard connection between AI applications and external capabilities. Without it, every application and data source would need a custom integration. MCP lets a client discover and call tools or read resources through a consistent protocol.

### What is the difference between an MCP tool and an MCP resource?

A tool is called with input to perform an operation or computation. A resource exposes readable data at a URI. In this project, topic searching and exact lookup are tools, while the topic catalogue is a read-only resource.

### What does this MCP server expose?

The server exposes `search_topics`, `get_topic_details` and the `topics://catalog` resource. These capabilities use the five records in `data/topics.json`.

### How does the agent use the MCP server?

The agent starts an MCP client connection over stdio. It calls `search_topics` to discover a candidate, then calls `get_topic_details` with the selected id. It formats only the returned topic data into a short study recommendation and saves the answer as Markdown.

### What should be checked before using a third-party MCP server?

Check who published it, whether it runs locally or remotely, which tools and resources it exposes, which files or systems it can access, which credentials it requires, whether it can modify data, and whether its permissions can be restricted. Its documentation and source should be reviewed before granting access.

### What limitation was observed in this implementation?

The clearest limitation is the small dataset combined with literal substring search. A reasonable question can fail simply because the requested topic or wording is not present. For example, the supplied dataset has no decorators topic, so the agent must report that no match exists rather than inventing an answer.

## Git Validation, Commit and Push

```bash
cd ~/mcp-intro
source .venv/bin/activate

python -m json.tool data/topics.json > /dev/null
python -m py_compile \
    server/learning_server.py \
    client/mcp_client.py \
    client/test_server.py \
    client/agent.py
python client/test_server.py
python client/agent.py "I want to study Python functions. What should I review first?"

git remote -v
git status
git add README.md
git commit -m "Complete MCP project documentation"
git push origin main
```

## Self-Validation

### Cumulative Project

- [x] Tasks 0–10 are documented as complete.
- [x] The project structure is documented.
- [x] The JSON dataset contains five valid topic records.
- [x] The FastMCP server has a script entry point.
- [x] `search_topics` is exposed through MCP.
- [x] `get_topic_details` is exposed through MCP.
- [x] `topics://catalog` is exposed as a read-only resource.
- [x] The direct MCP integration test checks tools, errors and the resource.
- [x] The agent calls both tools through MCP rather than direct imports.
- [x] A real sample response is saved in the output directory.
- [x] A third-party MCP server and its risks are reviewed.

### Task 10 — Complete Documentation and Reflection

- [x] `README.md` includes all required sections.
- [x] `README.md` explains what the server does.
- [x] `README.md` explains how to run the server.
- [x] `README.md` explains how to test the server.
- [x] `README.md` explains how to run the agent.
- [x] `README.md` lists the available tools.
- [x] `README.md` lists the available resources.
- [x] `README.md` includes the third-party MCP server review.
- [x] `README.md` includes one example output.
- [x] `README.md` includes known limitations.
- [x] `README.md` includes a reflection answering every required question.
- [x] No secrets are included.
