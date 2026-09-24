
import os
from pathlib import Path
from .models import ExecutionRequest, ExecutionDecision, DecisionType, ApprovedAction
from .registry import ToolCall, ToolDefinition, Capability
from .errors import WorkspaceViolation

class PolicyEngine:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve(strict=False)
        
    def _check_workspace_bounds(self, path: str) -> bool:
        if not path:
            return True
        try:
            # Resolve resolves symlinks and normalizes ../
            resolved = Path(path).resolve(strict=False)
            return str(resolved).startswith(str(self.workspace_root))
        except Exception:
            return False

    def evaluate(self, req: ExecutionRequest) -> ExecutionDecision:
        if req.working_directory and not self._check_workspace_bounds(req.working_directory):
            return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation")
            
        if req.operation_type in ["RunShellCommand", "RunPython", "RunExec"]:
            return ExecutionDecision(decision=DecisionType.ASK, reason="Execution requires explicit approval")
            
        if req.operation_type in ["ReadFile", "ListDirectory"]:
            target = req.arguments.get("path")
            if target and not self._check_workspace_bounds(target):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on read")
            return ExecutionDecision(decision=DecisionType.ALLOW, reason="Read allowed within workspace")
            
        if req.operation_type in ["WriteFile", "DeleteFile", "MoveFile", "CopyFile", "MakeDirectory"]:
            target = req.arguments.get("path")
            dest = req.arguments.get("destination")
            if target and not self._check_workspace_bounds(target):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on mutation target")
            if dest and not self._check_workspace_bounds(dest):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on mutation destination")
            return ExecutionDecision(decision=DecisionType.PREVIEW, reason="File mutation requires preview")
            
        if req.operation_type == "RunMCPTool":
            return ExecutionDecision(decision=DecisionType.ASK, reason="MCP Tool execution requires approval")
            
        return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Unknown operation type")

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
            

        decision = DecisionType.ALLOW
        reason = "Operation allowed based on capability subset"
        
        # Default allow for safe read-only operations
        if len(caps) == 1 and caps[0] == Capability.READ_ONLY:
            decision = DecisionType.ALLOW
            reason = "Read-only tool"
            
        if tool_def.requires_approval and decision == DecisionType.ALLOW:
            decision = DecisionType.ASK
            reason = "ToolDefinition statically requires approval"
            
        return ExecutionDecision(decision=decision, reason=reason)

