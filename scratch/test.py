with open('static/index.html', 'r') as f:
    html = f.read()

tools_start = html.find('<div class="section" id="tools-section">')
user_bar = html.find('<div class="sidebar-user-bar">')
tools_end = html.rfind('      </div>\n', tools_start, user_bar)
print(f"tools_start: {tools_start}, user_bar: {user_bar}, tools_end: {tools_end}")
