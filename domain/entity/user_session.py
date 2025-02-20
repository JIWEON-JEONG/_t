from datetime import datetime, timedelta, timezone
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase

from common.util import utc_now

class Base(DeclarativeBase):
    pass

class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column(String(64), primary_key=True)
    user_id = Column(Integer, nullable=False)
    ip = Column(String, nullable=False)  
    created_at = Column(DateTime, default=utc_now)  
    expires_at = Column(DateTime, default=lambda: utc_now() + timedelta(hours=3))  
    last_active = Column(DateTime, default=utc_now)  
    is_active = Column(Boolean, default=True) 

    @staticmethod
    def create(id: str, user_id: int, ip: str) -> 'UserSession':
        now = utc_now()
        return UserSession(
            id=id,
            user_id=user_id,
            ip = ip,
            created_at=now,
            expires_at=now + timedelta(hours=3),
            last_active=now,
            is_active=True
        )
