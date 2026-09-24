import re

with open("static/index.html", "r") as f:
    content = f.read()

# 1. Dim the background for the modal
content = content.replace(
    '<div id="provider-intelligence-modal" class="modal hidden">',
    '<div id="provider-intelligence-modal" class="modal hidden" style="background:rgba(0,0,0,0.5); backdrop-filter:blur(4px); pointer-events:auto;">'
)

with open("static/index.html", "w") as f:
    f.write(content)

with open("static/aurex-theme.css", "r") as f:
    css = f.read()

# 2. Make sure pi-modal-content has pointer-events auto
if "pointer-events: auto !important;" not in css:
    css = css.replace(
        ".pi-modal-content {",
        ".pi-modal-content {\n  pointer-events: auto !important;"
    )

with open("static/aurex-theme.css", "w") as f:
    f.write(css)

