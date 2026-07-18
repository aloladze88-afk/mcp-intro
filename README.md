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
