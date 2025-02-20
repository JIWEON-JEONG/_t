from datetime import datetime, UTC
from sqlalchemy import Column, Enum, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from domain.entity.enum import UserRole

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    # Unique
    email = Column(String(50), nullable=False, unique= True)
    role = Column(Enum(UserRole), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate= datetime.now(UTC))

    @staticmethod
    def create(company_id: int, email: str, password: str) -> 'User':
        return User(
            company_id = company_id,
            email=email,
            role=UserRole.VIEWER,
            password=password,
        )


