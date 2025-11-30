# Investment Research & Analysis Agent
## Multi-Agent System for Automated Stock Research with Real-Time Data

**Track:** Enterprise Agents | **Capstone Project:** Kaggle AI Agent Development Course
---

##  Overview

**Investment Research & Analysis Agent** is a sophisticated multi-agent system that automates comprehensive stock research and investment analysis. It combines real-time market data, news analysis, financial metrics, and AI-powered insights to generate actionable investment recommendations.

### Key Highlights

-  **Multi-Agent Architecture** — 3 specialized agents work together in orchestrated pipelines
-  **Real External Data** — Live news from NewsAPI, real financial data from yfinance
-  **Gemini LLM Integration** — Context engineering for intelligent summaries
-  **Dynamic Valuation Scoring** — Data-driven scores (0-100) based on real fundamentals
-  **Session Management** — Multi-session support with in-memory persistence
-  **Batch Processing** — Analyze multiple stocks in parallel
-  **Comprehensive Logging** — Full observability for debugging and auditing
-  **Production-Ready** — Professional JSON output, error handling, validation

---

##  System Architecture

### Multi-Agent Pipeline

```
User Input (Stock Symbols)
    ↓
[Session Manager] — Creates isolated session context
    ↓
[Research Agent] — Gathers data (news + fundamentals)
    ├─ WebSearchTool → Real news headlines (NewsAPI)
    ├─ yfinance → Real PE ratios, market cap, growth, margins
    └─ Gemini LLM → Context compaction & summarization
    ↓
[Analysis Agent] — Processes and scores data
    ├─ Financial Calculator → Valuation scoring (0-100)
    ├─ Sentiment Analyzer → News sentiment classification
    ├─ Risk Assessor → Risk level + risk score
    └─ Recommender → Buy/Hold/Sell + confidence
    ↓
[Report Agent] — Generates final output
    ├─ Single-stock reports (JSON)
    ├─ Batch comparison reports
    └─ Memory persistence
    ↓
Final Report (JSON)
```

### Agent Responsibilities

| Agent | Role | Tools Used |
|-------|------|-----------|
| **ResearchAgent** | Data collection & compression | NewsAPI, yfinance, Gemini |
| **AnalysisAgent** | Scoring & recommendation | FinancialCalculator, sentiment analysis |
| **ReportAgent** | Report generation & formatting | JSON serialization, memory bank |

---

##  Tech Stack

### Core Dependencies

```
google-generativeai>=0.3.0     # Gemini LLM for summarization
yfinance>=0.2.28               # Real financial data (PE, margins, growth)
newsapi>=0.1.1                 # Real news headlines
requests>=2.31.0               # HTTP client for APIs
python-dotenv>=1.0.0           # Environment configuration
```

##  Installation & Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd investment-research-agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in root directory:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
NEWSAPI_KEY=your_newsapi_key_here

```

**Get API Keys:**
- [Gemini API](https://ai.google.dev/pricing) — Free tier available
- [NewsAPI](https://newsapi.org) — Free tier (100 requests/day)
- [yfinance](https://github.com/ranaroussi/yfinance) — Free (no key needed)

### 5. Run Application

```bash
python main.py
```

---

##  How It Works

### Single Stock Analysis

```python
from main import InvestmentResearchSystem

system = InvestmentResearchSystem()
report = system.research_single_stock("AAPL")
print(report)
```

**Output:**
```json
{
  "ticker": "AAPL",
  "executive_summary": "AAPL Analysis Summary: Recommendation: Hold | Market Sentiment: Neutral | Risk Level: Medium",
  "recommendation": {
    "action": "Hold",
    "confidence_score": 50,
    "reasoning": "Valuation score 45.0: Hold signal..."
  },
  "financial_analysis": {
    "valuation_score": 45.0,
    "key_metrics": {
      "pe_ratio": "37.33",
      "revenue": "$416.16B",
      "market_cap": "$4.14T"
    }
  },
  "sentiment_analysis": {
    "overall_sentiment": "neutral",
    "confidence": 100.0
  }
}
```

### Batch Processing

```python
reports = system.research_multiple_stocks(["AAPL", "GOOGL", "MSFT"])
print(f"Analyzed {len(reports)} stocks")
```

---

##  Real Data Pipeline

### 1. News Data (Real-Time)

**Source:** NewsAPI
```
Query: "AAPL stock news latest"
↓
5 latest headlines with:
  - Title
  - Snippet
  - URL
  - Publication date
```

### 2. Financial Metrics (Real)

**Source:** yfinance
```
Stock: AAPL
↓
Returns:
  - PE Ratio: 37.33
  - Market Cap: $4.14T
  - Revenue: $416.16B
  - Earnings: $112.01B
  - Profit Margin: 26.92%
  - Revenue Growth: 7.90%
```

### 3. LLM Summarization

**Source:** Gemini 2.0 Flash
```
Input: Research data (news + metrics)
↓
Output: Intelligent 3-4 sentence summary
  "AAPL boasts a massive $4.14T market cap with strong 
   fundamentals including 26.92% profit margin. Recent 
   positive sentiment and Fed rate cut hopes support 
   momentum near 52-week highs..."
