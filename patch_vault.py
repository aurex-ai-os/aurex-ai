import re
with open("src/tools/vault.py", "r") as f:
    content = f.read()

imports = """
from src.executor.models import ExecutionRequest, DecisionType, ApprovedAction
from src.executor.policy import PolicyEngine
from src.executor.executor import SecureExecutor
from src.runtime_paths import get_app_root
"""
content = imports + content

secure_bw = """    req = ExecutionRequest(
        operation_type="RunExec",
        arguments={"command": ["bw"] + list(args)},
        origin_tool="vault"
    )
    policy = PolicyEngine(get_app_root())
    decision = policy.evaluate(req)
    if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
        return "", f"PolicyEngine denied Vault execution: {decision.reason}", 1

    action = ApprovedAction(req, decision)
    
    env = {}
    import os as _os
    env.update(_os.environ)
    if session:
        env["BW_SESSION"] = session

    try:
        res = await SecureExecutor.execute_exec(action, "bw", *args, timeout=30, env=env)
        return res["stdout"], res["stderr"], res["returncode"]
    except Exception as e:
        return "", str(e), 1
"""
content = re.sub(r'    env = \{\}.*?return stdout.decode\(errors="replace"\).strip\(\), stderr.decode\(errors="replace"\).strip\(\), proc.returncode', secure_bw, content, flags=re.DOTALL)

with open("src/tools/vault.py", "w") as f:
    f.write(content)
