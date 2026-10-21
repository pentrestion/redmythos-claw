# REDMYTHOS CLAW 🦀

Open-source AI coding agent for Termux and Android — a lightweight, Gemini-powered alternative to Claude Code for mobile-first software workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-red.svg)](https://python.org)
[![Termux](https://img.shields.io/badge/Termux-Optimized-black.svg)](https://termux.dev)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-red?logo=github)](https://github.com/pentrestion/redmythos-claw)

REDMYTHOS CLAW is an autonomous AI agent framework built for Android and Termux. It helps you automate coding tasks, terminal operations, file manipulation, search, web lookup, and task execution using Google Gemini from your phone or terminal.

This project is designed for developers, security researchers, and power users who want a mobile-first AI assistant that can reason through tasks, plan steps, and act with tool access.

## Why this project exists

Most AI tools are built around a desktop workflow. REDMYTHOS CLAW is built for the reality of mobile development and terminal-first environments:

- Run an AI agent from Termux on Android
- Automate research, planning, and execution loops
- Use Gemini to work with files, commands, and web tools
- Extend the system with custom tools, skills, and MCP support
- Keep the workflow lightweight and open source

## Key features

- Termux AI agent for Android
- Gemini-powered autonomous reasoning loop
- Claude Code-style workflow for coding and task execution
- Dynamic tool loading from the `tools/` directory
- Markdown skill system via `skills/`
- MCP server support for external integrations
- Built for research, coding, automation, and security workflows
- Lightweight Python architecture

## How it works

REDMYTHOS CLAW follows a structured reasoning lifecycle:

1. RESEARCH — inspect files, environment, and external sources
2. STRATEGY — turn the goal into a plan
3. PLAN — break the work into actionable tasks
4. ACT — execute tools and commands
5. VALIDATE — verify the result before finishing

This makes it useful for more than chat. It can act as a reasoning partner for development tasks and automation.

## Quick start

```bash
git clone https://github.com/pentrestion/redmythos-claw
cd redmythos-claw
bash install.sh
redmythosclaw
```

## Requirements

- Python 3.8+
- Termux or Linux/macOS environment
- Google Gemini API access
- Git

## Configuration

On first run, the project creates a config under `~/.redmythos/` and sets up:

- `~/.redmythos/config.json`
- `~/.redmythos/modes/`
- `~/.redmythos/extensions/`
- `~/.redmythos/mcp/`
- `~/.redmythos/memory/`

Set your Gemini API key in the generated config file before using the agent.

## Available commands

| Command | Description |
|---------|-------------|
| `/mode <name>` | Switch agent mode |
| `/modes` | List all available modes |
| `/mcp` | Manage MCP server configuration |
| `/memory` | View or clear session memory |
| `/help` | Show command list |
| `/exit` | Exit the app |

## Customization

### Add new tools

Drop any Python file into `tools/` with an `execute()` method. The registry auto-discovers it.

### Add new skills

Place `.md` or `.txt` files into `skills/` to give the agent domain-specific knowledge.

### MCP support

REDMYTHOS CLAW supports MCP servers for extending the agent with external tools and resources.

## Project structure

```text
.
├── README.md
├── LICENSE
├── install.sh
├── main.py
├── requirements.txt
├── config/
│   └── setup.py
├── core/
│   ├── agent.py
│   ├── gemini.py
│   ├── mcp_client.py
│   ├── memory.py
│   ├── mode_loader.py
│   └── tool_registry.py
├── modes/
├── skills/
├── tools/
│   ├── file_tool.py
│   ├── fix_tool.py
│   ├── search_tool.py
│   ├── shell_tool.py
│   └── web_tool.py
└── .gitignore
```

## Example use cases

- Run coding tasks from your Android device
- Use Gemini to inspect code and plan fixes
- Automate repetitive terminal workflows
- Research and validate security issues in a controlled environment
- Build custom mobile automation workflows with agentic reasoning

## Security

The project includes safety-oriented behavior. Dangerous actions may require confirmation depending on your active mode. Review the mode configuration and use the tool responsibly.

## License

MIT License

## Built for

- Termux users
- Android developers
- AI automation enthusiasts
- security researchers
- people exploring Gemini-powered autonomous agents

## Keywords

Termux AI, Android Agent, Gemini API, Autonomous Agent, Claude Code Alternative, AI Coding Agent, Mobile Automation, Open Source AI Tool, Termux Developer Tools, Python AI Agent

## Author

Built by Mir mahmood khan

---

If you want, I can also help you with:

- a stronger repo description for GitHub
- a better project tagline for SEO
- a polished landing page / docs page
- a one-page homepage for GitHub Pages
