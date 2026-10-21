"""
REDMYTHOS CLAW 🦀 — Web Tool
Fetch and summarize content from URLs.
"""

import ipaddress
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class WebTool:
    """Tool for fetching and processing web content."""

    def execute(self, action: str, url: str,
                selector: str = None) -> str:
        """
        Execute a web operation.

        Args:
            action: fetch/extract/headers
            url: Target URL
            selector: CSS selector for extraction

        Returns:
            Fetched content or summary
        """
        try:
            validated_url = self._validate_url(url)
        except ValueError as exc:
            return f"❌ Invalid URL: {exc}"

        try:
            if action == "fetch":
                return self._fetch(validated_url)
            if action == "extract":
                return self._extract(validated_url, selector)
            if action == "headers":
                return self._headers(validated_url)
            return f"❌ Unknown action: {action}. Use: fetch/extract/headers"
        except Exception as exc:
            return f"❌ Web tool error: {exc}"

    def _validate_url(self, url: str) -> str:
        """Reject SSRF-prone and non-HTTP targets."""
        if not isinstance(url, str) or not url.strip():
            raise ValueError("empty URL")

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("only http/https URLs are allowed")
        if not parsed.netloc:
            raise ValueError("URL is missing a hostname")

        hostname = parsed.hostname.lower() if parsed.hostname else ""
        if hostname in {"localhost", "0.0.0.0", "127.0.0.1", "::1"} or hostname.endswith(".localhost"):
            raise ValueError("localhost and loopback addresses are blocked")

        try:
            ip = ipaddress.ip_address(hostname)
        except ValueError:
            ip = None

        if ip is not None and (
            ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved
        ):
            raise ValueError("private/internal IP addresses are blocked")

        return url

    def _fetch(self, url: str) -> str:
        """Fetch URL and return text content."""
        response = requests.get(url, timeout=15, allow_redirects=False)
        if response.is_redirect or response.is_permanent_redirect:
            return "❌ Redirects are blocked to prevent SSRF or open redirect abuse."
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return f"🌐 CONTENT FROM {url}:\n\n{text[:5000]}..."

    def _extract(self, url: str, selector: str) -> str:
        """Extract specific elements using CSS selector."""
        if not selector:
            return "❌ Selector required for extract action."

        response = requests.get(url, timeout=15, allow_redirects=False)
        if response.is_redirect or response.is_permanent_redirect:
            return "❌ Redirects are blocked to prevent SSRF or open redirect abuse."
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select(selector)

        if not elements:
            return f"🔍 No elements found for selector: {selector}"

        results = [el.get_text().strip() for el in elements]
        return f"🔍 EXTRACTED ({selector}):\n\n" + "\n---\n".join(results[:20])

    def _headers(self, url: str) -> str:
        """Get HTTP headers for a URL."""
        response = requests.head(url, timeout=10, allow_redirects=False)
        headers = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
        return f"📋 HEADERS FOR {url}:\n\n{headers}"
