import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

# Add .msg-user .timestamp to the list of elements that get forced to high-contrast white
new_footer = r"""
.msg-user .msg-footer,
.msg-user .msg-footer span,
.msg-user .msg-footer div,
.msg-user .timestamp {
  color: rgba(255, 255, 255, 0.7) !important;
}
"""

text = re.sub(r'\.msg-user \.msg-footer,\n\.msg-user \.msg-footer span,\n\.msg-user \.msg-footer div \{\n  color: rgba\(255, 255, 255, 0\.7\) !important;\n\}', new_footer.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)
