"""
Investment Research & Analysis Agent

Main orchestration file for the multi-agent system.

Sequential: Research -> Analysis -> Report
Parallel:   Multiple stocks in parallel
"""
import os
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any
import logging

from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent

from memory.session_manager import SessionService
from memory.memory_bank import MemoryBank

from tools.web_search_tool import WebSearchTool
from tools.financial_calculator import FinancialCalculator

from observability.logger import setup_logging, log_agent_activity

logger = setup_logging()


from dotenv import load_dotenv

load_dotenv()  

from agents.research_agent import ResearchAgent
...



class InvestmentResearchSystem:
    

    def __init__(self, api_key: str | None = None) -> None:
        # Session + long‑term memory
        self.session_manager = SessionService()
        self.memory_bank = MemoryBank()

        # Tools
        self.web_search_tool = WebSearchTool()
        self.financial_calculator = FinancialCalculator()

        # Agents
        self.research_agent = ResearchAgent(
            api_key=api_key or "",
            tools=[self.web_search_tool],
        )
        self.analysis_agent = AnalysisAgent(
            financial_calculator=self.financial_calculator,
            memory_bank=self.memory_bank,
        )
        self.report_agent = ReportAgent(
            memory_bank=self.memory_bank,
        )

        logger.info("Investment Research System initialized successfully")

    async def research_single_stock(
        self, ticker: str, session_id: str
    ) -> Dict[str, Any]:
      
        log_agent_activity("System", f"Starting research for {ticker}", session_id)

        try:
            logger.info("[%s] Starting research phase", ticker)

            # 1) Research
            research_results = self.research_agent.research(ticker)

            # Session handling 
            session = self.session_manager.get_session(session_id)
            if session is None:
                session = self.session_manager.create_session()
                session_id = session.session_id
            session.add_research_result(ticker, research_results)
            session.update_state("last_research_timestamp", datetime.now().isoformat())
            self.session_manager.save_session(session)

            # 2) Analysis
            logger.info("[%s] Starting analysis phase", ticker)
            analysis_results = await self.analysis_agent.analyze_stock(
                ticker, research_results, session_id
            )

            session.update_state("analysis_data", analysis_results)
            self.session_manager.save_session(session)

            # 3) Report
            logger.info("[%s] Generating report", ticker)
            final_report = await self.report_agent.generate_report(
                ticker, research_results, analysis_results, session_id
            )

            # Persist to memory bank
            self.memory_bank.store_analysis(ticker, final_report)

            log_agent_activity("System", f"Completed research for {ticker}", session_id)
            return final_report

        except Exception as e:
            logger.error("Error researching %s: %s", ticker, str(e))
            log_agent_activity("System", f"Error for {ticker}: {str(e)}", session_id)
            return {"ticker": ticker, "status": "error", "error": str(e)}

    async def research_multiple_stocks(self, tickers: List[str]) -> Dict[str, Any]:
      
        batch_session = self.session_manager.create_session()
        session_id = batch_session.session_id

        batch_session.metadata["tickers"] = tickers
        batch_session.metadata["start_time"] = datetime.now().isoformat()
        batch_session.metadata["type"] = "batch_research"
        self.session_manager.save_session(batch_session)

        logger.info("Starting parallel research for %d stocks", len(tickers))
        log_agent_activity(
            "System", f"Batch research started for {tickers}", session_id
        )

        tasks = [
            self.research_single_stock(ticker, session_id) for ticker in tickers
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        successful: List[Dict[str, Any]] = []
        failed: List[str] = []

        for ticker, result in zip(tickers, results):
            if isinstance(result, Exception):
                failed.append(ticker)
                logger.error("Failed to research %s: %s", ticker, str(result))
            elif isinstance(result, dict) and result.get("status") == "error":
                failed.append(ticker)
            else:
                successful.append(result)

        comparative_report = await self.report_agent.generate_comparative_report(
            successful, session_id
        )

        batch_session.metadata["end_time"] = datetime.now().isoformat()
        batch_session.metadata["successful_count"] = len(successful)
        batch_session.metadata["failed_count"] = len(failed)
        batch_session.metadata["status"] = "completed"
        self.session_manager.save_session(batch_session)

        log_agent_activity("System", "Batch research completed", session_id)

        return {
            "session_id": session_id,
            "individual_reports": successful,
            "comparative_report": comparative_report,
            "failed_tickers": failed,
            "summary": {
                "total_stocks": len(tickers),
                "successful": len(successful),
                "failed": len(failed),
            },
        }

    def get_past_analysis(self, ticker: str) -> Dict[str, Any] | None:
        return self.memory_bank.retrieve_analysis(ticker)

    def get_session_history(self, session_id: str) -> Dict[str, Any] | None:
        summary = self.session_manager.get_session_summary(session_id)
        return summary


async def main() -> None:
    print("=" * 80)
    print("INVESTMENT RESEARCH & ANALYSIS AGENT")
    print("Multi-Agent System for Automated Stock Research")
    print("=" * 80)
    print()

    system = InvestmentResearchSystem()

    # Example 1: single stock
    print("Example 1: Researching single stock (AAPL)...")
    print("-" * 80)
    single_session = system.session_manager.create_session()
    result = await system.research_single_stock("AAPL", single_session.session_id)
    print(json.dumps(result, indent=2))
    print()

    # Simple, user-friendly summary for single stock
    try:
        ticker = result.get("ticker", "Unknown")
        rec = result.get("recommendation", {})
        action = rec.get("action", "Hold")
        confidence = rec.get("confidence_score", 50)
        risk = result.get("risk_assessment", {}).get("risk_level", "medium")
        llm_summary = result.get("llm_research_summary", "")

        print("Investor-friendly summary:")
        print(f"- For {ticker}, the system suggests: {action} "
              f"(confidence {confidence}/100, risk {risk}).")
        if llm_summary:
           
            first_sentence = llm_summary.split(". ")[0].strip()
            print(f"- Key takeaway: {first_sentence}.")
        print("- Note: This is educational analysis only and not personalized financial advice.")
        print()
    except Exception as e:
        print(f"[Summary generation error: {e}]")
        print()


    print("Example 2: Researching multiple stocks in parallel...")
    print("-" * 80)
    tickers = ["AAPL", "GOOGL", "MSFT"]
    batch_results = await system.research_multiple_stocks(tickers)
    print(json.dumps(batch_results["summary"], indent=2))
    print()

    # User-friendly batch summary: where to invest and why (at a high level)
    try:
        indiv = batch_results.get("individual_reports", [])
       
        buy_candidates = [
            r for r in indiv
            if "buy" in r.get("recommendation", {}).get("action", "").lower()
        ]
        print("High-level batch summary for this run:")
        print(f"- Total stocks analyzed: {batch_results['summary']['total_stocks']}")
        print(f"- Successful analyses: {batch_results['summary']['successful']}, "
              f"Failed: {batch_results['summary']['failed']}.")

        if buy_candidates:
            print("- Potentially most attractive ideas in this batch:")
            for r in buy_candidates:
                t = r.get("ticker", "N/A")
                rec = r.get("recommendation", {})
                action = rec.get("action", "Buy")
                conf = rec.get("confidence_score", 50)
                reason = rec.get("reasoning", "")
                print(f"  • {t}: {action} (confidence {conf}/100). Reason: {reason}")
        else:
            print("- In this run, the system did not strongly favor any one stock.")
            for r in indiv:
                t = r.get("ticker", "N/A")
                rec = r.get("recommendation", {})
                action = rec.get("action", "Hold")
                conf = rec.get("confidence_score", 50)
                print(f"  • {t}: {action} (confidence {conf}/100).")

        print("- Again, this is educational analysis only and not a direct recommendation to invest.")
        print()
    except Exception as e:
        print(f"[Batch summary generation error: {e}]")
        print()

    print("=" * 80)
    print("Research complete! Check logs for detailed observability data.")
    print("=" * 80)



if __name__ == "__main__":
    asyncio.run(main())
