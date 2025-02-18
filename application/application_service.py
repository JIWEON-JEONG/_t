from application.email_sender import EmailSender, SendEmailDto
from common.security_service import SecurityService
from common.transaction import transactional
from common.random_util import RandomUtil
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService
from dto.dto import SignUpRequest

class ApplicationService:
    def __init__(self, user_service: UserService, email_verification_service: EmailVerificationService, 
                emailSender: EmailSender, security_service: SecurityService):
        self.user_service = user_service
        self.email_verification_service = email_verification_service
        self.emailSender = emailSender
        self.security_service = security_service

    @transactional
    async def sign_up(self, param: SignUpRequest, db=None) -> int:
        code = RandomUtil.generate_random_code()
        self.email_verification_service.record(db, param.email, code)
        hashed_password = self.security_service.hash(param.password) 
        user = self.user_service.create_user(db, param.email, hashed_password)

        self.emailSender.send_email(SendEmailDto(recipient_email=user.email, code=code))
        return user.id

    