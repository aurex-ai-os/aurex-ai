import re

with open("src/agent_tools/subprocess_tools.py", "r") as f:
    content = f.read()

# Add imports at top
imports = """
from src.executor.models import ExecutionRequest, DecisionType, ApprovedAction
from src.executor.policy import PolicyEngine
from src.executor.executor import SecureExecutor
from src.executor.errors import ExecutorError
from src.runtime_paths import get_app_root
"""
content = imports + content

# Replace BashTool.execute entirely
bash_execute_new = """    async def execute(self, content: str, ctx: dict) -> dict:
        from src.tool_execution import agent_cwd, _truncate
        try:
            req = ExecutionRequest(
                operation_type="RunShellCommand", 
                arguments={"command": content}, 
                working_directory=agent_cwd(), 
                origin_tool="bash"
            )
            policy = PolicyEngine(get_app_root())
            decision = policy.evaluate(req)
            if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
                return {"error": f"PolicyEngine denied execution: {decision.reason}", "exit_code": 1}
            
            action = ApprovedAction(req, decision)
            result = await SecureExecutor.execute_shell(action, timeout=120)
            
            out = result["stdout"] + "\\n" + result["stderr"]
            return {
                "output": _truncate(out, 15000) or "(no output)",
                "exit_code": result["returncode"]
            }
        except Exception as e:
            return {"error": str(e), "exit_code": 1}
"""
content = re.sub(r'    async def execute\(self, content: str, ctx: dict\) -> dict:(.*?)(?=class PythonTool|class )', bash_execute_new, content, flags=re.DOTALL)

# Replace PythonTool.execute entirely
python_execute_new = """    async def execute(self, content: str, ctx: dict) -> dict:
        from src.tool_execution import agent_cwd, _truncate
        import sys
        try:
            req = ExecutionRequest(
                operation_type="RunPython", 
                arguments={"script": content}, 
                working_directory=agent_cwd(), 
                origin_tool="python"
            )
            policy = PolicyEngine(get_app_root())
            decision = policy.evaluate(req)
            if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
                return {"error": f"PolicyEngine denied Python execution: {decision.reason}", "exit_code": 1}
            
            action = ApprovedAction(req, decision)
            result = await SecureExecutor.execute_exec(action, sys.executable or "python", "-I", "-c", content, timeout=120, env=ctx.get("subproc_env"))
            
            out = result["stdout"] + "\\n" + result["stderr"]
            return {
                "output": _truncate(out, 15000) or "(no output)",
                "exit_code": result["returncode"]
            }
        except Exception as e:
            return {"error": str(e), "exit_code": 1}
"""
content = re.sub(r'(class PythonTool.*?    async def execute\(self, content: str, ctx: dict\) -> dict:).*', r'\1' + '\n' + python_execute_new, content, flags=re.DOTALL)

with open("src/agent_tools/subprocess_tools.py", "w") as f:
    f.write(content)
