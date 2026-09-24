import re

with open('static/index.html', 'r') as f:
    html = f.read()

# Replace overflow-plus-btn contents
old_btn = """            <button type="button" class="input-icon-btn overflow-plus-btn" id="overflow-plus-btn" title="More tools" aria-label="More tools" aria-haspopup="true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 15 12 9 18 15"/>
              </svg>
              <span class="plus-active-dot"></span>
            </button>"""

# We'll use a paperclip icon
new_btn = """            <button type="button" class="input-icon-btn overflow-plus-btn" id="overflow-plus-btn" title="Attach files and context" aria-label="Attach context" aria-haspopup="true">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
              </svg>
              <span class="plus-btn-label">Attach</span>
              <span class="plus-active-dot"></span>
            </button>"""

if old_btn in html:
    html = html.replace(old_btn, new_btn)
else:
    print("Could not find old_btn")

# Also let's add the welcome-tip for Drag-and-Drop Hint
old_welcome = """      <div class="welcome-tip" id="welcome-tip"></div>"""
new_welcome = """      <div class="welcome-tip" id="welcome-tip"></div>
      <div class="welcome-drag-hint" style="opacity: 0.35; font-size: 12px; margin-top: 16px;">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -1px; margin-right: 4px;"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>Drag & drop files here to begin
      </div>"""

if old_welcome in html:
    html = html.replace(old_welcome, new_welcome)

with open('static/index.html', 'w') as f:
    f.write(html)
print("Patched + button and welcome hint")
