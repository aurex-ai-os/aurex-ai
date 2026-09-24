import re
with open("src/tool_execution.py", "r") as f:
    text = f.read()

secure_fallback = """
    try:
        ctx = {
            "progress_cb": progress_cb,
            "subproc_env": _subproc_env,
            "session_id": session_id,
            "owner": owner,
        }
        
        # --- PHASE 2: REGISTRY BOUNDARY ---
        from src.executor.registry import default_registry, ToolCall, ToolNotFoundError
        from src.executor.policy import PolicyEngine
        from src.executor.models import DecisionType
        from src.runtime_paths import get_app_root
        
        try:
            tool_def = default_registry.resolve(tool)
        except ToolNotFoundError:
            return {"error": f"Tool '{tool}' not registered in canonical registry.", "exit_code": 1}
            
        call = ToolCall(call_id="legacy-call", tool_id=tool, arguments={"content": content})
        policy = PolicyEngine(get_app_root())
        
        decision = policy.evaluate_tool_call(call, tool_def)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied capability execution: {decision.reason}", "exit_code": 1}
            
        if tool_def.handler:
            return await tool_def.handler(content, ctx)
        return None

    except Exception as e:
        return {"error": f"{tool} execution error: {e}", "exit_code": 1}
"""

text = re.sub(r'    try:\n        ctx = \{.*?\n    return None', secure_fallback, text, flags=re.DOTALL)

with open("src/tool_execution.py", "w") as f:
    f.write(text)
