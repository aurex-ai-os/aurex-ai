import re

with open("static/index.html", "r") as f:
    text = f.read()

# Replace in index.html (favicon, welcome screen, sidebar logo)
old_circle = r"<circle cx='16' cy='16' r='14' stroke='([^']+)' stroke-width='1.5' fill='none' opacity='0.2'/>"
new_circle = r"<circle cx='16' cy='16' r='14' stroke='\1' stroke-width='2.5' fill='none' opacity='0.4'/>"
text = re.sub(old_circle, new_circle, text)

old_circle_double = r'<circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.2"/>'
new_circle_double = r'<circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="2.5" fill="none" opacity="0.4"/>'
text = re.sub(old_circle_double, new_circle_double, text)

with open("static/index.html", "w") as f:
    f.write(text)

with open("static/js/theme.js", "r") as f:
    js_text = f.read()

old_js_circle = r"<circle cx='16' cy='16' r='14' stroke='\$\{fg\}' stroke-width='1.5' fill='none' opacity='0.2'/>"
new_js_circle = r"<circle cx='16' cy='16' r='14' stroke='${fg}' stroke-width='2.5' fill='none' opacity='0.4'/>"

js_text = re.sub(old_js_circle, new_js_circle, js_text)

with open("static/js/theme.js", "w") as f:
    f.write(js_text)
