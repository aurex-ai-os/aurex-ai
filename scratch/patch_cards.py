import re

with open('static/aurex-theme.css', 'r') as f:
    css = f.read()

# Add pointer-events: auto to .welcome-setup-grid
old_block = """/* 30. Welcome Dashboard Grid */
.welcome-setup-grid {
  width: 100%;
  max-width: 600px;
  margin: 32px auto 0;
}"""

new_block = """/* 30. Welcome Dashboard Grid */
.welcome-setup-grid {
  width: 100%;
  max-width: 600px;
  margin: 32px auto 0;
  pointer-events: auto !important;
}"""

css = css.replace(old_block, new_block)

with open('static/aurex-theme.css', 'w') as f:
    f.write(css)

print("Fixed card pointer events")
