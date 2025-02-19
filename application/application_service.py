from application.email_sender import EmailSender, SendEmailDto
from common.security_service import SecurityService
from common.transaction import get_db, transactional
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
        verified_email: bool =self.email_verification_service.check_verified_email(db, param.email)
        if not verified_email:
            raise Exception(f"'{param.email}'이 아직 인증되지 않았습니다. 인증을 완료해주세요.")
        
        hashed_password = self.security_service.hash(param.password) 
        user = self.user_service.create_user(db, param.email, hashed_password)
        return user.id

    @transactional
    async def authenticate_email(self, email:str, db=None) -> None:
        already_exist: bool = self.email_verification_service.check_exist_verification_code(db, email)
        if already_exist:
            raise Exception(f"이미 '{email}'에 대한 인증 코드가 발급되어 있습니다. 기존 코드를 확인해주세요.")

        code = RandomUtil.generate_random_code()
        self.email_verification_service.record(db, email, code)
        self.emailSender.send_email(SendEmailDto(recipient_email=email, code=code))
    
    @transactional
    async def verify_email(self, email: str, code: str, db=None) -> None:
        self.email_verification_service.success_verification(db, email, code)

    
    @transactional
    async def verify_email(self, email: str, code: str, db=None) -> None:
        self.email_verification_service.success_verification(db, email, code)

    