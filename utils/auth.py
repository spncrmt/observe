"""
auth.py
This module implements basic user authentication and session management for the
Observe AI dashboard. It provides functions to load user credentials from a
JSON file, register new users, verify passwords, and manage simple login
sessions.

Because this project is meant as a learning exercise, the authentication
mechanism is intentionally simple. It stores hashed passwords in a local
``users.json`` file in the project root. In a production system you would
integrate a robust authentication provider or framework.

Usage::

    from observe_ai.utils.auth import UserAuth

    auth = UserAuth()
    if auth.authenticate(username, password):
        # proceed to dashboard
    else:
        # authentication failed

The module uses the ``hashlib`` library to compute SHA256 hashes of
passwords. The user data file is automatically created if it doesn’t
exist.
"""

import json
import os
import hashlib
from typing import Dict, Optional


class UserAuth:
    """Simple user authentication class for handling user credentials."""

    def __init__(self, user_file: Optional[str] = None) -> None:
        """Initialize the UserAuth system.

        Parameters
        ----------
        user_file : str, optional
            Path to the JSON file storing user credentials. If None, defaults
            to ``users.json`` in the project root.
        """
        if user_file is None:
            # Place user file in observe_ai/data directory
            base_dir = os.path.dirname(os.path.dirname(__file__))
            user_file = os.path.join(base_dir, "users.json")
        self.user_file = user_file
        self._load_users()

    def _load_users(self) -> None:
        """Load users from the JSON file. If file does not exist, create an empty one."""
        if not os.path.exists(self.user_file):
            with open(self.user_file, "w") as f:
                json.dump({}, f)
            self.users: Dict[str, str] = {}
        else:
            with open(self.user_file, "r") as f:
                self.users = json.load(f)

    def _save_users(self) -> None:
        """Save the current users dictionary to the JSON file."""
        with open(self.user_file, "w") as f:
            json.dump(self.users, f)

    def _hash_password(self, password: str) -> str:
        """Compute a SHA256 hash of the password.

        This is only intended as a learning example. In real systems you
        should use a proper password hashing algorithm like bcrypt.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a username and password.

        Returns True if registration is successful, False if the user already exists.
        """
        if username in self.users:
            return False
        password_hash = self._hash_password(password)
        self.users[username] = password_hash
        self._save_users()
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Check if the provided username and password match stored credentials."""
        if username not in self.users:
            return False
        password_hash = self._hash_password(password)
        return self.users[username] == password_hash

    def ensure_default_user(self) -> None:
        """Ensure that at least one default user exists.

        If no users are present, this method creates a default user with
        username 'admin' and password 'admin'. This makes it easier to log in
        during development. In a production environment you would remove
        default credentials and enforce user creation.
        """
        if not self.users:
            self.register_user("admin", "admin")