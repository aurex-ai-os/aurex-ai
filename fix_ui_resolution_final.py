import re

with open("static/index.html", "r") as f:
    html = f.read()

# Add settings-modal-content class to pi-modal-content
html = html.replace('class="modal-content pi-modal-content"', 'class="modal-content settings-modal-content pi-modal-content"')

with open("static/index.html", "w") as f:
    f.write(html)

with open("static/aurex-theme.css", "r") as f:
    css = f.read()

# Remove explicit width and height from pi-modal-content so settings-modal-content can handle it
css = re.sub(r'width:[^;]+;\n?', '', css)
css = re.sub(r'height:[^;]+;\n?', '', css)
css = re.sub(r'max-height:[^;]+;\n?', '', css)

# Wait, the regex might destroy other width/height rules in aurex-theme.css!
# Better to do exact string replacement or just isolate the block.
