from sqlalchemy.orm import Session
from domain.entity.email_verification import EmailVerification
from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort
from typing import Optional

class EmailVerificationRepository(EmailVerificationRepositoryPort):
    def __init__(self):
        pass

    def get_by_id(self, db: Session, id: int) -> Optional[EmailVerification]:
        return db.query(EmailVerification).filter(EmailVerification.id == id).first()
    
    def insert(self, db: Session, entity: EmailVerification) -> None:
        db.add(entity)
        db.flush()