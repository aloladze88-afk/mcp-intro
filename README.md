# MCP Servers in Python: Tools, Resources, and Agent Integration

## Description

This beginner project demonstrates how to build a small Model Context Protocol (MCP) server in Python, expose local learning data, connect through an MCP client, and later integrate the server with an AI agent.

## Project Status

- Task 0 — Project structure: complete
- Task 1 — MCP architecture explanation: complete
- Task 2 — Basic FastMCP server: complete
- Task 3 — Local topic dataset: complete
- Task 4 — First MCP tool: complete
- Task 5 — Topic details tool: complete
- Task 6 — Read-only topic catalogue resource: complete

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

The server is created in `server/learning_server.py`. `FastMCP(...)` creates the server, while `mcp.run()` starts it. The `if __name__ == "__main__":` condition means the server starts when this file is run directly.

FastMCP uses standard input and output, called stdio, by default. Ordinary debug messages should not be printed to stdout because they can interfere with MCP communication.

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

The file uses a top-level `topics` list so the MCP server can load and search the records.

## First MCP Tool: `search_topics`

The server exposes a tool named `search_topics` using the `@mcp.tool` decorator.

The tool:

- receives a `query` string;
- reads `data/topics.json`;
- searches topic titles and key concepts;
- ignores differences between uppercase and lowercase letters;
- returns at most three compact matches;
- returns each match's `id`, `title`, `summary`, `prerequisites` and `key_concepts`;
- returns a clear message when the query is blank or nothing matches.

The tool is deterministic: the same dataset and query produce the same result. It does not use an AI model, external API or random value.

Example searches:

```text
functions
methods
exception
```

A search for `functions` returns the Python Functions topic. A search for `methods` can return Lists, Dictionaries and Classes because those topics contain that key concept.

## Topic Details Tool: `get_topic_details`

The server now also exposes `get_topic_details`.

The tool:

- receives one exact topic id;
- reads the same local topic dataset;
- compares ids without case sensitivity;
- returns the complete matching topic record;
- returns a clear message for a blank or unknown id.

This creates a common two-step MCP workflow:

```text
1. search_topics discovers possible topics.
2. get_topic_details retrieves the complete selected topic.
```

Example valid id:

```text
python-functions
```

The returned dictionary includes the topic's id, title, summary, prerequisites, key concepts, common mistakes and practice idea.

## Read-Only Resource: `topics://catalog`

The server exposes a resource at `topics://catalog` using the `@mcp.resource` decorator.

The resource:

- reads the existing topic dataset;
- returns only each topic's `id` and `title`;
- serialises the catalogue with `json.dumps()`;
- returns an `application/json` response;
- does not create, edit or delete any data.

Example returned data:

```json
[
  {"id": "python-functions", "title": "Python Functions"},
  {"id": "python-lists", "title": "Python Lists"}
]
```

## Concepts to Remember

- A summary tool helps discover possible results.
- A details tool retrieves one complete record.
- Stable ids are safer for exact lookup than titles because titles can change or contain different capitalisation.
- `.strip()` removes accidental spaces around input.
- `.casefold()` makes text comparison case-insensitive.
- Returning an error dictionary is safer for an MCP client than allowing an expected lookup failure to crash the tool.
- Tools perform actions or lookups, while resources expose readable data.
- A resource URI gives clients a stable address for the data.
- Read-only resources should not modify files, records or application state.
- `json.dumps()` converts Python data into a JSON string.

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

Check the number of topics:

```bash
python -c "import json; data=json.load(open('data/topics.json')); print(len(data['topics']))"
```

Expected result:

```text
5
```

## Validate the Python Server

```bash
cd ~/mcp-intro
python -m py_compile server/learning_server.py
```

No output means the file compiled successfully.

Start the server:

```bash
python server/learning_server.py
```

The server should start and wait for MCP communication. Stop it with `Ctrl+C`.

## Test the MCP Tools

Open the FastMCP development interface:

```bash
cd ~/mcp-intro
source .venv/bin/activate
fastmcp dev server/learning_server.py
```

Test `search_topics` with:

```text
functions
methods
networking
```

Test `get_topic_details` with:

```text
python-functions
PYTHON-LISTS
unknown-topic
```

Also test it with a blank value. Valid ids should return complete topic records. Unknown and blank ids should return clear messages instead of crashing.

List the registered resource:

```bash
fastmcp list server/learning_server.py --resources
```

Read `topics://catalog` from an MCP client or the FastMCP development interface. It should return valid JSON containing exactly the five available topic ids and titles.

## Git Validation, Commit and Push

```bash
cd ~/mcp-intro
source .venv/bin/activate

python -m json.tool data/topics.json > /dev/null
python -m py_compile server/learning_server.py client/mcp_client.py client/agent.py
fastmcp list server/learning_server.py --resources

git remote -v
git status
git add server/learning_server.py README.md
git commit -m "Add read-only topic catalogue resource"
git push origin main
```

## Real-World Use Case

A learning application first reads `topics://catalog` to build a simple topic menu. After the student chooses a topic id, the application calls `get_topic_details` to retrieve the complete learning information.

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

### Task 4 — First MCP Tool

- [x] I implemented the `search_topics` tool.
- [x] The tool receives a query string.
- [x] The tool reads from `data/topics.json`.
- [x] The tool searches topic titles and key concepts.
- [x] The tool returns matching topic information.
- [x] The tool limits the result to a small number of matches.
- [x] The tool handles blank and no-match queries clearly.
- [x] The tool has a clear docstring.
- [x] The tool is deterministic.

### Task 5 — Topic Details Tool

- [x] I implemented the `get_topic_details` tool.
- [x] The tool receives a topic id.
- [x] The tool returns the full topic information.
- [x] The tool handles a blank id clearly.
- [x] The tool handles unknown ids clearly.
- [x] The tool has a clear docstring.
- [x] The lookup uses stable topic ids instead of titles.
- [x] The tool does not crash for expected invalid lookup values.


### Task 6 — Read-Only MCP Resource

- [x] I implemented a read-only MCP resource.
- [x] The resource has the clear URI `topics://catalog`.
- [x] The resource returns the available topic ids and titles.
- [x] The resource returns a JSON string produced by `json.dumps()`.
- [x] The resource does not modify files or data.
- [x] The resource has a clear docstring.
- [x] The resource returns only the information needed to browse the catalogue.
