from domain.entity.email_verification import EmailVerification, CreateEmailVerificationDto
from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort
from sqlalchemy.orm import Session

class EmailVerificationService:
    def __init__(self, email_verification_repository: EmailVerificationRepositoryPort):
        self.email_verification_repository = email_verification_repository

    def record(self, db: Session, email: str, code: str) -> None:
        email_verification = EmailVerification.create(CreateEmailVerificationDto(email=email, code=code))
        self.email_verification_repository.insert(db, email_verification)

    def check_exist_verification_code(self, db: Session, email: str) -> None:
        return self.email_verification_repository.exist_verification_code(db, email)
    
    def check_verified_email(self, db: Session, email: str) -> None:
        return self.email_verification_repository.is_verified_email(db, email)

    def success_verification(self, db: Session, email: str, code: str) -> None:
        return self.email_verification_repository.is_verified_email(db, email, code)
