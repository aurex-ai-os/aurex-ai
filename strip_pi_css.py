import re

with open("static/aurex-theme.css", "r") as f:
    css = f.read()

# First replace the HTML
with open("static/index.html", "r") as f:
    html = f.read()
    html = html.replace('class="modal-content pi-modal-content"', 'class="modal-content settings-modal-content pi-modal-content"')
with open("static/index.html", "w") as f:
    f.write(html)

# We want to strip out the width/height from .pi-modal-content
# and remove the @media (max-width: 768px) block we added for .pi-modal-content
pi_block_start = css.find(".pi-modal-content {")
if pi_block_start != -1:
    pi_block_end = css.find("}", pi_block_start)
    block = css[pi_block_start:pi_block_end+1]
    
    # Strip widths and heights
    block = re.sub(r'\s*width:[^;]+;?', '', block)
    block = re.sub(r'\s*height:[^;]+;?', '', block)
    block = re.sub(r'\s*max-height:[^;]+;?', '', block)
    
    css = css[:pi_block_start] + block + css[pi_block_end+1:]

# Remove the media query we added manually
media_start = css.find("@media (max-width: 768px) {\n  .pi-modal-content {")
if media_start != -1:
    # Remove everything from here to the end since we appended it at the end
    css = css[:media_start]

with open("static/aurex-theme.css", "w") as f:
    f.write(css)
