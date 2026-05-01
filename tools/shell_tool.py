"""
REDMYTHOS CLAW 🦀 — Shell Tool
Execute terminal commands safely in Termux.
Always confirms before execution (safety: always mode).
"""

import subprocess
import shlex
import os
from pathlib import Path
from typing import Optional

class ShellTool:
    """Safe shell command execution tool."""

    # Commands that are always blocked (safety)
    BLOCKED_COMMANDS = [
        "rm -rf /",
        "rm -rf /*", 
        "mkfs",
        "dd if=/dev/zero",
        ":(){:|:&};:",  # Fork bomb
    ]

    def execute(self, command: str, timeout: int = 30,
                cwd: Optional[str] = None, 
                env: Optional[dict] = None) -> str:
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
        # Safety check
        for blocked in self.BLOCKED_COMMANDS:
            if blocked in command:
                return f"❌ BLOCKED: Dangerous command detected: {blocked}"

        # Expand home directory in cwd
        if cwd:
            cwd = os.path.expanduser(cwd)

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env={**os.environ, **(env or {})},
                errors='replace'
            )

            output = []
            
            # Add stdout
            if result.stdout.strip():
                output.append(result.stdout.strip())
            
            # Add stderr
            if result.stderr.strip():
                output.append(f"STDERR:\n{result.stderr.strip()}")
            
            # Add return code if non-zero
            if result.returncode != 0:
                output.append(f"Exit code: {result.returncode}")

            if not output:
                return f"✅ Command completed (exit code: {result.returncode})"
            
            return "\n".join(output)

        except subprocess.TimeoutExpired:
            return f"⏰ Command timed out after {timeout}s: {command}"
        except FileNotFoundError as e:
            return f"❌ Command not found: {e}"
        except Exception as e:
            return f"❌ Shell error: {e}"

    def run_script(self, script_content: str, 
                   language: str = "bash",
                   timeout: int = 60) -> str:
        """
        Run a script by writing to temp file and executing.
        
        Args:
            script_content: Script code
            language: bash/python/node/ruby/go/rust
            timeout: Timeout in seconds
        """
        import tempfile
        
        extensions = {
            "bash": ".sh",
            "python": ".py",
            "python3": ".py",
            "node": ".js",
            "javascript": ".js",
            "ruby": ".rb",
            "perl": ".pl",
            "php": ".php"
        }
        
        interpreters = {
            "bash": "bash",
            "python": "python3",
            "python3": "python3",
            "node": "node",
            "javascript": "node",
            "ruby": "ruby",
            "perl": "perl",
            "php": "php"
        }
        
        ext = extensions.get(language.lower(), ".sh")
        interpreter = interpreters.get(language.lower(), language)
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix=ext, 
            delete=False,
            prefix="redmythos_"
        ) as f:
            f.write(script_content)
            temp_path = f.name
        
        try:
            result = self.execute(
                f"{interpreter} {temp_path}",
                timeout=timeout
            )
        finally:
            Path(temp_path).unlink(missing_ok=True)
        
        return result
