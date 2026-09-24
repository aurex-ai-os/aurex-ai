import re

with open("src/agent_loop.py", "r") as f:
    content = f.read()

# Replace `def _trim_route_request_messages` with `async def` and its body
old_trim_def = """    def _trim_route_request_messages(candidate_url, candidate_model, route_messages):"""

new_trim_def = """    async def _trim_route_request_messages(candidate_url, candidate_model, route_messages):
        \"\"\"Apply the candidate route's own context budget using the Context Engine.\"\"\"
        try:
            from src.context_engine.engine import ContextEngine
            from src.context_engine.gatherers.legacy import LegacyMessagesGatherer
            from src.context_engine.models import ContextRequest
            from src.model_context import budget_context_for_model
            from src.context_budget import get_setting, DEFAULT_BUDGET
            
            candidate_context = budget_context_for_model(
                candidate_url, candidate_model, fallback=context_length
            )
            _route_context_lengths[(candidate_url, candidate_model)] = candidate_context
            soft_budget = int(get_setting("agent_input_token_budget", DEFAULT_BUDGET) or 0)
            
            # ContextEngine Pipeline
            engine = ContextEngine([LegacyMessagesGatherer(route_messages)])
            req = ContextRequest(owner=owner, session_id=session_id)
            
            result = await engine.build_context(req, candidate_model, token_budget=soft_budget if soft_budget > 0 else candidate_context)
            final_messages = result["messages"]
            
            def _without_protection(items):
                return [{k: v for k, v in message.items() if k != "_protected"} for message in items]
                
            return _without_protection(final_messages)
        except Exception as e:
            logger.warning("[agent] ContextEngine trim skipped for route model=%s: %s", candidate_model, e)
            def _without_protection(items):
                return [{k: v for k, v in message.items() if k != "_protected"} for message in items]
            return _without_protection(route_messages)"""

# We need to replace the entire old function.
# It goes from `def _trim_route_request_messages` to the end of the except block `return _without_protection(route_messages)`.

# Actually, I'll use regex to replace it cleanly.
import re
pattern = re.compile(r'    def _trim_route_request_messages\(candidate_url, candidate_model, route_messages\):.*?            return _without_protection\(route_messages\)', re.DOTALL)
content = pattern.sub(new_trim_def, content)

# Now, we must add `await` to every call of `_trim_route_request_messages`.
content = content.replace('_trim_route_request_messages(', 'await _trim_route_request_messages(')

with open("src/agent_loop.py", "w") as f:
    f.write(content)

print("Patched agent_loop.py")
