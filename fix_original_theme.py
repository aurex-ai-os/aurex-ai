import re
with open("static/js/theme.js", "r") as f:
    text = f.read()

# Replace the dark theme palette with the sleek Aurex tokens
old_dark = r"dark:\s*\{ bg:'#282c34', fg:'#9cdef2', panel:'#111111', border:'#355a66', red:'#e06c75' \},"
new_dark = r"dark:       { bg:'#0A0A0A', fg:'#EDEDED', panel:'#141414', border:'#2A2A2A', red:'#337AFF' },"

text = re.sub(old_dark, new_dark, text)

with open("static/js/theme.js", "w") as f:
    f.write(text)
