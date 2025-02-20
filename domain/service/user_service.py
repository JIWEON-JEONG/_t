from typing import Optional

from fastapi import HTTPException
from common.security_service import SecurityService
from domain.entity.port.user_repository_port import UserRepositoryPort
from sqlalchemy.orm import Session
from domain.entity.user import User
from domain.entity.user_session import UserSession
from domain.service.user_session_service import UserSessionService

class UserService:
    def __init__(self, user_repository: UserRepositoryPort, security_service: SecurityService,
                 user_session_service: UserSessionService):
        self.user_repository = user_repository
        self.security_service = security_service
        self.user_session_service = user_session_service

    async def get_user_by_session(self, db: Session, session_id: str, ip: str) -> User:
        session: UserSession = self.user_session_service.verify_session_by_id_or_throw(db, session_id, ip)
        return self.get_user_by_id_or_throw(db, session.user_id)
    
    async def get_user_by_email_password_or_throw(self, db: Session, email: str, password: str) -> User:
        user: Optional[User] =self.user_repository.get_by_email(db, email)
        if user is None:
            raise HTTPException(status_code= 404, detail=f"사용자 Email {email}를 찾을 수 없습니다.")
        
        verified: bool = self.security_service.verify(password, user.password)
        if not verified:
            raise HTTPException(status_code= 400, detail=f"비밀번호가 올바르지 않습니다.")
        
        return user

    def create_user(self, db: Session, company_id: int, email: str, password: str) -> User:
        hashed_password = self.security_service.hash(password) 
        user = User.create(company_id, email, hashed_password)
        return self.user_repository.save(db, user)
    
    def update_password(self, db: Session, id: int, before_password: str, update_password: str) -> None:
        verified: bool = self.security_service.verify(before_password, update_password)
        if not verified:
            raise HTTPException(status_code= 400, detail=f"비밀번호가 올바르지 않습니다.")
        hashed_password = self.security_service.hash(update_password) 
        return self.user_repository.update_password(db, id, hashed_password)
    
    def get_user_by_id_or_throw(self, db: Session, id: int) -> User:
        user: Optional[User] = self.user_repository.get_by_id(db, id)
        if user is None:
            raise HTTPException(status_code= 404, detail=f"사용자 ID {id}를 찾을 수 없습니다.")
    
        return user
    
    def exist_by_id_or_throw(self, db: Session, id: int) -> None:
        exist: bool = self.user_repository.exist_by_id(db, id)
        if not exist:
            raise HTTPException(status_code= 404, detail=f"사용자 ID {id}를 찾을 수 없습니다.")

    