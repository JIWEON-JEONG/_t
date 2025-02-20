from datetime import datetime, UTC
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate= datetime.now(UTC))

    @staticmethod
    def create(project_id: int, manager_id: int, description: str) -> 'Task':
        """새로운 Task 객체 생성"""
        return Task(
            project_id=project_id,
            manager_id=manager_id,
            description=description,
            is_completed=False,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )


