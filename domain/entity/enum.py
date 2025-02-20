import enum

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    PROJECT_OWNER = "PROJECT_OWNER"
    MEMBER = "MEMBER"
    
class ProjectRole(enum.Enum):
    OWNER = "OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"

USER_ROLE_PERMISSIONS = {
    UserRole.ADMIN: {"CREATE", "INVITE", "EDIT", "VIEW", "DELETE", "DELETE_USER"},
    UserRole.PROJECT_OWNER: {"CREATE", "INVITE", "EDIT", "VIEW", "DELETE"},
    UserRole.MEMBER: {"EDITOR", "VIEW"},
}

PROJECT_ROLE_PERMISSIONS = {
    ProjectRole.OWNER: {"CREATE", "INVITE", "EDIT", "VIEW", "DELETE", "DELETE_USER"},
    ProjectRole.EDITOR: {"CREATE", "INVITE", "EDIT", "VIEW", "DELETE"},
    ProjectRole.VIEWER: {"EDITOR", "VIEW"},
}