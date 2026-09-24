import re
with open('static/js/chat.js', 'r') as f:
    content = f.read()

# Replace if (opts.characterName) label = opts.characterName;
# with if (opts.characterName) { label = opts.characterName; } else { label = 'Aurex'; }

content = re.sub(
    r'if \(opts\.characterName\) label = opts\.characterName;',
    r"if (opts.characterName) label = opts.characterName;\n    else label = 'Aurex';",
    content
)

with open('static/js/chat.js', 'w') as f:
    f.write(content)

print("Patched _setRoleModelLabel")
