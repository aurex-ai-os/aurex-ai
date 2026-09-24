import re

with open("src/bg_jobs.py", "r") as f:
    content = f.read()

# Add policy imports
imports = """
from src.executor.models import ExecutionRequest, DecisionType
from src.executor.policy import PolicyEngine
from src.runtime_paths import get_app_root
"""
content = imports + content

# Patch launch function
secure_launch = """def launch(command: str, session_id: str, cwd: Optional[str] = None) -> Dict[str, Any]:
    # --- SECURE EXECUTION BOUNDARY ---
    req = ExecutionRequest(
        operation_type="RunShellCommand",
        arguments={"command": command, "detached": True},
        working_directory=cwd,
        origin_tool="bash (bg)"
    )
    policy = PolicyEngine(get_app_root())
    decision = policy.evaluate(req)
    if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
        raise ValueError(f"PolicyEngine denied background execution: {decision.reason}")
    # End Boundary
"""

content = re.sub(r'def launch\(command: str, session_id: str, cwd: Optional\[str\] = None\) -> Dict\[str, Any\]:', secure_launch, content)

with open("src/bg_jobs.py", "w") as f:
    f.write(content)
