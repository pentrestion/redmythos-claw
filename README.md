# REDMYTHOS CLAW 🦀

<div align="center">

  <img src="https://raw.githubusercontent.com/pentrestion/redmythos-claw/master/assets/banner.png" alt="REDMYTHOS CLAW banner" width="100%" />

  <h3><strong>Termux AI Coding Agent for Android</strong></h3>
  <p>
    <strong>Gemini-powered autonomous AI agent</strong> for mobile-first coding, terminal workflows, research, automation, and security tasks.
  </p>

  <p>
    <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-red.svg" /></a>
    <a href="https://www.python.org"><img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8+-red.svg" /></a>
    <a href="https://termux.dev"><img alt="Termux optimized" src="https://img.shields.io/badge/Termux-Optimized-black.svg" /></a>
    <a href="https://github.com/pentrestion/redmythos-claw/stargazers"><img alt="GitHub stars" src="https://img.shields.io/badge/GitHub-Stars-⭐-red.svg" /></a>
  </p>

</div>

## The problem REDMYTHOS CLAW solves

Most AI tools are built for desktop workflows. REDMYTHOS CLAW is built for the reality of mobile development and terminal-first environments.

It brings the power of an autonomous coding agent to:

- Termux and Android users
- Mobile-first software engineering
- Research, bug hunting, and security workflows
- Automation for terminal tasks and file operations
- Lightweight AI workflows powered by Google Gemini

## Why this project stands out

REDMYTHOS CLAW combines autonomous reasoning, dynamic tool loading, and mobile-friendly execution into one lightweight framework.

- Gemini-powered agent loop
- Claude Code-like workflow for coding tasks
- Dynamic loading from the `tools/` directory
- Markdown-based modes and skills system
- MCP support for external integrations
- Built for Android, Termux, Linux, and macOS
- Open-source, lightweight, and developer-first

## A quick visual overview

```text
┌──────────────────────────────────────────────────────────────┐
│  REDMYTHOS CLAW                                            │
│  Research → Strategy → Plan → Act → Validate               │
│                                                            │
│  • Read files / search / inspect code                      │
│  • Execute terminal commands in a controlled workflow      │
│  • Use Gemini to reason and plan                           │
│  • Automate actions with tools and modes                  │
│  • Validate output before finishing                        │
└──────────────────────────────────────────────────────────────┘
```

## Features

### AI coding agent for mobile
Build and automate software tasks from a phone or Android terminal, without needing a full desktop workstation.

### Autonomous reasoning loop
The agent follows a structured lifecycle:

1. RESEARCH
2. STRATEGY
3. PLAN
4. ACT
5. VALIDATE

### Dynamic tools and modes
The project is designed to grow with your workflow:

- add tools by dropping Python files in `tools/`
- add modes by dropping `.md` files in `~/.redmythos/modes/`
- add skills in the `skills/` folder
- connect MCP servers for external capabilities

### Security-focused design
The framework is built for controlled local execution and includes safety-minded operation patterns.

## Quick start

```bash
git clone https://github.com/pentrestion/redmythos-claw.git
cd redmythos-claw
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"
python main.py
```

### Or on Termux

```bash
git clone https://github.com/pentrestion/redmythos-claw
cd redmythos-claw
bash install.sh
redmythosclaw
```

## First-run configuration

On first launch, the project creates a config folder under:

- `~/.redmythos/config.json`
- `~/.redmythos/modes/`
- `~/.redmythos/extensions/`
- `~/.redmythos/mcp/`
- `~/.redmythos/memory/`

Set your Gemini API key before using the agent.

## Available commands

```text
/mode <name>      Switch to a mode
/modes            List available modes
/mcp              List MCP servers
/extensions       List loaded extensions
/memory           View session memory
/memory clear    Clear memory
/help             Show help
/clear           Clear screen
/exit            Exit app
```

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

## Use cases

- AI coding assistant for Android and Termux
- Mobile-first automation and scripting
- Security research and reconnaissance workflows
- Code inspection and debugging support
- Research + planning + execution loops for technical tasks
- Building custom workflows with Blueprints, MCP, and tools

## SEO-friendly keywords

This repository is positioned around these relevant terms:

- Termux AI agent
- Android AI coding assistant
- Gemini AI agent
- autonomous coding agent
- Claude Code alternative
- AI terminal assistant
- mobile automation tool
- research agent
- coding agent for Android
- Python AI project
- AI agent framework
- Termux automation
- Google Gemini tool

## Community and contribution

Contributions are welcome.

If you want to improve the project:

- add new tools
- improve safety controls
- add better modes
- improve documentation
- contribute security hardening improvements

## Security note

This project includes autonomous execution capabilities. Use it responsibly, validate commands before running them in sensitive environments, and keep your API keys private.

## License

MIT License

## Sponsor / support

If this project helps you, consider starring the repo and sharing it with developers working in mobile or cybersecurity automation.

```bash
# In GitHub, hit the star button to help visibility and discovery.
```

## Built for

- Termux users
- Android developers
- AI automation enthusiasts
- CTF and security researchers
- developers exploring autonomous AI workflows

---

<p align="center">
  <strong>⭐ Star this repo</strong> if you want to support mobile-first AI tooling and open-source autonomous agent development.
</p>
