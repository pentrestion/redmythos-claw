"""
REDMYTHOS CLAW 🦀 — Memory System
Persistent session memory across conversations.
Stores in ~/.redmythos/memory/
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class Memory:
    """Session and persistent memory for the agent."""

    def __init__(self):
        self.memory_dir = Path.home() / ".redmythos" / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.memory_dir / "session.json"
        self.long_term_file = self.memory_dir / "long_term.json"
        self.session_memory: Dict = {}
        self.long_term_memory: Dict = {}
        self._load()

    def _load(self):
        """Load memories from disk."""
        if self.session_file.exists():
            try:
                with open(self.session_file) as f:
                    self.session_memory = json.load(f)
            except Exception:
                self.session_memory = {}

        if self.long_term_file.exists():
            try:
                with open(self.long_term_file) as f:
                    self.long_term_memory = json.load(f)
            except Exception:
                self.long_term_memory = {}

    def add(self, query: str, response: str):
        """Add a query-response pair to memory."""
        key = query[:50]  # First 50 chars as key
        self.session_memory[key] = {
            "query": query,
            "response": response[:500],  # First 500 chars
            "timestamp": datetime.now().isoformat()
        }
        self._save_session()

    def remember(self, key: str, value: str):
        """Store something in long-term memory."""
        self.long_term_memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_long_term()

    def recall(self, key: str) -> Optional[str]:
        """Recall something from long-term memory."""
        item = self.long_term_memory.get(key)
        if item:
            return item.get("value")
        return None

    def get_context(self) -> str:
        """Get recent memory as context string."""
        if not self.long_term_memory:
            return ""
        
        items = []
        for key, data in list(self.long_term_memory.items())[-5:]:
            items.append(f"- {key}: {data.get('value', '')}")
        
        return "\n".join(items)

    def get_all(self) -> Dict:
        """Get all session memory."""
        return {
            **{k: v.get("value", v) 
               for k, v in self.long_term_memory.items()},
        }

    def clear(self):
        """Clear session memory."""
        self.session_memory = {}
        self._save_session()

    def clear_all(self):
        """Clear all memory including long-term."""
        self.session_memory = {}
        self.long_term_memory = {}
        self._save_session()
        self._save_long_term()

    def _save_session(self):
        """Save session memory to disk."""
        try:
            with open(self.session_file, "w") as f:
                json.dump(self.session_memory, f, indent=2)
        except Exception:
            pass

    def _save_long_term(self):
        """Save long-term memory to disk."""
        try:
            with open(self.long_term_file, "w") as f:
                json.dump(self.long_term_memory, f, indent=2)
        except Exception:
            pass
