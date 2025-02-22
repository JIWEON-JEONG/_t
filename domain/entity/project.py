from datetime import datetime, UTC
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    description = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate= datetime.now(UTC))

    @staticmethod
    def create(company_id: int, owner_id: int, description: str) -> 'Project':
        """새로운 Project 객체 생성"""
        return Project(
            company_id=company_id,
            owner_id=owner_id,
            description=description,
            is_deleted = False,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )


