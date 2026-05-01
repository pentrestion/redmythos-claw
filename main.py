#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║          REDMYTHOS CLAW 🦀 v1.0.0                   ║
║     Your Personal AI Agent Framework                 ║
║     Built for Termux | Powered by Gemini             ║
║     Open Source | MIT License                        ║
╚══════════════════════════════════════════════════════╝

USER GUIDE:
-----------
1. Add your Gemini API key to ~/.redmythos/config.json
2. Drop .md files in ~/.redmythos/modes/ to add new modes
3. Add MCP servers in ~/.redmythos/mcp/servers.json
4. Drop extensions in ~/.redmythos/extensions/
5. Run: python main.py

COMMANDS:
---------
/mode <name>     - Switch mode
/modes           - List all modes
/mcp             - List MCP servers
/extensions      - List extensions
/memory          - Show session memory
/clear           - Clear screen
/help            - Show help
/exit            - Exit
"""

import os
import sys
import json
import readline
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import print as rprint

from core.agent import RedMythosAgent
from core.mode_loader import ModeLoader
from core.memory import Memory
from core.mcp_client import MCPClient
from config.setup import ensure_setup

console = Console()

BANNER = """
[red]██████╗ ███████╗██████╗ [/red][white] ███╗   ███╗██╗   ██╗████████╗██╗  ██╗ ██████╗ ███████╗[/white]
[red]██╔══██╗██╔════╝██╔══██╗[/red][white] ████╗ ████║╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗██╔════╝[/white]
[red]██████╔╝█████╗  ██║  ██║[/red][white] ██╔████╔██║ ╚████╔╝    ██║   ███████║██║   ██║███████╗[/white]
[red]██╔══██╗██╔══╝  ██║  ██║[/red][white] ██║╚██╔╝██║  ╚██╔╝     ██║   ██╔══██║██║   ██║╚════██║[/white]
[red]██║  ██║███████╗██████╔╝[/red][white] ██║ ╚═╝ ██║   ██║      ██║   ██║  ██║╚██████╔╝███████║[/white]
[red]╚═╝  ╚═╝╚══════╝╚═════╝ [/red][white] ╚═╝     ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/white]
[red]                          ██████╗██╗      █████╗ ██╗    ██╗ 🦀[/red]
[red]                         ██╔════╝██║     ██╔══██╗██║    ██║[/red]
[red]                         ██║     ██║     ███████║██║ █╗ ██║[/red]
[red]                         ██║     ██║     ██╔══██║██║███╗██║[/red]
[red]                         ╚██████╗███████╗██║  ██║╚███╔███╔╝[/red]
[red]                          ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝[/red]
"""

def show_banner():
    console.clear()
    console.print(BANNER)
    console.print(Panel(
        "[white]v1.0.0 | Powered by Gemini | Open Source MIT[/white]\n"
        "[dim]Your Personal AI Agent — Drop .md files to customize![/dim]",
        border_style="red",
        padding=(0, 2)
    ))

def show_help():
    help_text = """
## REDMYTHOS CLAW Commands 🦀

| Command | Description |
|---------|-------------|
| `/mode <name>` | Switch to a mode |
| `/modes` | List all available modes |
| `/mcp` | List MCP servers |
| `/mcp connect <name>` | Connect to MCP server |
| `/extensions` | List all extensions |
| `/memory` | Show session memory |
| `/memory clear` | Clear session memory |
| `/clear` | Clear the screen |
| `/help` | Show this help |
| `/exit` | Exit REDMYTHOS CLAW |

## How To Add Custom Modes
Drop any `.md` file in `~/.redmythos/modes/`

## How To Add Extensions  
Drop extension folder in `~/.redmythos/extensions/`

