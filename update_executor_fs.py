import os
with open("src/executor/executor.py", "r") as f:
    content = f.read()

# Make sure we import shutil and os in executor.py
if "import shutil" not in content:
    content = "import shutil\nimport os\n" + content

# Add secure environment filtering
env_filter_code = """
    @staticmethod
    def _sanitize_env(env: dict) -> dict:
        if not env:
            return {}
        safe_env = {}
        # Block known secret patterns in env keys
        blocked_substrings = ["API_KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "AUTH"]
        for k, v in env.items():
            k_upper = k.upper()
            if any(sub in k_upper for sub in blocked_substrings):
                continue
            safe_env[k] = v
        return safe_env
"""

if "_sanitize_env" not in content:
    # insert before execute_shell
    content = content.replace("    @staticmethod\n    async def execute_shell", env_filter_code + "\n    @staticmethod\n    async def execute_shell")
    content = content.replace("env=env,", "env=SecureExecutor._sanitize_env(env),")
    content = content.replace("env=_subproc_env,", "env=SecureExecutor._sanitize_env(_subproc_env),") # In case it's named differently

# Add file system mutators
fs_code = """
    @staticmethod
    async def execute_fs(action: ApprovedAction) -> dict:
        req = action.request
        op = req.operation_type
        args = req.arguments
        
        try:
            if op == "WriteFile":
                path = args.get("path")
                content = args.get("content", "")
                mode = args.get("mode", "w")
                with open(path, mode) as f:
                    f.write(content)
                return {"status": "SUCCESS"}
            elif op == "DeleteFile":
                path = args.get("path")
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                return {"status": "SUCCESS"}
            elif op == "MoveFile" or op == "CopyFile":
                src = args.get("path")
                dst = args.get("destination")
                if op == "MoveFile":
                    shutil.move(src, dst)
                else:
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                return {"status": "SUCCESS"}
            elif op == "MakeDirectory":
                path = args.get("path")
                os.makedirs(path, exist_ok=True)
                return {"status": "SUCCESS"}
            else:
                raise ExecutionFailed(f"Unsupported FS operation: {op}")
        except Exception as e:
            # Do not leak absolute paths that might contain user names in generic exceptions if we can avoid it, 
            # but we already sanitize secrets.
            err_msg = sanitize_secrets(str(e))
            log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "ERROR", error=err_msg)
            raise ExecutionFailed(f"FS operation failed: {err_msg}")
"""

if "execute_fs" not in content:
    content += fs_code

with open("src/executor/executor.py", "w") as f:
    f.write(content)
