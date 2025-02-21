from common.transaction import transactional
from domain.entity.project import Project
from domain.entity.user import User
from domain.service.project_service import ProjectService
from dto.dto import CreateProjectRequest, InviteProjectRequest, UpdateProjectRequest
from sqlalchemy.orm import Session

class ProjectApplicationService:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    @transactional
    async def create(self, user: User, param: CreateProjectRequest, db=Session) -> int:
        project: Project = self.project_service.create(db, user, param.description)
        return project.id
    
    @transactional
    async def update(self, user: User, project_id: int, param: UpdateProjectRequest, db=Session) -> int:
        return self.project_service.update(db, user, project_id, param)
    
    @transactional
    async def delete(self, user: User, project_id: int, db=Session) -> int:
        return self.project_service.delete(db, user, project_id)
    
    @transactional
    async def invite(self, user: User, project_id: int, param: InviteProjectRequest, db=Session) -> int:
        return self.project_service.invite(db, user, project_id, param)
    
    async def read(self, user: User, project_id: int, db=Session) -> int:
        return self.project_service.read(db, user, project_id)