import re
with open("src/agent_tools/filesystem_tools.py", "r") as f:
    content = f.read()

# Replace the specific diff application block with secure executor requests
secure_apply = """            diffs = []
            for kind, path, old, new in prepared:
                if kind == "delete":
                    req = ExecutionRequest(
                        operation_type="DeleteFile",
                        arguments={"path": path},
                        origin_tool="apply_patch"
                    )
                else:
                    req = ExecutionRequest(
                        operation_type="WriteFile",
                        arguments={"path": path, "content": new},
                        origin_tool="apply_patch"
                    )
                policy = PolicyEngine(get_app_root())
                decision = policy.evaluate(req)
                if decision.decision in [DecisionType.FORBIDDEN, DecisionType.ASK]:
                    return {"error": f"PolicyEngine denied patch mutation: {decision.reason}", "exit_code": 1}
                
                action = ApprovedAction(req, decision)
                await SecureExecutor.execute_fs(action)
                
                diff = _unified_diff(old, new, path)
                if diff:
                    diffs.append(diff)"""

content = re.sub(r'            diffs = \[\]\n            for kind, path, old, new in prepared:.*?(?=\n        except \(ValueError, UnicodeDecodeError, PermissionError, OSError\))', secure_apply, content, flags=re.DOTALL)

with open("src/agent_tools/filesystem_tools.py", "w") as f:
    f.write(content)
