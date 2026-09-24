import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

# Replace the overly aggressive body background override
new_body = r"""
body.bg-pattern-none,
body.bg-pattern-solid {
  /* Subtle ambient light only when no heavy pattern is active */
  background: radial-gradient(circle at 10% 0%, color-mix(in srgb, var(--aurex-accent) 12%, var(--aurex-bg)), var(--aurex-bg) 50%), 
              radial-gradient(circle at 90% 100%, color-mix(in srgb, var(--aurex-accent) 8%, var(--aurex-bg)), var(--aurex-bg) 50%) !important;
  background-attachment: fixed !important;
}

body {
  background-color: var(--aurex-bg);
}
"""

text = re.sub(r'body \{\n  /\* Subtle ambient light in the background to give the frosted glass something to refract \*/\n  background: radial-gradient\(.*?\) !important;\n  background-color: var\(--aurex-bg\) !important;\n  background-attachment: fixed !important;\n\}', new_body.strip('\n'), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)
