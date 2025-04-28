import pytest
from mr_h4shtag.core.auth import Auth

def test_oauth_token_generation():
    auth = Auth()
    token = auth.generate_oauth_token(client_id="test_client", client_secret="test_secret")
    assert token is not None
    assert isinstance(token, str)

def test_jwt_validation():
    auth = Auth()
    token = auth.generate_jwt(user_id="test_user")
    assert auth.validate_jwt(token) == "test_user"

def test_basic_auth():
    auth = Auth()
    credentials = auth.encode_basic_auth(username="admin", password="pass")
    assert auth.verify_basic_auth(credentials, username="admin", password="pass")