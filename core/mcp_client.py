"""
REDMYTHOS CLAW 🦀 — MCP Client
Connects to Model Context Protocol servers.
Supports HTTP and local MCP servers.

Configure in: ~/.redmythos/mcp/servers.json
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console

console = Console()

class MCPClient:
    """
    MCP (Model Context Protocol) client.
    Connects to external MCP servers for extra capabilities.
    
    servers.json format:
    {
      "servers": [
        {
          "name": "filesystem",
          "type": "local",
          "command": "npx @modelcontextprotocol/server-filesystem /home"
        },
        {
          "name": "brave-search",
          "type": "http",
          "url": "http://localhost:3000/mcp"
        }
      ]
    }
    """

    def __init__(self):
        self.servers_file = Path.home() / ".redmythos" / "mcp" / "servers.json"
        self.servers_file.parent.mkdir(parents=True, exist_ok=True)
        self.registered_servers: List[Dict] = []
        self.connected_servers: Dict[str, Any] = {}
        self._load_servers()
        self._ensure_example_config()

    def _ensure_example_config(self):
        """Create example servers.json if it doesn't exist."""
        if not self.servers_file.exists():
            example = {
                "_comment": "REDMYTHOS CLAW MCP Server Configuration",
                "_docs": "Add MCP servers here. Restart to apply changes.",
                "servers": [
                    {
                        "name": "filesystem",
                        "type": "local",
                        "command": "npx -y @modelcontextprotocol/server-filesystem ~",
                        "description": "Access filesystem via MCP",
                        "enabled": False
                    },
                    {
                        "name": "brave-search",
                        "type": "http",
                        "url": "http://localhost:3001/mcp",
                        "description": "Web search via Brave",
                        "enabled": False
                    },
                    {
                        "name": "github",
                        "type": "local",
                        "command": "npx -y @modelcontextprotocol/server-github",
                        "env": {
                            "GITHUB_TOKEN": "your_token_here"
                        },
                        "description": "GitHub integration",
                        "enabled": False
                    }
                ]
            }
            with open(self.servers_file, "w") as f:
                json.dump(example, f, indent=2)

    def _load_servers(self):
        """Load server configurations from servers.json."""
        if not self.servers_file.exists():
            return
        
        try:
            with open(self.servers_file) as f:
                config = json.load(f)
                servers = config.get("servers", [])
                # Only load enabled servers
                self.registered_servers = [
                    s for s in servers
                    if s.get("enabled", True)
                ]
        except Exception as e:
            console.print(f"[red]Error loading MCP config: {e}[/red]")

    def register_server(self, server: Dict):
        """Register a server from mode file."""
        # Check if already registered
        for existing in self.registered_servers:
            if existing.get("name") == server.get("name"):
                return
        self.registered_servers.append(server)

    def list_servers(self) -> List[Dict]:
        """List all configured servers with status."""
        result = []
        for server in self.registered_servers:
            server_info = server.copy()
            name = server.get("name", "")
            server_info["status"] = (
                "connected" if name in self.connected_servers 
                else "disconnected"
            )
            result.append(server_info)
        return result

    def connect(self, server_name: str) -> str:
        """
        Connect to an MCP server.
        
        Args:
            server_name: Name of server to connect to
            
        Returns:
            Status message
        """
        server = None
        for s in self.registered_servers:
            if s.get("name") == server_name:
                server = s
                break
        
        if not server:
            return f"❌ Server '{server_name}' not found in configuration."

        server_type = server.get("type", "http")

        try:
            if server_type == "local":
                return self._connect_local(server)
            elif server_type == "http":
                return self._connect_http(server)
            else:
                return f"❌ Unknown server type: {server_type}"
        except Exception as e:
            return f"❌ Connection failed: {e}"

    def _connect_local(self, server: Dict) -> str:
        """Connect to a local MCP server process."""
        name = server.get("name")
        command = server.get("command", "")
        
        if not command:
            return f"❌ No command specified for '{name}'"

        # Store as connected (simplified - real impl would start process)
        self.connected_servers[name] = {
            "type": "local",
            "command": command,
            "server": server
        }
        
        return f"✅ Connected to local MCP server: {name}"

    def _connect_http(self, server: Dict) -> str:
        """Connect to an HTTP MCP server."""
        name = server.get("name")
        url = server.get("url", "")
        
        if not url:
            return f"❌ No URL specified for '{name}'"

        # Test connection
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=5)
            self.connected_servers[name] = {
                "type": "http",
                "url": url,
                "server": server
            }
            return f"✅ Connected to HTTP MCP server: {name} at {url}"
        except Exception as e:
            return f"⚠️ Server '{name}' at {url} is not responding: {e}"

    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool is available from any MCP server."""
        for server_data in self.connected_servers.values():
            tools = server_data.get("tools", [])
            if any(t.get("name") == tool_name for t in tools):
                return True
        return False

    def get_available_tools(self) -> List[Dict]:
        """Get all tools from connected MCP servers."""
        tools = []
        for name, server_data in self.connected_servers.items():
            server_tools = server_data.get("tools", [])
            for tool in server_tools:
                tool_copy = tool.copy()
                tool_copy["_from_mcp"] = name
                tools.append(tool_copy)
        return tools

    def call_tool(self, tool_name: str, tool_input: Dict) -> str:
        """
        Call a tool on an MCP server.
        
        Args:
            tool_name: Name of the tool
            tool_input: Tool parameters
            
        Returns:
            Tool result as string
        """
        for server_name, server_data in self.connected_servers.items():
            server_type = server_data.get("type")
            
            if server_type == "http":
                return self._call_http_tool(
                    server_data.get("url"), 
                    tool_name, 
                    tool_input
                )
        
        return f"❌ No connected server has tool: {tool_name}"

    def _call_http_tool(self, url: str, tool_name: str, tool_input: Dict) -> str:
        """Call a tool on an HTTP MCP server."""
        try:
            import urllib.request
            import urllib.parse
            
            payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": tool_input
                },
                "id": 1
            }).encode()
            
            req = urllib.request.Request(
                f"{url}/tools/call",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read())
                return json.dumps(result.get("result", result))
                
        except Exception as e:
            return f"❌ MCP tool call failed: {e}"
