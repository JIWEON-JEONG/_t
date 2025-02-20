from sqlalchemy.orm import Session
from domain.entity.port.project_repository_port import ProjectRepositoryPort
from domain.entity.project import Project
from domain.entity.project_user_role import ProjectUserRole
from domain.entity.user import User
from typing import Optional

class ProjectRepository(ProjectRepositoryPort):
    def __init__(self):
        pass

    def delete(self, db: Session, project_id) -> bool:
        result = db.query(Project)\
            .filter(Project.id == project_id)\
            .filter(Project.is_deleted == False)\
            .update({"is_deleted": True}, synchronize_session=False)
        
        db.flush()
        if(result == 0):
            return False
        return True

    def get_by_id(self, db: Session, id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == id).first()
    
    def save(self, db: Session, project: Project) -> Project:
        db.add(project)
        db.flush()

        return project 
    
    def save_user_role(self, db: Session, user_role: ProjectUserRole) -> ProjectUserRole:
        db.add(user_role)
        db.flush()

        return user_role 
    
    def update_project_description(self, db: Session, project_id, desc) -> bool:
        result = db.query(Project)\
            .filter(Project.id == project_id)\
            .filter(Project.is_deleted == False)\
            .update({"description": desc}, synchronize_session=False)
        
        db.flush()
        if(result == 0):
            return False
        return True
    
    def get_role_by_project_and_user(self, db: Session, project_id, user_id) -> Optional[ProjectUserRole]:
        db.query(ProjectUserRole)\
            .filter(ProjectUserRole.project_id == project_id)\
            .filter(ProjectUserRole.user_id == user_id)\
            .first

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User)\
            .filter(User.email == email)\
            .first()
