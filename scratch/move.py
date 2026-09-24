import re

with open('static/index.html', 'r') as f:
    html = f.read()

# Extract <details class="advanced-tools-details"... </details>
start_idx = html.find('<details class="advanced-tools-details"')
end_idx = html.find('</details>', start_idx) + len('</details>\n')

details_block = html[start_idx:end_idx]
html = html[:start_idx] + html[end_idx:]

# Find tools-section
tools_start = html.find('<div class="section" id="tools-section">')
# Find the end of tools-section (it's the next closing div that matches the level)
# Let's just find <div class="sidebar-user-bar"> which is after tools-section
user_bar = html.find('<div class="sidebar-user-bar">')
# Look back for the closing div
tools_end = html.rfind('      </div>\n', tools_start, user_bar)

html = html[:tools_end] + '        ' + details_block + html[tools_end:]

with open('static/index.html', 'w') as f:
    f.write(html)
print("Moved details block.")
