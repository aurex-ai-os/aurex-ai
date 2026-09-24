with open("src/agent_loop.py", "r") as f:
    content = f.read()

content = content.replace("async def await _trim_route_request_messages(", "async def _trim_route_request_messages(")

with open("src/agent_loop.py", "w") as f:
    f.write(content)
