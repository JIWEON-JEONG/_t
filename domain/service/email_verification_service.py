import logging
from typing import Optional

from fastapi import HTTPException
from domain.entity.email_verification import EmailVerification, CreateEmailVerificationDto
from sqlalchemy.orm import Session

from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort

class EmailVerificationService:
    def __init__(self, email_verification_repository: EmailVerificationRepositoryPort):
        self.email_verification_repository = email_verification_repository
        self.logger = logging.getLogger(__name__)  

    def record(self, db: Session, email: str, code: str) -> None:
        email_verification = EmailVerification.create(CreateEmailVerificationDto(email, code))
        self.email_verification_repository.insert(db, email_verification)

    def check_exist_verification_code(self, db: Session, email: str) -> None:
        return self.email_verification_repository.exist_verification_code(db, email)
    
    def verify_email(self, db: Session, email: str, code: str) -> bool:
        verification: Optional[EmailVerification] = self.email_verification_repository.get_by_email(db, email)
        if verification is None:
            raise HTTPException(status_code= 404, detail=f"이메일 인증코드 발급을 먼저 해주세요.")
        retry_count: int = verification.retry_count + 1
        if(verification.code == code):
            self.email_verification_repository.success(db, verification.id, retry_count)
            return True
        self.email_verification_repository.fail(db, verification.id, retry_count)
        self.logger.warning(f"이메일 인증 실패 ({email}) - 입력 코드: {code}")
        return False

    def check_verified_email(self, db: Session, email: str) -> bool:
        return self.email_verification_repository.is_verified_email(db, email)