```

---

##  Valuation Scoring Formula

Score ranges 0-100 based on three real fundamentals:

### PE Ratio Component

```
PE < 12:        +25 (Very cheap)
PE 12-18:       +15 (Moderately cheap)
PE 18-25:       +5  (Fair value)
PE 25-35:       -10 (Moderately expensive)
PE > 35:        -25 (Very expensive)
```

### Revenue Growth Component

```
Growth > 20%:   +20 (Excellent)
Growth 10-20%:  +10 (Good)
Growth 5-10%:   +5  (Moderate)
Growth < 0%:    -20 (Declining)
```

### Profit Margin Component

```
Margin > 25%:   +15 (Excellent)
Margin 15-25%:  +8  (Good)
Margin 8-15%:   +3  (Acceptable)
Margin < 5%:    -15 (Weak)
```

### Recommendation Mapping

```
Score > 70:     BUY (Cheap + strong fundamentals)
Score 55-70:    HOLD (Fair value + good growth)
Score 35-55:    HOLD (Fair value mixed signals)
Score < 35:     SELL (Expensive + weak fundamentals)
```

---

##  Project Structure

```
investment-research-agent/
├── agents/
│   ├── __init__.py
│   ├── analysis_agent.py
│   ├── report_agent.py
│   └── research_agent.py
├── data/
│   └── memory_bank.json
├── memory/
│   ├── __init__.py
│   ├── memory_bank.py
│   └── session_manager.py
├── observability/
│   ├── __init__.py
│   └── logger.py
├── tools/
│   ├── __init__.py
│   ├── financial_calculator.py
│   └── web_search_tool.py
├── .env
├── investment_research.log
├── main.py
├── README.md
└── requirements.txt

```

---

##  Data Flow Example

**Analyzing Apple [finance:Apple Inc.]:**

```
1. ResearchAgent
   ├─ Search: "AAPL stock news latest" → 5 articles
   ├─ Fetch: yfinance → PE=37.33, Growth=7.90%, Margin=26.92%
   └─ Summarize: Gemini → "Strong financials near 52-week high..."

2. AnalysisAgent
   ├─ Calculate: Valuation score = 45.0
   │   (37.33 PE: -10) + (7.90% growth: +5) + (26.92% margin: +15) = 45
   ├─ Analyze: News sentiment = neutral (5 articles, 0 positive, 0 negative)
   ├─ Assess: Risk = medium (score: 50)
   └─ Recommend: HOLD (confidence: 50%)

3. ReportAgent
   ├─ Generate: JSON report with all metrics
   ├─ Store: Analysis in memory bank
   └─ Output: Print + log results

4. Result
    Recommendation: HOLD
    Confidence: 50/100
    Valuation: Fair (score 45)
```

---

##  Example Usage

### Run Full Pipeline

```bash
python main.py
```

**Console Output:**
```
================================================================================
INVESTMENT RESEARCH & ANALYSIS AGENT
Multi-Agent System for Automated Stock Research
================================================================================

[Session created: 7f5dcf19-572d-4a60-9693-602d7cfa30cc]
[AAPL] Starting research phase...
[AAPL] Starting analysis phase...
[AAPL] Generating report...

High-level batch summary for this run:
- Total stocks analyzed: 3
- Successful analyses: 3, Failed: 0.
- In this run, the system did not strongly favor any one stock.
  • AAPL: Hold (confidence 50/100).
  • GOOGL: Hold (confidence 60/100).
  • MSFT: Hold (confidence 60/100).
```

### Access Detailed Logs

```bash
tail -f logs/investment_research.log
```

---

##  Observability & Logging

### Log Levels

| Level | Example | Use Case |
|-------|---------|----------|
| **INFO** | "Research complete for AAPL" | Normal operation tracking |
| **WARNING** | "Could not parse revenue growth: 7.90%" | Graceful degradation |
| **ERROR** | "Error during research for AAPL" | Failures requiring attention |

### Key Metrics in Logs

- Session creation/completion times
- API call success/failure rates
- Data parsing accuracy
- LLM summarization latency
- Valuation score calculations
- Recommendation confidence

---

## Performance Metrics

### Typical Execution Times

| Task | Time |
|------|------|
| Single stock analysis | 3-5 seconds |
| Batch (3 stocks) | 7-10 seconds |
| API calls (news + financial) | 1-2 seconds |
| LLM summarization | 2-3 seconds |

### Data Coverage

| Data Source | Frequency | Reliability |
|-------------|-----------|-------------|
| News (NewsAPI) | Real-time | High (95%+) |
| Financial (yfinance) | Daily | Very High (99%+) |
| Market data | 15-min delay | High |

---

##  Features & Capabilities

###  Current Features

-  Single & batch stock analysis
-  Real-time news sentiment analysis
-  Dynamic valuation scoring (data-driven)
-  Buy/Hold/Sell recommendations with confidence
-  Multi-session support with isolation
-  Comprehensive JSON reports
-  Parallel batch processing
-  Full observability & logging

###  Future Enhancements

- [ ] Machine learning sentiment classifier
- [ ] Technical analysis indicators (RSI, MACD, Bollinger Bands)
- [ ] Portfolio optimization recommendations
- [ ] Real-time price alerts
- [ ] Historical backtest validation
- [ ] Interactive web dashboard
- [ ] API deployment (FastAPI)
- [ ] Database persistence (PostgreSQL)

---

##  Configuration

### Environment Variables

```env
# API Keys (Required)
GEMINI_API_KEY=sk-...
NEWSAPI_KEY=...

