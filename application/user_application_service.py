from common.security_service import SecurityService
from common.transaction import transactional
from domain.entity.user import User
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService
from dto.dto import CreateUserRequest, UpdateUserPasswordRequest

class UserApplicationService:
    def __init__(self, user_service: UserService, email_verification_service: EmailVerificationService,
                security_service: SecurityService):
        self.user_service = user_service
        self.email_verification_service = email_verification_service
        self.security_service = security_service

    @transactional
    async def create_user(self, param: CreateUserRequest, db=None) -> int:
        verified_email: bool =self.email_verification_service.check_verified_email(db, param.email)
        if not verified_email:
            raise Exception(f"'{param.email}'이 아직 인증되지 않았습니다. 인증을 완료해주세요.")
        
        hashed_password = self.security_service.hash(param.password) 
        user = self.user_service.create_user(db, param.email, hashed_password)
        return user.id
    
    @transactional
    async def update_password(self, user_id: int, param: UpdateUserPasswordRequest, db=None) -> int:
        user: User =self.user_service.get_user_by_id_or_throw(db, user_id)
        verified: bool = self.security_service.verify(param.before_password, user.password)
        if not verified:
            raise Exception(f"비밀번호가 올바르지 않습니다.")

        hashed_password = self.security_service.hash(param.update_password) 
        self.user_service.update_password(db, user.id, hashed_password)
        return user.id

    