import re

with open("static/index.html", "r") as f:
    content = f.read()

# Insert the new Provider Intelligence button into the left panel
old_nav = """      <div class="list-item" id="sidebar-search-btn" title="Search conversations (Ctrl+K)">
        <svg class="sidebar-action-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="10" cy="10" r="7"/><path d="M21 21l-4.35-4.35"/></svg>
        <span class="grow" style="position:relative;left:-1px;">Search</span>
      </div>"""

new_nav = old_nav + """
      <div class="list-item" id="sidebar-pi-btn" title="Provider Intelligence Center">
        <svg class="sidebar-action-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M2 12h4l3-9 5 18 3-9h5"/></svg>
        <span class="grow" style="position:relative;left:-1px;">Intelligence</span>
      </div>"""

if "id=\"sidebar-pi-btn\"" not in content:
    content = content.replace(old_nav, new_nav)

with open("static/index.html", "w") as f:
    f.write(content)
