"""
JWT authentication utilities for securing API endpoints.
"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..utils.config import Config

SECRET_KEY = Config().get("auth.secret_key", "your-secret-key")
ALGORITHM = "HS256"

def create_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    """Create a JWT token.
    
    Args:
        data (dict): Payload data to encode.
        expires_delta (timedelta): Token expiration time.
    
    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verify a JWT token.
    
    Args:
        token (str): JWT token to verify.
    
    Returns:
        dict: Decoded payload.
    
    Raises:
        JWTError: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"Token verification failed: {str(e)}")