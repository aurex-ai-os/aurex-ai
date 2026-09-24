import re

with open('static/js/settings.js', 'r') as f:
    content = f.read()

old_code = """        var o = document.createElement('option');
        o.value = m;
        o.textContent = m.split('/').pop();
        selectEl.appendChild(o);"""

new_code = """        var o = document.createElement('option');
        o.value = m;
        var isFree = m.toLowerCase().includes(':free') || m.toLowerCase().includes('-free');
        o.textContent = m.split('/').pop() + (isFree ? ' [Free]' : '');
        selectEl.appendChild(o);"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('static/js/settings.js', 'w') as f:
        f.write(content)
    print("Patched settings.js successfully!")
else:
    print("Could not find old_code in settings.js")
