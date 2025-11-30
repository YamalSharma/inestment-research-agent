import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class MemoryBank:
    """
    Long-term memory storage for investment analyses
    Stores historical data for trend comparison
    """
    def __init__(self, storage_path: str = "data/memory_bank.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory: Dict[str, List[Dict]] = self._load_memory()
        logger.info("MemoryBank initialized")
    
    def _load_memory(self) -> Dict:
        """Load memory from file"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_memory(self):
        """Save memory to file"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def store_analysis(self, ticker: str, analysis: Dict[str, Any]):
        """Store analysis result"""
        if ticker not in self.memory:
            self.memory[ticker] = []
        
        analysis['stored_at'] = datetime.now().isoformat()
        self.memory[ticker].append(analysis)
        self._save_memory()
        logger.info(f"Stored analysis for {ticker}")
    
    def retrieve_analysis(self, ticker: str) -> Optional[Dict]:
        """Retrieve latest analysis for ticker"""
        if ticker in self.memory and self.memory[ticker]:
            return self.memory[ticker][-1]
        return None
    
    def get_analysis_history(self, ticker: str) -> List[Dict]:
        """Get all historical analyses for ticker"""
        return self.memory.get(ticker, [])
