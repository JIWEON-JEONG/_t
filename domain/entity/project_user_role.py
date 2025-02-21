from datetime import datetime, UTC
from sqlalchemy import Column, Enum, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from domain.entity.enum import ProjectRole

Base = declarative_base()

class ProjectUserRole(Base):
    __tablename__ = 'project_user_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    role = Column(Enum(ProjectRole), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate= datetime.now(UTC))

    @staticmethod
    def create(project_id: int, user_id: int, role: ProjectRole) -> 'ProjectUserRole':
        """새로운 ProjsectUserRole 객체 생성"""
        return ProjectUserRole(
            project_id=project_id,
            user_id=user_id,
            role=role,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ) 

