from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from domain.entity.email_verification import EmailVerification  

class EmailVerificationRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, id: int) -> Optional[EmailVerification]:
        pass

    @abstractmethod
    def insert(self, db: Session, entity: EmailVerification) -> None:
        pass    

    @abstractmethod
    def exist_verification_code(self, db: Session, email: str) -> bool:
        pass    

    @abstractmethod
    def is_verified_email(self, db: Session, email: str) -> bool:
        pass

    @abstractmethod
    def success_by_email_and_code(self, db: Session, email: str, code: str, retry_count: int) -> None:
        pass
    
    @abstractmethod
    def success(self, db: Session, id: int, retry_count: int) -> None:
        pass

    @abstractmethod
    def fail(self, db: Session, id: int) -> None:
        pass          

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> Optional[EmailVerification]:
        pass