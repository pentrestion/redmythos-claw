"""
REDMYTHOS CLAW 🦀 — Mode Loader
Reads .md files from ~/.redmythos/modes/
and converts them into agent configurations.

MODE FILE FORMAT:
----------------
# Mode Name

## Description
Short description of this mode.

## Role
You are an expert in...

## Tools
- file_tool: enabled/disabled/read-only
- shell_tool: enabled/disabled
- web_tool: enabled/disabled
- search_tool: enabled/disabled
- fix_tool: enabled/disabled

## MCP Servers
- server-name: url or local

## Extensions
- extension_name

## Safety
confirm: always/dangerous_only/never

## Format
How responses should be formatted...

## Prompt Prefix
Text added before every message...
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console

console = Console()

class ModeLoader:
    """
    Loads and parses .md mode files from ~/.redmythos/modes/
    Users can drop any .md file to add new modes instantly.
    """

    def __init__(self):
        self.modes_dir = Path.home() / ".redmythos" / "modes"
        self.modes_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Dict] = {}
        self._ensure_default_modes()

    def _ensure_default_modes(self):
        """Create default modes if they don't exist."""
        default_path = self.modes_dir / "default.md"
        if not default_path.exists():
            self._create_default_mode()

    def _create_default_mode(self):
        """Create the default mode file."""
        content = """# Default Mode

## Description
The standard REDMYTHOS CLAW mode for general tasks.

## Role
You are REDMYTHOS CLAW, an intelligent AI agent assistant running in Termux.
You help users with coding, file management, system tasks, and automation.
You are precise, efficient, and always explain what you're doing.

## Tools
- file_tool: enabled
- shell_tool: enabled
- search_tool: enabled
- fix_tool: enabled
- web_tool: enabled

## Safety
confirm: always

## Format
Provide clear, structured responses.
Use markdown formatting when helpful.
Always explain actions before taking them.

## Prompt Prefix
You are running in Termux on Android. Be mindful of mobile constraints.
"""
        (self.modes_dir / "default.md").write_text(content)

    def list_modes(self) -> List[str]:
        """List all available mode names."""
        modes = []
        for f in self.modes_dir.glob("*.md"):
            modes.append(f.stem)
        return sorted(modes)

    def load_mode(self, name: str) -> Optional[Dict]:
        """
        Load a mode by name from .md file.
        
        Args:
            name: Mode name (without .md extension)
            
        Returns:
            Dict with parsed mode configuration
        """
        # Check cache first
        mode_file = self.modes_dir / f"{name}.md"
        
        if not mode_file.exists():
            # Try case-insensitive search
            for f in self.modes_dir.glob("*.md"):
                if f.stem.lower() == name.lower():
                    mode_file = f
                    break
            else:
                return None

        # Check if cached version is still fresh
        mtime = mode_file.stat().st_mtime
        if name in self._cache and self._cache[name].get("_mtime") == mtime:
            return self._cache[name]

        # Parse the .md file
        try:
            content = mode_file.read_text(encoding="utf-8")
            parsed = self._parse_mode_file(content, name)
            parsed["_mtime"] = mtime
            parsed["_file"] = str(mode_file)
            self._cache[name] = parsed
            return parsed
        except Exception as e:
            console.print(f"[red]Error loading mode '{name}': {e}[/red]")
            return None

    def _parse_mode_file(self, content: str, name: str) -> Dict:
        """Parse a .md mode file into a config dict."""
        
        mode = {
            "name": name,
            "description": "",
            "role": "",
            "tools": {
                "file_tool": "enabled",
                "shell_tool": "enabled",
                "search_tool": "enabled",
                "fix_tool": "enabled",
                "web_tool": "enabled"
            },
            "mcp_servers": [],
            "extensions": [],
            "safety": "always",
            "format": "",
            "prompt_prefix": "",
            "raw": content
        }

        # Split into sections by ## headers
        sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
        
        # Get title from # header
        title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            mode["name"] = title_match.group(1).strip()

        for section in sections:
            if not section.strip():
                continue

            lines = section.strip().split('\n')
            section_name = lines[0].strip().lower()
            section_content = '\n'.join(lines[1:]).strip()

            if section_name == "description":
                mode["description"] = section_content

            elif section_name == "role":
                mode["role"] = section_content

            elif section_name == "tools":
                tools = self._parse_list_section(section_content)
                for tool_line in tools:
                    if ':' in tool_line:
                        tool_name, tool_status = tool_line.split(':', 1)
                        tool_name = tool_name.strip().lower().replace(' ', '_')
                        tool_status = tool_status.strip().lower()
                        if tool_name.endswith('_tool') or '_tool' in tool_name:
                            mode["tools"][tool_name] = tool_status
                        else:
                            mode["tools"][f"{tool_name}_tool"] = tool_status

            elif section_name == "mcp servers":
                servers = self._parse_list_section(section_content)
                for server in servers:
                    if ':' in server:
                        srv_name, srv_url = server.split(':', 1)
                        mode["mcp_servers"].append({
                            "name": srv_name.strip(),
                            "url": srv_url.strip()
                        })
                    else:
                        mode["mcp_servers"].append({
                            "name": server.strip(),
                            "url": "local"
                        })

            elif section_name == "extensions":
                mode["extensions"] = self._parse_list_section(section_content)

            elif section_name == "safety":
                safety_match = re.search(r'confirm:\s*(\w+)', section_content, re.IGNORECASE)
                if safety_match:
                    mode["safety"] = safety_match.group(1).lower()
                else:
                    mode["safety"] = section_content.strip().lower()

            elif section_name == "format":
                mode["format"] = section_content

            elif section_name == "prompt prefix":
                mode["prompt_prefix"] = section_content

        # Build system prompt from role + format + prefix
        mode["system_prompt"] = self._build_system_prompt(mode)

        return mode

    def _parse_list_section(self, content: str) -> List[str]:
        """Parse a bullet list section."""
        items = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                items.append(line[2:].strip())
            elif line.startswith('* '):
                items.append(line[2:].strip())
            elif line.startswith('• '):
                items.append(line[2:].strip())
            elif line and not line.startswith('#'):
                items.append(line)
        return [i for i in items if i]

    def _build_system_prompt(self, mode: Dict) -> str:
        """Build the full system prompt for this mode."""
        parts = []

        if mode["role"]:
            parts.append(mode["role"])

        if mode["format"]:
            parts.append(f"\nRESPONSE FORMAT:\n{mode['format']}")

        if mode["prompt_prefix"]:
            parts.append(f"\nADDITIONAL CONTEXT:\n{mode['prompt_prefix']}")

        # Add tool availability
        enabled_tools = [
            name for name, status in mode["tools"].items()
            if status in ["enabled", "read-only"]
        ]
        if enabled_tools:
            parts.append(f"\nAVAILABLE TOOLS: {', '.join(enabled_tools)}")

        return '\n'.join(parts)

    def reload_mode(self, name: str) -> Optional[Dict]:
        """Force reload a mode from disk."""
        if name in self._cache:
            del self._cache[name]
        return self.load_mode(name)

    def get_mode_info(self, name: str) -> str:
        """Get formatted info about a mode."""
        mode = self.load_mode(name)
        if not mode:
            return f"Mode '{name}' not found."
        
        info = f"""
**Mode:** {mode['name']}
**File:** {mode.get('_file', 'unknown')}
**Description:** {mode['description']}
**Tools:** {', '.join([k for k, v in mode['tools'].items() if v != 'disabled'])}
**MCP Servers:** {len(mode['mcp_servers'])}
**Extensions:** {len(mode['extensions'])}
**Safety:** {mode['safety']}
"""
        return info
