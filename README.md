# REDMYTHOS CLAW 🦀

> **The Ultimate Autonomous AI Agent for Termux** | Powered by Google Gemini

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-red.svg)](https://python.org)
[![Termux](https://img.shields.io/badge/Termux-Optimized-black.svg)](https://termux.dev)

**REDMYTHOS CLAW** is a powerful, agentic AI framework built specifically for **Termux on Android**. Inspired by **Claude Code**, it brings high-level automation, software engineering, and security research capabilities to your mobile device for FREE using the Gemini API.

---

## 🔍 SEO & Key Features
- **Termux AI Agent:** Run a full-scale AI agent in your Termux environment.
- **Autonomous Reasoning:** Follows a strict `RESEARCH → STRATEGY → PLAN → ACT → VALIDATE` lifecycle.
- **Gemini AI Termux:** Optimized for Gemini 1.5 Flash (Free Tier).
- **Claude Code for Android:** A mobile-first alternative for autonomous coding and system tasks.
- **Dynamic Extensibility:** Add custom tools (.py) and skills (.md) instantly.
- **Security Research:** Built-in modes for offensive security and bug bounty hunting.

---

## 🚀 How It Works

REDMYTHOS CLAW doesn't just chat; it **acts**. It uses a persistent task list to manage complex goals:

1. **RESEARCH:** Scans your files, terminal environment, and web sources.
2. **STRATEGY:** Generates a comprehensive task list to achieve your goal.
3. **PLAN:** Breaks down the immediate next steps with validation criteria.
4. **ACT:** Executes tools (Shell, File, Web, Search) autonomously.
5. **VALIDATE:** Checks every result to ensure the task was completed correctly.

---

## 🛠️ Installation (Termux)

Copy and paste these commands to get started:

```bash
# Clone the repository
git clone https://github.com/pentrestion/redmythos-claw

# Enter directory
cd redmythos-claw

# Run the automated installer
bash install.sh

# Start the agent from anywhere
redmythosclaw
```

---

## 🧩 Customization

### Add New Tools
Drop any Python file in `tools/`. Ensure it has an `execute()` method. The agent will discover it automatically.

### Add New Skills
Drop Markdown files in `skills/` to provide the agent with specialized documentation or procedures.

### MCP Support
Fully compatible with **Model Context Protocol (MCP)** servers for infinite tool expansion.

---

## 📜 Commands

| Command | Description |
|---------|-------------|
| `/mode <name>` | Switch agent persona (e.g., gemini_cli, active_mode) |
| `/modes` | List all available personas |
| `/mcp` | Manage MCP server connections |
| `/memory clear` | Reset session memory |
| `/help` | Show full command list |
| `/exit` | Shut down the agent |

---

## ⚠️ Security
REDMYTHOS CLAW has built-in safety modes. By default, it asks for confirmation before executing "dangerous" commands (like `rm` or `shell`). You can customize this in your mode files.

---

## 📄 License
MIT — Open Source and Free Forever.

**Built for the community by Mir mahmood khan 🦀**
**Keywords:** Termux AI, Android Agent, Gemini API, Autonomous Agent, Claude Code, RedMythos Claw, Mobile Hacking, AI Automation.
