from typing import Optional
import fastapi
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from domain.entity.enum import ProjectRole, UserRole
from domain.entity.project_user_role import ProjectUserRole
from domain.service.project_service import ProjectService
from domain.entity.project import Project
from domain.entity.user import User
from dto.dto import InviteProjectRequest, UpdateProjectRequest

@pytest.fixture
def mock_project_repository():
    return MagicMock()

@pytest.fixture
def project_service(mock_project_repository):
    return ProjectService(mock_project_repository)

@pytest.fixture
def mock_admin():
    return User(id=1, company_id=1, role=UserRole.ADMIN, email="test_admin@gmail.com")

@pytest.fixture
def mock_member():
    return User(id=1, company_id=1, role=UserRole.MEMBER, email="test_member@gmail.com")

@pytest.fixture
def mock_project_owner():
    return User(id=1, company_id=1, role=UserRole.PROJECT_OWNER, email="test_project_owner@gmail.com")

@pytest.fixture
def mock_project():
    return Project(id=1, company_id=1, owner_id=1, description="Test Project")

@pytest.fixture
def mock_project_role_viewer():
    return ProjectUserRole(id=1, project_id=1, user_id=1, role=ProjectRole.VIEWER)

@pytest.fixture
def mock_project_role_editor():
    return ProjectUserRole(id=1, project_id=1, user_id=1, role=ProjectRole.EDITOR)

@pytest.fixture
def mock_project_role_owner():
    return ProjectUserRole(id=1, project_id=1, user_id=1, role=ProjectRole.OWNER)

@pytest.fixture
def mock_db():
    return MagicMock()

# 삭제 테스트

def test_ADMIN_사용자가_프로젝트를_삭제_할_수_있다(project_service, mock_admin, mock_db, mock_project):
    project_service.project_repository_port.get_by_id.return_value = mock_project
    project_service.project_repository_port.get_role_by_project_and_user.return_value = None

    project_id = 1
    result = project_service.delete(mock_db, mock_admin, project_id)

    assert result == project_id

def test_MEMBER_이고_프로젝트_역할이_없을경우_프로젝트를_삭제_할_수_없다(project_service, mock_member, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = None

    project_id = 1
    with pytest.raises(HTTPException) as exc_info:
        project_service.delete(mock_db, mock_member, project_id)

    assert exc_info.value.status_code == 403
    assert "권한이 없습니다." in exc_info.value.detail


def test_MEMBER_이고_프로젝트_역할이_VIEWER_일경우_프로젝트를_삭제_할_수_없다(project_service, mock_member, mock_project_role_viewer, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = mock_project_role_viewer

    project_id = 1
    with pytest.raises(HTTPException) as exc_info:
        project_service.delete(mock_db, mock_member, project_id)

    assert exc_info.value.status_code == 403
    assert "권한이 없습니다." in exc_info.value.detail


# 초대 테스트
def test_ADMIN_사용자가_프로젝트에_사용자를_초대할_수_있다(project_service, mock_admin, mock_db, mock_project):
    project_service.project_repository_port.get_by_id.return_value = mock_project
    project_service.project_repository_port.get_role_by_project_and_user.return_value = None

    project_id = 1
    param: InviteProjectRequest = InviteProjectRequest(member_id = 3, member_role=ProjectRole.VIEWER)
    result = project_service.invite(mock_db, mock_admin, project_id, param)

    assert result == 1


def test_MEMBER_사용자가_프로젝트_역할이_VIEWER_일경우_초대_할_수_없다(project_service, mock_member, mock_project_role_viewer, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = mock_project_role_viewer

    project_id = 1
    param: InviteProjectRequest = InviteProjectRequest(member_id = 3, member_role=ProjectRole.VIEWER)
    with pytest.raises(HTTPException) as exc_info:
        project_service.invite(mock_db, mock_member, project_id, param)

    assert exc_info.value.status_code == 403


# 생성 테스트

def test_ADMIN_사용자가_프로젝트를_생성할_수_있다(project_service, mock_admin, mock_db):
    mock_project = MagicMock()
    mock_project.id = 1  # Set the expected ID value
    project_service.project_repository_port.save.return_value = mock_project

    result = project_service.create(mock_db, mock_admin, "New Project")

    assert result.id == mock_project.id


def test_MEMBER_사용자가_프로젝트_역할이_VIEWER_일경우_프로젝트를_생성할_수_없다(project_service, mock_member, mock_db):
    with pytest.raises(HTTPException) as exc_info:
        project_service.create(mock_db, mock_member, "New Project")

    assert exc_info.value.status_code == 403


# 조회 테스트

def test_VIEWER_권한으로_프로젝트를_읽을_수_있다(project_service, mock_member, mock_project_role_viewer, mock_project, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = mock_project_role_viewer
    project_service.project_repository_port.get_by_id.return_value = mock_project

    project_id = 1
    result = project_service.read(mock_db, mock_member, project_id)

    assert result == mock_project

def test_MEMBER_이고_프로젝트_역할이_없을경우_프로젝트를_읽을_수_없다(project_service, mock_member, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = None

    project_id = 1
    with pytest.raises(HTTPException) as exc_info:
        project_service.read(mock_db, mock_member, project_id)

    assert exc_info.value.status_code == 403


# 업데이트 테스트

def test_ADMIN_사용자가_프로젝트를_수정할_수_있다(project_service, mock_admin, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = None
    project_service.project_repository_port.update_project_description.return_value = True

    param = UpdateProjectRequest(description="Updated Project Description")
    project_id = 1

    result = project_service.update(mock_db, mock_admin, project_id, param)

    assert result == project_id


def test_프로젝트_역할이_EDITOR_사용자는_프로젝트를_수정할_수_있다(project_service, mock_member, mock_project_role_editor, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = mock_project_role_editor
    project_service.project_repository_port.update_project_description.return_value = True

    param = UpdateProjectRequest(description="Updated Project Description")
    project_id = 1

    result = project_service.update(mock_db, mock_member, project_id, param)

    assert result == project_id


def test_프로젝트_역할이_VIEWER_역할_사용자는_프로젝트를_수정할_수_없다(project_service, mock_member, mock_project_role_viewer, mock_db):
    # 프로젝트 역할이 VIEWER인 경우 권한이 없으므로, 403 에러가 발생해야 함
    project_service.project_repository_port.get_role_by_project_and_user.return_value = mock_project_role_viewer

    param = UpdateProjectRequest(description="Updated Project Description")
    project_id = 1

    with pytest.raises(HTTPException) as exc_info:
        project_service.update(mock_db, mock_member, project_id, param)

    assert exc_info.value.status_code == 403
    assert "권한이 없습니다." in exc_info.value.detail


def test_업데이트_실패_이미삭제(project_service, mock_admin, mock_db):
    project_service.project_repository_port.get_role_by_project_and_user.return_value = None
    project_service.project_repository_port.update_project_description.return_value = False

    param = UpdateProjectRequest(description="Updated Project Description")
    project_id = 1

    with pytest.raises(HTTPException) as exc_info:
        project_service.update(mock_db, mock_admin, project_id, param)

    assert exc_info.value.status_code == 400
    assert "이미 삭제된 프로젝트입니다." in exc_info.value.detail
