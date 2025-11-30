"""
Session Service - Manages session state and persistence

This service provides:
- Session creation and management
- State tracking across requests
- In-memory session storage
- Session retrieval and persistence
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class Session:
    
    def __init__(self, session_id: str = None):
       
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.research_results = {}
        self.state = {}
        self.metadata = {}
        
        logger.info(f"Session created: {self.session_id}")
    
    def add_research_result(self, symbol: str, result: Dict[str, Any]):
      
        self.research_results[symbol] = result
        self.updated_at = datetime.now()
        logger.debug(f"Added research result for {symbol} to session {self.session_id}")
    
    def get_research_result(self, symbol: str) -> Optional[Dict[str, Any]]:
       
        return self.research_results.get(symbol)
    
    def update_state(self, key: str, value: Any):
      
        self.state[key] = value
        self.updated_at = datetime.now()
        logger.debug(f"Updated session state: {key}")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        
        return self.state.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
  
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "research_results": self.research_results,
            "state": self.state,
            "metadata": self.metadata
        }
    
    def get_symbols_researched(self) -> List[str]:
     
        return list(self.research_results.keys())


class SessionService:
    
    def __init__(self):
        """Initialize Session Service with in-memory storage"""
        self._sessions: Dict[str, Session] = {}
        logger.info("SessionService initialized with in-memory storage")
    
    def create_session(self) -> Session:
      
        session = Session()
        self._sessions[session.session_id] = session
        logger.info(f"Created session: {session.session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
    
        session = self._sessions.get(session_id)
        if session:
            logger.debug(f"Retrieved session: {session_id}")
        else:
            logger.warning(f"Session not found: {session_id}")
        return session
    
    def save_session(self, session: Session):
       
        self._sessions[session.session_id] = session
        session.updated_at = datetime.now()
        logger.debug(f"Saved session: {session.session_id}")
    
    def delete_session(self, session_id: str) -> bool:
       
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        logger.warning(f"Cannot delete - session not found: {session_id}")
        return False
    
    def list_sessions(self) -> List[str]:
        
        return list(self._sessions.keys())
    
    def get_session_count(self) -> int:
       
        return len(self._sessions)
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
       
        now = datetime.now()
        to_delete = []
        
        for session_id, session in self._sessions.items():
            age_hours = (now - session.updated_at).total_seconds() / 3600
            if age_hours > max_age_hours:
                to_delete.append(session_id)
        
        for session_id in to_delete:
            self.delete_session(session_id)
        
        if to_delete:
            logger.info(f"Cleaned up {len(to_delete)} old sessions")
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
       
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "stocks_researched": len(session.research_results),
            "symbols": session.get_symbols_researched()
        }