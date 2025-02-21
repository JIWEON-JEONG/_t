import datetime
from fastapi import BackgroundTasks, HTTPException
from application.email_sender import CommonSendEmailDto, EmailSender
from common.security_service import SecurityService
from common.transaction import  transactional
from domain.entity.user import User
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService
from domain.service.user_session_service import UserSessionService
from dto.dto import LoginRequest
from sqlalchemy.orm import Session

class AuthApplicationService:
    def __init__(self, user_service: UserService, email_verification_service: EmailVerificationService, 
                user_session_service: UserSessionService, security_service: SecurityService,
                email_sender: EmailSender):
        self.user_service = user_service
        self.email_verification_service = email_verification_service
        self.email_sender = email_sender
        self.security_service = security_service
        self.user_session_service = user_session_service

    @transactional
    async def login(self, param: LoginRequest, ip: str,  db=Session) -> str:
        user: User = self.user_service.get_user_by_email_password_or_throw(db, param.email, param.password)
        return self.user_session_service.get_valid_session(db, user.id, ip)
    
    def get_user_by_session(self, db: Session, session_id: str, ip: str) -> str:
        if not session_id:
            raise HTTPException(status_code=400, detail="세션 ID는 필수입니다.")
        if not ip:
            raise HTTPException(status_code=400, detail="IP 주소는 필수입니다.")
        return self.user_service.get_user_by_session(db=db, session_id=session_id, ip=ip)
        
    @transactional
    async def authenticate_email(self, email: str, background_tasks: BackgroundTasks, db=Session) -> None:
        already_exist: bool = self.email_verification_service.check_exist_verification_code(db, email)
        if already_exist:
            raise Exception(f"이미 '{email}'에 대한 인증 코드가 발급되어 있습니다. 기존 코드를 확인해주세요.")

        code: str = self.security_service.generate_random_code()
        self.email_verification_service.record(db, email, code)
        background_tasks.add_task(self.email_sender.send_email, CommonSendEmailDto(recipient_email=email, body={"code": code}))

    @transactional
    async def verify_email(self, email: str, code: str, db=Session) -> bool:
        return self.email_verification_service.verify_email(db, email, code)

    async def send_email_update_password(self, user_id: int, email: str, background_tasks: BackgroundTasks) -> None:
        body: dict = {
            "user_id": user_id,
        }
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        token: str = self.security_service.generate_token(body, expires_at)
        # Update Password Web URI 링크
        update_password_link: str = "http://localhost:8000/reset-password"  # 실제 링크로 변경 필요

        link: str = update_password_link + '/?token=' + token
        background_tasks.add_task(self.email_sender.send_email_with_link, CommonSendEmailDto(recipient_email=email, body={}), link)