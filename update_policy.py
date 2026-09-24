import re

with open("src/executor/policy.py", "r") as f:
    content = f.read()

imports = """from .registry import ToolCall, ToolDefinition, Capability
"""

if "from .registry import" not in content:
    content = content.replace("from .errors import", imports + "from .errors import")

new_policy_method = """
    def evaluate_tool_call(self, call: ToolCall, tool_def: ToolDefinition) -> ExecutionDecision:
        caps = tool_def.capabilities
        
        # Deny inherently dangerous unaccounted states
        if Capability.CREDENTIAL_ACCESS in caps and Capability.NETWORK_ACCESS in caps:
            return ExecutionDecision(decision=DecisionType.ASK, reason="Credential exposure to network requires approval")
            
        if Capability.PROCESS_EXECUTION in caps:
            return ExecutionDecision(decision=DecisionType.ASK, reason="Process execution requires explicit approval")
            
        if Capability.MCP_EXECUTION in caps:
            return ExecutionDecision(decision=DecisionType.ASK, reason="MCP Tool execution requires explicit approval")
            
        if Capability.FILESYSTEM_WRITE in caps or Capability.FILESYSTEM_DELETE in caps:
            # Need to check bounds on the arguments if we know them
            path = call.arguments.get("path")
            dest = call.arguments.get("destination")
            if path and not self._check_workspace_bounds(path):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on mutation target")
            if dest and not self._check_workspace_bounds(dest):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on mutation destination")
            return ExecutionDecision(decision=DecisionType.PREVIEW, reason="File mutation requires preview")
            
        if Capability.FILESYSTEM_READ in caps:
            path = call.arguments.get("path")
            if path and not self._check_workspace_bounds(path):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on read target")
            
        # Default allow for safe read-only operations
        if len(caps) == 1 and caps[0] == Capability.READ_ONLY:
            return ExecutionDecision(decision=DecisionType.ALLOW, reason="Read-only tool")
            
        return ExecutionDecision(decision=DecisionType.ALLOW, reason="Operation allowed based on capability subset")
"""

if "evaluate_tool_call" not in content:
    content += new_policy_method
    
with open("src/executor/policy.py", "w") as f:
    f.write(content)
