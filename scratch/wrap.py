import re

with open('static/index.html', 'r') as f:
    html = f.read()

# The start of attach-strip
start_pattern = r'    <!-- Attachments strip -->'
# The end of chat-input-bar
end_pattern = r'    <form id="chat-form"'

start_idx = html.find(start_pattern)
end_idx = html.find(end_pattern)

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + '    <!-- Input Island Wrapper -->\n    <div class="input-island-wrapper">\n' + html[start_idx:end_idx] + '    </div>\n' + html[end_idx:]
    with open('static/index.html', 'w') as f:
        f.write(new_html)
    print("Wrapped input island successfully.")
else:
    print("Failed to find patterns.")
