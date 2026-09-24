import re

with open("src/tool_execution.py", "r") as f:
    content = f.read()

secure_bg_tool = """
        _is_bg, _bg_cmd = _split_bg_marker(content)
        if _is_bg and _bg_cmd:
            from src import bg_jobs
            try:
                rec = bg_jobs.launch(_bg_cmd, session_id=session_id, cwd=agent_cwd())
            except Exception as e:
                return "bash (background)", {"error": str(e), "exit_code": 1}
"""

content = re.sub(r'        _is_bg, _bg_cmd = _split_bg_marker\(content\)\n        if _is_bg and _bg_cmd:\n            from src import bg_jobs\n            rec = bg_jobs.launch\(_bg_cmd, session_id=session_id, cwd=agent_cwd\(\)\)', secure_bg_tool, content)

with open("src/tool_execution.py", "w") as f:
    f.write(content)
