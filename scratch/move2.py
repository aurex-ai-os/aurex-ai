import re

with open('static/index.html', 'r') as f:
    html = f.read()

# 1. Extract the details block
start_idx = html.find('<details class="advanced-tools-details"')
end_idx = html.find('</details>', start_idx) + len('</details>\n')

if start_idx == -1:
    print("Could not find advanced-tools-details")
    exit(1)

details_block = html[start_idx:end_idx]
html = html[:start_idx] + html[end_idx:]

# 2. Find the correct insertion point
# We want to insert it at the end of tools-section.
# tools-section ends right before the closing of sidebar-inner.
# And sidebar-inner closes right before sidebar-user-bar.
user_bar_idx = html.find('<div class="sidebar-user-bar" id="sidebar-user-bar">')
if user_bar_idx == -1:
    print("Could not find sidebar-user-bar")
    exit(1)

# Find the end of tools-section which is two '</div>' before user_bar
# Wait, let's just insert it right before the last </div> of tools-section.
tools_start = html.find('<div class="section" id="tools-section">')
tools_end = html.rfind('      </div>\n', tools_start, user_bar_idx)

if tools_end != -1:
    html = html[:tools_end] + details_block + html[tools_end:]
    with open('static/index.html', 'w') as f:
        f.write(html)
    print("Moved correctly!")
else:
    print("Could not find tools_end")

