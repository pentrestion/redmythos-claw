"""
REDMYTHOS CLAW 🦀 — Gemini API Client
Handles all Gemini API calls with structured agentic reasoning.
"""

import os
import time
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Generator
import google.generativeai as genai
from rich.console import Console

console = Console()

class GeminiClient:
    """
    Gemini API client optimized for REDMYTHOS agentic loop.
    Model: gemini-1.5-flash
    """

    MODEL = "gemini-1.5-flash"
    MAX_RPM = 15
    MIN_DELAY = 4.0

    def __init__(self):
        self.api_key = self._load_api_key()
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.MODEL)
        self.last_request_time = 0
        self.request_count_today = 0
        self.conversation_history = []

    def _load_api_key(self) -> str:
        """Load API key from config."""
        config_path = Path.home() / ".redmythos" / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                key = config.get("gemini_api_key", "")
                if key and key != "YOUR_GEMINI_API_KEY_HERE":
                    return key
        return os.environ.get("GEMINI_API_KEY", "")

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.MIN_DELAY:
            time.sleep(self.MIN_DELAY - elapsed)
        self.last_request_time = time.time()

    def chat_with_tools(self,
                        message: str,
                        system_prompt: str,
                        available_tools: List[Dict]) -> Dict:
        """
        Chat with tool use enabled and agentic state tracking.
        """
        self._rate_limit()
        
        tool_descriptions = "\n".join([
            f"- {t['name']}: {t['description']}"
            for t in available_tools
        ])
        
        agentic_prompt = f"""
{system_prompt}

You have access to these tools:
{tool_descriptions}

To use a tool, respond with JSON in this format:
{{
  "thought": "your current reasoning/analysis",
  "plan": "your next 1-3 steps",
  "new_tasks": ["task 1", "task 2"],
  "completed_task": "task name from current task list",
  "action": "tool_name",
  "action_input": {{tool parameters}},
  "validation": "how you will verify the result",
  "final_answer": null
}}

If you have the final answer (no tool needed):
{{
  "thought": "your final reasoning",
  "plan": null,
  "new_tasks": [],
  "completed_task": "the main user task",
  "action": null,
  "action_input": null,
  "validation": null,
  "final_answer": "your answer here"
}}

User request: {message}
"""
        
        try:
            response = self.model.generate_content(
                agentic_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=4096,
                )
            )
            
            response_text = response.text.strip()
            self.request_count_today += 1
            
            try:
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                parsed = json.loads(response_text.strip())
                
                # Ensure all agentic fields exist
                fields = ["thought", "plan", "new_tasks", "completed_task", 
                          "action", "action_input", "validation", "final_answer"]
                for field in fields:
                    if field not in parsed:
                        parsed[field] = None if field != "new_tasks" else []
                
                return parsed

            except json.JSONDecodeError:
                return {
                    "thought": "Direct response",
                    "plan": None,
                    "new_tasks": [],
                    "completed_task": None,
                    "action": None,
                    "action_input": None,
                    "validation": None,
                    "final_answer": response_text
                }
                
        except Exception as e:
            return {
                "thought": f"Error: {e}",
                "plan": None,
                "new_tasks": [],
                "completed_task": None,
                "action": None,
                "action_input": None,
                "validation": None,
                "final_answer": f"❌ Error: {e}"
            }

    def reset_conversation(self):
        self.conversation_history = []
