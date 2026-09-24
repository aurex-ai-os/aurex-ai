import re
with open("src/mcp_manager.py", "r") as f:
    text = f.read()

imports = """
from src.executor.registry import default_registry, ToolCall, ToolDefinition, Capability
from src.executor.policy import PolicyEngine
from src.runtime_paths import get_app_root
"""
text = imports + text

# Inside call_tool
secure_mcp_patch = """        server_id = parts[1]
        tool_name = parts[2]

        # --- PHASE 2: SECURE EXECUTION BOUNDARY ---
        # Represent MCP tools dynamically in the registry if not present
        tool_def = ToolDefinition(
            tool_id=qualified_name,
            name=f"MCP Tool {tool_name}",
            description="MCP execution",
            capabilities=[Capability.MCP_EXECUTION],
            requires_approval=True
        )
        
        call = ToolCall(
            call_id="legacy-mcp-call",
            tool_id=qualified_name,
            arguments=arguments
        )
        
        policy = PolicyEngine(get_app_root())
        decision = policy.evaluate_tool_call(call, tool_def)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied MCP execution: {decision.reason}", "exit_code": 1}
"""

text = re.sub(r'        server_id = parts\[1\]\n        tool_name = parts\[2\]\n.*?return {"error": f"PolicyEngine denied MCP Tool execution.*?}', secure_mcp_patch, text, flags=re.DOTALL)

with open("src/mcp_manager.py", "w") as f:
    f.write(text)
