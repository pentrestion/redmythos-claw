"""
REDMYTHOS CLAW 🦀 — ReAct Agent Brain
The core intelligence loop:
RESEARCH → STRATEGY → PLAN → ACT → VALIDATE
"""

import json
import time
import os
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.markdown import Markdown

from core.gemini import GeminiClient
from core.memory import Memory
from core.mcp_client import MCPClient
from core.tool_registry import ToolRegistry

console = Console()

class RedMythosAgent:
    """
    The main REDMYTHOS CLAW agent.
    Follows Research -> Strategy -> Execution (Plan-Act-Validate) lifecycle.
    Implements autonomous reasoning with dynamic tool loading.
    """

    MAX_ITERATIONS = 15  # Safety limit

    def __init__(self, mode_loader, memory: Memory, mcp: MCPClient):
        self.mode_loader = mode_loader
        self.memory = memory
        self.mcp = mcp
        self.gemini = GeminiClient()
        self.current_mode = None
        self.current_mode_name = "default"
        
        # Initialize Tool Registry (Dynamic Loading)
        # Assuming core/agent.py is in redmythos-claw/core/
        tools_path = Path(__file__).parent.parent / "tools"
        self.tool_registry = ToolRegistry(tools_path)
        
        # Extensions loaded dynamically
        self.extensions: Dict = {}
        
        # Agentic State (Claude Code inspired)
        self.task_list: List[str] = []
        self.completed_tasks: List[str] = []

    def set_mode(self, mode: Dict):
        """Set the active mode."""
        self.current_mode = mode
        self.current_mode_name = mode.get("name", "default")
        self.gemini.reset_conversation()
        
        for server in mode.get("mcp_servers", []):
            self.mcp.register_server(server)

        for ext_name in mode.get("extensions", []):
            self._load_extension(ext_name)

    def _load_extension(self, name: str):
        """Load an extension by name."""
        import importlib.util
        from pathlib import Path
        ext_path = Path.home() / ".redmythos" / "extensions" / name / "main.py"
        if ext_path.exists():
            try:
                spec = importlib.util.spec_from_file_location(name, ext_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'Extension'):
                    self.extensions[name] = module.Extension()
                    console.print(f"[dim]✅ Extension loaded: {name}[/dim]")
            except Exception as e:
                console.print(f"[red]Failed to load extension '{name}': {e}[/red]")

    def list_extensions(self) -> List[str]:
        """List loaded extensions."""
        from pathlib import Path
        ext_dir = Path.home() / ".redmythos" / "extensions"
        if not ext_dir.exists():
            return []
        return [d.name for d in ext_dir.iterdir() if d.is_dir()]

    def _get_available_tools(self) -> List[Dict]:
        """Get tools available in current mode."""
        mode_tools = {}
        if self.current_mode:
            mode_tools = self.current_mode.get("tools", {})

        all_definitions = self.tool_registry.get_definitions()
        available = []

        for definition in all_definitions:
            tool_name = definition["name"]
            status = mode_tools.get(tool_name, "enabled")
            if status != "disabled":
                tool_def = definition.copy()
                if status == "read-only":
                    tool_def["description"] += " [READ ONLY]"
                available.append(tool_def)

        # Add MCP tools
        available.extend(self.mcp.get_available_tools())

        return available

    def _execute_tool(self, tool_name: str, tool_input: Dict) -> str:
        """Execute a tool and return the result."""
        # Permission check
        if self.current_mode:
            mode_tools = self.current_mode.get("tools", {})
            status = mode_tools.get(tool_name, "enabled")
            if status == "disabled":
                return f"❌ Tool '{tool_name}' is disabled."
            if status == "read-only" and tool_input.get("action") in ["write", "edit", "delete"]:
                return f"❌ Tool '{tool_name}' is read-only."

        # Safety confirmation
        safety = self.current_mode.get("safety", "always") if self.current_mode else "always"
        should_confirm = (safety == "always") or (
            safety == "dangerous_only" and (
                tool_name in ["shell_tool"] or 
                tool_input.get("action") in ["delete", "write", "edit"]
            )
        )

        if should_confirm:
            console.print(Panel(
                f"[yellow]Tool:[/yellow] {tool_name}\n[yellow]Input:[/yellow] {json.dumps(tool_input, indent=2)}",
                title="⚠️ CONFIRM ACTION", border_style="yellow"
            ))
            if not Confirm.ask("[yellow]Execute?[/yellow]"):
                return "❌ Cancelled."

        try:
            tool = self.tool_registry.get_tool(tool_name)
            if tool:
                return tool.execute(**tool_input)
            elif self.mcp.has_tool(tool_name):
                return self.mcp.call_tool(tool_name, tool_input)
            return f"❌ Unknown tool: {tool_name}"
        except Exception as e:
            return f"❌ Tool error: {str(e)}"

    def run(self, user_message: str) -> str:
        """Main agent loop with Research-Strategy-Execution lifecycle."""
        system_prompt = self.current_mode.get("system_prompt", "") if self.current_mode else ""
        memory_context = self.memory.get_context()
        if memory_context:
            system_prompt += f"\n\nREMEMBER FROM PAST:\n{memory_context}"

        # Inject Agentic State
        state_context = f"\n\nCURRENT TASK LIST:\n{json.dumps(self.task_list, indent=2)}"
        state_context += f"\nCOMPLETED TASKS:\n{json.dumps(self.completed_tasks, indent=2)}"
        system_prompt += state_context

        available_tools = self._get_available_tools()
        iteration = 0
        tool_results_context = ""
        current_stage = "RESEARCH"

        while iteration < self.MAX_ITERATIONS:
            iteration += 1
            current_message = user_message
            if tool_results_context:
                current_message = f"{user_message}\n\nTOOL RESULTS:\n{tool_results_context}"

            response = self.gemini.chat_with_tools(
                message=current_message,
                system_prompt=system_prompt,
                available_tools=available_tools
            )

            # Update Internal Task State if provided by LLM in response
            if "new_tasks" in response and response["new_tasks"]:
                self.task_list.extend(response["new_tasks"])
            if "completed_task" in response and response["completed_task"]:
                if response["completed_task"] in self.task_list:
                    self.task_list.remove(response["completed_task"])
                    self.completed_tasks.append(response["completed_task"])

            thought = response.get("thought", "")
            plan = response.get("plan", "")
            action = response.get("action")
            action_input = response.get("action_input", {})
            validation = response.get("validation", "")
            final_answer = response.get("final_answer")

            if thought:
                console.print(Panel(
                    Markdown(f"**THOUGHT:** {thought}\n\n**PLAN:** {plan}\n\n**VALIDATION:** {validation}"),
                    title=f"[bold red]💭 {current_stage}[/bold red]", border_style="red"
                ))

            if final_answer is not None:
                self.memory.add(user_message, final_answer)
                return final_answer

            if action:
                if "search" in action or "read" in action_input.get("action", ""):
                    current_stage = "RESEARCH"
                elif "write" in action_input.get("action", "") or "shell" in action:
                    current_stage = "EXECUTION"
                else:
                    current_stage = "STRATEGY"

                console.print(f"\n[bold red]⚡ ACTING:[/bold red] {action}")
                result = self._execute_tool(action, action_input or {})
                tool_results_context += f"\n[{action}]: {result}\n"
            else:
                return response.get("final_answer", "Clarification needed.")

        return "⚠️ Max iterations reached."
