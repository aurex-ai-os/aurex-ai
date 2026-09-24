import re
with open('static/js/chat.js', 'r') as f:
    content = f.read()

content = re.sub(
    r'const agentModelLabel = _shortModel\(agentMeta\?\.model\);',
    r"const agentModelLabel = presetsModule.getCharacterName ? presetsModule.getCharacterName() : 'Aurex';",
    content
)

content = re.sub(
    r'_role\.textContent = _shortModel\(_meta\?\.model\);',
    r"_role.textContent = presetsModule.getCharacterName ? presetsModule.getCharacterName() : 'Aurex';",
    content
)

with open('static/js/chat.js', 'w') as f:
    f.write(content)

print("Patched remaining _shortModel occurrences")
