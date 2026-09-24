import re
with open("src/mcp_manager.py", "r") as f:
    text = f.read()

# Fix the broken string literal in mcp_manager.py
# The patch resulted in something like:
#     return {"error": f"PolicyEngine denied MCP execution: {decision.reason}
# ", "exit_code": 1}
# We'll regex it out
text = re.sub(r'return \{"error": f"PolicyEngine denied MCP execution: \{decision\.reason\}"\n", "exit_code": 1\}',
              r'return {"error": f"PolicyEngine denied MCP execution: {decision.reason}", "exit_code": 1}', text)
              
# Just in case it's formatted differently
lines = text.split('\n')
for i in range(len(lines)):
    if '", "exit_code": 1}' in lines[i] and 'return {"error"' not in lines[i]:
        if i > 0 and 'return {"error": f"PolicyEngine denied MCP execution: {decision.reason}' in lines[i-1]:
            lines[i-1] = '        if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:\n            return {"error": f"PolicyEngine denied MCP execution: {decision.reason}", "exit_code": 1}'
            lines[i] = ""

with open("src/mcp_manager.py", "w") as f:
    f.write("\n".join(lines))
