import enum

class ProjectRole(enum.Enum):
    ADMIN = "ADMIN"
    PROJECT_OWNER = "PROJECT_OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"
