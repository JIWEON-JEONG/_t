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
    description: str

class InviteProjectRequest(BaseModel):
    member_id: int
    member_role: ProjectRole

class ProjectResponseDto(BaseModel):
    id: int
    company_id: int
    owner_id: int
    description: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime