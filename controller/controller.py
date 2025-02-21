from application.auth_application_service import AuthApplicationService
from application.email_sender import EmailSender
from application.project_application_service import ProjectApplicationService
from common.transaction import get_db
from domain.entity.port.email_verification_repository_port import EmailVerificationRepositoryPort
from domain.entity.port.project_repository_port import ProjectRepositoryPort
from domain.entity.port.user_session_repository_port import UserSessionRepositoryPort
from domain.entity.project import Project
from domain.entity.user import User
from domain.service.project_service import ProjectService
from domain.service.user_session_service import UserSessionService
from dto.dto import CreateProjectRequest, CreateUserRequest, InviteProjectRequest, LoginRequest, ProjectResponseDto, SendEmailRequest, UpdateProjectRequest, UpdateUserPasswordRequest, VerifyEmailRequest
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from sqlalchemy.orm import Session
from application.user_application_service import UserApplicationService
from domain.service.email_verification_service import EmailVerificationService
from common.security_service import SecurityService
from domain.entity.port.user_repository_port import UserRepositoryPort
from domain.service.user_service import UserService
from domain.service.email_verification_service import EmailVerificationService
from repository.project_repository import ProjectRepository
from repository.user_repository import UserRepository
from repository.email_verification_repository import EmailVerificationRepository

from passlib.context import CryptContext

from repository.user_session_repository import UserSessionRepository

# repository
def get_email_verification_repository() -> EmailVerificationRepositoryPort:
    return EmailVerificationRepository() 

def get_user_repository() -> UserRepositoryPort:
    return UserRepository()

def get_user_session_repository() -> UserSessionRepositoryPort:
    return UserSessionRepository() 

def get_project_repository() -> ProjectRepositoryPort:
    return ProjectRepository()  

# service
def get_crypto_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_security_service(context: CryptContext = Depends(get_crypto_context)):
    return SecurityService(context)

def get_email_verification_service(email_verification_repository: EmailVerificationRepositoryPort = Depends(get_email_verification_repository)) -> EmailVerificationService:
    return EmailVerificationService(email_verification_repository)

def get_user_session_service(user_session_repository: UserSessionRepositoryPort = Depends(get_user_session_repository),
                             security_service: SecurityService = Depends(get_security_service)) -> UserSessionService:
    return UserSessionService(user_session_repository, security_service)

def get_user_service(user_repository: UserRepositoryPort = Depends(get_user_repository),
                     user_session_service: UserSessionService = Depends(get_user_session_service),
                     security_service: SecurityService = Depends(get_security_service)) -> UserService:
    return UserService(user_repository, security_service, user_session_service)

def get_project_service(project_repository: ProjectRepositoryPort = Depends(get_project_repository)) -> ProjectService:
    return ProjectService(project_repository)

# application
def get_email_sender() -> EmailSender:
    return EmailSender()

def get_auth_application_service(user_service: UserService = Depends(get_user_service),
    email_verification_service: EmailVerificationService = Depends(get_email_verification_service),
    user_session_service: UserSessionService = Depends(get_user_session_service), security_service: SecurityService = Depends(get_security_service),
    email_sender: EmailSender = Depends(get_email_sender)
    ) -> AuthApplicationService:
    return AuthApplicationService(user_service, email_verification_service, user_session_service, security_service, email_sender) 

def get_user_application_service(user_service: UserService = Depends(get_user_service),
    email_verification_service: EmailVerificationService = Depends(get_email_verification_service),
    ) -> UserApplicationService:
    return UserApplicationService(user_service, email_verification_service) 

def get_project_application_service(project_service: ProjectService = Depends(get_project_service)) -> ProjectApplicationService:
    return ProjectApplicationService(project_service) 

router = APIRouter()

@router.get("/health")
async def root():
    return {"message": "success"}

