import sys
with open("src/executor/executor.py", "r") as f:
    content = f.read()

exec_code = """
    @staticmethod
    async def execute_exec(action: ApprovedAction, *args: str, timeout: int = 60, env=None) -> dict:
        req = action.request
        cwd = req.working_directory
        start_time = time.time()
        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                cwd=cwd,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
                status = "SUCCESS" if proc.returncode == 0 else "FAILED"
                log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", status, time.time() - start_time)
                return {
                    "stdout": sanitize_secrets(stdout.decode(errors='replace'))[:10000],
                    "stderr": sanitize_secrets(stderr.decode(errors='replace'))[:10000],
                    "returncode": proc.returncode
                }
            except (asyncio.TimeoutError, TimeoutError):
                proc.terminate()
                await proc.wait()
                log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "TIMEOUT", time.time() - start_time)
                raise Timeout(f"Execution timed out after {timeout} seconds")
        except ExecutorError:
            raise
        except asyncio.CancelledError:
            log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "CANCELLED", time.time() - start_time)
            raise Cancelled("Execution was cancelled")
        except Exception as e:
            log_audit_event(req.task_id or "N/A", req.origin_tool, req.operation_type, "ALLOW", "ERROR", time.time() - start_time, error=str(e))
            raise ExecutionFailed(f"Failed to execute: {str(e)}")
"""

content = content + exec_code
with open("src/executor/executor.py", "w") as f:
    f.write(content)
