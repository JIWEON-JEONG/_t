from sqlalchemy.orm import Session
from domain.entity.user import User
from domain.entity.port.user_repository_port import UserRepositoryPort
from typing import Optional

class UserRepository(UserRepositoryPort):
    def __init__(self):
        pass

    def get_by_id(self, db: Session, id: int) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()
    
    def save(self, db: Session, user: User) -> User:
        db.add(user)
        db.flush()
        return user