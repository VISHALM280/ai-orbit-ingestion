import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

class DataProcessor:
    @staticmethod
    def sanitize_text(html_content: str) -> str:
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        return re.sub(r'\s+', ' ', soup.get_text(separator=" ")).strip()

    @staticmethod
    def normalize_url(url: str) -> str:
        if not url:
            return ""
        parsed = urlparse(url)
        return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip('/'), '', '', ''))

    @staticmethod
    def resolve_entity_name(name: str) -> str:
        return name.strip()
