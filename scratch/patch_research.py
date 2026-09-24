import re

with open('routes/research/research_routes.py', 'r') as f:
    content = f.read()

# Replace raise HTTPException(404, "No research found for this session")
# but ONLY in research_status endpoint.

def replace_research_status(match):
    body = match.group(0)
    body = body.replace('raise HTTPException(404, "No research found for this session")', 'return {"status": "none", "active": False}')
    return body

content = re.sub(
    r'@router\.get\("/api/research/status/\{session_id\}"\).*?return status',
    replace_research_status,
    content,
    flags=re.DOTALL
)

with open('routes/research/research_routes.py', 'w') as f:
    f.write(content)

print("Patched research_routes.py")
