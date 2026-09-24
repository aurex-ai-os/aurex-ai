with open("src/executor/registration.py", "r") as f:
    text = f.read()
text = text.replace('schemas_by_name = {schema["name"]: schema["parameters"] for schema in FUNCTION_TOOL_SCHEMAS}', 'schemas_by_name = {schema["function"]["name"]: schema["function"].get("parameters", {}) for schema in FUNCTION_TOOL_SCHEMAS if "function" in schema}')
text = text.replace('description=schema.get("description", f"Legacy tool {tool_id}"),', 'description=next((s["function"].get("description", f"Legacy tool {tool_id}") for s in FUNCTION_TOOL_SCHEMAS if "function" in s and s["function"]["name"] == tool_id), f"Legacy tool {tool_id}"),')
with open("src/executor/registration.py", "w") as f:
    f.write(text)
