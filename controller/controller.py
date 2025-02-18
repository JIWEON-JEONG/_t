from application.email_sender import EmailSender
from dto.dto import SignUpRequest
from fastapi import APIRouter, HTTPException, Depends
from application.application_service import ApplicationService
from domain.service.email_verification_service import EmailVerificationService
from common.security_service import SecurityService
from domain.entity.port.user_repository_port import UserRepositoryPort
from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService
from repository.user_repository import UserRepository
from repository.email_verification_repository import EmailVerificationRepository

from passlib.context import CryptContext

# repository
def get_email_verification_repository() -> EmailVerificationRepositoryPort:
    return EmailVerificationRepository() 

def get_user_repository() -> UserRepositoryPort:
    return UserRepository() 

# service
def get_crypto_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_security_service(context: CryptContext = Depends(get_crypto_context)):
    return SecurityService(context)

def get_email_verification_service(email_verification_repository: EmailVerificationRepository = Depends(get_email_verification_repository)) -> EmailVerificationService:
    return EmailVerificationService(email_verification_repository)

def get_user_service(user_repository: UserRepositoryPort = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)

# application
def get_email_sender() -> EmailSender:
    return EmailSender()

def get_application_service(user_service: UserService = Depends(get_user_service),
    email_verification_service: EmailVerificationService = Depends(get_email_verification_service),
    email_sender: EmailSender = Depends(get_email_sender), security_service: SecurityService = Depends(get_security_service)
    ) -> ApplicationService:
    return ApplicationService(user_service, email_verification_service, email_sender,security_service) 

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

# @router.get("/user/{user_id}", response_model=UserResponseDto)
# def read_user(user_id: int, application_service: ApplicationService = Depends(get_application_service)):
#     user = User()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@router.post("/sign-up")
async def sign_up(
    user_data: SignUpRequest,
    application_service: ApplicationService = Depends(get_application_service)):

    user_id = await application_service.sign_up(user_data)
    if not user_id:
        raise HTTPException(status_code=400, detail="Sign-up failed")
    return {"message": "User signed up successfully", "user_id": user_id}