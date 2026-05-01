"""
REDMYTHOS CLAW 🦀 — Search Tool
Search for patterns in files and directories.
"""

import os
import re
from pathlib import Path
from typing import List, Optional

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
        path = os.path.expanduser(path)
        p = Path(path)
        
        if not p.exists():
            return f"❌ Path not found: {path}"

        results = []
        flags = 0 if case_sensitive else re.IGNORECASE

        try:
            regex = re.compile(pattern, flags)
        except re.error:
            # Not a regex, search as literal string
            regex = re.compile(re.escape(pattern), flags)

        # Search files
        if p.is_file():
            files_to_search = [p]
        else:
            files_to_search = []
            for root, dirs, files in os.walk(path):
                # Skip hidden and common ignore dirs
                dirs[:] = [d for d in dirs if not d.startswith('.') 
                           and d not in ['node_modules', '__pycache__', 
                                        '.git', 'venv', 'env']]
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
                content = file_path.read_text(encoding='utf-8', errors='replace')
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    if regex.search(line):
                        results.append(
                            f"📄 {file_path}:{line_num}: {line.strip()}"
                        )
                        if len(results) >= max_results:
                            break
            except Exception:
                continue  # Skip unreadable files

        if not results:
            return f"🔍 No matches found for '{pattern}' in {path}"
        
        header = f"🔍 Found {len(results)} match(es) for '{pattern}':\n"
        if len(results) >= max_results:
            header += f"(Showing first {max_results} results)\n"
        
        return header + "\n".join(results)
