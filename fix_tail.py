with open("src/agent_tools/subprocess_tools.py", "r") as f:
    text = f.read()

import re
# Find the start of class PythonTool and replace it completely
text = re.sub(r'class PythonTool:.*', 'class PythonTool:\n    async def execute(self, content: str, ctx: dict) -> dict:\n        from src.tool_execution import agent_cwd, _truncate\n        import sys\n        try:\n            req = ExecutionRequest(operation_type="RunPython", arguments={"script": content}, working_directory=agent_cwd(), origin_tool="python")\n            policy = PolicyEngine(get_app_root())\n            decision = policy.evaluate(req)\n            if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:\n                return {"error": f"PolicyEngine denied Python execution: {decision.reason}", "exit_code": 1}\n            action = ApprovedAction(req, decision)\n            result = await SecureExecutor.execute_exec(action, sys.executable or "python", "-I", "-c", content, timeout=120, env=ctx.get("subproc_env"))\n            out = result["stdout"] + "\\n" + result["stderr"]\n            return {"output": _truncate(out, 15000) or "(no output)", "exit_code": result["returncode"]}\n        except Exception as e:\n            return {"error": str(e), "exit_code": 1}\n', text, flags=re.DOTALL)

with open("src/agent_tools/subprocess_tools.py", "w") as f:
    f.write(text)
