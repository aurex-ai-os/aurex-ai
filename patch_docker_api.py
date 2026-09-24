import re
with open("app.py", "r") as f:
    text = f.read()

new_api = r"""
@app.get("/api/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# --- DOCKER MANAGER API ---
@app.post("/api/search/autohost")
async def autohost_searxng():
    from src.executor.docker_manager import DockerManager
    success, message = DockerManager.launch_searxng()
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=message)
    return {"status": "success", "message": message, "url": "http://localhost:8080"}
"""

text = re.sub(r'@app\.get\("/api/health"\)\nasync def health_check\(\) -> Dict\[str, str\]:\n    return \{"status": "healthy", "timestamp": datetime\.now\(timezone\.utc\)\.isoformat\(\)\}', new_api.strip(), text)

with open("app.py", "w") as f:
    f.write(text)
