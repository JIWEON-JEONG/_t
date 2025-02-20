from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from domain.entity.user_session import UserSession  

class UserSessionRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, id: str) -> Optional[UserSession]:
        pass

    @abstractmethod
    def get_active_by_user_id(self, db: Session, user_id: int) -> Optional[UserSession]:
        pass

    @abstractmethod
    def in_activate_by_id(self, db: Session, id: str) -> None:
        pass

    @abstractmethod
    def save(self, db: Session, entity: UserSession) -> UserSession:
        pass      