import datetime
import logging
from typing import Optional

from fastapi import HTTPException
from common.security_service import SecurityService
from domain.entity.port.user_session_repository_port import UserSessionRepositoryPort
from sqlalchemy.orm import Session

from domain.entity.user_session import UserSession, utc_now

class UserSessionService:
    def __init__(self, session_repository_port: UserSessionRepositoryPort, security_service: SecurityService):
        self.session_repository_port = session_repository_port
        self.security_service = security_service
        self.logger = logging.getLogger(__name__)

    def verify_session_by_id_or_throw(self, db: Session, id: str, ip: str) -> UserSession:
        session: Optional[UserSession] = self.session_repository_port.get_active_by_id(db, id)
        if not self.is_valid_session(session, ip):
            raise HTTPException(status_code= 401, detail=f"사용자 세션이 만료되었습니다. 다시 로그인해주세요.")
        
        return session      

    def get_valid_session(self, db: Session, user_id: int, ip: str) -> str:
        session: Optional[UserSession] = self.session_repository_port.get_active_by_user_id(db, user_id)

        if self.is_valid_session(session, ip):
            return session.id

        return self._invalidate_and_create_new_session(db, session, user_id, ip).id

    def is_valid_session(self, session: Optional[UserSession], ip: str) -> bool:
        """세션이 유효한지 검사"""
        if session is None:
            return False
        if self._is_expired(session):
            return False
        if self._is_ip_changed(session, ip):
            return False
        return True

    def _is_expired(self, session: UserSession) -> bool:
        expires_at = session.expires_at.replace(tzinfo=datetime.timezone.utc)
        return expires_at <= utc_now()

    def _is_ip_changed(self, session: UserSession, ip: str) -> bool:
        """IP가 변경되었는지 확인"""
        return session.ip != ip

    def _invalidate_and_create_new_session(self, db: Session, session: Optional[UserSession], user_id: int, ip: str) -> UserSession:
        """기존 세션을 비활성화하고 새 세션을 생성"""
        if session:
            self.session_repository_port.in_activate_by_id(db, session.id)
            if self._is_ip_changed(session, ip):
                self.logger.warning(f"IP 변경 감지: user_id={user_id}, old_ip={session.ip}, new_ip={ip}")

        session_id = self.security_service.generate_session_id()
        new_session = UserSession.create(session_id, user_id, ip)
        return self.session_repository_port.save(db, new_session)
