import re
with open("src/executor/policy.py", "r") as f:
    text = f.read()

# Replace the final return statement to handle requires_approval
new_logic = """
        decision = DecisionType.ALLOW
        reason = "Operation allowed based on capability subset"
        
        # Default allow for safe read-only operations
        if len(caps) == 1 and caps[0] == Capability.READ_ONLY:
            decision = DecisionType.ALLOW
            reason = "Read-only tool"
            
        if tool_def.requires_approval and decision == DecisionType.ALLOW:
            decision = DecisionType.ASK
            reason = "ToolDefinition statically requires approval"
            
        return ExecutionDecision(decision=decision, reason=reason)
"""

text = re.sub(r'        # Default allow for safe read-only operations.*?return ExecutionDecision\(decision=DecisionType\.ALLOW, reason="Operation allowed based on capability subset"\)', new_logic, text, flags=re.DOTALL)

with open("src/executor/policy.py", "w") as f:
    f.write(text)
