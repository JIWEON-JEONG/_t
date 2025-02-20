import hashlib
import os
import secrets
import jwt
import datetime
from passlib.context import CryptContext

class SecurityService:

    _SECRET_KEY: str = "your-secret-key"

    def __init__(self, context: CryptContext, algorithm: str = "HS256"):
        self.context = context
        self.algorithm = algorithm

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)

    def generate_token(self, data: dict, expires_at: datetime.datetime) -> str:
        payload = data.copy()
        payload.update({"exp": expires_at})

        return jwt.encode(payload, self._SECRET_KEY, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            decoded_data = jwt.decode(token, self._SECRET_KEY, algorithms=[self.algorithm])
            return decoded_data
        except jwt.ExpiredSignatureError:
            raise ValueError("토큰이 만료되었습니다.")
        except jwt.InvalidTokenError:
            raise ValueError("유효하지 않은 토큰입니다.")
    
    def generate_random_code(length: int = 12) -> str:
        return secrets.token_hex(length)  
    
    def generate_session_id() -> str:
        return hashlib.sha256(os.urandom(64)).hexdigest()  # 64자리
