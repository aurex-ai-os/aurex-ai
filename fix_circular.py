import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

# Delete the specific block to avoid circular reference
text = re.sub(r'/\* Overrides for Legacy Style\.css variables.*?\*/.*?--font-family: var\(--aurex-font-sans\);\s*/\* Switch global font to sans-serif \*/', '', text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)
