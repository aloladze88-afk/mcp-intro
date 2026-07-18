# Programming Learning MCP Server

This project will demonstrate how a Python MCP server can expose
programming-study tools and resources to a client or AI agent.

## Task 0 status

The initial project structure has been created.

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

- `server/`: the MCP server, tools, and resources.
- `client/`: the MCP client and agent.
- `data/`: local programming-topic data.
- `output/`: generated example responses.
- `requirements.txt`: Python dependencies.
- `.env.example`: example environment variables.
- `.gitignore`: files Git must not commit.

## MCP Architecture Summary

MCP, or the Model Context Protocol, is a standard way for an AI application to connect to external tools and information without requiring a different custom integration for every system.

The main parts are:

- **MCP host:** the main AI application. It manages the conversation, the AI model, permissions, and connections to MCP servers.
- **MCP client:** the connection component created by the host. Each client normally connects to one MCP server and sends requests between the host and that server.
- **MCP server:** a separate program that provides specific capabilities, such as searching programming topics or reading a topic catalogue.
- **Tools:** functions that perform an operation or return a calculated result. For example, `search_topics("decorators")` could search the dataset.
- **Resources:** read-only information that the client can retrieve. For example, a resource could provide the complete programming-topic catalogue.

A simple flow in this project is:

```text
Student asks a question
        ↓
MCP host runs the AI application
        ↓
MCP client sends a request
        ↓
MCP server uses a tool or provides a resource
        ↓
The result returns to the AI application
```

A server should expose only the capabilities it genuinely needs. This keeps the server simpler, reduces mistakes, and limits access to files, data, or actions that are not required.

### What to remember

- The **host** manages the complete AI experience.
- The **client** connects the host to one server.
- The **server** provides focused capabilities.
- A **tool does something**.
- A **resource provides information to read**.
- Limiting server capabilities improves clarity and safety.

### Real-world example

A company support assistant could connect to a documentation MCP server. The server could provide a resource containing product manuals and a tool for searching them. The assistant could then answer a customer’s question without receiving access to unrelated company files.

### Task 1 self-validation

- [x] I explained what MCP is.
- [x] I explained the role of an MCP host.
- [x] I explained the role of an MCP client.
- [x] I explained the role of an MCP server.
- [x] I explained the difference between tools and resources.
- [x] I used my own words.

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Current test

Run the starter files:

```bash
python server/learning_server.py
python client/mcp_client.py
python client/agent.py
```

These files currently confirm that the structure exists. The real MCP
implementation belongs to later tasks.

## Self-validation

- [x] Required project directories created.
- [x] MCP server file created.
- [x] Client and agent files created.
- [x] Data directory created.
- [x] `README.md` created.
- [x] `requirements.txt` created.
- [x] `.env.example` created.
- [x] `.gitignore` created.
- [x] `.env` excluded from Git.
- [x] Virtual-environment directories excluded from Git.
- [x] Server code kept separate from client and agent code.
