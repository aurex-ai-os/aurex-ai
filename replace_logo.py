import re

with open("static/index.html", "r") as f:
    text = f.read()

# Replace favicon
# Old: <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 4L16 22L6 22Z' fill='%23e06c75'/%3E%3Cpath d='M16 8L16 22L24 22Z' fill='%23e06c75' opacity='0.6'/%3E%3Cpath d='M4 24Q10 20 16 24Q22 28 28 24' stroke='%23e06c75' stroke-width='2.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
# New spark: <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9Z' fill='%23337AFF'/></svg>
new_favicon = "<link rel=\"icon\" type=\"image/svg+xml\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9Z' fill='%23337AFF'/%3E%3C/svg%3E\">"

text = re.sub(r'<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml.*?">', new_favicon, text)

# Replace welcome screen logo
# Old: <svg class="welcome-boat" viewBox="0 0 32 32"><path d="M16 4L16 22L6 22Z" fill="currentColor"/><path d="M16 8L16 22L24 22Z" fill="currentColor" opacity="0.6"/><path d="M4 24Q10 20 16 24Q22 28 28 24" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/></svg>
new_welcome = '<svg class="welcome-boat" viewBox="0 0 24 24"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9Z" fill="currentColor"/></svg>'

text = re.sub(r'<svg class="welcome-boat" viewBox="0 0 32 32">.*?</svg>', new_welcome, text)

with open("static/index.html", "w") as f:
    f.write(text)
