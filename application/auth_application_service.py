import datetime
from application.email_sender import CommonSendEmailDto, EmailSender
from common.security_service import SecurityService
from common.transaction import transactional
from common.random_util import RandomUtil
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService

class AuthApplicationService:
    def __init__(self, user_service: UserService, email_verification_service: EmailVerificationService, 
                email_sender: EmailSender, security_service: SecurityService):
        self.user_service = user_service
        self.email_verification_service = email_verification_service
        self.email_sender = email_sender
        self.security_service = security_service

    @transactional
    async def authenticate_email(self, email:str, db=None) -> None:
        already_exist: bool = self.email_verification_service.check_exist_verification_code(db, email)
        if already_exist:
            raise Exception(f"이미 '{email}'에 대한 인증 코드가 발급되어 있습니다. 기존 코드를 확인해주세요.")

        code = RandomUtil.generate_random_code()
        self.email_verification_service.record(db, email, code)
        self.email_sender.send_email(CommonSendEmailDto(recipient_email=email, body= {"code": code}))
    
    @transactional
    async def verify_email(self, email: str, code: str, db=None) -> None:
        self.email_verification_service.success_verification(db, email, code)

    @transactional
    async def send_email_update_password(self, user_id: int, email: str, db=None) -> None:
        body: dict = {
            "user_id" : user_id,
        }
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        token: str = self.security_service.generate_token(body, expires_at)
        # Update Password Web URI  링크 가정. 
        update_password_link: str = "http://localhost:8000/health"

        link: str = update_password_link + '/?token=' + token
        self.email_sender.send_email_with_link(CommonSendEmailDto(recipient_email=email, body= {"link": link}))
    