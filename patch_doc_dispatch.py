import re
with open("src/tool_execution.py", "r") as f:
    text = f.read()

patch = """async def _document_tool_dispatch(
    tool: str,
    content: str,
    session_id: Optional[str] = None,
    owner: Optional[str] = None,
    document_id: Optional[str] = None,
    document_version: Optional[int] = None,
    document_digest: Optional[str] = None,
) -> Optional[Dict]:
    ctx = {
        "session_id": session_id,
        "owner": owner,
        "doc_id": document_id,
        "expected_document_version": document_version,
        "expected_document_digest": document_digest,
    }
    # --- PHASE 2: REGISTRY BOUNDARY ---
    try:
        from src.executor.registry import default_registry, ToolCall, ToolNotFoundError
        from src.executor.policy import PolicyEngine
        from src.executor.models import DecisionType
        from src.runtime_paths import get_app_root
        
        tool_def = default_registry.resolve(tool)
        call = ToolCall(call_id="legacy-doc-call", tool_id=tool, arguments={"content": content})
        policy = PolicyEngine(get_app_root())
        decision = policy.evaluate_tool_call(call, tool_def)
        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
            return {"error": f"PolicyEngine denied document capability: {decision.reason}", "exit_code": 1}
            
        if tool_def.handler:
            return await tool_def.handler(content, ctx)
    except ToolNotFoundError:
        pass
    except Exception as e:
        return {"error": f"Doc dispatch registry error: {e}", "exit_code": 1}
    return None
"""

text = re.sub(r'async def _document_tool_dispatch\(.*?\)\s*->\s*Optional\[Dict\]:.*?return None\n', patch, text, flags=re.DOTALL)

with open("src/tool_execution.py", "w") as f:
    f.write(text)
