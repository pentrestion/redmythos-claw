"""
Centralized safety helpers for REDMYTHOS CLAW.
Provides workspace isolation, command allowlisting, and public-only URL validation.
"""

from __future__ import annotations

import ipaddress
import os
import re
import shlex
from pathlib import Path
from urllib.parse import urlparse


class SafetyPolicy:
    """Restrict unsafe filesystem and shell access to safe defaults."""

    ALLOWED_COMMANDS = {
        "ls",
        "pwd",
        "echo",
        "cat",
        "head",
        "tail",
        "grep",
        "find",
        "python",
        "python3",
        "git",
        "node",
        "npm",
        "npx",
        "pip",
        "pip3",
        "jq",
        "sed",
        "awk",
        "uname",
        "whoami",
        "which",
    }

    BLOCKED_PATTERNS = [
        r"rm\s+-rf\s+/?",
        r"mkfs",
        r"dd\s+if=/dev/zero",
        r":\(\)\s*\{\s*:\s*\|\s*:&\s*\}\s*;\s*:",
        r"chmod\s+777",
        r"wget\s+.*\|\s*(bash|sh)",
        r"curl\s+.*\|\s*(bash|sh)",
    ]

    def __init__(self, workspace_root: str | None = None):
        base = Path(workspace_root).expanduser() if workspace_root else Path.home() / ".redmythos" / "workspace"
        self.workspace_root = base.resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def resolve_workspace_path(self, user_path: str) -> str:
        """Resolve a user path and enforce that it stays inside the workspace root."""
        if not user_path or user_path in (".", "./"):
            return str(self.workspace_root)

        candidate = Path(user_path).expanduser()
        if not candidate.is_absolute():
            candidate = (self.workspace_root / candidate).resolve()
        else:
            candidate = candidate.resolve()

        try:
            candidate.relative_to(self.workspace_root)
        except ValueError as exc:
            raise ValueError(f"Access denied: '{user_path}' is outside the workspace root") from exc

        return str(candidate)

    def validate_command(self, command: str) -> list[str]:
        """Reject risky shell operations and enforce a limited command allowlist."""
        if not command or not command.strip():
            raise ValueError("Empty command is not allowed")

        normalized = command.strip()
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, normalized, flags=re.IGNORECASE):
                raise ValueError(f"Dangerous command pattern blocked: {normalized[:120]}")

        if any(token in normalized for token in (";", "&&", "||", "|", "`", "$(", ">", "<")):
            raise ValueError("Shell operators are blocked for safety")

        parts = shlex.split(normalized, posix=True)
        if not parts:
            raise ValueError("Command parsed to empty input")

        executable = os.path.basename(parts[0])
        if executable not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command '{executable}' is not allowed in this environment")

        return parts

    def validate_url(self, url: str) -> str:
        """Reject local/private targets and require public http(s) URLs."""
        parsed = urlparse(url)
        if parsed.scheme.lower() not in {"http", "https"}:
            raise ValueError("Only http:// and https:// URLs are permitted")

        hostname = (parsed.hostname or "").lower()
        if not hostname:
            raise ValueError("URL hostname is missing")

        if hostname in {"localhost", "0.0.0.0", "127.0.0.1", "::1"}:
            raise ValueError("Local network targets are blocked")

        try:
            ip = ipaddress.ip_address(hostname)
        except ValueError:
            ip = None

        if ip is not None and (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise ValueError(f"Private or reserved network target blocked: {hostname}")

        return url
