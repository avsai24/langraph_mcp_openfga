# Secure AI Agent System: Integrating OpenFGA with MCP and LangGraph

Welcome! This guide explains, in clear and simple terms, how to connect OpenFGA authorization to an AI agent system built with LangGraph and MCP tools. Whether you have a single agent, multiple agents, or several MCP servers, this README will help you understand the architecture and steps—no coding background required.

## What Is This System?

- **LangGraph**: A framework that lets you build smart AI agents that can reason, plan, and use tools.
- **MCP (Model Context Protocol) Client**: Connects your agent(s) to real-world tools like file systems, git, or databases, running each tool in a safe, separate environment.
- **OpenFGA**: A security system that acts as a “gatekeeper,” deciding what each agent is allowed to do, based on easy-to-manage permission rules.

## Why Use This Setup?

- **Security**: Every action by an agent is checked against your rules before it happens.
- **Flexibility**: Works with one or many agents, and one or many tool servers.
- **Transparency**: You can see and control exactly who can do what.

## How Does It Work? (Big Picture)

1. **You give an instruction** (like “read a file, then write a summary”).
2. **The agent thinks** about the steps needed.
3. **Before using any tool**, the agent asks OpenFGA: “Am I allowed to do this?”
4. **If allowed**, the action happens. If not, it’s blocked.
5. **You get a clear report** of what worked and what was denied.

## Key Components and Files

| File/Config           | What It Does                                                      |
|-----------------------|-------------------------------------------------------------------|
| `openfga_multiagent.py` | The main script that runs your agent(s) and connects everything. |
| `.env`                | Stores your secret keys and OpenFGA IDs.                          |
| `auth-model.fga`      | Human-readable file describing your permission rules.              |
| `model.json`          | Machine-readable version of your rules for OpenFGA.               |
| `tuples.json`         | The actual permissions (who can do what) for OpenFGA.             |
| `readme.md`           | This guide!                                                       |

## Step-by-Step Setup

### 1. Prepare Your Environment

- Make sure you have Docker installed (for tool isolation).
- Install the OpenFGA server (usually via Docker).
- Install the OpenFGA CLI (for setup commands).
- Clone or download the project files.

### 2. Start OpenFGA

```sh
docker run -p 8080:8080 openfga/openfga run
```

### 3. Create a Store in OpenFGA

- Use the CLI or API to create a store.
- Save the store ID for later.

### 4. Upload Your Authorization Model

- Upload `model.json` to your store:
  ```sh
  curl -X POST http://localhost:8080/stores//authorization-models \
    -H "Content-Type: application/json" \
    -d @model.json
  ```
- Note the returned `authorization_model_id`.

### 5. Add Permission Tuples

- Upload `tuples.json` to your store:
  ```sh
  curl -X POST http://localhost:8080/stores//write \
    -H "Content-Type: application/json" \
    -H "Authorization-Model-Id: " \
    -d @tuples.json
  ```

### 6. Configure Your `.env` File

Fill in your keys and IDs:

```env
GEMINI_API_KEY="your-gemini-api-key"
FGA_STORE_ID=""
FGA_MODEL_ID=""
```

### 7. Run the Agent System

```sh
python openfga_multiagent.py
```

## How It Handles Multiple Agents and MCP Servers

- **Multiple Agents**: Each agent can have its own user ID. OpenFGA rules can be set per agent, so you control what each one can do.
- **Multiple MCP Servers**: You can add more tool servers in the configuration. Each tool (filesystem, git, chroma, etc.) is isolated and checked separately.
- **All Permissions Centralized**: No matter how many agents or servers, OpenFGA is the single source of truth for permissions.

## Example: What Happens During Execution

1. **Agent receives your instruction** (e.g., “Summarize a file, write the summary, check git status”).
2. **Agent plans the steps** (read, summarize, write, git status).
3. **Before each tool use**, the agent checks with OpenFGA if it’s allowed.
4. **If allowed**, the tool runs (e.g., reads file, writes summary).
5. **If not allowed**, the agent reports “Permission denied.”
6. **Final report**: You see what was done, and what was blocked.

## Frequently Asked Questions

**Q: Can I add or remove agents or tools later?**  
A: Yes! Just update your OpenFGA tuples and configuration.

**Q: What if I want some agents to have more permissions than others?**  
A: Assign different permissions in `tuples.json` for each agent.

**Q: Does this work if I add more tool servers?**  
A: Yes. Just add them to the MCP client config and set up permissions in OpenFGA.

**Q: Do I need to restart everything if I change permissions?**  
A: No. OpenFGA changes take effect immediately.

## Troubleshooting

- **Permission denied for allowed action?**
  - Check that the path in your tuple matches the tool’s internal path (e.g., `/projects/readme.md`).
  - Ensure the agent’s user ID matches the one in the tuple.
  - Confirm your `.env` has the correct `FGA_STORE_ID` and `FGA_MODEL_ID`.

- **Tool says “not allowed directory”?**
  - Make sure the Docker container’s working directory and mount match the path in your permission.

- **ChromaDB access is always denied?**
  - You must explicitly grant `collection_lister` permission in a tuple for that agent.

## Summary Table: What You Control

| What You Want To Do                         | Where To Set It           |
|---------------------------------------------|---------------------------|
| Add a new agent                             | Add a tuple in `tuples.json` |
| Grant/restrict tool access                  | Edit `tuples.json` and re-upload |
| Add a new tool server                       | Update MCP config in Python script |
| Change permission rules                     | Edit `auth-model.fga`/`model.json` and re-upload |
| Change API keys or IDs                      | Edit `.env` file          |

## Final Notes

- **No code changes are needed to change permissions**—just update OpenFGA.
- **You can safely experiment**: If you make a mistake, just update the tuples or model and try again.
- **This setup is secure by default**: If a permission is missing, the action is blocked.

**Congratulations!**  
You now have a secure, modular, and easy-to-manage AI agent system with centralized authorization.  
If you follow this guide, you can confidently add agents, tools, and permissions as your needs grow—no deep programming required.
