import re

with open("static/index.html", "r") as f:
    text = f.read()

old_svg_start = r'<svg class="sidebar-logo" viewBox="0 0 32 32" style="width:18px;height:18px;margin-right:6px;color:var(--brand-color, var\(--red\));">'
new_svg_start = r'<svg class="sidebar-logo" viewBox="0 0 32 32" style="width:24px;height:24px;margin-right:8px;margin-left:-4px;color:var(--brand-color, var(--red));">'

text = re.sub(old_svg_start, new_svg_start, text)

with open("static/index.html", "w") as f:
    f.write(text)
