import re
with open("src/tool_execution.py", "r") as f:
    text = f.read()

imports = """
from src.executor.registry import default_registry, ToolCall, ToolNotFoundError
from src.executor.policy import PolicyEngine
from src.executor.models import DecisionType
from src.executor.registration import bootstrap_registry
from src.runtime_paths import get_app_root
import os

bootstrap_registry()

"""

text = text.replace("import asyncio\n", "import asyncio\n" + imports)

intercept = """    tool = block.tool_type
    content = block.content

    # --- PHASE 2: TOOL REGISTRY & POLICY INTERCEPTION ---
    try:
        tool_def = default_registry.resolve(tool)
        call = ToolCall(call_id="legacy-call", tool_id=tool, arguments={"content": content})
        policy = PolicyEngine(get_app_root())
        
        decision = policy.evaluate_tool_call(call, tool_def)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return f"{tool}: BLOCKED", {"error": f"PolicyEngine denied capability execution: {decision.reason}", "exit_code": 1}
            
        if tool_def.handler:
            _subproc_env = {**os.environ, "TERM": "xterm-256color", "HOME": _AGENT_WORKDIR}
            ctx = {"progress_cb": progress_cb, "subproc_env": _subproc_env, "session_id": session_id, "owner": owner}
            result = await tool_def.handler(content, ctx)
            first_line = (content or "").split(chr(10))[0][:80]
            desc = f"{tool}: {first_line}" if first_line else tool
            return desc, result
    except ToolNotFoundError:
        pass # Fallback to legacy path for non-migrated tools
    except Exception as e:
        return f"{tool}: ERROR", {"error": f"ToolRegistry error: {e}", "exit_code": 1}
    # ---------------------------------------------------
"""

text = re.sub(r'    tool = block\.tool_type\n    content = block\.content', intercept, text)

with open("src/tool_execution.py", "w") as f:
    f.write(text)
