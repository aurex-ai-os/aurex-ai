import re
with open("src/tool_execution.py", "r") as f:
    text = f.read()

imports = """
from src.executor.registry import default_registry, ToolCall, ToolNotFoundError
from src.executor.policy import PolicyEngine
from src.executor.models import DecisionType, ApprovedAction
from src.executor.registration import bootstrap_registry
from src.runtime_paths import get_app_root

bootstrap_registry()

"""
text = imports + text

direct_fallback_patch = """async def _direct_fallback(
    tool: str,
    content: str,
    progress_cb: Optional[Callable[[Dict], Awaitable[None]]] = None,
    session_id: Optional[str] = None,
    owner: Optional[str] = None,
) -> Optional[Dict]:
    _subproc_env = {
        **os.environ,
        "TERM": "xterm-256color",
        "COLUMNS": "120",
        "LINES": "40",
        "HOME": _AGENT_WORKDIR,
    }

    try:
        ctx = {
            "progress_cb": progress_cb,
            "subproc_env": _subproc_env,
            "session_id": session_id,
            "owner": owner,
        }
        
        # --- PHASE 2: REGISTRY & POLICY BOUNDARY ---
        try:
            tool_def = default_registry.resolve(tool)
        except ToolNotFoundError:
            return {"error": f"Tool '{tool}' not registered in canonical registry.", "exit_code": 1}
            
        call = ToolCall(call_id="legacy-call", tool_id=tool, arguments={"content": content})
        policy = PolicyEngine(get_app_root())
        
        # The internal tool might do its own fine-grained checks (like WriteFile checking path), 
        # but we also do a capability-level check here before even invoking the handler.
        decision = policy.evaluate_tool_call(call, tool_def)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied capability execution: {decision.reason}", "exit_code": 1}
            
        # Execute the handler (Phase 1 ApprovedAction check still occurs deep inside for privileged actions)
        return await tool_def.handler(content, ctx)

    except Exception as e:
        logger.exception(f"_direct_fallback failed for {tool}")
        return {"error": f"{tool} execution error: {e}", "exit_code": 1}
"""

text = re.sub(r'async def _direct_fallback\(.*?\).*?return await TOOL_HANDLERS\[tool\]\(content, ctx\)\n\n.*?return {"error": f"{tool} execution error: {e}", "exit_code": 1}', direct_fallback_patch, text, flags=re.DOTALL)

with open("src/tool_execution.py", "w") as f:
    f.write(text)
