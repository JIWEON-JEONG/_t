from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from domain.entity.user import User 

class UserRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, id: int) -> Optional[User]:
        pass

    @abstractmethod
    def exist_by_id(self, db: Session, id: int) -> bool:
        pass

    @abstractmethod
    def update_password(self, db: Session, id: int, password: str) -> bool:
        pass

    @abstractmethod
    def save(self, db: Session, user: User) -> User:
        pass

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        pass


