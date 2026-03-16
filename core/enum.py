from enum import Enum

class TaskStatus(str, Enum):
    in_progress = "in_progress"
    done = "done"
    

class UserRole(str, Enum):
    admin = "admin"
    worker = "worker"