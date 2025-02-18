from domain.entity.port.user_repository_port import UserRepositoryPort
from sqlalchemy.orm import Session
from domain.entity.user import User

class UserService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def create_user(self, db: Session, email: str, password: str):
        user = User.create(email, password)
        return self.user_repository.save(db, user)