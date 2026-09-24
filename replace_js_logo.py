import re

with open("static/js/theme.js", "r") as f:
    text = f.read()

old_svg = r"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><path d='M16 4L16 22L6 22Z' fill='\$\{fg\}'/><path d='M16 8L16 22L24 22Z' fill='\$\{fg\}' opacity='0\.6'/><path d='M4 24Q10 20 16 24Q22 28 28 24' stroke='\$\{fg\}' stroke-width='2\.5' fill='none' stroke-linecap='round'/></svg>"
new_svg = r"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9Z' fill='${fg}'/></svg>"

text = re.sub(old_svg, new_svg, text)

with open("static/js/theme.js", "w") as f:
    f.write(text)
