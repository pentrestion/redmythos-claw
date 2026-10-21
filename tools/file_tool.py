"""
REDMYTHOS CLAW 🦀 — Shell Tool
Execute terminal commands safely in a workspace-limited environment.
"""

import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from core.safety import SafetyPolicy


class ShellTool:
    """Safe shell command execution tool."""

    def __init__(self, workspace_root: Optional[str] = None):
        self.policy = SafetyPolicy(workspace_root)
        self.workspace_root = str(self.policy.workspace_root)

    def execute(self, command: str, timeout: int = 30, cwd: Optional[str] = None, env: Optional[dict] = None) -> str:
        """
        Execute a shell command.

        Args:
            command: Shell command to execute
            timeout: Timeout in seconds
            cwd: Working directory
            env: Environment variables

        Returns:
            Command output (stdout + stderr)
        """
        try:
            self.policy.validate_command(command)
        except ValueError as exc:
            return f"❌ BLOCKED: {exc}"

        target_cwd = self.workspace_root if not cwd else self.policy.resolve_workspace_path(cwd)

        safe_env = {**os.environ, **(env or {})}
        safe_env.setdefault("HOME", str(Path.home()))
        safe_env.setdefault("PATH", os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"))

        try:
            cmd_parts = shlex.split(command, posix=True)
            result = subprocess.run(
                cmd_parts,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=target_cwd,
                env=safe_env,
                errors="replace",
            )

            output = []
            if result.stdout.strip():
                output.append(result.stdout.strip())
            if result.stderr.strip():
                output.append(f"STDERR:\n{result.stderr.strip()}")
            if result.returncode != 0:
                output.append(f"Exit code: {result.returncode}")

            if not output:
                return f"✅ Command completed (exit code: {result.returncode})"
            return "\n".join(output)

        except subprocess.TimeoutExpired:
            return f"⏰ Command timed out after {timeout}s: {command}"
        except FileNotFoundError as exc:
            return f"❌ Command not found: {exc}"
        except Exception as exc:
            return f"❌ Shell error: {exc}"

    def run_script(self, script_content: str, language: str = "bash", timeout: int = 60) -> str:
        """
        Run a script by writing to a temporary workspace file and executing it.

        Args:
            script_content: Script code
            language: bash/python/node/ruby/go/rust
            timeout: Timeout in seconds
        """
        extensions = {
            "bash": ".sh",
            "python": ".py",
            "python3": ".py",
            "node": ".js",
            "javascript": ".js",
            "ruby": ".rb",
            "perl": ".pl",
            "php": ".php",
        }

        interpreters = {
            "bash": "bash",
            "python": "python3",
            "python3": "python3",
            "node": "node",
            "javascript": "node",
            "ruby": "ruby",
            "perl": "perl",
            "php": "php",
        }

        normalized_language = language.lower()
        if normalized_language not in interpreters:
            return f"❌ Script language '{language}' is not allowed"

        ext = extensions[normalized_language]
        interpreter = interpreters[normalized_language]

        storage_dir = Path(self.workspace_root) / ".tmp"
        storage_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=ext,
            dir=str(storage_dir),
            delete=False,
            prefix="redmythos_",
        ) as handle:
            handle.write(script_content)
            temp_path = handle.name

        try:
            return self.execute(f"{interpreter} {shlex.quote(temp_path)}", timeout=timeout, cwd=self.workspace_root)
        finally:
            Path(temp_path).unlink(missing_ok=True)