## How To Add MCP Servers
Edit `~/.redmythos/mcp/servers.json`
"""
    console.print(Markdown(help_text))

def handle_command(cmd: str, agent: RedMythosAgent, 
                   mode_loader: ModeLoader, mcp: MCPClient,
                   memory: Memory) -> bool:
    """Handle slash commands. Returns False if should exit."""
    
    parts = cmd.strip().split()
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []

    if command == "/exit":
        console.print("\n[red]🦀 REDMYTHOS CLAW shutting down... Goodbye![/red]\n")
        return False

    elif command == "/clear":
        show_banner()

    elif command == "/help":
        show_help()

    elif command == "/modes":
        modes = mode_loader.list_modes()
        console.print(Panel(
            "\n".join([f"[red]•[/red] [white]{m}[/white]" for m in modes]),
            title="[red]🦀 Available Modes[/red]",
            border_style="red"
        ))

    elif command == "/mode":
        if not args:
            console.print("[red]Usage: /mode <name>[/red]")
        else:
            mode_name = args[0]
            mode = mode_loader.load_mode(mode_name)
            if mode:
                agent.set_mode(mode)
                console.print(Panel(
                    f"[white]Switched to [red]{mode_name}[/red] mode![/white]\n"
                    f"[dim]{mode.get('description', '')}[/dim]",
                    border_style="red"
                ))
            else:
                console.print(f"[red]Mode '{mode_name}' not found![/red]")

    elif command == "/mcp":
        if args and args[0] == "connect":
            if len(args) < 2:
                console.print("[red]Usage: /mcp connect <server_name>[/red]")
            else:
                result = mcp.connect(args[1])
                console.print(f"[white]{result}[/white]")
        else:
            servers = mcp.list_servers()
            if servers:
                console.print(Panel(
                    "\n".join([
                        f"[red]•[/red] [white]{s['name']}[/white] "
                        f"[dim]({s.get('status','disconnected')})[/dim]"
                        for s in servers
                    ]),
                    title="[red]🔌 MCP Servers[/red]",
                    border_style="red"
                ))
            else:
                console.print("[dim]No MCP servers configured. Edit ~/.redmythos/mcp/servers.json[/dim]")

    elif command == "/extensions":
        extensions = agent.list_extensions()
        if extensions:
            console.print(Panel(
                "\n".join([f"[red]•[/red] [white]{e}[/white]" for e in extensions]),
                title="[red]🔌 Extensions[/red]",
                border_style="red"
            ))
        else:
            console.print("[dim]No extensions installed. Drop folders in ~/.redmythos/extensions/[/dim]")

    elif command == "/memory":
        if args and args[0] == "clear":
            memory.clear()
            console.print("[red]Memory cleared![/red]")
        else:
            mem = memory.get_all()
            if mem:
                console.print(Panel(
                    "\n".join([f"[dim]{k}:[/dim] [white]{v}[/white]" 
                               for k, v in mem.items()]),
                    title="[red]🧠 Session Memory[/red]",
                    border_style="red"
                ))
            else:
                console.print("[dim]Memory is empty.[/dim]")
    else:
        console.print(f"[red]Unknown command: {command}[/red] — type /help")

    return True

def main():
    # Setup ~/.redmythos/ structure
    ensure_setup()

    # Show banner
    show_banner()

    # Initialize components
    try:
        mode_loader = ModeLoader()
        memory = Memory()
        mcp = MCPClient()
        agent = RedMythosAgent(
            mode_loader=mode_loader,
            memory=memory,
            mcp=mcp
        )
    except Exception as e:
        console.print(f"[red]Startup error: {e}[/red]")
        sys.exit(1)

    # Load default mode if exists
    default_mode = mode_loader.load_mode("default")
    if default_mode:
        agent.set_mode(default_mode)

    console.print("\n[dim]Type /help for commands or just start chatting! 🦀[/dim]\n")

    # Main loop
    while True:
        try:
            # Show current mode in prompt
            mode_name = agent.current_mode_name or "default"
            user_input = Prompt.ask(
                f"[red]🦀 REDMYTHOS[/red][dim]({mode_name})[/dim][red]>[/red]"
            )

            if not user_input.strip():
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                should_continue = handle_command(
                    user_input, agent, mode_loader, mcp, memory
                )
                if not should_continue:
                    break
                continue

            # Send to agent
            console.print()
            with console.status("[red]🦀 Thinking...[/red]", spinner="dots"):
                response = agent.run(user_input)

            # Display response
            console.print(Panel(
                Markdown(response),
                border_style="red",
                title=f"[red]🦀 REDMYTHOS CLAW[/red] [dim]({mode_name})[/dim]",
                padding=(1, 2)
            ))
            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Use /exit to quit[/dim]")
            continue
        except EOFError:
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")
            continue

if __name__ == "__main__":
    main()
