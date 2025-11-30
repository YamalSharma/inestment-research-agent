"""
Report Agent - Generates comprehensive investment reports

This agent is responsible for:
1. Formatting analysis results into readable reports
2. Creating comparative analysis across multiple stocks
3. Generating visualizations and summaries
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import json

from memory.memory_bank import MemoryBank
from observability.logger import log_agent_activity

logger = logging.getLogger(__name__)


class ReportAgent:
    """
    Report Agent powered by LLM

    Responsibilities:
    - Generate formatted reports
    - Create comparative analysis
    - Summarize findings
    - Export reports in multiple formats
    """

    def __init__(self, memory_bank: MemoryBank) -> None:
        
        self.memory_bank = memory_bank
        self.agent_name = "ReportAgent"

        logger.info(f"{self.agent_name} initialized")

    async def generate_report(
        self,
        ticker: str,
        research_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
        session_id: str,
    ) -> Dict[str, Any]:
       
        log_agent_activity(
            self.agent_name,
            f"Generating report for {ticker}",
            session_id,
        )

        report: Dict[str, Any] = {
            "ticker": ticker,
            "report_date": datetime.now().isoformat(),
            "executive_summary": self._generate_executive_summary(
                ticker, research_data, analysis_data
            ),
            # NEW: explicitly expose Gemini summary from ResearchAgent, if present
            "llm_research_summary": research_data.get("summary", ""),
            "company_overview": self._format_company_overview(research_data),
            "financial_analysis": self._format_financial_analysis(analysis_data),
            "sentiment_analysis": self._format_sentiment_analysis(analysis_data),
            "risk_assessment": self._format_risk_assessment(analysis_data),
            "recommendation": self._format_recommendation(analysis_data),
            "recent_news": self._format_news(research_data),
            "metadata": {
                "session_id": session_id,
                "generated_at": datetime.now().isoformat(),
            },
        }

        log_agent_activity(
            self.agent_name,
            f"Report generated for {ticker}",
            session_id,
        )

        return report

    async def generate_comparative_report(
        self,
        stock_reports: List[Dict[str, Any]],
        session_id: str,
    ) -> Dict[str, Any]:
       
        log_agent_activity(
            self.agent_name,
            f"Generating comparative report for {len(stock_reports)} stocks",
            session_id,
        )

        comparative_report: Dict[str, Any] = {
            "report_date": datetime.now().isoformat(),
            "stocks_analyzed": len(stock_reports),
            "comparison_table": self._create_comparison_table(stock_reports),
            "top_picks": self._identify_top_picks(stock_reports),
            "risk_comparison": self._compare_risks(stock_reports),
            "sentiment_overview": self._compare_sentiments(stock_reports),
            "summary": self._generate_comparative_summary(stock_reports),
        }

        log_agent_activity(
            self.agent_name,
            "Comparative report generated",
            session_id,
        )

        return comparative_report

    def _generate_executive_summary(
        self,
        ticker: str,
        research_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
    ) -> str:
        recommendation = analysis_data.get("recommendation", {})
        action = recommendation.get("action", "Hold")

        sentiment = analysis_data.get("sentiment_analysis", {})
        overall_sentiment = sentiment.get("overall_sentiment", "neutral")

        risk = analysis_data.get("risk_assessment", {})
        risk_level = risk.get("risk_level", "medium")

        summary = (
            f"{ticker} Analysis Summary: "
            f"Recommendation: {action} | "
            f"Market Sentiment: {overall_sentiment.capitalize()} | "
            f"Risk Level: {risk_level.capitalize()}"
        )

        return summary

    def _format_company_overview(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
       
        company_info = research_data.get("company_info", {})

        return {
            "summary": company_info.get("summary", "N/A"),
            "business_model": company_info.get("business_model", "N/A"),
            "key_products": company_info.get("key_products", []),
            "sources": company_info.get("sources", []),
        }

    def _format_financial_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        
        financial = analysis_data.get("financial_analysis", {})

        return {
            "valuation_score": financial.get("valuation_score", "N/A"),
            "valuation_category": financial.get("valuation_category", "N/A"),
            "key_metrics": financial.get("key_metrics", {}),
            "financial_health": financial.get("financial_health", "N/A"),
        }

    def _format_sentiment_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
      
        sentiment = analysis_data.get("sentiment_analysis", {})

        return {
            "overall_sentiment": sentiment.get("overall_sentiment", "neutral"),
            "confidence": sentiment.get("confidence", 0),
            "positive_count": sentiment.get("positive_count", 0),
            "negative_count": sentiment.get("negative_count", 0),
            "neutral_count": sentiment.get("neutral_count", 0),
            "recent_headlines": sentiment.get("recent_headlines", []),
        }

    def _format_risk_assessment(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        
        risk = analysis_data.get("risk_assessment", {})

        return {
            "risk_level": risk.get("risk_level", "medium"),
            "risk_score": risk.get("risk_score", 50),
            "risk_factors": risk.get("risk_factors", []),
            "mitigation_suggestions": risk.get("mitigation_suggestions", []),
        }

    def _format_recommendation(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        
        recommendation = analysis_data.get("recommendation", {})

        return {
            "action": recommendation.get("action", "Hold"),
            "confidence_score": recommendation.get("confidence_score", 50),
            "reasoning": recommendation.get("reasoning", ""),
            "time_horizon": recommendation.get("time_horizon", ""),
            "key_points": recommendation.get("key_points", []),
        }

    def _format_news(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        return research_data.get("recent_news", [])

    def _create_comparison_table(self, stock_reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
      
        comparison: List[Dict[str, Any]] = []

        for report in stock_reports:
            ticker = report.get("ticker", "N/A")
            recommendation = report.get("recommendation", {})
            sentiment = report.get("sentiment_analysis", {})
            risk = report.get("risk_assessment", {})

            comparison.append(
                {
                    "ticker": ticker,
                    "recommendation": recommendation.get("action", "Hold"),
                    "confidence": recommendation.get("confidence_score", 50),
                    "sentiment": sentiment.get("overall_sentiment", "neutral"),
                    "risk_level": risk.get("risk_level", "medium"),
                    "risk_score": risk.get("risk_score", 50),
                }
            )

        return comparison

    def _identify_top_picks(self, stock_reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
       
        sorted_reports = sorted(
            stock_reports,
            key=lambda x: x.get("recommendation", {}).get("confidence_score", 0),
            reverse=True,
        )

        top_picks: List[Dict[str, Any]] = []
        for report in sorted_reports[:3]:
            ticker = report.get("ticker", "N/A")
            recommendation = report.get("recommendation", {})

            top_picks.append(
                {
                    "ticker": ticker,
                    "action": recommendation.get("action", "Hold"),
                    "confidence": recommendation.get("confidence_score", 50),
                    "reasoning": recommendation.get("reasoning", ""),
                }
            )

        return top_picks

    def _compare_risks(self, stock_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
       
        risk_levels: Dict[str, List[str]] = {"low": [], "medium": [], "high": []}

        for report in stock_reports:
            ticker = report.get("ticker", "N/A")
            risk = report.get("risk_assessment", {})
            risk_level = risk.get("risk_level", "medium")

            risk_levels[risk_level].append(ticker)

        return {
            "low_risk_stocks": risk_levels["low"],
            "medium_risk_stocks": risk_levels["medium"],
            "high_risk_stocks": risk_levels["high"],
        }

    def _compare_sentiments(self, stock_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare sentiment across stocks."""
        sentiments: Dict[str, List[str]] = {"positive": [], "neutral": [], "negative": []}

        for report in stock_reports:
            ticker = report.get("ticker", "N/A")
            sentiment = report.get("sentiment_analysis", {})
            overall = sentiment.get("overall_sentiment", "neutral")

            sentiments.setdefault(overall, []).append(ticker)

        return {
            "positive_sentiment_stocks": sentiments.get("positive", []),
            "neutral_sentiment_stocks": sentiments.get("neutral", []),
            "negative_sentiment_stocks": sentiments.get("negative", []),
        }

    def _generate_comparative_summary(self, stock_reports: List[Dict[str, Any]]) -> str:
        """Generate summary for comparative analysis."""
        total_stocks = len(stock_reports)

        buy_count = sum(
            1
            for r in stock_reports
            if "Buy" in r.get("recommendation", {}).get("action", "")
        )
        hold_count = sum(
            1
            for r in stock_reports
            if "Hold" in r.get("recommendation", {}).get("action", "")
        )
        sell_count = sum(
            1
            for r in stock_reports
            if "Sell" in r.get("recommendation", {}).get("action", "")
        )

        summary = (
            f"Analyzed {total_stocks} stocks. "
            f"Recommendations: {buy_count} Buy, {hold_count} Hold, {sell_count} Sell."
        )

        return summary
