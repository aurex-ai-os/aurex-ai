import re

with open('static/js/modelPicker.js', 'r') as f:
    content = f.read()

# Add a check for "free" in the mid to add a pill
old_code = """      nameSpan.className = 'mp-model-name';
      nameSpan.textContent = m.display;
      // Long model names are clipped with ellipsis — expose the full name on
      // hover so the suffix/variant tag is still discoverable (#1982).
      nameSpan.title = m.display;
      row.appendChild(nameSpan);"""

new_code = """      nameSpan.className = 'mp-model-name';
      nameSpan.textContent = m.display;
      nameSpan.title = m.display;
      row.appendChild(nameSpan);

      // Show a [Free] tag if the model ID explicitly contains "free" (common for OpenRouter)
      if (m.mid.toLowerCase().includes(':free') || m.mid.toLowerCase().includes('-free')) {
        const freeTag = document.createElement('span');
        freeTag.style.cssText = 'margin-left:6px; font-size:10px; font-weight:700; background:var(--green, #50fa7b); color:#000; padding:1px 5px; border-radius:4px; flex-shrink:0;';
        freeTag.textContent = 'FREE';
        row.appendChild(freeTag);
      }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('static/js/modelPicker.js', 'w') as f:
        f.write(content)
    print("Patched modelPicker.js successfully!")
else:
    print("Could not find old_code in modelPicker.js")
