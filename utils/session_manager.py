import json
import os
from typing import Optional, Dict, Any


class SessionManager:
    """Manages persistent session state across Streamlit page refreshes."""
    
    def __init__(self, session_file: str = "session.json"):
        self.session_file = session_file
    
    def save_session(self, session_data: Dict[str, Any]) -> None:
        """Save session data to file."""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def load_session(self) -> Dict[str, Any]:
        """Load session data from file."""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading session: {e}")
        return {}
    
    def clear_session(self) -> None:
        """Clear session data."""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception as e:
            print(f"Error clearing session: {e}")
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        session = self.load_session()
        return session.get('logged_in', False)
    
    def get_username(self) -> Optional[str]:
        """Get logged in username."""
        session = self.load_session()
        return session.get('username', '')
    
    def login(self, username: str) -> None:
        """Set user as logged in."""
        session = self.load_session()
        session['logged_in'] = True
        session['username'] = username
        self.save_session(session)
    
    def logout(self) -> None:
        """Log out user."""
        self.clear_session()
    
    def save_monitoring_state(self, active: bool, interval: int) -> None:
        """Save monitoring state."""
        session = self.load_session()
        session['monitoring_active'] = active
        session['monitoring_interval'] = interval
        self.save_session(session)
    
    def get_monitoring_state(self) -> tuple[bool, int]:
        """Get monitoring state."""
        session = self.load_session()
        return session.get('monitoring_active', False), session.get('monitoring_interval', 60) 