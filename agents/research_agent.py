"""
Research Agent - Gathers information from web sources


This agent is responsible for:
- Searching for company information, news, and financial data
- Fetching real financial metrics from yfinance
- Extracting and structuring research data
- Applying context compaction to summarize lengthy content


Uses: Google Search tool, yfinance, Gemini LLM for summarization
"""


import os
import logging
from typing import Dict, List, Any


import google.generativeai as genai
import yfinance as yf


logger = logging.getLogger(__name__)



class ResearchAgent:
    """
    Research Agent powered by Gemini LLM


    This agent uses web search tools, yfinance, and LLM capabilities to:
    1. Find relevant information about stocks/companies
    2. Extract real financial data from Yahoo Finance
    3. Summarize lengthy articles (context engineering)
    4. Structure data for analysis
    """


    def __init__(self, api_key: str | None, tools: List[Any]) -> None:
    
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.tools = tools
        self.web_search_tool = tools[0] if tools else None


        # Configure Gemini 
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("models/gemini-2.0-flash")
            logger.info("Research Agent initialized with Gemini model")
        else:
            self.model = None
            logger.warning("Research Agent initialized without API key - limited functionality")


    def research(self, symbol: str) -> Dict[str, Any]:
       
        logger.info(f"ResearchAgent: Starting research for {symbol}")


        research_data: Dict[str, Any] = {
            "symbol": symbol,
            "company_name": "",
            "company_info": {},
            "recent_news": [],
            "financial_highlights": {},
            "sources": [],
            "raw_data": [],
        }

        try:
            # Search 1: Company information
            logger.info(f"Searching company information for {symbol}")
            company_results = self._search_company_info(symbol)
            research_data["company_info"] = company_results
            research_data["company_name"] = company_results.get("name", symbol)


            # Search 2: Recent news
            logger.info(f"Searching recent news for {symbol}")
            news_results = self._search_recent_news(symbol)
            research_data["recent_news"] = news_results


            # Search 3: Real financial metrics from yfinance
            logger.info(f"Fetching real financial metrics for {symbol} from yfinance")
            financial_results = self._fetch_real_financial_metrics(symbol)
            research_data["financial_highlights"] = financial_results


            # Context compaction - summarize lengthy content
            if self.model:
                logger.info("Applying context compaction to research data")
                research_data["summary"] = self._compact_context(research_data)


            logger.info(f"Research complete for {symbol}")
            return research_data


        except Exception as e:
            logger.error(f"Error during research for {symbol}: {str(e)}")
            research_data["error"] = str(e)
            return research_data


    def _search_company_info(self, symbol: str) -> Dict[str, Any]:
       
        if not self.web_search_tool:
            return self._mock_company_info(symbol)


        # Use web search tool to find company information
        query = f"{symbol} company information stock overview"
        results = self.web_search_tool.search(query, max_results=3)


        # Extract relevant information
        company_info = {
            "name": self._extract_company_name(symbol, results),
            "industry": self._extract_field(results, "industry"),
            "sector": self._extract_field(results, "sector"),
            "description": self._extract_field(results, "description"),
            "sources": [r.get("url", "") for r in results],
        }


        return company_info


    def _search_recent_news(self, symbol: str) -> List[Dict[str, Any]]:
        
        if not self.web_search_tool:
            return self._mock_news(symbol)


        query = f"{symbol} stock news latest"
        results = self.web_search_tool.search(query, max_results=5)


        news_articles: List[Dict[str, Any]] = []
        for result in results:
            article = {
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "url": result.get("url", ""),
                "date": result.get("date", ""),
            }
            news_articles.append(article)


        return news_articles


    def _fetch_real_financial_metrics(self, symbol: str) -> Dict[str, Any]:
       
        try:
            logger.info(f"Fetching real financial data for {symbol} from yfinance")
            stock = yf.Ticker(symbol)
            info = stock.info 


            # Extract real values from yfinance
            pe_ratio = info.get("trailingPE") or info.get("forwardPE")
            market_cap = info.get("marketCap")
            revenue = info.get("totalRevenue")
            earnings = info.get("netIncomeToCommon")
            profit_margin = info.get("profitMargins")
            revenue_growth = info.get("revenueGrowth")


            # Helper function to format large numbers
            def format_large_number(val):
                if val is None:
                    return "N/A"
                v = float(val)
                if v >= 1e12:
                    return f"${v/1e12:.2f}T"
                if v >= 1e9:
                    return f"${v/1e9:.2f}B"
                if v >= 1e6:
                    return f"${v/1e6:.2f}M"
                return f"${v:,.0f}"


            metrics = {
                "pe_ratio": f"{pe_ratio:.2f}" if pe_ratio is not None else "N/A",
                "market_cap": format_large_number(market_cap),
                "revenue": f"${revenue/1e9:.2f}B" if revenue else "N/A",
                "earnings": f"${earnings/1e9:.2f}B" if earnings else "N/A",
                "profit_margin": f"{profit_margin*100:.2f}%" if profit_margin else "N/A",
                "revenue_growth": f"{revenue_growth*100:.2f}%" if revenue_growth else "N/A",
                "52_week_high": f"${info.get('fiftyTwoWeekHigh', 'N/A')}" if info.get('fiftyTwoWeekHigh') else "N/A",
                "52_week_low": f"${info.get('fiftyTwoWeekLow', 'N/A')}" if info.get('fiftyTwoWeekLow') else "N/A",
                "current_price": f"${info.get('currentPrice', 'N/A')}" if info.get('currentPrice') else "N/A",
            }


            logger.info(f"Real financial data fetched for {symbol}: PE={metrics['pe_ratio']}, Market Cap={metrics['market_cap']}")
            return metrics


        except Exception as e:
            logger.error(f"Error fetching real financials for {symbol}: {str(e)}")
            logger.warning(f"Falling back to mock data for {symbol}")
            return self._mock_financial_metrics(symbol)


    def _compact_context(self, research_data: Dict[str, Any]) -> str:
        
        if not self.model:
            return "Context compaction unavailable without API key"


        try:
            prompt = f"""
Summarize the following investment research data concisely:


Company: {research_data.get('company_name', 'Unknown')}
Industry: {research_data.get('company_info', {}).get('industry', 'Unknown')}


Recent News ({len(research_data.get('recent_news', []))} articles):
{self._format_news_for_summary(research_data.get('recent_news', []))}


Financial Metrics:
{self._format_metrics_for_summary(research_data.get('financial_highlights', {}))}


Provide a 3-4 sentence summary highlighting the most important points for an investor.
"""
            response = self.model.generate_content(prompt)
            summary = (getattr(response, "text", "") or "").strip()


            logger.info("Context compaction complete")
            return summary


        except Exception as e:
            logger.error(f"Error in context compaction: {str(e)}")
            return f"Error generating summary: {str(e)}"


    def _format_news_for_summary(self, news: List[Dict[str, Any]]) -> str:
        """Format news articles for summary"""
        formatted: List[str] = []
        for article in news[:3]: 
            formatted.append(f"- {article.get('title', 'No title')}")
        return "\n".join(formatted)


    def _format_metrics_for_summary(self, metrics: Dict[str, Any]) -> str:
        """Format financial metrics for summary"""
        formatted: List[str] = []
        for key, value in metrics.items():
            if value and value != "N/A":
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}")
        return "\n".join(formatted)


    def _extract_company_name(self, symbol: str, results: List[Dict[str, Any]]) -> str:
        """Extract company name from search results"""
        for result in results:
            title = result.get("title", "")
            if symbol in title:
                return title.split("-")[0].strip() if "-" in title else symbol
        return symbol


    def _extract_field(self, results: List[Dict[str, Any]], field: str) -> str:
        """Extract specific field from search results"""
        for result in results:
            snippet = result.get("snippet", "").lower()
            if field.lower() in snippet:
                return f"Information about {field} found"
        return "Not found"


    # Mock data methods for demonstration when no API key or yfinance fails
    def _mock_company_info(self, symbol: str) -> Dict[str, Any]:
        """Mock company information"""
        mock_data: Dict[str, Dict[str, Any]] = {
            "AAPL": {"name": "Apple Inc.", "industry": "Technology", "sector": "Consumer Electronics"},
            "MSFT": {"name": "Microsoft Corporation", "industry": "Technology", "sector": "Software"},
            "GOOGL": {"name": "Alphabet Inc.", "industry": "Technology", "sector": "Internet Services"},
        }
        return mock_data.get(symbol, {"name": symbol, "industry": "Unknown", "sector": "Unknown"})


    def _mock_news(self, symbol: str) -> List[Dict[str, Any]]:
        """Mock news data"""
        return [
            {
                "title": f"{symbol} announces strong quarterly earnings",
                "snippet": "Company beats expectations",
                "url": "https://example.com/news1",
            },
            {
                "title": f"{symbol} launches new product line",
                "snippet": "Innovation drives growth",
                "url": "https://example.com/news2",
            },
        ]


    def _mock_financial_metrics(self, symbol: str) -> Dict[str, Any]:
        """Mock financial metrics - fallback when yfinance fails"""
        return {
            "current_price": "$150.25",
            "pe_ratio": "25.5",
            "market_cap": "$2.5T",
            "revenue": "$365.82B",
            "earnings": "$93.74B",
            "profit_margin": "25.65%",
            "revenue_growth": "5.23%",
            "52_week_high": "$180.00",
            "52_week_low": "$120.00",
        }