@router.post("/auth/send-email", summary="회원가입 인증 이메일 전송", description="회원가입을 진행하기 위해 인증코드를 이메일로 전송합니다.")
async def authenticate_email(
    request: SendEmailRequest,
    background_tasks: BackgroundTasks,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    await auth_application_service.authenticate_email(request.email, background_tasks= background_tasks, db=db)
    return {"message": "Success Send Email"}

@router.post("/auth/verify-email", summary="회원가입 인증 이메일 검증", description="회원가입을 진행하기 위해 인증코드를 검증합니다.")
async def verify_email(
    request: VerifyEmailRequest,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    response = await auth_application_service.verify_email(request.email, request.code, db=db)
    return {"message": response}

@router.post("/auth/login", summary="로그인", description="로그인을 하여 유저 세션을 생성합니다.")
async def login(
    request: LoginRequest, 
    client_request: Request, 
    response: Response,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    session_id = await auth_application_service.login(request, client_ip, db=db)

    response.set_cookie(
        key="session_id", 
        value=session_id, 
        max_age=10700,  
        httponly=True, 
        secure=True,  
        samesite="Strict"
    )
    return {"message": session_id}

@router.post("/auth/password", summary="비밀번호 변경 링크 전송", description="비밀번호 변경 링크를 유저의 이메일로 전송합니다.")
async def send_email_update_password(
    client_request: Request, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),  # DB 세션 주입
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service)
):
    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]

    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)
    session_id = await auth_application_service.send_email_update_password(user.id, user.email, background_tasks)

    return {"message": "Success Send Email"}

@router.patch("/user/password", summary="비밀번호 변경", description="비밀번호를 변경합니다.")
async def update_password(
    client_request: Request, 
    request: UpdateUserPasswordRequest, 
    db: Session = Depends(get_db),  # DB 세션 주입
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    user_application_service: UserApplicationService = Depends(get_user_application_service)
):
    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    
    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)
    user_id = await user_application_service.update_password(user.id, request, db=db)

    return {"message": user_id}

@router.post("/user", summary="회원가입", description="인증이 완료된 유저를 생성합니다.")
async def create_user(
    request: CreateUserRequest,
    user_application_service: UserApplicationService = Depends(get_user_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    user_id = await user_application_service.create_user(request, db=db)
    return {"message": user_id}

@router.post("/project", summary="프로젝트 생성", description="프로젝트를 생성합니다.")
async def create_project(
    client_request: Request,
    request: CreateProjectRequest,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    project_application_service: ProjectApplicationService = Depends(get_project_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)

    project_id = await project_application_service.create(user, request, db=db)
    return {"message": project_id}

@router.patch("/project/{project_id}", summary="프로젝트 수정", description="프로젝트를 수정합니다.")
async def update_project(
    client_request: Request,
    project_id: int,
    request: UpdateProjectRequest,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    project_application_service: ProjectApplicationService = Depends(get_project_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)

    project_id = await project_application_service.update(user, project_id, request, db=db)
    return {"message": project_id}

@router.get("/project/{project_id}", summary="프로젝트 조회", description="프로젝트를 조회합니다.")
async def read_project(
    client_request: Request,
    project_id: int,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    project_application_service: ProjectApplicationService = Depends(get_project_application_service),
    db: Session = Depends(get_db)) -> ProjectResponseDto: 

    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)

    project: Project = await project_application_service.read(user, project_id, db=db)
    return ProjectResponseDto(
        id=project.id,
        company_id=project.company_id,
        owner_id=project.owner_id,
        description=project.description,
        is_deleted=project.is_deleted,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.post("/project/{project_id}/member", summary="프로젝트 멤버 초대", description="프로젝트에 멤버를 초대합니다.")
async def invite_project(
    client_request: Request,
    project_id: int,
    request: InviteProjectRequest,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    project_application_service: ProjectApplicationService = Depends(get_project_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)

    project_id = await project_application_service.invite(user, project_id, request, db=db)
    return {"message": project_id}

@router.delete("/project/{project_id}", summary="프로젝트 삭제", description="프로젝트를 삭제합니다.")
async def delete_project(
    client_request: Request,
    project_id: int,
    auth_application_service: AuthApplicationService = Depends(get_auth_application_service),
    project_application_service: ProjectApplicationService = Depends(get_project_application_service),
    db: Session = Depends(get_db)  # DB 세션 주입
):
    session_id = client_request.cookies.get("session_id")
    client_ip: str = client_request.headers.get('X-Forwarded-For', client_request.client.host).split(',')[0]
    user: User = auth_application_service.get_user_by_session(db, session_id, client_ip)

    project_id = await project_application_service.delete(user, project_id, db=db)
    return {"message": project_id}