import re
with open("src/agent_tools/subprocess_tools.py", "r") as f:
    text = f.read()

text = re.sub(r'out = result\["stdout"\] \+ "\n" \+ result\["stderr"\]', 
              r'out = result["stdout"] + "\\n" + result["stderr"]', 
              text)
text = re.sub(r'out = result\["stdout"\] \+ "\\n "\n" \+ result\["stderr"\]', 
              r'out = result["stdout"] + "\\n" + result["stderr"]', 
              text)

with open("src/agent_tools/subprocess_tools.py", "w") as f:
    f.write(text)
