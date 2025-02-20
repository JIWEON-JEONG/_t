from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from domain.entity.project import Project
from domain.entity.project_user_role import ProjectUserRole
from domain.entity.user import User 

class ProjectRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, id: int) -> Optional[Project]:
        pass

    @abstractmethod
    def save(self, db: Session, project: Project) -> Project:
        pass

    @abstractmethod
    def save_user_role(self, db: Session, user_role: ProjectUserRole) -> ProjectUserRole:
        pass

    @abstractmethod
    def update_project_description(self, db: Session, project_id, desc) -> bool:
        pass

    @abstractmethod
    def delete(self, db: Session, project_id) -> bool:
        pass

    @abstractmethod
    def get_role_by_project_and_user(self, db: Session, project_id, user_id) -> Optional[ProjectUserRole]:
        pass




