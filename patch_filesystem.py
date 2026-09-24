import re

with open("src/agent_tools/filesystem_tools.py", "r") as f:
    content = f.read()

# Add imports
imports = """
from src.executor.models import ExecutionRequest, DecisionType, ApprovedAction
from src.executor.policy import PolicyEngine
from src.executor.executor import SecureExecutor
from src.runtime_paths import get_app_root
"""
content = imports + content

# Patch WriteFileTool
write_patch = """
        # --- SECURE EXECUTION BOUNDARY ---
        req = ExecutionRequest(
            operation_type="WriteFile",
            arguments={"path": path, "content": body},
            origin_tool="write_file"
        )
        policy = PolicyEngine(get_app_root())
        decision = policy.evaluate(req)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied filesystem mutation: {decision.reason}", "exit_code": 1}
        
        # Approve and execute via SecureExecutor instead of directly
        action = ApprovedAction(req, decision)
        try:
            await SecureExecutor.execute_fs(action)
        except Exception as e:
            return {"error": f"write_file: {e}", "exit_code": 1}
            
        return {"output": f"Wrote bytes to {path}", "exit_code": 0}
"""
content = re.sub(r'        try:\n            def _write\(\).*?return result', write_patch, content, flags=re.DOTALL)

# Patch EditFileTool (assuming it's named EditFileTool or ApplyPatchTool)
# Actually, it's ApplyPatchTool.
# ApplyPatchTool just calls _apply_patch_hunks and writes. Let's just wrap the write.
apply_patch = """
        # --- SECURE EXECUTION BOUNDARY ---
        req = ExecutionRequest(
            operation_type="WriteFile",
            arguments={"path": path, "content": new_content},
            origin_tool="apply_patch"
        )
        policy = PolicyEngine(get_app_root())
        decision = policy.evaluate(req)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied filesystem mutation: {decision.reason}", "exit_code": 1}
        
        action = ApprovedAction(req, decision)
        try:
            await SecureExecutor.execute_fs(action)
        except Exception as e:
            return {"error": f"apply_patch: write failed: {e}", "exit_code": 1}
"""
content = re.sub(r'        try:\n            def _apply\(\).*?return result', apply_patch, content, flags=re.DOTALL)

with open("src/agent_tools/filesystem_tools.py", "w") as f:
    f.write(content)
