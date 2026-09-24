import re

with open('static/index.html', 'r') as f:
    html = f.read()

# Replace text content in spans
html = html.replace('<span class="grow">Compare</span>', '<span class="grow">Compare Models</span>')
html = html.replace('<span class="grow">Cookbook</span>', '<span class="grow">Prompt Templates</span>')
html = html.replace('<span class="grow">Deep Research</span>', '<span class="grow">Web Researcher</span>')
html = html.replace('<span class="grow">Gallery</span>', '<span class="grow">Image Gallery</span>')

with open('static/index.html', 'w') as f:
    f.write(html)
print("Renamed tools")
