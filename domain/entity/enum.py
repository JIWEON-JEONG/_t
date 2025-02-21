import enum

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    PROJECT_OWNER = "PROJECT_OWNER"
    MEMBER = "MEMBER"
    
class ProjectRole(enum.Enum):
    OWNER = "OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"