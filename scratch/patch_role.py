import re

with open('static/js/chat.js', 'r') as f:
    content = f.read()

# Replace in line 2031-2033
content = re.sub(
    r'var roleLabel = _modelRouteLabel\(modelName, modelName\);\s*var _charNameInit = presetsModule\.getCharacterName \? presetsModule\.getCharacterName\(\) : \'\';\s*if \(_charNameInit\) roleLabel = _charNameInit;',
    r"var roleLabel = _modelRouteLabel(modelName, modelName);\n      var _charNameInit = presetsModule.getCharacterName ? presetsModule.getCharacterName() : '';\n      roleLabel = _charNameInit || 'Aurex';",
    content
)

# Replace in line 4976
content = re.sub(
    r'const roleLabel = _shortModel\(meta && meta\.model\);',
    r"var _charNameInit = presetsModule.getCharacterName ? presetsModule.getCharacterName() : '';\n    const roleLabel = _charNameInit || 'Aurex';",
    content
)

# Replace in line 5225
content = re.sub(
    r'var roleLabel = _shortModel\(meta && meta\.model\);',
    r"var _charNameInit = presetsModule.getCharacterName ? presetsModule.getCharacterName() : '';\n      var roleLabel = _charNameInit || 'Aurex';",
    content
)

with open('static/js/chat.js', 'w') as f:
    f.write(content)

print("Replaced roleLabel in chat.js")
