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
- Task 7 — Direct MCP server testing: complete
- Task 8 — Simple MCP-connected agent: complete
- Task 9 — Third-party MCP server review: complete

## Project Structure

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

## Direct Server Test: `client/test_server.py`

Task 7 adds a small FastMCP client that connects to the local server through
stdio and tests it before any agent is involved.

The script verifies that:

- the server starts and responds to a ping;
- `search_topics` and `get_topic_details` are listed;
- `search_topics` returns a valid match;
- `get_topic_details` returns a complete topic record;
- blank and unknown inputs return understandable messages;
- `topics://catalog` is listed and can be read;
- the catalogue contains five ids and titles.

Run the direct integration test:

```bash
cd ~/mcp-intro
source .venv/bin/activate
python client/test_server.py
```

Sample successful output:

```text
[PASS] Server started and responded to ping.
[PASS] Tools are visible: ['get_topic_details', 'search_topics']
[PASS] search_topics returned: Python Functions
[PASS] get_topic_details returned the full record for: Python Functions
[PASS] Resource is visible: topics://catalog
[PASS] Catalogue resource returned 5 topics.
All MCP server tests passed.
```

## Simple MCP-Connected Agent: `client/agent.py`

Task 8 adds a deterministic agent-like client. It connects to the MCP server
through FastMCP's stdio client and never imports the server tools directly.

The program:

- receives a programming topic or student question;
- extracts useful search terms from the question;
- calls `search_topics` through MCP;
- selects the first relevant topic returned by the server;
- calls `get_topic_details` through MCP;
- formats a short student-facing Markdown answer;
- saves the answer in `output/sample_agent_response.md`;
- clearly reports when the local dataset has no matching topic.

Interaction flow:

```text
Student question
        ↓
client/agent.py
        ↓
FastMCP Client over stdio
        ↓
Programming Learning Server
        ↓
search_topics → get_topic_details
        ↓
data/topics.json
```

Run the agent with a question:

```bash
cd ~/mcp-intro
source .venv/bin/activate
python client/agent.py "I want to study Python functions. What should I review first?"
```

You can also run it without an argument and enter a question when prompted:

```bash
python client/agent.py
```

A successful response contains the recommended topic, its relevance,
prerequisites, key concepts, practice idea and common mistakes. The response is
also written to `output/sample_agent_response.md`.

Sample result:

```text
Recommended topic: Python Functions
Prerequisites: Variables; Basic Python syntax
Key concepts: Defining functions; Parameters and arguments; Return values
Practice idea: Create a function that receives two numbers and returns their total.
```

A question about an unavailable topic, such as Python decorators, produces a
clear no-match response instead of inventing information.

## Third-Party MCP Server Review: Filesystem Server

For Task 9, I reviewed the official reference **Filesystem MCP Server** from
the `modelcontextprotocol/servers` repository. I inspected its README, tool
list, access-control explanation and local configuration example. I did not
grant it access to personal files.

### What the server does

The server exposes controlled filesystem operations to an MCP client. It can
read files, inspect directories and metadata, search files, create directories,
write or edit files, and move files or directories.

### Where it runs

It runs **locally** as a Node.js process and normally communicates with the MCP
client through stdio. It can be started with `npx` or Docker.

### Exposed capabilities

The documented tools include:

- `read_text_file`, `read_media_file` and `read_multiple_files`;
- `list_directory`, `list_directory_with_sizes` and `directory_tree`;
- `search_files` and `get_file_info`;
- `create_directory`, `write_file`, `edit_file` and `move_file`;
- `list_allowed_directories`.

The reviewed documentation describes tools rather than MCP resources.

### Permissions and credentials

The server does not require an API key or personal account credential. It does
require explicit directory access. The allowed directories are supplied as
command-line arguments or through MCP Roots. The process runs with the current
user's filesystem permissions inside those allowed directories.

A deliberately restricted example would be:

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

### Risk

If the server is given access to a broad directory such as the home folder, an
AI application could read sensitive files or overwrite, edit or move important
files. The `write_file`, `edit_file` and `move_file` tools can change data.

### Safety measure

