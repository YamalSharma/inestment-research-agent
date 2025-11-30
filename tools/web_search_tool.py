import logging
import os
from typing import List, Dict, Any
import requests

logger = logging.getLogger(__name__)

class WebSearchTool:

    def __init__(self, api_key: str = None):
        self.tool_name = "WebSearchTool"
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        if not self.api_key:
            logger.warning("NEWS_API_KEY not set; web news will fall back to simulation.")
        logger.info(f"{self.tool_name} initialized")

    def search(
        self,
        query: str,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        
        logger.info(f"Searching: '{query}' (max_results={max_results})")

        if not self.api_key:
            return self._simulate_search_results(query, max_results)
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": self.api_key,
            "pageSize": max_results
        }
        try:
            resp = requests.get(url, params=params, timeout=7)
            resp.raise_for_status()
            articles = resp.json().get("articles", [])
            results = [
                {
                    'title': article.get('title', ''),
                    'snippet': article.get('description', '') or '',
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', '')
                }
                for article in articles[:max_results]
            ]
            logger.info(f"Found {len(results)} news results for: '{query}'")
            return results
        except Exception as e:
            logger.error(f"NewsAPI error: {e}. Falling back to simulation.")
            return self._simulate_search_results(query, max_results)

    def _simulate_search_results(
        self,
        query: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
       
        base_results = [
            {
                'title': f'Result for: {query}',
                'snippet': f'Simulated result for {query}.',
                'url': f'https://example.com/result-{i}',
                'source': 'Simulated'
            }
            for i in range(max_results)
        ]
        return base_results

    def fetch_page_content(self, url: str) -> Dict[str, Any]:
      
        logger.info(f"Fetching content from: {url}")
        return {
            'url': url,
            'content': 'Full page content would be here...',
            'title': 'Page Title',
            'text_length': 5000
        }
