"""
REDMYTHOS CLAW 🦀 — Fix Tool
Analyze errors and suggest/apply fixes.
Uses Gemini to understand and fix code errors.
"""

from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()

class FixTool:
    """Auto-fix code errors using AI analysis."""

    def execute(self, error: str, file_path: Optional[str] = None,
                language: Optional[str] = None) -> str:
        """
        Analyze an error and suggest a fix.
        
        Args:
            error: Error message or traceback
            file_path: Path to the file with error
            language: Programming language
            
        Returns:
            Fix suggestion or applied fix
        """
        result = []
        result.append(f"🔧 ERROR ANALYSIS:\n{error[:500]}\n")
        
        # Read the file if provided
        file_content = ""
        if file_path:
            p = Path(file_path)
            if p.exists():
                file_content = p.read_text(encoding='utf-8', errors='replace')
                result.append(f"📄 File: {file_path}\n")
                
                # Try to detect language from extension
                if not language:
                    ext_map = {
                        '.py': 'Python', '.js': 'JavaScript',
                        '.ts': 'TypeScript', '.go': 'Go',
                        '.rs': 'Rust', '.rb': 'Ruby',
                        '.php': 'PHP', '.sh': 'Bash',
                        '.java': 'Java', '.cpp': 'C++',
                    }
                    language = ext_map.get(p.suffix, 'Unknown')

        # Common error patterns and fixes
        fixes = self._common_fixes(error)
        if fixes:
            result.append(f"💡 QUICK FIX:\n{fixes}\n")
        
        # Extract line number from error
        line_num = self._extract_line_number(error)
        if line_num and file_content:
            lines = file_content.split('\n')
            if line_num <= len(lines):
                start = max(0, line_num - 3)
                end = min(len(lines), line_num + 2)
                context = '\n'.join([
                    f"{'→ ' if i+start+1 == line_num else '  '}"
                    f"{i+start+1}: {lines[i+start]}"
                    for i in range(end - start)
                ])
                result.append(f"📍 ERROR LOCATION:\n{context}\n")

        result.append(
            "🤖 Pass this error to Gemini agent for AI-powered fix suggestion."
        )
        
        return '\n'.join(result)

    def _extract_line_number(self, error: str) -> Optional[int]:
        """Extract line number from error message."""
        import re
        patterns = [
            r'line (\d+)',
            r':(\d+):',
            r'at line (\d+)',
            r'Line (\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, error)
            if match:
                return int(match.group(1))
        return None

    def _common_fixes(self, error: str) -> str:
        """Suggest fixes for common errors."""
        error_lower = error.lower()
        
        fixes = {
            "modulenotfounderror": "Run: pip install {module_name} --break-system-packages",
            "importerror": "Check if package is installed: pip list | grep {package}",
            "syntaxerror": "Check for missing colons, brackets, or indentation",
            "indentationerror": "Fix indentation — use spaces not tabs (4 spaces per level)",
            "nameerror": "Variable is not defined — check spelling and scope",
            "typeerror": "Wrong data type — check function arguments",
            "filenotfounderror": "File path doesn't exist — check the path with ls",
            "permissionerror": "Run with proper permissions or check file ownership",
            "connectionrefused": "Service not running — start the service first",
            "port already in use": "Kill existing process: lsof -ti:{port} | xargs kill",
            "command not found": "Install the package: pkg install {command}",
            "no module named": "Install: pip install {module} --break-system-packages",
        }
        
        for pattern, fix in fixes.items():
            if pattern in error_lower:
                return fix
        
        return ""
