import os
from pathlib import Path

# 1. Update models.py for ApprovedAction integrity
models_code = """
from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class DecisionType(str, Enum):
    ALLOW = "ALLOW"
    PREVIEW = "PREVIEW"
    ASK = "ASK"
    FORBIDDEN = "FORBIDDEN"

class ExecutionRequest(BaseModel):
    operation_type: str
    arguments: Dict[str, Any]
    working_directory: Optional[str] = None
    requested_permissions: List[str] = []
    origin_tool: str = "unknown"
    task_id: Optional[str] = None

class ExecutionDecision(BaseModel):
    decision: DecisionType
    reason: str

class ApprovedAction:
    def __init__(self, request: ExecutionRequest, decision: ExecutionDecision):
        if decision.decision not in (DecisionType.ALLOW, DecisionType.PREVIEW):
            raise ValueError(f"Cannot create ApprovedAction from {decision.decision} decision")
        # Store immutable copies to prevent post-approval mutation
        self._request = request.model_copy(deep=True)
        self._decision = decision.model_copy(deep=True)
        self._is_approved = True
        
    @property
    def request(self) -> ExecutionRequest:
        return self._request.model_copy(deep=True)
        
    @property
    def decision(self) -> ExecutionDecision:
        return self._decision.model_copy(deep=True)
"""
with open("src/executor/models.py", "w") as f:
    f.write(models_code)

# 2. Update policy.py for proper symlink and traversal resolution
policy_code = """
import os
from pathlib import Path
from .models import ExecutionRequest, ExecutionDecision, DecisionType, ApprovedAction
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
"""
with open("src/executor/policy.py", "w") as f:
    f.write(policy_code)
