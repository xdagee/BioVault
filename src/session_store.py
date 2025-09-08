"""
In-memory session storage for secure session management.
Simple memory-based session storage without Redis dependencies.
"""

import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from logging_config import app_logger
from config import config
from exceptions import SessionError


class MemorySessionStore:
    """In-memory session storage implementation."""
    
    def __init__(self):
        """Initialize memory-based session storage."""
        self._memory_store: Dict[str, Dict[str, Any]] = {}
        app_logger.info("Memory session store initialized successfully")
    
    def create_session(self, session_id: str, user_id: str, data: Optional[Dict[str, Any]] = None) -> bool:
        """Create a new session."""
        try:
            session_data = {
                'user_id': user_id,
                'created_at': datetime.utcnow().isoformat(),
                'last_activity': datetime.utcnow().isoformat(),
                'data': data or {}
            }
            
            # Store in memory
            self._memory_store[session_id] = session_data
            
            app_logger.info(f"Session created: {session_id} for user: {user_id}")
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to create session {session_id}: {str(e)}")
            raise SessionError(f"Failed to create session: {str(e)}", session_id)
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data by session ID."""
        try:
            # Get from memory
            session_data = self._memory_store.get(session_id)
            if not session_data:
                return None
            
            # Check expiration for memory store
            last_activity = datetime.fromisoformat(session_data['last_activity'])
            if datetime.utcnow() - last_activity > timedelta(minutes=config.security.session_timeout_minutes):
                del self._memory_store[session_id]
                return None
            
            # Update last activity
            session_data['last_activity'] = datetime.utcnow().isoformat()
            self._memory_store[session_id] = session_data
            
            return session_data
            
        except Exception as e:
            app_logger.error(f"Failed to get session {session_id}: {str(e)}")
            return None
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session data."""
        try:
            session_data = self.get_session(session_id)
            if not session_data:
                return False
            
            session_data['data'].update(data)
            session_data['last_activity'] = datetime.utcnow().isoformat()
            
            self._memory_store[session_id] = session_data
            
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to update session {session_id}: {str(e)}")
            return False
    
    def destroy_session(self, session_id: str) -> bool:
        """Destroy a session."""
        try:
            success = session_id in self._memory_store
            if success:
                del self._memory_store[session_id]
            
            if success:
                app_logger.info(f"Session destroyed: {session_id}")
            
            return success
            
        except Exception as e:
            app_logger.error(f"Failed to destroy session {session_id}: {str(e)}")
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        try:
            expired_sessions = []
            cutoff_time = datetime.utcnow() - timedelta(minutes=config.security.session_timeout_minutes)
            
            for session_id, session_data in self._memory_store.items():
                last_activity = datetime.fromisoformat(session_data['last_activity'])
                if last_activity < cutoff_time:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self._memory_store[session_id]
            
            if expired_sessions:
                app_logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
            return len(expired_sessions)
            
        except Exception as e:
            app_logger.error(f"Failed to cleanup expired sessions: {str(e)}")
            return 0
    
    def get_active_session_count(self) -> int:
        """Get count of active sessions."""
        try:
            return len(self._memory_store)
        except Exception as e:
            app_logger.error(f"Failed to get active session count: {str(e)}")
            return 0


# Global session store instance
session_store = MemorySessionStore()