"""
REDMYTHOS CLAW 🦀 — Shell Tool
Execute terminal commands safely in Termux.
Only allows direct argument execution without shell metacharacters.
"""

import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class ShellTool:
    """Safe shell command execution tool."""

    BLOCKED_COMMANDS = [
        "rm -rf /",
        "rm -rf /*",
        "mkfs",
        "dd if=/dev/zero",
        ":(){:|:&};:",
    ]

    ALLOWED_INTERPRETERS = {
        "bash",
        "python",
        "python3",
        "node",
        "ruby",
        "perl",
        "php",
    }

    DANGEROUS_SHELL_CHARS = (";", "&&", "||", "|", ">", "<", "`", "$(")

    def execute(self, command: str, timeout: int = 30,
                cwd: Optional[str] = None,
                env: Optional[dict] = None) -> str:
        """
        Execute a shell command using argument arrays instead of shell=True.

        Args:
            command: Shell command to execute
            timeout: Timeout in seconds
            cwd: Working directory
            env: Environment variables

        Returns:
            Command output (stdout + stderr)
        """
        if not isinstance(command, str) or not command.strip():
            return "❌ Empty command provided."

        normalized = command.strip()
        for blocked in self.BLOCKED_COMMANDS:
            if blocked in normalized:
                return f"❌ BLOCKED: Dangerous command detected: {blocked}"

        if any(token in normalized for token in self.DANGEROUS_SHELL_CHARS):
            return (
                "❌ Refusing command because it contains shell operators that can be used "
                "for command injection or redirection."
            )

        try:
            argv = shlex.split(normalized, posix=True)
        except ValueError as exc:
            return f"❌ Invalid command syntax: {exc}"

        if not argv:
            return "❌ Empty command after parsing."

        executable = Path(argv[0]).name
        if executable not in self.ALLOWED_INTERPRETERS and not os.path.isabs(argv[0]):
            return f"❌ BLOCKED: Command '{argv[0]}' is not allowed in this environment"

        if cwd:
            cwd = os.path.expanduser(cwd)
            if not os.path.isdir(cwd):
                return f"❌ Working directory does not exist: {cwd}"

        try:
            result = subprocess.run(
                argv,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env={**os.environ, **(env or {})},
                errors='replace'
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
            return f"⏰ Command timed out after {timeout}s: {normalized}"
        except FileNotFoundError as exc:
            return f"❌ Command not found: {exc}"
        except Exception as exc:
            return f"❌ Shell error: {exc}"

    def run_script(self, script_content: str,
                   language: str = "python3",
                   timeout: int = 60) -> str:
        """
        Run a script by writing to temp file and executing it.

        Args:
            script_content: Script code
            language: bash/python/node/ruby/go/rust
            timeout: Timeout in seconds
        """
        language = (language or "python3").lower()
        if language not in self.ALLOWED_INTERPRETERS:
            return f"❌ BLOCKED: Interpreter '{language}' is not allowed in this environment"

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

        ext = extensions.get(language, ".sh")
        interpreter = interpreters.get(language, language)

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=ext,
            delete=False,
            prefix="redmythos_"
        ) as temp_file:
            temp_file.write(script_content)
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [interpreter, temp_path],
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                errors='replace'
            )

            output = []
            if result.stdout.strip():
                output.append(result.stdout.strip())
            if result.stderr.strip():
                output.append(f"STDERR:\n{result.stderr.strip()}")
            if result.returncode != 0:
                output.append(f"Exit code: {result.returncode}")
            return "\n".join(output) if output else f"✅ Script completed (exit code: {result.returncode})"
        except subprocess.TimeoutExpired:
            return f"⏰ Script timed out after {timeout}s"
        except FileNotFoundError as exc:
            return f"❌ Interpreter not found: {exc}"
        except Exception as exc:
            return f"❌ Shell script error: {exc}"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    @staticmethod
    def _is_allowed_executable(command: str) -> bool:
        """Return True when an executable is explicitly allowed."""
        return Path(command).name.lower() in ShellTool.ALLOWED_INTERPRETERS


__all__ = ["ShellTool"]
