import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

new_text = r"""
/* 14. Welcome Screen Text Visibility */
#welcome-screen .welcome-sub {
  font-size: 1.1rem !important;
  color: var(--aurex-text) !important;
  opacity: 1 !important;
  font-weight: 500 !important;
  letter-spacing: 0.02em !important;
}

#welcome-screen .welcome-tip {
  font-size: 0.95rem !important;
  color: var(--aurex-text) !important;
  opacity: 0.85 !important;
  font-weight: 400 !important;
  letter-spacing: 0.03em !important;
  margin-top: 16px !important;
}
"""

text = re.sub(r'/\* 14\. Welcome Screen Text Visibility \*/.*?#welcome-screen \.welcome-tip \{.*?\}', new_text.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)
