import re
with open("src/mcp_manager.py", "r") as f:
    content = f.read()

imports = """
from src.executor.models import ExecutionRequest, DecisionType
from src.executor.policy import PolicyEngine
from src.runtime_paths import get_app_root
"""
content = imports + content

secure_mcp_patch = """        server_id = parts[1]
        tool_name = parts[2]

        # --- SECURE EXECUTION BOUNDARY ---
        req = ExecutionRequest(
            operation_type="RunMCPTool",
            arguments={"server": server_id, "tool": tool_name, "args": arguments},
            origin_tool=qualified_name
        )
        policy = PolicyEngine(get_app_root())
        decision = policy.evaluate(req)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied MCP Tool execution: {decision.reason}", "exit_code": 1}
"""

content = content.replace("        server_id = parts[1]\n        tool_name = parts[2]\n", secure_mcp_patch)

with open("src/mcp_manager.py", "w") as f:
    f.write(content)
