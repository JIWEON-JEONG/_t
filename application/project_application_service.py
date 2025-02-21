from common.transaction import transactional
from domain.entity.project import Project
from domain.entity.user import User
from domain.service.project_service import ProjectService
from domain.service.user_service import UserService
from dto.dto import CreateProjectRequest, DeleteProjectRequest, InviteProjectRequest, UpdateProjectRequest, UserSessionDto
from sqlalchemy.orm import Session

class ProjectApplicationService:
    def __init__(self, user_service: UserService, project_service: ProjectService):
        self.user_service = user_service
        self.project_service = project_service

    @transactional
    async def create(self, session_: UserSessionDto, param: CreateProjectRequest, db=Session) -> int:
        user: User = self.user_service.get_user_by_session(db, session_.session_id, session_.ip)
        project: Project = self.project_service.create(db, user, param.description)
        return project.id
    
    @transactional
    async def update(self, session_: UserSessionDto, param: UpdateProjectRequest, db=Session) -> int:
        user: User = self.user_service.get_user_by_session(db, session_.session_id, session_.ip)
        return self.project_service.update(db, user, param)
    
    @transactional
    async def delete(self, session_: UserSessionDto, param: DeleteProjectRequest, db=Session) -> int:
        user: User = self.user_service.get_user_by_session(db, session_.session_id, session_.ip)
        return self.project_service.delete(db, user, param.project_id)
    
    @transactional
    async def invite(self, session_: UserSessionDto, param: InviteProjectRequest, db=Session) -> int:
        user: User = self.user_service.get_user_by_session(db, session_.session_id, session_.ip)
        return self.project_service.invite(db, user, param.project_id)
    
    async def read(self, session_: UserSessionDto, project_id: int, db=Session) -> int:
        user: User = self.user_service.get_user_by_session(db, session_.session_id, session_.ip)
        return self.project_service.read(db, user, project_id)