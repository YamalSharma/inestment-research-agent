"""
Analysis Agent - Analyzes research data and calculates financial metrics

This agent is responsible for:
1. Processing research data from Research Agent
2. Calculating financial metrics and ratios
3. Performing sentiment analysis on news
4. Generating investment insights
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from tools.financial_calculator import FinancialCalculator
from memory.memory_bank import MemoryBank
from observability.logger import log_agent_activity


logger = logging.getLogger(__name__)

class AnalysisAgent:
    """
    Analysis Agent powered by LLM
    
    Responsibilities:
    - Financial metric calculation
    - Sentiment aggregation
    - Risk assessment
    - Investment recommendation generation
    """
    
    def __init__(self, financial_calculator: FinancialCalculator, memory_bank: MemoryBank):
        
        self.financial_calculator = financial_calculator
        self.memory_bank = memory_bank
        self.agent_name = "AnalysisAgent"
        
        logger.info(f"{self.agent_name} initialized")
    
    async def analyze_stock(
        self, 
        ticker: str, 
        research_data: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        
        log_agent_activity(
            self.agent_name,
            f"Starting analysis for {ticker}",
            session_id
        )
        
        analysis_results = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'financial_analysis': None,
            'sentiment_analysis': None,
            'risk_assessment': None,
            'recommendation': None
        }
        
        try:
            # Step 1: Analyze financial metrics
            logger.info(f"[{ticker}] Analyzing financial metrics")
            financial_highlights = research_data.get('financial_highlights', {})
            analysis_results['financial_analysis'] = self._analyze_financials(
                ticker,
                financial_highlights
            )
            
            log_agent_activity(
                self.agent_name,
                f"Financial analysis complete for {ticker}",
                session_id
            )
            
            # Step 2: Aggregate sentiment from news
            logger.info(f"[{ticker}] Analyzing news sentiment")
            recent_news = research_data.get('recent_news', [])
            analysis_results['sentiment_analysis'] = self._analyze_sentiment(
                recent_news
            )
            
            log_agent_activity(
                self.agent_name,
                f"Sentiment analysis complete for {ticker}",
                session_id
            )
            
            # Step 3: Assess risk factors
            logger.info(f"[{ticker}] Assessing risk factors")
            analysis_results['risk_assessment'] = self._assess_risk(
                analysis_results['financial_analysis'],
                analysis_results['sentiment_analysis']
            )
            
            # Step 4: Generate recommendation
            logger.info(f"[{ticker}] Generating recommendation")
            analysis_results['recommendation'] = self._generate_recommendation(
                analysis_results['financial_analysis'],
                analysis_results['sentiment_analysis'],
                analysis_results['risk_assessment']
            )
            
            # Compare with past analysis if available (using memory)
            past_analysis = self.memory_bank.retrieve_analysis(ticker)
            if past_analysis:
                analysis_results['comparison_with_past'] = self._compare_with_past(
                    analysis_results,
                    past_analysis
                )
            
            log_agent_activity(
                self.agent_name,
                f"Analysis complete for {ticker}",
                session_id
            )
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error during analysis for {ticker}: {str(e)}")
            log_agent_activity(
                self.agent_name,
                f"Error analyzing {ticker}: {str(e)}",
                session_id
            )
            raise
    
    def _analyze_financials(
        self, 
        ticker: str, 
        financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
       
        # Use financial calculator tool to compute metrics
        valuation_score = self.financial_calculator.calculate_valuation_score(
            pe_ratio=financial_data.get('pe_ratio'),
            revenue_growth=financial_data.get('revenue_growth'),
            profit_margin=financial_data.get('profit_margin')
        )
        
        financial_analysis = {
            'valuation_score': valuation_score,
            'valuation_category': self._categorize_valuation(valuation_score),
            'key_metrics': {
                'pe_ratio': financial_data.get('pe_ratio', 'N/A'),
                'revenue': financial_data.get('revenue', 'N/A'),
                'earnings': financial_data.get('earnings', 'N/A'),
                'market_cap': financial_data.get('market_cap', 'N/A')
            },
            'financial_health': self._assess_financial_health(financial_data)
        }
        
        logger.info(f"Financial analysis complete for {ticker}: "
                   f"Valuation score = {valuation_score}")
        
        return financial_analysis
    
    def _analyze_sentiment(self, news_items: List[Dict]) -> Dict[str, Any]:
       
        if not news_items:
            return {
                'overall_sentiment': 'neutral',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'confidence': 0
            }
        
        # Count sentiment types
        sentiments = [item.get('sentiment', 'neutral') for item in news_items]
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        # Determine overall sentiment
        if positive_count > negative_count:
            overall = 'positive'
        elif negative_count > positive_count:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        # Calculate confidence based on consensus
        total = len(sentiments)
        max_count = max(positive_count, negative_count, neutral_count)
        confidence = (max_count / total) * 100 if total > 0 else 0
        
        sentiment_analysis = {
            'overall_sentiment': overall,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'confidence': round(confidence, 2),
            'recent_headlines': [item.get('title', '') for item in news_items[:3]]
        }
        
        logger.info(f"Sentiment analysis: {overall} "
                   f"(confidence: {sentiment_analysis['confidence']}%)")
        
        return sentiment_analysis
    
    def _assess_risk(
        self, 
        financial_analysis: Dict[str, Any],
        sentiment_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        # Calculate risk score (0-100, higher = more risk)
        risk_factors = []
        risk_score = 50  
        
        # Factor 1: Valuation
        valuation_category = financial_analysis.get('valuation_category', 'fair')
        if valuation_category == 'overvalued':
            risk_score += 15
            risk_factors.append("Stock may be overvalued")
        elif valuation_category == 'undervalued':
            risk_score -= 10
        
        # Factor 2: Sentiment
        overall_sentiment = sentiment_analysis.get('overall_sentiment', 'neutral')
        if overall_sentiment == 'negative':
            risk_score += 20
            risk_factors.append("Negative news sentiment")
        elif overall_sentiment == 'positive':
            risk_score -= 15
        
        # Factor 3: Sentiment confidence
        confidence = sentiment_analysis.get('confidence', 0)
        if confidence < 50:
            risk_score += 10
            risk_factors.append("Mixed or uncertain market sentiment")
        
        # Normalize risk score
        risk_score = max(0, min(100, risk_score))
        
        # Categorize risk
        if risk_score < 30:
            risk_level = 'low'
        elif risk_score < 60:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        risk_assessment = {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'mitigation_suggestions': self._suggest_risk_mitigation(risk_level)
        }
        
        logger.info(f"Risk assessment: {risk_level} (score: {risk_score})")
        
        return risk_assessment
    
    def _generate_recommendation(self, financial_data: Dict[str, Any], sentiment: Dict[str, Any], risk: Dict[str, Any]) -> Dict[str, Any]:
        
        valuation_score = financial_data.get("valuation_score", 50.0)
        
        # Use the calculator's recommendation logic
        rec = self.financial_calculator.get_recommendation_from_score(valuation_score)
        
        return {
            "action": rec["action"],  
            "confidence_score": rec["confidence"],
            "reasoning": f"Valuation score {valuation_score:.1f}: {rec['action']} signal. Sentiment: {sentiment['overall_sentiment']}, Risk: {risk['risk_level']}.",
            "time_horizon": "medium-term (6-12 months)",
            "key_points": [
                f"Valuation: {valuation_score:.1f}/100",
                f"Sentiment: {sentiment['overall_sentiment']}",
                f"Risk: {risk['risk_level']}",
            ],
        }

    
    def _categorize_valuation(self, score: float) -> str:
        """Categorize valuation based on score"""
        if score < 40:
            return 'undervalued'
        elif score > 60:
            return 'overvalued'
        else:
            return 'fair'
    
    def _assess_financial_health(self, financial_data: Dict) -> str:
        """Assess overall financial health"""
        
        return 'healthy'
    
    def _suggest_risk_mitigation(self, risk_level: str) -> List[str]:
        """Suggest risk mitigation strategies"""
        if risk_level == 'high':
            return [
                "Consider smaller position size",
                "Use stop-loss orders",
                "Diversify across multiple stocks"
            ]
        elif risk_level == 'medium':
            return [
                "Monitor regularly",
                "Maintain balanced portfolio"
            ]
        else:
            return ["Continue regular monitoring"]
    
    def _generate_reasoning(self, financial, sentiment, risk, action) -> str:
        """Generate reasoning for recommendation"""
        return (f"Based on {financial.get('valuation_category', 'fair')} valuation, "
                f"{sentiment.get('overall_sentiment', 'neutral')} sentiment, "
                f"and {risk.get('risk_level', 'medium')} risk level.")
    
    def _suggest_time_horizon(self, risk_level: str) -> str:
        """Suggest investment time horizon"""
        if risk_level == 'low':
            return 'long-term (1+ years)'
        elif risk_level == 'medium':
            return 'medium-term (6-12 months)'
        else:
            return 'short-term (< 6 months)'
    
    def _extract_key_points(self, financial, sentiment, risk) -> List[str]:
        """Extract key points for the recommendation"""
        points = []
        points.append(f"Valuation: {financial.get('valuation_category', 'fair')}")
        points.append(f"Sentiment: {sentiment.get('overall_sentiment', 'neutral')}")
        points.append(f"Risk: {risk.get('risk_level', 'medium')}")
        return points
    
    def _compare_with_past(self, current, past) -> Dict[str, Any]:
        """Compare current analysis with past analysis from memory"""
        return {
            'has_improved': True,  # Simplified for demo
            'key_changes': ['Sentiment improved', 'Valuation more attractive']
        }