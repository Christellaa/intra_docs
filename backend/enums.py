from enum import Enum

################################
# User enums ###################
################################
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"

################################
# File enums ###################
################################
class FileVisibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"

################################
# Log enums ####################
################################
class ActionType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    
class TargetType(str, Enum):
    USER = "user"
    FILE = "file"