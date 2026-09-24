import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

new_header = r"""
/* 12. Sidebar Header Alignment */
.sidebar-header {
  justify-content: flex-start !important;
  padding-left: 36px !important;
  padding-top: 8px !important; /* Move it higher up */
}
"""

text = re.sub(r'/\* 12\. Sidebar Header Alignment \*/.*?\.sidebar-header \{.*?\}', new_header.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)
