import re
with open("src/builtin_actions.py", "r") as f:
    content = f.read()

# Add imports
imports = """
from src.executor.models import ExecutionRequest, DecisionType, ApprovedAction
from src.executor.policy import PolicyEngine
from src.executor.executor import SecureExecutor
from src.runtime_paths import get_app_root
"""

content = imports + content

run_sub_new = """async def _run_subprocess(argv, *, shell: bool = False, timeout: int = 120, label: str = "Command") -> Tuple[str, bool]:
    # Intercepted by Phase 1 Secure Boundary
    req = ExecutionRequest(
        operation_type="RunShellCommand" if shell else "RunExec",
        arguments={"command": str(argv)},
        origin_tool="builtin_actions"
    )
    policy = PolicyEngine(get_app_root())
    decision = policy.evaluate(req)
    if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
        return f"PolicyEngine blocked execution: {decision.reason}", True

    action = ApprovedAction(req, decision)
    try:
        if shell:
            res = await SecureExecutor.execute_shell(action, timeout=timeout)
        else:
            res = await SecureExecutor.execute_exec(action, *argv, timeout=timeout)
        return (res["stdout"] + "\\n" + res["stderr"]), False
    except Exception as e:
        return str(e), True
"""

content = re.sub(r'async def _run_subprocess\(argv, \*, shell: bool = False, timeout: int = 120, label: str = "Command"\) -> Tuple\[str, bool\]:.*?return output, False', run_sub_new, content, flags=re.DOTALL)

with open("src/builtin_actions.py", "w") as f:
    f.write(content)
