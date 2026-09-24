import re

with open("static/index.html", "r") as f:
    text = f.read()

sidebar_svg = """<svg class="sidebar-logo" viewBox="0 0 32 32" style="width:18px;height:18px;margin-right:6px;color:var(--brand-color, var(--red));">
          <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.2"/>
          <path d="M16 4 L5 24 L11 24 L16 14 Z" fill="currentColor" opacity="0.5"/>
          <path d="M16 4 L27 24 L21 24 L16 14 Z" fill="currentColor" opacity="0.9"/>
          <path d="M16 17 L19 20 L16 23 L13 20 Z" fill="currentColor"/>
        </svg>"""

text = re.sub(r'<span class="sidebar-brand-title">Aurex</span>', sidebar_svg + '\n        <span class="sidebar-brand-title">Aurex</span>', text)

with open("static/index.html", "w") as f:
    f.write(text)
