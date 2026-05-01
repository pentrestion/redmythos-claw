"""
REDMYTHOS CLAW 🦀 — Web Tool
Fetch and summarize content from URLs.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional

class WebTool:
    """Tool for fetching and processing web content."""

    def execute(self, action: str, url: str, 
                selector: Optional[str] = None) -> str:
        """
        Execute a web operation.
        
        Args:
            action: fetch/extract/headers
            url: Target URL
            selector: CSS selector for extraction
            
        Returns:
            Fetched content or summary
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            if action == "fetch":
                return self._fetch(url)
            elif action == "extract":
                return self._extract(url, selector)
            elif action == "headers":
                return self._headers(url)
            else:
                return f"❌ Unknown action: {action}. Use: fetch/extract/headers"
        except Exception as e:
            return f"❌ Web tool error: {e}"

    def _fetch(self, url: str) -> str:
        """Fetch URL and return text content."""
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return f"🌐 CONTENT FROM {url}:\n\n{text[:5000]}..."

    def _extract(self, url: str, selector: str) -> str:
        """Extract specific elements using CSS selector."""
        if not selector:
            return "❌ Selector required for extract action."
            
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select(selector)
        
        if not elements:
            return f"🔍 No elements found for selector: {selector}"
            
        results = [el.get_text().strip() for el in elements]
        return f"🔍 EXTRACTED ({selector}):\n\n" + "\n---\n".join(results[:20])

    def _headers(self, url: str) -> str:
        """Get HTTP headers for a URL."""
        response = requests.head(url, timeout=10)
        headers = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
        return f"📋 HEADERS FOR {url}:\n\n{headers}"
