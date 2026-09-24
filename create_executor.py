import os
from pathlib import Path

def create_file(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

os.makedirs("src/executor", exist_ok=True)

create_file("src/executor/__init__.py", "")

create_file("src/executor/errors.py", """
class ExecutorError(Exception): pass
class PolicyDenied(ExecutorError): pass
class ApprovalRequired(ExecutorError): pass
class WorkspaceViolation(ExecutorError): pass
class Timeout(ExecutorError): pass
class Cancelled(ExecutorError): pass
class ExecutionFailed(ExecutorError): pass
class InvalidRequest(ExecutorError): pass
class ResourceNotFound(ExecutorError): pass
class SecretBlocked(ExecutorError): pass
""")

create_file("src/executor/models.py", """
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
            raise ValueError("Cannot create ApprovedAction from denied/pending decision")
        self._request = request
        self._decision = decision
        self._is_approved = True
        
    @property
    def request(self) -> ExecutionRequest:
        return self._request
""")

create_file("src/executor/audit.py", """
import re
import logging

logger = logging.getLogger("aurex.audit")

def sanitize_secrets(text: str) -> str:
    if not isinstance(text, str):
        return text
    # Very basic defense-in-depth sanitization
    # Strip bearer tokens
    text = re.sub(r'(Bearer\s+)[A-Za-z0-9\-\._~+]+', r'\1[REDACTED]', text, flags=re.IGNORECASE)
    # Strip AWS keys
    text = re.sub(r'(AKIA[0-9A-Z]{16})', r'[REDACTED]', text)
    # Strip generic password fields in JSON/args
    text = re.sub(r'("?password"?\s*[:=]\s*"?)[^"&\s]+("?)', r'\1[REDACTED]\2', text, flags=re.IGNORECASE)
    return text

def log_audit_event(request_id: str, tool: str, operation: str, decision: str, status: str, duration: float = 0.0, **kwargs):
    sanitized_kwargs = {k: sanitize_secrets(str(v)) for k, v in kwargs.items()}
    logger.info(f"AUDIT | Req:{request_id} | Tool:{tool} | Op:{operation} | Decision:{decision} | Status:{status} | Duration:{duration:.2f}s | {sanitized_kwargs}")
""")

create_file("src/executor/policy.py", """
import os
from pathlib import Path
from .models import ExecutionRequest, ExecutionDecision, DecisionType, ApprovedAction
from .errors import WorkspaceViolation

class PolicyEngine:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()
        
    def _check_workspace_bounds(self, path: str) -> bool:
        if not path:
            return True
        try:
            resolved = Path(path).resolve()
            return str(resolved).startswith(str(self.workspace_root))
        except Exception:
            return False

    def evaluate(self, req: ExecutionRequest) -> ExecutionDecision:
        # Check workspace bounds
        if req.working_directory and not self._check_workspace_bounds(req.working_directory):
            return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation")
            
        if req.operation_type in ["RunShellCommand", "RunPython"]:
            # Need to ask for interactive shell execution unless we have a specific override
            return ExecutionDecision(decision=DecisionType.ASK, reason="Shell execution requires explicit approval")
            
        if req.operation_type in ["ReadFile"]:
            # Check path
            target = req.arguments.get("path")
            if target and not self._check_workspace_bounds(target):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on read")
            return ExecutionDecision(decision=DecisionType.ALLOW, reason="Read allowed within workspace")
            
        if req.operation_type in ["WriteFile", "DeleteFile", "MoveFile"]:
            target = req.arguments.get("path")
            if target and not self._check_workspace_bounds(target):
                return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Workspace boundary violation on mutation")
            return ExecutionDecision(decision=DecisionType.PREVIEW, reason="File mutation requires preview")
            
        return ExecutionDecision(decision=DecisionType.FORBIDDEN, reason="Unknown operation type")
""")

create_file("src/executor/executor.py", """
import asyncio
import subprocess
import time
from .models import ApprovedAction, ExecutionRequest
from .errors import ExecutionFailed, Timeout, Cancelled, PolicyDenied
from .audit import log_audit_event, sanitize_secrets

class SecureExecutor:
    @staticmethod
    async def execute_shell(action: ApprovedAction, timeout: int = 60) -> dict:
        req = action.request
        cmd = req.arguments.get("command", "")
        cwd = req.working_directory
        
        start_time = time.time()
        try:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
                status = "SUCCESS" if proc.returncode == 0 else "FAILED"
                log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", status, time.time() - start_time)
                return {
                    "stdout": sanitize_secrets(stdout.decode(errors='replace'))[:10000],
                    "stderr": sanitize_secrets(stderr.decode(errors='replace'))[:10000],
                    "returncode": proc.returncode
                }
            except asyncio.TimeoutError:
                proc.terminate()
                await proc.wait()
                log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "TIMEOUT", time.time() - start_time)
                raise Timeout(f"Execution timed out after {timeout} seconds")
        except asyncio.CancelledError:
            log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "CANCELLED", time.time() - start_time)
            raise Cancelled("Execution was cancelled")
        except Exception as e:
            log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "ERROR", time.time() - start_time, error=str(e))
            raise ExecutionFailed(f"Failed to execute: {str(e)}")
""")
