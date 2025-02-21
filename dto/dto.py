from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime

from domain.entity.enum import ProjectRole

class SendEmailRequest(BaseModel):
    email: EmailStr

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str

class CreateUserRequest(BaseModel):
    company_id: int
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    body: dict
    exp: datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUserPasswordRequest(BaseModel):
    token: str
    update_password: str
    before_password: str  

class UserSessionDto(BaseModel):
    session_id: str
    ip: str

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