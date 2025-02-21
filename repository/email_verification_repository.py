from sqlalchemy.orm import Session
from domain.entity.email_verification import EmailVerification
from typing import Optional

from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort

class EmailVerificationRepository(EmailVerificationRepositoryPort):
    def __init__(self):
        pass

    def get_by_id(self, db: Session, id: int) -> Optional[EmailVerification]:
        return db.query(EmailVerification)\
            .filter(EmailVerification.id == id)\
            .first()
    
    def insert(self, db: Session, entity: EmailVerification) -> None:
        db.add(entity)
        db.flush()

    def exist_verification_code(self, db: Session, email: str) -> bool:
        result = db.query(EmailVerification.id)\
              .filter(EmailVerification.email == email)\
              .filter(EmailVerification.success == False)\
              .limit(1)\
              .first()
    
        return result is not None
    
    def get_by_email(self, db: Session, email: str) -> Optional[EmailVerification]:
        return db.query(EmailVerification)\
              .filter(EmailVerification.email == email)\
              .filter(EmailVerification.success == False)\
              .limit(1)\
              .first()
        
    def is_verified_email(self, db: Session, email: str) -> bool:
        result = db.query(EmailVerification.id)\
              .filter(EmailVerification.email == email)\
              .filter(EmailVerification.success == True)\
              .limit(1)\
              .first()
    
        return result is not None  
    
    def success_by_email_and_code(self, db: Session, email: str, code: str, retry_count: int) -> None:
        db.query(EmailVerification)\
              .filter(EmailVerification.email == email)\
              .filter(EmailVerification.code == code)\
              .update({"success": True, "retry_count" : retry_count}, synchronize_session=False)
    
        db.flush()

    def success(self, db: Session, id: int, retry_count: int) -> None:
        db.query(EmailVerification)\
              .filter(EmailVerification.id == id)\
              .update({"success": True, "retry_count" : retry_count}, synchronize_session=False)
    
        db.flush()

    def fail(self, db: Session, id: int, retry_count: int) -> None:
        db.query(EmailVerification)\
              .filter(EmailVerification.id == id)\
              .update({"retry_count" : retry_count}, synchronize_session=False)
    
        db.flush()