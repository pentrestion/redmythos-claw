# REDMYTHOS CLAW 🦀

> The Autonomous AI Agent Framework for Termux | Refined by Gemini CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Agentic](https://img.shields.io/badge/Agent-Autonomous-red.svg)](https://redmythos.dev)

---

## Evolution: From RedMythos to REDMYTHOS

REDMYTHOS CLAW is a high-autonomy agent framework inspired by **Claude Code** and **Gemini CLI**. It doesn't just chat—it **thinks, plans, and executes** across your terminal.

### 🌟 New Agentic Features
- **Dynamic Tool Loading:** Add any `.py` file to `tools/` and it becomes a tool instantly.
- **Persistent Task Tracking:** The agent maintains a "Task List" and "Completed Tasks" across its loop.
- **RedMythos Reasoning:** Follows a strict `RESEARCH → STRATEGY → PLAN → ACT → VALIDATE` lifecycle.
- **Skills System:** Drop `.md` files in `skills/` to give the agent new expertise.

---

## How It Works

```
You give a task
      ↓
Agent RESEARCHES (Scans codebase/environment)
      ↓
Agent STRATEGIZES (Builds a task list)
      ↓
Agent PLANS (Decides next 3 steps)
      ↓  
Agent ACTS (Uses dynamic tools autonomously)
      ↓
Agent VALIDATES (Verifies behavioral correctness)
      ↓
Agent REPEATS until all tasks are COMPLETED ✅
```

---

## Adding Your Own "Stuffs"

### 🛠️ Add New Tools
Simply drop a Python file in `tools/`. Ensure it has an `execute()` method:

```python
class MyCustomTool:
    """Description for the AI."""
    def execute(self, arg1, arg2):
        # Your logic here
        return "Result for the agent"
```

### 🧠 Add New Skills
Drop an `.md` file in `skills/`. The agent will use this knowledge when needed.

### 🎭 Add New Modes
Drop an `.md` file in `modes/` (e.g., `security_researcher.md`).

---

## Quick Install

```bash
git clone https://github.com/yourusername/redmythos-claw
cd redmythos-claw
bash install.sh
python3 main.py
```


---

## Customization (The Magic Part 🪄)

### Add Custom Modes
Just drop a `.md` file in `~/.redmythos/modes/`:

```markdown
# My Custom Mode

## Description
My specialized mode for X

## Role
You are an expert in...

## Tools
- file_tool: enabled
- shell_tool: enabled
- web_tool: disabled

## Safety
confirm: dangerous_only

## Format
Always respond with...
```

Then use it:
```
/mode my_custom_mode
```

**That's it. No coding needed!**

---

### Add MCP Servers
Edit `~/.redmythos/mcp/servers.json`:

```json
{
  "servers": [
    {
      "name": "my-server",
      "type": "http",
      "url": "http://localhost:3000/mcp",
      "enabled": true
    }
  ]
}
```

---

### Add Extensions
Drop a folder in `~/.redmythos/extensions/my-extension/`:

```
my-extension/
├── extension.md    # Config (same .md format!)
├── main.py         # Extension code
└── README.md
```

---

## Built-In Modes

| Mode | Description |
|------|-------------|
| `default` | General purpose assistant |
| `active_mode` | Security research + bug bounty |
| `building_mode` | Full-stack development |
| `new_mode` | SaaS architecture |

---

## Commands

| Command | What It Does |
|---------|-------------|
| `/mode <name>` | Switch mode |
| `/modes` | List all modes |
| `/mcp` | Show MCP servers |
| `/mcp connect <name>` | Connect to MCP server |
| `/extensions` | List extensions |
| `/memory` | Show memory |
| `/memory clear` | Clear memory |
| `/clear` | Clear screen |
| `/help` | Show help |
| `/exit` | Exit |

---

## Configuration

Edit `~/.redmythos/config.json`:

```json
{
  "gemini_api_key": "your_key_here",
  "default_mode": "default",
  "max_iterations": 10,
  "auto_save_memory": true
}
```

Get free Gemini API key: https://aistudio.google.com/apikey

---

## File Structure

```
~/.redmythos/              # Your config home
├── config.json            # Main config
├── modes/                 # Your .md mode files
│   ├── default.md
│   ├── active_mode.md
│   ├── building_mode.md
│   └── your_custom.md     # Drop any .md here!
├── extensions/            # Extensions
│   └── my-extension/
├── mcp/
│   └── servers.json       # MCP servers
├── memory/                # Session memory
└── logs/                  # Logs
```

---

## License

MIT — Free to use, modify, share, sell.

---

## Credits

Built by khan77319 🦀
Powered by Google Gemini
Inspired by Claude Code
