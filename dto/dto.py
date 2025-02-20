from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime

from domain.entity.enum import ProjectRole

class CreateUserRequest(BaseModel):
    company_id: int
    email: EmailStr
    password: str

class UserSessionDto(BaseModel):
    session_id: str
    ip: str

class UpdateUserPasswordRequest(BaseModel):
    before_password: str
    update_password: str

class CreateProjectRequest(BaseModel):
    description: str

class UpdateProjectRequest(BaseModel):
    project_id: int
    description: str

class InviteProjectRequest(BaseModel):
    project_id: int
    member_id: int
    member_role: ProjectRole

class DeleteProjectRequest(BaseModel):
    project_id: int

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    verification_code: str

class PasswordResetRequest(BaseModel):
    email: EmailStr
    new_password: str
    reset_code: str  # 이메일로 발송된 재설정 코드를 입력받음

class UserResponseDto(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

    @field_validator('created_at', 'updated_at')
    def convert_datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v