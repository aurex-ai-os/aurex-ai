import re

with open("static/index.html", "r") as f:
    content = f.read()

old_code = """      <div class="list-item" id="sidebar-pi-btn" title="Provider Intelligence Center">
        <svg class="sidebar-action-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="position:relative;left:-2px;"><path d="M2 12h4l3-9 5 18 3-9h5"/></svg>
        <span class="grow" style="position:relative;left:-4px;">Intelligence</span>
      </div>"""

new_code = """      <div class="list-item" id="sidebar-pi-btn" title="Provider Intelligence Center">
        <svg class="sidebar-action-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="position:relative;left:-6px;"><path d="M2 12h4l3-9 5 18 3-9h5"/></svg>
        <span class="grow" style="position:relative;left:-8px;">Intelligence</span>
      </div>"""

content = content.replace(old_code, new_code)

with open("static/index.html", "w") as f:
    f.write(content)
