from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Unique
    email = Column(String(50), nullable=False, unique= True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate= datetime.now(UTC))

    @staticmethod
    def create(email: str, password: str) -> 'User':
        return User(
            email=email,
            password=password,
        )
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, created_at={self.created_at}, updated_at={self.updated_at})>"


