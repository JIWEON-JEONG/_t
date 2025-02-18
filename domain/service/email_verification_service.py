from domain.entity.email_verification import EmailVerification, CreateEmailVerificationDto
from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort
from sqlalchemy.orm import Session

class EmailVerificationService:
    def __init__(self, email_verification_repository: EmailVerificationRepositoryPort):
        self.email_verification_repository = email_verification_repository

    def record(self, db: Session, email: str, code: str) -> None:
        email_verification = EmailVerification.create(CreateEmailVerificationDto(email=email, code=code))
        self.email_verification_repository.insert(db, email_verification)

