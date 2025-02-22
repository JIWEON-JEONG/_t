import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import timedelta
from domain.entity.user_session import UserSession, utc_now
from domain.service.user_session_service import UserSessionService

@pytest.fixture
def mock_session_repository():
    return MagicMock()

@pytest.fixture
def mock_security_service():
    service = MagicMock()
    service.generate_session_id.return_value = "new-session-id"
    return service

@pytest.fixture
def user_session_service(mock_session_repository, mock_security_service):
    return UserSessionService(mock_session_repository, mock_security_service)

@pytest.fixture
def db():
    return MagicMock()

# Fixture: 유효한 세션 (만료 시간이 미래이고 IP가 일치하는 세션)
@pytest.fixture
def valid_session():
    session_id = "valid-session-id"
    user_id = 1
    ip = "127.0.0.1"
    session = UserSession.create(session_id, user_id, ip)
    session.expires_at = utc_now() + timedelta(hours=3)
    session.ip = ip
    return session

@pytest.fixture
def expired_session(valid_session):
    valid_session.expires_at = utc_now() - timedelta(minutes=1)
    return valid_session

@pytest.fixture
def ip_changed_session(valid_session):
    valid_session.ip = "192.168.1.1"  # 요청 IP "127.0.0.1"과 다르게 설정
    return valid_session


def test_유효한_세션은_IP가_일치하고_만료_되지않아야_합니다(user_session_service, db, valid_session):
    user_session_service.session_repository_port.get_active_by_id.return_value = valid_session

    # IP가 일치하고 세션이 유효하므로 valid_session을 그대로 반환해야 함
    result = user_session_service.verify_session_by_id_or_throw(db, valid_session.id, "127.0.0.1")
    assert result == valid_session

def test_세션이_없다면_예외를_발생시킵니다(user_session_service, db):
    user_session_service.session_repository_port.get_active_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_session_service.verify_session_by_id_or_throw(db, "nonexistent-id", "127.0.0.1")
    assert exc_info.value.status_code == 401

def test_세션이_만료되었다면_예외를_발생시킵니다(user_session_service, db, expired_session):
    user_session_service.session_repository_port.get_active_by_id.return_value = expired_session

    with pytest.raises(HTTPException) as exc_info:
        user_session_service.verify_session_by_id_or_throw(db, expired_session.id, "127.0.0.1")
    assert exc_info.value.status_code == 401

def test_로그인과_다른_IP_에서_접근_할_경우_예외를_발생시킵니다(user_session_service, db, ip_changed_session):
    user_session_service.session_repository_port.get_active_by_id.return_value = ip_changed_session

    with pytest.raises(HTTPException) as exc_info:
        user_session_service.verify_session_by_id_or_throw(db, ip_changed_session.id, "127.0.0.1")
    assert exc_info.value.status_code == 401

def test_만료된_세션_일경우_기존_세션을_비활성화_후_새_세션을_반환합니다(user_session_service, db, expired_session):
    # _invalidate_and_create_new_session이 호출되어 새 세션을 생성함.
    user_session_service.session_repository_port.get_active_by_user_id.return_value = expired_session

    # 새 세션 객체 생성: security_service.generate_session_id()는 "new-session-id"를 반환하도록 설정됨.
    new_session = UserSession.create("new-session-id", expired_session.user_id, "127.0.0.1")
    new_session.expires_at = utc_now() + timedelta(hours=3)
    user_session_service.session_repository_port.save.return_value = new_session

    result = user_session_service.get_valid_session(db, expired_session.user_id, "127.0.0.1")
    
    # 기존 세션이 만료되었으므로 새 세션의 id가 반환되어야 함
    assert result == new_session.id

def test_IP_변경_된_세션_일경우_기존_세션을_비활성화_후_새_세션을_반환합니다(user_session_service, db, ip_changed_session):
    # _invalidate_and_create_new_session이 호출되어 새 세션을 생성함.
    user_session_service.session_repository_port.get_active_by_user_id.return_value = ip_changed_session

    new_session = UserSession.create("new-session-id", ip_changed_session.user_id, "127.0.0.1")
    new_session.expires_at = utc_now() + timedelta(hours=3)
    user_session_service.session_repository_port.save.return_value = new_session

    result = user_session_service.get_valid_session(db, ip_changed_session.user_id, "127.0.0.1")
    
    assert result == new_session.id
