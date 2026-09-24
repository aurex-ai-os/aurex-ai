import re

with open('routes/chat_routes.py', 'r') as f:
    content = f.read()

# Replace _verify_session_owner(request, session) with _verify_session_owner(request, session, session_manager)
content = re.sub(
    r'_verify_session_owner\(request, session\)',
    r'_verify_session_owner(request, session, session_manager)',
    content
)

# And for session_id
content = re.sub(
    r'_verify_session_owner\(request, session_id\)',
    r'_verify_session_owner(request, session_id, session_manager)',
    content
)

with open('routes/chat_routes.py', 'w') as f:
    f.write(content)

print("Patched chat_routes.py")
