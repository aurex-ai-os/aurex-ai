import pytest
import asyncio
from pathlib import Path
from src.executor.models import ExecutionRequest, DecisionType
from src.executor.policy import PolicyEngine
from src.executor.executor import SecureExecutor
from src.executor.audit import sanitize_secrets
from src.executor.errors import Timeout, Cancelled

@pytest.fixture
def policy_engine(tmp_path):
    return PolicyEngine(workspace_root=str(tmp_path))

def test_workspace_boundary(policy_engine, tmp_path):
    # Authorized write
    req1 = ExecutionRequest(operation_type="WriteFile", arguments={"path": str(tmp_path / "test.txt")})
    dec1 = policy_engine.evaluate(req1)
    assert dec1.decision == DecisionType.PREVIEW

    # Escape denied
    req2 = ExecutionRequest(operation_type="WriteFile", arguments={"path": str(tmp_path / ".." / "outside.txt")})
    dec2 = policy_engine.evaluate(req2)
    assert dec2.decision == DecisionType.FORBIDDEN

    # Absolute outside denied
    req3 = ExecutionRequest(operation_type="WriteFile", arguments={"path": "/etc/passwd"})
    dec3 = policy_engine.evaluate(req3)
    assert dec3.decision == DecisionType.FORBIDDEN

def test_shell_policy(policy_engine):
    req = ExecutionRequest(operation_type="RunShellCommand", arguments={"command": "echo test"})
    dec = policy_engine.evaluate(req)
    assert dec.decision == DecisionType.ASK

def test_secret_sanitization():
    assert sanitize_secrets("Authorization: Bearer sk-12345ABCD") == "Authorization: Bearer [REDACTED]"
    assert sanitize_secrets("AWS_KEY=AKIAIOSFODNN7EXAMPLE") == "AWS_KEY=[REDACTED]"
    assert sanitize_secrets('{"password": "secret_pass"}') == '{"password": "[REDACTED]"}'
    assert sanitize_secrets("normal text") == "normal text"

@pytest.mark.asyncio
async def test_shell_timeout(policy_engine, tmp_path):
    req = ExecutionRequest(operation_type="RunShellCommand", arguments={"command": "sleep 10"}, working_directory=str(tmp_path))
    # Mock approval
    from src.executor.models import ExecutionDecision, ApprovedAction
    action = ApprovedAction(req, ExecutionDecision(decision=DecisionType.ALLOW, reason="Mock"))
    
    with pytest.raises(Timeout):
        await SecureExecutor.execute_shell(action, timeout=1)

@pytest.mark.asyncio
async def test_shell_cancellation(policy_engine, tmp_path):
    req = ExecutionRequest(operation_type="RunShellCommand", arguments={"command": "sleep 10"}, working_directory=str(tmp_path))
    from src.executor.models import ExecutionDecision, ApprovedAction
    action = ApprovedAction(req, ExecutionDecision(decision=DecisionType.ALLOW, reason="Mock"))
    
    task = asyncio.create_task(SecureExecutor.execute_shell(action, timeout=5))
    await asyncio.sleep(0.5)
    task.cancel()
    
    with pytest.raises(Cancelled) or pytest.raises(asyncio.CancelledError):
        await task
