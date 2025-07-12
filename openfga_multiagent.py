import os
import asyncio
import json
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List

import aiohttp
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition

# ──────────────────────────────────────────────────────────────────────────────
# 1. Configuration
# ──────────────────────────────────────────────────────────────────────────────
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
STORE_ID = os.getenv("FGA_STORE_ID")
MODEL_ID = os.getenv("FGA_MODEL_ID")
FGA_BASE = os.getenv("FGA_BASE")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0, # Set to 0 for more predictable tool usage
    api_key=GEMINI_KEY
)

client = MultiServerMCPClient({
    "filesystem": {
        "command": "docker", "args": [
            "run", "-i", "--rm",
            # Add the -w flag to set the working directory
            "-w", "/projects", 
            "--mount", f"type=bind,src={os.getcwd()},dst=/projects",
            "mcp/filesystem", "/projects"
        ], "transport": "stdio"
    },
    "git": {
        "command": "python", "args": ["-m", "mcp_server_git", "--repository", os.getcwd()],
        "transport": "stdio"
    },
    "chroma": {
        "command": "chroma-mcp-server", "args": ["--client-type", "persistent", "--data-dir", "./my_data"],
        "transport": "stdio"
    }
})

# ──────────────────────────────────────────────────────────────────────────────
# 2. OpenFGA Authorization
# ──────────────────────────────────────────────────────────────────────────────
async def check_permission(user: str, relation: str, object_ref: str) -> bool:
    """Check permission using OpenFGA API. Object format is 'type:id'."""
    url = f"{FGA_BASE}/stores/{STORE_ID}/check"
    payload = {"tuple_key": {"user": user, "relation": relation, "object": object_ref}}
    headers = {"Authorization-Model-Id": MODEL_ID} if MODEL_ID else {}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(data)
                    allowed = data.get("allowed", False)
                    print(f"🔐 PERM CHECK: {user} -> {relation} on {object_ref}? {'✅ ALLOWED' if allowed else '❌ DENIED'}")
                    return allowed
                print(f"FGA API Error: {resp.status} - {await resp.text()}")
                return False
    except Exception as e:
        print(f"FGA Connection Error: {e}")
        return False

# ──────────────────────────────────────────────────────────────────────────────
# 3. Tool Definitions
# ──────────────────────────────────────────────────────────────────────────────
@tool
async def read_file(path: str) -> str:
    """Read a file's content from the project directory."""
    try:
        t = next(t for t in await client.get_tools() if t.name == "read_file")
        return await t.ainvoke({"path": path})
    except Exception as e:
        return f"Error reading file: {e}"

@tool
async def write_file(path: str, content: str) -> str:
    """Write content to a file in the project directory."""
    try:
        t = next(t for t in await client.get_tools() if t.name == "write_file")
        await t.ainvoke({"path": path, "content": content})
        return "✅ File written successfully."
    except Exception as e:
        return f"Error writing file: {e}"

@tool
async def git_status(repo_path: str = os.getcwd()) -> str:
    """Get the git status of the project repository."""
    try:
        t = next(t for t in await client.get_tools() if t.name == "git_status")
        return await t.ainvoke({"repo_path": repo_path})
    except Exception as e:
        return f"Error getting git status: {e}"

@tool
async def chroma_list_collections() -> str:
    """List all collections in the ChromaDB instance."""
    try:
        t = next(t for t in await client.get_tools() if t.name == "chroma_list_collections")
        res = await t.ainvoke({})
        return f"Collections: {res.get('collection_names', []) if isinstance(res, dict) else res}"
    except Exception as e:
        return f"Error listing collections: {e}"

# ──────────────────────────────────────────────────────────────────────────────
# 4. State and Agent Setup
# ──────────────────────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_id: str

all_tools = [read_file, write_file, git_status, chroma_list_collections]
# Bind tools to the LLM so it knows how to call them
llm_with_tools = llm.bind_tools(all_tools)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Graph Nodes with Explicit Logic
# ──────────────────────────────────────────────────────────────────────────────
async def agent_node(state: AgentState) -> dict:
    """Calls the LLM to decide the next action."""
    print("🤖 Agent Node: Deciding next action...")
    response = await llm_with_tools.ainvoke(state["messages"])
    print(f"🧠 LLM Response: {response.content}")
    if response.tool_calls:
        print(f"🛠️ LLM decided to call tools: {[tc['name'] for tc in response.tool_calls]}")
    return {"messages": [response]}

async def tools_node(state: AgentState) -> dict:
    """The custom tool node that performs authorization before execution."""
    print("\n🔧 Tools Node: Executing tools with authorization...")
    last_message = state["messages"][-1]
    user_id = state["user_id"]
    
    if not last_message.tool_calls:
        return {}

    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_call_id = tool_call["id"]
        name = tool_call["name"]
        args = tool_call["args"]
        result = ""
        
        try:
            if name == "read_file":
                path = args.get("path", "")
                # FIX: Align the object reference with the path inside the Docker container
                object_ref = f"file:/projects/{path}"
                if await check_permission(user_id, "reader", object_ref):
                    result = await read_file.ainvoke(args)
                else:
                    result = f"Permission denied to read file: {path}"
                    
            elif name == "write_file":
                path = args.get("path", "")
                content = args.get("content", "")
                # FIX: Align the object reference with the path inside the Docker container
                object_ref = f"file:/projects/{path}"
                if await check_permission(user_id, "writer", object_ref):
                    # Pass args dictionary to the tool
                    result = await write_file.ainvoke({"path": path, "content": content})
                else:
                    result = f"Permission denied to write file: {path}"

            elif name == "git_status":
                repo_path = args.get("repo_path", os.getcwd())
                # This check is correct as it uses the full, absolute host path
                if await check_permission(user_id, "status_checker", f"git_repo:{repo_path}"):
                    result = await git_status.ainvoke(args)
                else:
                    result = "Permission denied to check git status."

            elif name == "chroma_list_collections":
                # This check is correct
                if await check_permission(user_id, "collection_lister", "chroma_instance:default"):
                    result = await chroma_list_collections.ainvoke(args)
                else:
                    result = "Permission denied to list Chroma collections."
            else:
                result = f"Unknown tool: {name}"
        except Exception as e:
            result = f"Error executing {name}: {e}"



        print(f"📤 Tool '{name}' Result: {result}")
        tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call_id))
    
    return {"messages": tool_messages}

# ──────────────────────────────────────────────────────────────────────────────
# 6. Graph Construction and Execution
# ──────────────────────────────────────────────────────────────────────────────
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tools_node)
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "agent")
app = graph_builder.compile()
app.get_graph().print_ascii()

async def main():
    print("🚀 Starting LangGraph Agent with OpenFGA...")
    
    initial_state = {
        "messages": [{
            "role": "user",
            "content": (
                "First, please generate a brief, one-paragraph explanation of what the 'artificial intelligence' is. "
                "Then, write that explanation into the file named 'readme.md'. "
                "After you have written the file, show the git status for the repository. "
                "Finally, try to list the chroma collections."
            )
        }],
        "user_id": "user:agent"
    }

    
    print("\n" + "="*50)
    async for event in app.astream(initial_state, config={"recursion_limit": 50}):
        for key, value in event.items():
            print(f"--- Event: {key} ---")
            print(value)
            print("\n")
    print("="*50 + "\n🏁 Workflow Finished.")

if __name__ == "__main__":
    # Ensure your OpenFGA server is running and you have set up the
    # required tuples/permissions for 'user:agent' before running.
    asyncio.run(main())
