import re

with open("static/index.html", "r") as f:
    text = f.read()

# Replace favicon
new_favicon = "<link rel=\"icon\" type=\"image/svg+xml\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='14' stroke='%23337AFF' stroke-width='1.5' fill='none' opacity='0.2'/%3E%3Cpath d='M16 4 L5 24 L11 24 L16 14 Z' fill='%23337AFF' opacity='0.5'/%3E%3Cpath d='M16 4 L27 24 L21 24 L16 14 Z' fill='%23337AFF' opacity='0.9'/%3E%3Cpath d='M16 17 L19 20 L16 23 L13 20 Z' fill='%23337AFF'/%3E%3C/svg%3E\">"

text = re.sub(r'<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml.*?">', new_favicon, text)

# Replace welcome screen logo
new_welcome = """<svg class="welcome-boat" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.2"/>
  <path d="M16 4 L5 24 L11 24 L16 14 Z" fill="currentColor" opacity="0.5"/>
  <path d="M16 4 L27 24 L21 24 L16 14 Z" fill="currentColor" opacity="0.9"/>
  <path d="M16 17 L19 20 L16 23 L13 20 Z" fill="currentColor"/>
</svg>"""

text = re.sub(r'<svg class="welcome-boat" viewBox="0 0 24 24">.*?</svg>', new_welcome, text, flags=re.DOTALL)

with open("static/index.html", "w") as f:
    f.write(text)

with open("static/js/theme.js", "r") as f:
    js_text = f.read()

old_svg = r"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9Z' fill='\$\{fg\}'/></svg>"
new_svg = r"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><circle cx='16' cy='16' r='14' stroke='${fg}' stroke-width='1.5' fill='none' opacity='0.2'/><path d='M16 4 L5 24 L11 24 L16 14 Z' fill='${fg}' opacity='0.5'/><path d='M16 4 L27 24 L21 24 L16 14 Z' fill='${fg}' opacity='0.9'/><path d='M16 17 L19 20 L16 23 L13 20 Z' fill='${fg}'/></svg>"

js_text = re.sub(old_svg, new_svg, js_text)

with open("static/js/theme.js", "w") as f:
    f.write(js_text)