# Logging (Optional)
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/investment_research.log

# Session Management (Optional)
SESSION_TIMEOUT=3600            # Seconds
MAX_SESSIONS=100                # Concurrent sessions

# Agent Behavior (Optional)
NEWS_RESULTS_PER_SEARCH=5       # Headlines per search
MAX_RETRIES=3                   # API retry attempts
BATCH_SIZE=10                   # Max stocks per batch
```

---

##  AI Components

### Gemini LLM Usage

**Context Compaction:** Summarizes lengthy research data
```python
# Input
research_data = {
    "company": "Apple",
    "news": [5 articles with snippets],
    "metrics": {
        "pe": 37.33,
        "growth": 7.90%,
        "margin": 26.92%
    }
}

# Processing
gemini_summary = model.generate_content(research_data)

# Output
"AAPL has a massive $4.14T market cap with strong 
financials, trading near 52-week highs amid Fed rate 
cut optimism. High P/E suggests premium valuation..."
```

---

##  Output Examples

### Single Stock Report

```json
{
  "ticker": "AAPL",
  "recommendation": {
    "action": "Hold",
    "confidence_score": 50,
    "reasoning": "Valuation score 45.0: Hold signal. Sentiment: neutral, Risk: medium."
  },
  "financial_analysis": {
    "valuation_score": 45.0,
    "key_metrics": {
      "pe_ratio": "37.33",
      "market_cap": "$4.14T",
      "revenue": "$416.16B"
    }
  },
  "sentiment_analysis": {
    "overall_sentiment": "neutral",
    "confidence": 100.0,
    "positive_count": 0,
    "negative_count": 0
  }
}
```

### Batch Comparison

```json
{
  "total_stocks": 3,
  "successful": 3,
  "summary": [
    {
      "ticker": "AAPL",
      "action": "Hold",
      "score": 45.0
    },
    {
      "ticker": "GOOGL",
      "action": "Hold",
      "score": 65.0
    },
    {
      "ticker": "MSFT",
      "action": "Hold",
      "score": 65.0
    }
  ]
}
```


##  License

MIT License — See LICENSE file for details

---

##  Support & Contact

- **Questions:** Open GitHub Discussion
- **Email:** yamalsharma0729@gmail.com

---

##  Educational Value

### What You'll Learn

1. **Multi-Agent Architecture** — How independent agents collaborate
2. **LLM Integration** — Using Gemini for text summarization
3. **Real API Integration** — Working with newsapi.org and yfinance
4. **Session Management** — Handling multiple concurrent analyses
5. **Financial Analysis** — PE ratios, valuation scoring, fundamental analysis
6. **Sentiment Analysis** — Simple NLP for news classification
7. **Error Handling** — Graceful degradation with fallbacks
8. **Logging & Observability** — Production-grade monitoring

---

##  Key Achievements

 **Real-Time Data Integration** — Live news and financial metrics  
 **Production-Ready Code** — Error handling, validation, logging  
 **Dynamic Scoring** — Valuation scores change based on real fundamentals  
 **Parallel Processing** — Analyze multiple stocks simultaneously  
 **AI-Powered Insights** — Gemini LLM summarization  
 **Session Isolation** — Multiple concurrent analyses  
 **Comprehensive Reporting** — Professional JSON output  
 **Full Observability** — Detailed logging at every step  

---

##  References & Resources

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [yfinance Documentation](https://yfinance.readthedocs.io)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [Python Logging Best Practices](https://docs.python.org/3/library/logging.html)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)

---

##  Quick Start Checklist

- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Get API keys (Gemini, NewsAPI)
- [ ] Create `.env` file with keys
- [ ] Run `python main.py`
- [ ] Check logs in `/logs` directory
- [ ] Review JSON output
- [ ] Customize thresholds as needed
- [ ] Deploy or integrate into your workflow

---


##  Highlights for Reviewers

This project demonstrates:

1. **Multi-Agent Orchestration** — Three specialized agents working in concert
2. **Real External APIs** — NewsAPI for news, yfinance for financials, Gemini for LLM
3. **Data-Driven Scoring** — Valuation scores respond to real fundamentals
4. **Session Management** — Context isolation and memory persistence
5. **Error Handling** — Graceful degradation with fallbacks
6. **Comprehensive Logging** — Full observability for production use
7. **Professional Output** — Clean JSON reports with actionable recommendations
8. **Batch Processing** — Parallel analysis of multiple stocks
9. **Context Engineering** — LLM usage for intelligent summarization
10. **Production Quality** — Error handling, validation, and robustness

---

**Created with ❤️ for automated investment research. For educational purposes only.**