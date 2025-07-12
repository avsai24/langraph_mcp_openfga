(.venv) (base) venkatasaiancha@Mac langgraph_mcp % python openfga_multiagent.py
        +-----------+         
        | __start__ |         
        +-----------+         
               *              
               *              
               *              
          +-------+           
          | agent |           
          +-------+*          
          .         *         
        ..           **       
       .               *      
+---------+         +-------+ 
| __end__ |         | tools | 
+---------+         +-------+ 
🚀 Starting LangGraph Agent with OpenFGA...

==================================================
🤖 Agent Node: Deciding next action...
🧠 LLM Response: Artificial intelligence (AI) is a broad field encompassing the development of computer systems capable of performing tasks that typically require human intelligence.  These tasks include learning, reasoning, problem-solving, perception, and natural language understanding. AI systems achieve this through various techniques, such as machine learning, deep learning, and natural language processing, enabling them to analyze data, identify patterns, and make predictions or decisions.  The goal of AI is to create intelligent agents that can interact with the world and solve complex problems autonomously.
🛠️ LLM decided to call tools: ['write_file', 'git_status', 'chroma_list_collections']
--- Event: agent ---
{'messages': [AIMessage(content='Artificial intelligence (AI) is a broad field encompassing the development of computer systems capable of performing tasks that typically require human intelligence.  These tasks include learning, reasoning, problem-solving, perception, and natural language understanding. AI systems achieve this through various techniques, such as machine learning, deep learning, and natural language processing, enabling them to analyze data, identify patterns, and make predictions or decisions.  The goal of AI is to create intelligent agents that can interact with the world and solve complex problems autonomously.', additional_kwargs={'function_call': {'name': 'chroma_list_collections', 'arguments': '{}'}}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'safety_ratings': []}, id='run--d56b57f4-d966-4038-bdd1-e74f9c94d8b1-0', tool_calls=[{'name': 'write_file', 'args': {'content': 'Artificial intelligence (AI) is a broad field encompassing the development of computer systems capable of performing tasks that typically require human intelligence.  These tasks include learning, reasoning, problem-solving, perception, and natural language understanding. AI systems achieve this through various techniques, such as machine learning, deep learning, and natural language processing, enabling them to analyze data, identify patterns, and make predictions or decisions.  The goal of AI is to create intelligent agents that can interact with the world and solve complex problems autonomously.', 'path': 'readme.md'}, 'id': '8fd50e1c-163a-468d-9234-4a4feaa3ef9f', 'type': 'tool_call'}, {'name': 'git_status', 'args': {}, 'id': '652b7259-4e68-491a-8c17-bcdeea2b3c14', 'type': 'tool_call'}, {'name': 'chroma_list_collections', 'args': {}, 'id': 'a202d518-4263-4aad-8ff3-0cf8e0fa051c', 'type': 'tool_call'}], usage_metadata={'input_tokens': 129, 'output_tokens': 224, 'total_tokens': 353, 'input_token_details': {'cache_read': 0}})]}



🔧 Tools Node: Executing tools with authorization...
{'allowed': True, 'resolution': ''}
🔐 PERM CHECK: user:agent -> writer on file:/projects/readme.md? ✅ ALLOWED
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1752290290.690028 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
I0000 00:00:1752290290.695787 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
I0000 00:00:1752290290.698890 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
Secure MCP Filesystem Server running on stdio
Allowed directories: [ '/projects' ]
2025-07-11 22:18:12,032 | chromamcp.unconfigured | WARNING | Logger requested before main configuration.
Starting server in default (HTTP) mode...
SERVER: Calling asyncio.run(run_server())...
SERVER: Attempting to enter stdio_server context...
SERVER: Entered stdio_server context. Attempting server.run...
I0000 00:00:1752290292.142756 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
Secure MCP Filesystem Server running on stdio
Allowed directories: [ '/projects' ]
📤 Tool 'write_file' Result: ✅ File written successfully.
{'allowed': True, 'resolution': ''}
🔐 PERM CHECK: user:agent -> status_checker on git_repo:/Users/venkatasaiancha/Documents/captenai/langgraph_mcp? ✅ ALLOWED
I0000 00:00:1752290292.417710 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
I0000 00:00:1752290292.424209 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
I0000 00:00:1752290292.428876 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
Secure MCP Filesystem Server running on stdio
Allowed directories: [ '/projects' ]
2025-07-11 22:18:13,552 | chromamcp.unconfigured | WARNING | Logger requested before main configuration.
Starting server in default (HTTP) mode...
SERVER: Calling asyncio.run(run_server())...
SERVER: Attempting to enter stdio_server context...
SERVER: Entered stdio_server context. Attempting server.run...
I0000 00:00:1752290293.601251 3725077 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers
📤 Tool 'git_status' Result: Repository status:
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env
        .gitignore
        auth-model.fga
        chroma-mcp/
        logs/
        main.py
        mcp/
        model.json
        multi_agent.py
        my_data/
        openfga_multiagent.py
        readme.md
        requirements.txt
        servers/
        test_chromadb.py
        tuples.json

nothing added to commit but untracked files present (use "git add" to track)
{'allowed': False, 'resolution': ''}
🔐 PERM CHECK: user:agent -> collection_lister on chroma_instance:default? ❌ DENIED
📤 Tool 'chroma_list_collections' Result: Permission denied to list Chroma collections.
--- Event: tools ---
{'messages': [ToolMessage(content='✅ File written successfully.', id='1cd015e6-bc25-47d3-94d4-ad3c6cd8d861', tool_call_id='8fd50e1c-163a-468d-9234-4a4feaa3ef9f'), ToolMessage(content='Repository status:\nOn branch master\n\nNo commits yet\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\t.env\n\t.gitignore\n\tauth-model.fga\n\tchroma-mcp/\n\tlogs/\n\tmain.py\n\tmcp/\n\tmodel.json\n\tmulti_agent.py\n\tmy_data/\n\topenfga_multiagent.py\n\treadme.md\n\trequirements.txt\n\tservers/\n\ttest_chromadb.py\n\ttuples.json\n\nnothing added to commit but untracked files present (use "git add" to track)', id='1546af37-46ff-453c-8b01-cee23da0fd56', tool_call_id='652b7259-4e68-491a-8c17-bcdeea2b3c14'), ToolMessage(content='Permission denied to list Chroma collections.', id='7e03a57d-f229-4da9-ab7c-c3baa6b36487', tool_call_id='a202d518-4263-4aad-8ff3-0cf8e0fa051c')]}


🤖 Agent Node: Deciding next action...
🧠 LLM Response: I have created a `readme.md` file containing a brief explanation of artificial intelligence.  The git status shows that the file is currently untracked.  Finally, I was unable to list the Chroma collections due to a permission issue.
--- Event: agent ---
{'messages': [AIMessage(content='I have created a `readme.md` file containing a brief explanation of artificial intelligence.  The git status shows that the file is currently untracked.  Finally, I was unable to list the Chroma collections due to a permission issue.', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'safety_ratings': []}, id='run--4d47c68b-c765-4e13-aa15-1f9182afcf16-0', usage_metadata={'input_tokens': 426, 'output_tokens': 50, 'total_tokens': 476, 'input_token_details': {'cache_read': 0}})]}


==================================================
🏁 Workflow Finished.
