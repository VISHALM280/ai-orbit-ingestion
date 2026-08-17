import requests
import feedparser
from typing import List, Dict, Any

class EcosystemIngestor:
    def __init__(self, github_token: str = None):
        self.headers = {"Authorization": f"token {github_token}"} if github_token else {}

    def fetch_github_repos(self, query: str = "topic:ai", limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repositories from GitHub API."""
        url = f"https://api.github.com/search/repositories?q={query}&per_page={limit}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])
        except Exception as e:
            print(f"Error fetching GitHub repos: {e}")
        return []

    def fetch_mcp_servers(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch Model Context Protocol (MCP) servers from GitHub."""
        url = f"https://api.github.com/search/repositories?q=topic:mcp-server&per_page={limit}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])
        except Exception as e:
            print(f"Error fetching MCP servers: {e}")
        return []

    def fetch_huggingface_models(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch AI models from Hugging Face API."""
        url = f"https://huggingface.co/api/models?limit={limit}&full=true"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching Hugging Face models: {e}")
        return []

    def fetch_rss_news(self, rss_url: str = "https://techcrunch.com/category/artificial-intelligence/feed/") -> List[Dict[str, Any]]:
        """Parse AI news from RSS feeds."""
        try:
            feed = feedparser.parse(rss_url)
            return feed.entries
        except Exception as e:
            print(f"Error parsing RSS feed {rss_url}: {e}")
            return []