I would create a dedicated test directory containing only disposable files and
grant access only to that directory. I would inspect the allowed directories
with `list_allowed_directories`, use dry-run mode before edits, and prefer a
read-only Docker mount when write access is unnecessary. I would never expose
the entire home directory, SSH keys, browser profiles, password stores or
project secrets.

### Sources reviewed

- Filesystem server README: `https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem`
- MCP local-server guide: `https://modelcontextprotocol.io/docs/develop/connect-local-servers`

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
- Testing the server directly separates MCP problems from later agent problems.
- A FastMCP `Client` can start a local Python server through stdio.
- Assertions make a test stop immediately when an expected result is missing.
- An agent-like client can be deterministic; an LLM is not required.
- Calling tools through `Client` proves that MCP is being used.
- Importing server tool functions directly would bypass MCP and fail the task.
- Tool results should be treated as the source of topic-specific information.
- Third-party MCP servers should be inspected before they are installed or connected.
- Filesystem access should be limited to the smallest safe directory.

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
python -m py_compile server/learning_server.py client/test_server.py client/agent.py
```

No output means the file compiled successfully.

Start the server:

```bash
python server/learning_server.py
```

The server should start and wait for MCP communication. Stop it with `Ctrl+C`.

## Test the MCP Server Directly

Run the cumulative FastMCP client test:

```bash
cd ~/mcp-intro
source .venv/bin/activate
python client/test_server.py
```

This one command starts the server through stdio, lists its tools and
resources, calls both tools, checks invalid inputs and reads the catalogue.

You can also inspect the server manually with the FastMCP development
interface:

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

## Run and Validate the Agent

```bash
cd ~/mcp-intro
source .venv/bin/activate

python client/agent.py "I want to study Python functions. What should I review first?"
cat output/sample_agent_response.md
```

Test the no-match behaviour:

```bash
python client/agent.py "I want to study Python decorators. What should I review first?"
```

The first command should call both MCP tools and save a complete recommendation.
The second command should explain that no matching local topic was found.

## Git Validation, Commit and Push

```bash
cd ~/mcp-intro
source .venv/bin/activate

python -m json.tool data/topics.json > /dev/null
python -m py_compile server/learning_server.py client/mcp_client.py client/agent.py client/test_server.py
python client/test_server.py
python client/agent.py "I want to study Python functions. What should I review first?"

git remote -v
git status
git add client/agent.py output/sample_agent_response.md README.md
git commit -m "Connect simple agent to MCP server"
git push origin main
```

## Real-World Use Case

A student asks what to review before learning Python functions. The agent-like
client calls the MCP server, retrieves the complete Functions topic and creates
a concise study recommendation without reading the dataset or importing the
server functions directly.

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


### Task 7 — Direct MCP Server Testing

- [x] I tested that the MCP server starts.
- [x] I verified that the tools are visible.
- [x] I tested `search_topics` with a valid query.
- [x] I tested `get_topic_details` with a valid topic id.
- [x] I tested blank and unknown invalid inputs.
- [x] I tested that the catalogue resource is visible.
- [x] I read and validated `topics://catalog`.
- [x] I documented how to run the server test.
- [x] I included sample successful output.

### Task 8 — Simple MCP-Connected Agent

- [x] I created `client/agent.py`.
- [x] The agent receives a topic or student question.
- [x] The agent connects to the server through a FastMCP client.
- [x] The agent calls `search_topics` through MCP.
- [x] The agent calls `get_topic_details` through MCP.
- [x] The agent does not import the MCP server functions directly.
- [x] The final response uses data returned by the MCP server.
- [x] The response includes the recommended topic when available.
- [x] The response includes relevance, prerequisites and key concepts.
- [x] The response includes a practice idea and common mistakes.
- [x] A no-match result is stated clearly.
- [x] I saved a real sample response in `output/sample_agent_response.md`.
- [x] I documented how to run and validate the agent.

### Task 9 — Third-Party MCP Server Review

- [x] I selected one third-party MCP server.
- [x] I described what the server does.
- [x] I identified that it runs locally.
- [x] I identified the tools it exposes.
- [x] I identified its required filesystem permissions.
- [x] I confirmed that it does not require personal credentials.
- [x] I described the risk of broad read and write access.
- [x] I described a restricted-directory safety measure.
- [x] I documented the review in `README.md`.
