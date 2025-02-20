from sqlalchemy.orm import Session
from domain.entity.email_verification import EmailVerification
from domain.entity.port.user_session_repository_port import EmailVerificationRepositoryPort
from typing import Optional

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
    
    def is_verified_email(self, db: Session, email: str) -> bool:
        result = db.query(EmailVerification.id)\
              .filter(EmailVerification.email == email)\
              .filter(EmailVerification.success == True)\
              .limit(1)\
              .first()
    
        return result is not None  
    
    def success(self, db: Session, email: str, code: str) -> None:
        db.query(EmailVerification)\
              .filter(EmailVerification.email == email)\
              .filter(EmailVerification.code == code)\
              .update({"success": True}, synchronize_session=False)
    
        db.flush()