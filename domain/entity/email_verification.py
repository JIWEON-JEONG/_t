from datetime import datetime, UTC
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class CreateEmailVerificationDto:
    email: str
    code: str  

class EmailVerification(Base):
    __tablename__ = 'email_verification'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    code = Column(String(), nullable=False)
    retry_count = Column(Integer, nullable=False, default=0)
    success = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate= datetime.now(UTC))

    @staticmethod
    def create(dto:CreateEmailVerificationDto) -> 'EmailVerification':
        return EmailVerification(
            email=dto.email,
            code=dto.code,
            retry_count=0,
            success=False
        )
