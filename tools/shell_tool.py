"""
REDMYTHOS CLAW 🦀 — Search Tool
Search for patterns in files and directories.
"""

import os
import re
from pathlib import Path
from typing import Optional


class SearchTool:
    """Search files and directories for patterns."""

    def execute(self, pattern: str, path: str = ".",
                file_type: Optional[str] = None,
                case_sensitive: bool = False,
                max_results: int = 50) -> str:
        """
        Search for a pattern in files.

        Args:
            pattern: Search pattern or regex
            path: Directory or file to search
            file_type: Filter by extension (e.g., 'py', 'js')
            case_sensitive: Case sensitive search
            max_results: Max results to return
        """
        expanded_path = os.path.expanduser(path)
        base_path = Path(expanded_path).resolve(strict=False)

        if not base_path.exists():
            return f"❌ Path not found: {path}"

        results = []
        flags = 0 if case_sensitive else re.IGNORECASE

        try:
            regex = re.compile(pattern, flags)
        except re.error:
            regex = re.compile(re.escape(pattern), flags)

        if base_path.is_file():
            files_to_search = [base_path]
        else:
            files_to_search = []
            for root, dirs, files in os.walk(base_path, topdown=True, followlinks=False):
                root_path = Path(root).resolve(strict=False)
                dirs[:] = [
                    d for d in dirs
                    if not d.startswith('.')
                    and d not in ['node_modules', '__pycache__', '.git', 'venv', 'env']
                    and not (root_path / d).is_symlink()
                ]

                for file in files:
                    file_path = (root_path / file).resolve(strict=False)
                    try:
                        file_path.relative_to(base_path.resolve())
                    except ValueError:
                        continue

                    if file_path.is_symlink():
                        continue

                    if file_type:
                        if not file_path.name.endswith(f".{file_type.lstrip('.')}"):
                            continue
                    files_to_search.append(file_path)

        for file_path in files_to_search:
            if len(results) >= max_results:
                break

            try:
                if file_path.is_symlink():
                    continue
                if not file_path.exists():
                    continue
                resolved_file = file_path.resolve(strict=False)
                try:
                    resolved_file.relative_to(base_path.resolve())
                except ValueError:
                    continue

                content = resolved_file.read_text(encoding='utf-8', errors='replace')
                lines = content.split('\n')

                for line_num, line in enumerate(lines, 1):
                    if regex.search(line):
                        results.append(f"📄 {resolved_file}:{line_num}: {line.strip()}")
                        if len(results) >= max_results:
                            break
            except Exception:
                continue

        if not results:
            return f"🔍 No matches found for '{pattern}' in {path}"

        header = f"🔍 Found {len(results)} match(es) for '{pattern}':\n"
        if len(results) >= max_results:
            header += f"(Showing first {max_results} results)\n"

        return header + "\n".join(results)
