"""
REDMYTHOS CLAW 🦀 — Search Tool
Search for patterns in files and directories.
"""

import os
import re
from pathlib import Path
from typing import Optional

from core.safety import SafetyPolicy


class SearchTool:
    """Search files and directories for patterns."""

    def __init__(self, workspace_root: Optional[str] = None):
        self.policy = SafetyPolicy(workspace_root)
        self.workspace_root = str(self.policy.workspace_root)

    def execute(self, pattern: str, path: str = ".", file_type: Optional[str] = None, case_sensitive: bool = False, max_results: int = 50) -> str:
        """
        Search for a pattern in files.

        Args:
            pattern: Search pattern or regex
            path: Directory or file to search
            file_type: Filter by extension (e.g., 'py', 'js')
            case_sensitive: Case sensitive search
            max_results: Max results to return
        """
        try:
            search_root = self.policy.resolve_workspace_path(path)
        except ValueError as exc:
            return f"❌ {exc}"

        p = Path(search_root)
        if not p.exists():
            return f"❌ Path not found: {search_root}"

        results = []
        flags = 0 if case_sensitive else re.IGNORECASE

        try:
            regex = re.compile(pattern, flags)
        except re.error:
            regex = re.compile(re.escape(pattern), flags)

        if p.is_file():
            files_to_search = [p]
        else:
            files_to_search = []
            for root, dirs, files in os.walk(search_root):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", "__pycache__", ".git", "venv", "env"]]
                for file in files:
                    file_path = Path(root) / file
                    if file_type:
                        if not file.endswith(f".{file_type.lstrip('.')}"):
                            continue
                    files_to_search.append(file_path)

        for file_path in files_to_search:
            if len(results) >= max_results:
                break
            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                for line_num, line in enumerate(content.split("\n"), 1):
                    if regex.search(line):
                        results.append(f"📄 {file_path}:{line_num}: {line.strip()}")
                        if len(results) >= max_results:
                            break
            except Exception:
                continue

        if not results:
            return f"🔍 No matches found for '{pattern}' in {search_root}"

        header = f"🔍 Found {len(results)} match(es) for '{pattern}':\n"
        if len(results) >= max_results:
            header += f"(Showing first {max_results} results)\n"

        return header + "\n".join(results)
