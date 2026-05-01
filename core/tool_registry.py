"""
REDMYTHOS CLAW 🦀 — Tool Registry
Dynamically loads tools from the tools/ directory.
Allows users to add new tools by simply dropping .py files.
"""

import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console

console = Console()

class ToolRegistry:
    """Registry for managing and dynamically loading tools."""

    def __init__(self, tools_dir: str):
        self.tools_dir = Path(tools_dir)
        self.tools: Dict[str, Any] = {}
        self.tool_definitions: List[Dict] = []
        self._load_all_tools()

    def _load_all_tools(self):
        """Scan the tools directory and load all valid tool classes."""
        if not self.tools_dir.exists():
            console.print(f"[red]Tools directory not found: {self.tools_dir}[/red]")
            return

        for file_path in self.tools_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
            
            self._load_tool_from_file(file_path)

    def _load_tool_from_file(self, file_path: Path):
        """Load a tool class from a single file."""
        module_name = file_path.stem
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find classes that have an 'execute' method and a docstring
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, 'execute') and obj.__module__ == module_name:
                    tool_instance = obj()
                    tool_name = module_name # Default to filename
                    
                    # Store instance
                    self.tools[tool_name] = tool_instance
                    
                    # Extract definition for AI
                    description = obj.__doc__ or f"Tool for {tool_name}"
                    
                    # Try to get parameter info from docstring or signature
                    # For now, we'll keep it simple as the agent is good at inferring
                    self.tool_definitions.append({
                        "name": tool_name,
                        "description": description.strip(),
                        "parameters": {} # To be refined if needed
                    })
                    
                    # console.print(f"[dim]🔌 Tool registered: {tool_name}[/dim]")

        except Exception as e:
            console.print(f"[red]Failed to load tool from {file_path.name}: {e}[/red]")

    def get_tool(self, name: str):
        """Get a tool instance by name."""
        return self.tools.get(name)

    def get_definitions(self) -> List[Dict]:
        """Get definitions for all registered tools."""
        return self.tool_definitions

    def has_tool(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self.tools
