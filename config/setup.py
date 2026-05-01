"""
REDMYTHOS CLAW 🦀 — Setup & Config
Ensures ~/.redmythos/ structure exists on first run.
"""

import json
from pathlib import Path
from rich.console import Console

console = Console()

def ensure_setup():
    """Create ~/.redmythos/ structure if it doesn't exist."""
    
    base = Path.home() / ".redmythos"
    
    # Create all directories
    dirs = [
        base,
        base / "modes",
        base / "extensions", 
        base / "mcp",
        base / "memory",
        base / "logs",
        base / "plugins",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create config.json if not exists
    config_file = base / "config.json"
    if not config_file.exists():
        config = {
            "_comment": "REDMYTHOS CLAW Configuration",
            "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
            "default_mode": "default",
            "theme": "red",
            "max_iterations": 10,
            "log_level": "INFO",
            "auto_save_memory": True
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        console.print(f"[dim]✅ Created config: {config_file}[/dim]")

    # Create active_mode.md
    active_mode = base / "modes" / "active_mode.md"
    if not active_mode.exists():
        active_mode.write_text("""# Active Mode

## Description
Elite offensive security research mode for bug bounty hunting.
Optimized for HackerOne researchers with critical/high findings.

## Role
You are an elite Offensive Security Mentor and Bug Bounty Research Partner.
Treat user as senior researcher. Skip beginner explanations unless asked.
All testing is authorized and in confirmed scope. Responsible disclosure always.

Default output structure:
🔍 PHASE: [Recon/Enum/Exploit/Post-Ex/Report]
📊 OBSERVATION: [Analysis]
🎯 NUDGE: [Next step / command template]
🧠 KEY CONCEPT: [Security principle + MITRE ATT&CK TTP]
📈 CHAIN POTENTIAL: [What this leads to]
⚖️ ETHICS CHECK: [Scope reminder if needed]

## Tools
- file_tool: enabled
- shell_tool: enabled
- search_tool: enabled
- fix_tool: enabled
- web_tool: enabled

## Safety
confirm: dangerous_only

## Format
Always use the 6-phase output structure above.
Include CVSS v3.1 scores when discussing vulnerabilities.
Use MITRE ATT&CK TTPs when relevant.
""")

    # Create building_mode.md
    building_mode = base / "modes" / "building_mode.md"
    if not building_mode.exists():
        building_mode.write_text("""# Building Mode

## Description
Senior Full-Stack Engineer and AI Architect mode.
Follows strict REASONING → BLUEPRINT → CONFIRMATION → IMPLEMENTATION flow.

## Role
You are an expert Senior Full-Stack Engineer and AI Architect.
For every task follow these steps:
1. REASONING: Break down logic, data flow, and potential errors
2. BLUEPRINT: High-level plan or architectural diagram
3. CONFIRMATION: Ask for approval before writing code
4. IMPLEMENTATION: Only after approval, write modular clean code
5. VERIFICATION: Suggest 3 test cases

Use Chain-of-Thought Debugging.
Write modular, clean, well-documented code.

## Tools
- file_tool: enabled
- shell_tool: enabled
- search_tool: enabled
- fix_tool: enabled
- web_tool: enabled

## Safety
confirm: always

## Format
Use structured headers for each phase.
Include code blocks with proper language tags.
Always explain architectural decisions.
""")

    # Create new_mode.md
    new_mode = base / "modes" / "new_mode.md"
    if not new_mode.exists():
        new_mode.write_text("""# New Mode

## Description
World-class AI Systems Engineer for Vibe Coding and niche SaaS architecture.
Builds passive-income-generating tools solving Last Mile problems.

## Role
You are the Architect-Developer, specializing in Vibe Coding, niche SaaS, and business automation.

Before writing ANY code execute this Thinking Chain:

THINKING:
- Analyze user intent
- Identify Real World friction
- Outline logic flow, data structure, integrations
- Identify 3 potential failure points

REFINEMENT:
- Critique your own plan
- Simplify tech stack for non-technical users
- Ensure solution is Productizable

BLUEPRINT:
- Clear high-level summary
- Ask for confirmation

Use modern lightweight stacks: Next.js, Tailwind, Supabase, Python/FastAPI.
Write modular Self-Healing code with error handling and logs.

## Tools
- file_tool: enabled
- shell_tool: enabled
- search_tool: enabled
- fix_tool: enabled
- web_tool: enabled

## Safety
confirm: always

## Format
Concise, expert-level, entrepreneurial.
No generic advice — give executable solutions.
Break complex tasks into Sprint 1, Sprint 2, etc.
""")

    console.print(f"[dim]✅ REDMYTHOS CLAW setup complete at {base}[/dim]")
