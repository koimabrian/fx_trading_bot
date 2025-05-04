# Purpose: Handles authentication for user and partner access
import bcrypt
import logging
from typing import Optional

class AuthManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Hardcoded credentials for testing (to be replaced with DB-driven auth)
        self.users = {
            "admin": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()),
            "partner": bcrypt.hashpw("partner123".encode('utf-8'), bcrypt.gensalt()),
        }

    def authenticate(self, username: str, password: str, role: str = "admin") -> bool:
        """Authenticate user or partner"""
        if username not in self.users:
            self.logger.error(f"Authentication failed: Unknown user {username}")
            return False

        hashed = self.users[username]
        if bcrypt.checkpw(password.encode('utf-8'), hashed):
            self.logger.info(f"Authentication successful for {username} as {role}")
            return True
        self.logger.error(f"Authentication failed for {username}: Invalid password")
        return False