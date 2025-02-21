import hashlib
import os
import secrets
import jwt
import datetime
from passlib.context import CryptContext

from dto.dto import TokenPayload

class SecurityService:

    _SECRET_KEY: str = "your-secret-key"

    def __init__(self, context: CryptContext, algorithm: str = "HS256"):
        self.context = context
        self.algorithm = algorithm

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        print(f"Hashed Password: {hashed_password}")
        print(f"Password Verified: {password}")
        return self.context.verify(password, hashed_password)

    def generate_token(self, data: dict, expires_at: datetime.datetime) -> str:
        payload: TokenPayload = TokenPayload(body=data.copy(), exp= expires_at)
        return jwt.encode(payload.model_dump(), self._SECRET_KEY, algorithm=self.algorithm)

    def decode_token(self, token: str) -> TokenPayload:
        try:
            decoded_data = jwt.decode(token, self._SECRET_KEY, algorithms=[self.algorithm])
            return TokenPayload(**decoded_data)  
        except jwt.ExpiredSignatureError:
            raise ValueError("토큰이 만료되었습니다.")
        except jwt.InvalidTokenError:
            raise ValueError("유효하지 않은 토큰입니다.")
    
    @staticmethod
    def generate_random_code(length: int = 12) -> str:
        return secrets.token_hex(length) 
    
    @staticmethod
    def generate_session_id() -> str:
        return hashlib.sha256(os.urandom(64)).hexdigest()  # 64자리
