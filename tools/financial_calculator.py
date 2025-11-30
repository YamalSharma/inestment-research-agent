"""
Financial Calculator Tool - Custom tool for financial metric calculations

This tool provides agents with financial calculation capabilities including:
- Valuation score calculation (based on PE, growth, margins)
- Ratio analysis
- Growth rate computation
- Risk metrics
"""

import logging
import re
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class FinancialCalculator:
   
    
    def __init__(self):
       
        logger.info("FinancialCalculatorTool initialized")
    
    def calculate_valuation_score(
            self,
            pe_ratio: float | None = None,
            revenue_growth: float | None = None,
            profit_margin: float | None = None,
        ) -> float:
           
            score = 50.0  # neutral baseline

            # PE Ratio: Lower PE = cheaper valuation
            if pe_ratio is not None:
                try:
                    pe = float(pe_ratio)
                    if pe < 12:
                        score += 25  
                    elif pe < 18:
                        score += 15  
                    elif pe < 25:
                        score += 5  
                    elif pe < 35:
                        score -= 10  
                    else:
                        score -= 25  
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse PE ratio: {pe_ratio}")

            # Revenue Growth: Higher growth = better fundamentals
            if revenue_growth is not None:
                try:
                    rg = self._parse_percentage(revenue_growth)
                    if rg is None:
                        raise ValueError()
                    if rg > 0.20:  
                        score += 20
                    elif rg > 0.10:  
                        score += 10
                    elif rg > 0.05: 
                        score += 5
                    elif rg < 0:  
                        score -= 20
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse revenue growth: {revenue_growth}")

            # Profit Margin: Higher margin = stronger profitability
            if profit_margin is not None:
                try:
                    pm = self._parse_percentage(profit_margin)
                    if pm is None:
                        raise ValueError()
                    if pm > 0.25:  
                        score += 15
                    elif pm > 0.15:  
                        score += 8
                    elif pm > 0.08:  
                        score += 3
                    elif pm < 0.05: 
                        score -= 15
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse profit margin: {profit_margin}")

            # Clamp score to 0-100
            final_score = max(0.0, min(100.0, score))
            logger.info(f"Valuation score calculated: {final_score:.1f} (PE={pe_ratio}, Growth={revenue_growth}, Margin={profit_margin})")
            return final_score
    
    def get_recommendation_from_score(self, valuation_score: float) -> Dict[str, Any]:
      
        if valuation_score > 70:
            return {
                "action": "Buy",
                "confidence": min(95, 50 + (valuation_score - 70) * 2),
            }
        elif valuation_score > 55:
            return {
                "action": "Hold",
                "confidence": 60,
            }
        elif valuation_score > 35:
            return {
                "action": "Hold",
                "confidence": 50,
            }
        else:
            return {
                "action": "Sell",
                "confidence": min(90, 50 + (35 - valuation_score)),
            }
    
    def calculate_growth_score(self, revenue_growth: str, earnings_growth: str) -> float:
      
        logger.info(f"Calculating growth score - Revenue: {revenue_growth}, Earnings: {earnings_growth}")
        
        try:
            # Parse growth rates
            rev_growth = self._parse_percentage(revenue_growth)
            earn_growth = self._parse_percentage(earnings_growth)
            
            if rev_growth is None or earn_growth is None:
                logger.warning("Could not parse growth rates, using neutral score")
                return 0.5
            
            # Score based on growth rates
            # Strong growth: >20%, Moderate: 10-20%, Weak: <10%
            rev_score = min(rev_growth / 0.20, 1.0)  # Normalize to 20% as max
            earn_score = min(earn_growth / 0.25, 1.0)  # Normalize to 25% as max
            
            # Weighted combination (earnings growth weighted higher)
            growth_score = (rev_score * 0.4) + (earn_score * 0.6)
            
            logger.info(f"Growth score calculated: {growth_score:.3f}")
            return growth_score
            
        except Exception as e:
            logger.error(f"Error calculating growth score: {str(e)}")
            return 0.5
    
    def calculate_profitability_score(self, operating_margin: str, roe: str) -> float:
       
        logger.info(f"Calculating profitability score - Margin: {operating_margin}, ROE: {roe}")
        
        try:
            margin = self._parse_percentage(operating_margin)
            roe_value = self._parse_percentage(roe)
            
            if margin is None or roe_value is None:
                logger.warning("Could not parse profitability metrics, using neutral score")
                return 0.5
            
            # Score based on profitability metrics
            # Strong margins: >25%, ROE: >20%
            margin_score = min(margin / 0.30, 1.0)  # Normalize to 30% as excellent
            roe_score = min(roe_value / 0.25, 1.0)  # Normalize to 25% as excellent
            
            profitability_score = (margin_score * 0.5) + (roe_score * 0.5)
            
            logger.info(f"Profitability score calculated: {profitability_score:.3f}")
            return profitability_score
            
        except Exception as e:
            logger.error(f"Error calculating profitability score: {str(e)}")
            return 0.5
    
    def _parse_numeric_value(self, value: str) -> Optional[float]:
      
        if not value:
            return None
        
        try:
            # Remove currency symbols, commas, % sign, and whitespace
            cleaned = re.sub(r'[$,%\s]', '', str(value))
            
            # Try to convert to float
            return float(cleaned)
            
        except (ValueError, TypeError):
            logger.warning(f"Could not parse numeric value: {value}")
            return None
    
    def _parse_percentage(self, value: str) -> Optional[float]:
        
        parsed = self._parse_numeric_value(value)
        
        if parsed is None:
            return None
        
        # If value is large (>1), assume it's in percentage format
        if parsed > 1:
            return parsed / 100.0
        
        return parsed
    
    def _calculate_market_cap_score(self, market_cap: str) -> float:
      
        if not market_cap:
            return 0.5
        
        try:
            # Extract numeric value and unit
            cleaned = market_cap.upper().replace('$', '').replace(',', '').strip()
            
            # Determine multiplier
            if 'T' in cleaned:
                multiplier = 1000  # Trillion to Billion
                cleaned = cleaned.replace('T', '')
            elif 'B' in cleaned:
                multiplier = 1
                cleaned = cleaned.replace('B', '')
            elif 'M' in cleaned:
                multiplier = 0.001  # Million to Billion
                cleaned = cleaned.replace('M', '')
            else:
                # Assume it's already in billions
                multiplier = 1
            
            value_billions = float(cleaned) * multiplier
            
            if value_billions > 200:
                return 0.7
            elif value_billions > 10:
                return 0.6
            elif value_billions > 2:
                return 0.5
            else:
                return 0.4
                
        except Exception as e:
            logger.warning(f"Could not parse market cap: {market_cap}, error: {str(e)}")
            return 0.5
    
    def calculate_composite_score(self, metrics: Dict[str, str]) -> float:
       
        logger.info("Calculating composite financial score")
        
        scores = []
        
        # Valuation score
        if 'pe_ratio' in metrics and 'market_cap' in metrics:
            val_score = self.calculate_valuation_score(
                metrics['pe_ratio'], 
                metrics['market_cap']
            )
            scores.append(val_score)
        
        # Growth score
        if 'revenue_growth' in metrics and 'earnings_growth' in metrics:
            growth_score = self.calculate_growth_score(
                metrics['revenue_growth'],
                metrics['earnings_growth']
            )
            scores.append(growth_score)
        
        # Profitability score
        if 'operating_margin' in metrics and 'roe' in metrics:
            profit_score = self.calculate_profitability_score(
                metrics['operating_margin'],
                metrics['roe']
            )
            scores.append(profit_score)
        
        # Calculate average if we have any scores
        if scores:
            composite = sum(scores) / len(scores)
            logger.info(f"Composite score calculated: {composite:.3f} from {len(scores)} metrics")
            return composite
        
        logger.warning("No valid metrics for composite score calculation")
        return 0.5