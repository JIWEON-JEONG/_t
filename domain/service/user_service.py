from typing import Optional
from domain.entity.port.user_repository_port import UserRepositoryPort
from sqlalchemy.orm import Session
from domain.entity.user import User

class UserService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def create_user(self, db: Session, email: str, password: str) -> User:
        user = User.create(email, password)
        return self.user_repository.save(db, user)
    
    def update_password(self, db: Session, id: int, password: str) -> None:
        return self.user_repository.update_password(db, id, password)
    
    def get_user_by_id_or_throw(self, db: Session, id: int) -> User:
        user: Optional[User] = self.user_repository.get_by_id(db, id)
        if user is None:
            raise Exception(f"사용자 ID {id}를 찾을 수 없습니다.")
    
        return user
    
    def exist_by_id_or_throw(self, db: Session, id: int) -> None:
        exist: bool = self.user_repository.exist_by_id(db, id)
        if not exist:
            raise Exception(f"사용자 ID {id}를 찾을 수 없습니다.")
    