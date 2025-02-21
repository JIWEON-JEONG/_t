from fastapi import HTTPException
from common.transaction import transactional
from domain.entity.user import User
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService
from dto.dto import CreateUserRequest, UpdateUserPasswordRequest
from sqlalchemy.orm import Session

class UserApplicationService:
    def __init__(self, user_service: UserService, email_verification_service: EmailVerificationService):
        self.user_service = user_service
        self.email_verification_service = email_verification_service

    @transactional
    async def create_user(self, param: CreateUserRequest, db=Session) -> int:
        verified_email: bool =self.email_verification_service.check_verified_email(db, param.email)
        if not verified_email:
            raise HTTPException(status_code= 403, detail=f"'{param.email}'이 아직 인증되지 않았습니다. 인증을 완료해주세요.")
        
        user = self.user_service.create_user(db, param.company_id, param.email, param.password)
        return user.id
    
    @transactional
    async def update_password(self, user_id: int, param: UpdateUserPasswordRequest, db=Session) -> int:
        user: User =self.user_service.get_user_by_id_or_throw(db, user_id)
        self.user_service.update_password(db, user.id, param.before_password, param.update_password)
        return user.id

    