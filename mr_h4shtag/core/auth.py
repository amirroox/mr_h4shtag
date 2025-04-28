import base64
import jwt
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional

class Auth:
    """Authentication handler for various auth methods"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.oauth_tokens = {}

    def generate_oauth_token(self, client_id: str, client_secret: str) -> str:
        """Generate OAuth 2.0 token"""
        token = secrets.token_urlsafe(32)
        self.oauth_tokens[token] = {
            'client_id': client_id,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        }
        return token

    def generate_jwt(self, user_id: str, expires_in: int = 3600) -> str:
        """Generate JSON Web Token"""
        payload = {
            'sub': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def encode_basic_auth(self, username: str, password: str) -> str:
        """Encode credentials for Basic Authentication"""
        credentials = f"{username}:{password}"
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    def validate_jwt(self, token: str) -> bool:
        """Validate JWT token"""
        try:
            jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return True
        except jwt.PyJWTError:
            return False

    def validate_oauth_token(self, token: str) -> bool:
        """Validate OAuth token"""
        if token not in self.oauth_tokens:
            return False
            
        token_data = self.oauth_tokens[token]
        return datetime.utcnow() < token_data['expires_at']