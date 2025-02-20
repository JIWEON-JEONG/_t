from sqlalchemy.orm import Session
from domain.entity.port.user_session_repository_port import UserSessionRepositoryPort
from typing import Optional

from domain.entity.user_session import UserSession

class UserSessionRepository(UserSessionRepositoryPort):
    def __init__(self):
        pass

    def get_by_id(self, db: Session, id: str) -> Optional[UserSession]:
        return db.query(UserSession)\
            .filter(UserSession.id == id)\
            .first()
    
    def in_activate_by_id(self, db: Session, id: str) -> None:
        db.query(UserSession)\
            .filter(UserSession.id == id)\
            .update({"is_active": False}, synchronize_session=False)
        db.flush()
    
    def save(self, db: Session, entity: UserSession) -> UserSession:
        db.add(entity)
        db.flush() 
        return entity

    def get_active_by_user_id(self, db: Session, user_id: int) -> Optional[UserSession]:
        return db.query(UserSession)\
            .filter(UserSession.user_id == user_id)\
            .filter(UserSession.is_active == True)\
            .first()
    
