import sys

content = open("routes/provider_routes.py").read()
if '"is_local": is_local,' in content and '"is_free":' not in content:
    content = content.replace(
        '"health": "HEALTHY",',
        '"health": "HEALTHY",\n                        "is_free": "free" in m_id.lower() or "llama" in m_id.lower() or "mistral" in m_id.lower() or "qwen" in m_id.lower() or is_local,'
    )
    with open("routes/provider_routes.py", "w") as f:
        f.write(content)
    print("Patched provider_routes.py")
else:
    print("Already patched or pattern not found")
