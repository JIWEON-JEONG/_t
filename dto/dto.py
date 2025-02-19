from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUserPasswordRequest(BaseModel):
    before_password: str
    update_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

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