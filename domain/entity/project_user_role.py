from datetime import datetime, UTC
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from domain.entity.enum import ROLE_PERMISSIONS, ProjectRole

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

    @staticmethod
    def can_perform_action(role: ProjectRole, action: str) -> bool:
        """해당 역할(role)이 특정 액션(action)을 수행할 수 있는지 확인"""
        return action.upper() in ROLE_PERMISSIONS.get(role, set())  

