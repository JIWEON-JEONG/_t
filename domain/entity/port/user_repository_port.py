from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from domain.entity.user import User 

class UserRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, id: int) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, db: Session, user: User) -> User:
        pass
