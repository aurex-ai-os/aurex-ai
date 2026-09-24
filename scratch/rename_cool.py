import re

with open('static/index.html', 'r') as f:
    html = f.read()

# Replace text content in spans
html = html.replace('<span class="grow">Compare Models</span>', '<span class="grow">Arena</span>')
html = html.replace('<span class="grow">Prompt Templates</span>', '<span class="grow">Codex</span>')
html = html.replace('<span class="grow">Web Researcher</span>', '<span class="grow">Oracle</span>')
html = html.replace('<span class="grow">Image Gallery</span>', '<span class="grow">Canvas</span>')

with open('static/index.html', 'w') as f:
    f.write(html)
print("Renamed tools to aesthetic names")
