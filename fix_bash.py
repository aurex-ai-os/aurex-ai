import re
with open("src/agent_tools/subprocess_tools.py", "r") as f:
    text = f.read()

# Replace any newline character between double quotes that isn't escaped properly, specifically in the out = result line.
lines = text.split("\n")
for i in range(len(lines)):
    if 'out = result["stdout"]' in lines[i]:
        lines[i] = '            out = result["stdout"] + "\\n" + result["stderr"]'
    if '\" + result[\"stderr\"]' in lines[i]:
        lines[i] = '' # Clear the dangling line
        
with open("src/agent_tools/subprocess_tools.py", "w") as f:
    f.write("\n".join(lines))
