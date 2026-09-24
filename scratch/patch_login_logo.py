import re

with open('static/login.html', 'r') as f:
    html = f.read()

old_logo = '<svg class="logo-boat" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path d="M16 4L16 22L6 22Z" fill="currentColor"/><path d="M16 8L16 22L24 22Z" fill="currentColor" opacity="0.6"/><path d="M4 24Q10 20 16 24Q22 28 28 24" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/></svg>'

new_logo = '<svg class="logo-boat" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="2.5" fill="none" opacity="0.4"/><path d="M16 4 L5 24 L11 24 L16 14 Z" fill="currentColor" opacity="0.5"/><path d="M16 4 L27 24 L21 24 L16 14 Z" fill="currentColor" opacity="0.9"/><path d="M16 17 L19 20 L16 23 L13 20 Z" fill="currentColor"/></svg>'

if old_logo in html:
    html = html.replace(old_logo, new_logo)
    with open('static/login.html', 'w') as f:
        f.write(html)
    print("Replaced logo in login.html")
else:
    print("Could not find old logo in login.html")
