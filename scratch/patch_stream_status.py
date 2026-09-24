import re

with open('routes/chat_routes.py', 'r') as f:
    content = f.read()

# Replace raise HTTPException(404, "No active stream for this session")
content = re.sub(
    r'raise HTTPException\(404, "No active stream for this session"\)',
    r'return {"active": False, "status": "none"}',
    content
)

with open('routes/chat_routes.py', 'w') as f:
    f.write(content)

with open('static/js/chat.js', 'r') as f:
    chat_js = f.read()

# In chat.js, stream_status check
old_check = r"if \(res\.status !== 404\) return;"
new_check = r"""if (res.status === 404) {
        // legacy 404 behavior
      } else if (res.ok) {
        const json = await res.json();
        if (json.active === false || json.status === 'none') {
          // stale
        } else {
          return;
        }
      } else {
        return;
      }"""

chat_js = chat_js.replace(old_check, new_check)
with open('static/js/chat.js', 'w') as f:
    f.write(chat_js)

print("Patched chat_stream_status")
