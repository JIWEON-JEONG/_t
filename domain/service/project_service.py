import datetime
import logging
from typing import Optional

from fastapi import HTTPException
from domain.entity.enum import ProjectRole, UserRole
from domain.entity.port.project_repository_port import ProjectRepositoryPort
from sqlalchemy.orm import Session

from domain.entity.project import Project
from domain.entity.project_user_role import ProjectUserRole
from domain.entity.user import User
from dto.dto import InviteProjectRequest, UpdateProjectRequest

class ProjectService:
    def __init__(self, project_repository_port: ProjectRepositoryPort):
        self.project_repository_port = project_repository_port
        self.logger = logging.getLogger(__name__)        

    def invite(self, db: Session, user: User, project_id: int, param: InviteProjectRequest) -> int:
        user_project_role: ProjectUserRole = self.project_repository_port.get_role_by_project_and_user(db, project_id, user.id)
        if(not self.check_invite_permission(user.role, user_project_role)):
            self.logger.warning(f"[프로젝트 초대 실패] 사용자 {user.id}가 권한 없이 프로젝트 초대 시도")

        project: Optional[Project] = self.project_repository_port.get_by_id(db, project_id)
        if project is None:
            raise HTTPException(status_code= 404, detail=f"프로젝트 {project_id} 를  찾을 수 없습니다.")

        self.project_repository_port.save_user_role(db, ProjectUserRole.create(project_id, param.member_id, param.member_role))
        self.logger.info(f"[프로젝트 초대 성공] 프로젝트 ID: {project_id}, 생성자: {user.id}, 멤버: {param.member_id}, 권한: {param.member_role}")
        return project_id
    
    def create(self, db: Session, user: User, desc: str) -> int:
        if(not self.check_create_permission(user.role)):
            self.logger.warning(f"[프로젝트 생성 실패] 사용자 {user.id}가 권한 없이 프로젝트 생성 시도")
            raise HTTPException(status_code= 403, detail=f"권한이 없습니다.")

        project: Project = self.project_repository_port.save(db, Project.create(user.company_id, user.id, desc))
        self.project_repository_port.save_user_role(db, ProjectUserRole.create(project.id, user.id, ProjectRole.OWNER))

        self.logger.info(f"[프로젝트 생성 성공] 프로젝트 ID: {project.id}, 생성자: {user.id}, 회사 ID: {user.company_id}")
        return project
    
    def update(self, db: Session, user: User, project_id: int , param: UpdateProjectRequest) -> int:
        user_project_role: ProjectUserRole = self.project_repository_port.get_role_by_project_and_user(db, project_id, user.id)
        if(not self.check_update_permission(user.role, user_project_role)):
            self.logger.warning(f"[프로젝트 수정 실패] 사용자 {user.id}가 권한 없이 프로젝트({project_id}) 수정 시도")
            raise HTTPException(status_code= 403, detail=f"권한이 없습니다.")

        complete: bool = self.project_repository_port.update_project_description(db, project_id, param.description)
        if complete == False : 
            raise HTTPException(status_code= 400, detail=f"이미 삭제된 프로젝트입니다.")
    
        self.logger.info(f"[프로젝트 수정 성공] 프로젝트 ID: {project_id}, 수정자: {user.id}, 변경된 설명: {param.description}")
        return project_id
    
    def delete(self, db: Session, user: User, project_id: int) -> int:
        user_project_role: ProjectUserRole = self.project_repository_port.get_role_by_project_and_user(db, project_id, user.id)
        if(not self.check_delete_permission(user.role, user_project_role)):
            self.logger.warning(f"[프로젝트 삭제 실패] 사용자 {user.id}가 권한 없이 프로젝트 삭제 시도")
            raise HTTPException(status_code= 403, detail=f"권한이 없습니다.")

        complete: bool = self.project_repository_port.delete(db, project_id)
        if complete == False : 
            self.logger.warning("이미 삭제된 프로젝트입니다.")
        
        self.logger.info(f"[프로젝트 삭제 성공] 프로젝트 ID: {project_id}, 수정자: {user.id}")
        return project_id
    
    def read(self, db: Session, user: User, project_id: int) -> Project:
        user_project_role: ProjectUserRole = self.project_repository_port.get_role_by_project_and_user(db, project_id, user.id)
        if(not self.check_read_permission(user.role, user_project_role)):
            self.logger.warning(f"[프로젝트 읽기 실패] 사용자 {user.id}가 권한 없이 프로젝트 읽기 시도")
            raise HTTPException(status_code= 403, detail=f"권한이 없습니다.")

        project: Optional[Project] = self.project_repository_port.get_by_id(db, project_id)
        if project is None:
            raise HTTPException(status_code= 404, detail=f"프로젝트 {project_id} 를  찾을 수 없습니다.")
        
        return project

    def check_invite_permission(self, user_role: UserRole, project_role: Optional[ProjectRole]) -> bool:
        return user_role == UserRole.ADMIN or project_role == ProjectRole.OWNER
       
    def check_read_permission(self, user_role: UserRole, project_role: Optional[ProjectRole]) -> bool:
        return user_role == UserRole.ADMIN or project_role in {ProjectRole.OWNER, ProjectRole.EDITOR, ProjectRole.VIEWER}

    def check_create_permission(self, user_role: UserRole) -> bool:
        return user_role in {UserRole.ADMIN, UserRole.PROJECT_OWNER}

    def check_update_permission(self, user_role: UserRole, project_role: Optional[ProjectRole]) -> bool:
        return user_role == UserRole.ADMIN or project_role in {ProjectRole.OWNER, ProjectRole.EDITOR}
    
    def check_delete_permission(self, user_role: UserRole, project_role: Optional[ProjectRole]) -> bool:
        return user_role == UserRole.ADMIN or project_role == ProjectRole.OWNER
