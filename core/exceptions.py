from fastapi import HTTPException, status


class BaseAppExeption(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundError(BaseAppExeption):
    def __init__(self, user_id: int = None, email: str = None):
        if user_id:
            self.detail = f"User with id: {user_id} not found."
        elif email:
            self.detail = f"User with email: {email} not found."
        else:
            self.detail = f"Not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)
        self.user_id = user_id
        self.email = email

class Error(BaseAppExeption):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Error")
        
class UsersNotFoundError(BaseAppExeption):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found.")

class TasksNotFoundError(BaseAppExeption):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found.")

class TaskAlreadyError(BaseAppExeption):
    def __init__(self, task_id: int):
        if task_id:
            self.detail = f"Task with id: {task_id} already."

        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=self.detail)
        self.task_id=task_id

class UserAlreadyError(BaseAppExeption):
    def __init__(self, email: str = None, user_id: int = None):
        if user_id:
            detail = f"User with id: {user_id} already."
        elif email:
            detail = f" User with email: {email} already."
        else:
            detail = f"User is already."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
        self.user_id=user_id
        self.email=email

class InsufficientPermissionsError(BaseAppExeption):
    def __init__(self, required_role: str, user_role: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error you need role: {required_role} your role: {user_role}"
        )
        self.required_role=required_role
        self.user_role=user_role

class InvalidRoleUser(BaseAppExeption):
    def __init__(self, expected_role: str, actual_role: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error role: we wait: {expected_role} your actual role: {actual_role}"
        )
        self.expected_role=expected_role
        self.actual_role=actual_role

class UserUpdateError(BaseAppExeption):
    def __init__(self, reason="Error Update", user_id: int = None):
        detail = f"Error update user: {user_id} - {reason}" if user_id else f"Error update: {reason}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.user_id=user_id
        self.reason=reason

class TaskUpdateError(BaseAppExeption):
    def __init__(self, reason="Error Update", task_id: int = None):
        detail = f"Error update task: {task_id} - {reason}" if task_id else f"Error update task: {reason}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.task_id=task_id
        self.reason=reason

class UserDeleteError(BaseAppExeption):
    def __init__(self, reason="Error Delete", user_id: int = None):
        detail = f"Error delete user: {user_id} - {reason}" if user_id else f"Error delete: {reason}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.user_id=user_id
        self.reason=reason

class TaskDeleteError(BaseAppExeption):
    def __init__(self, reason="Error delete.", task_id: int = None):
        detail = f"Error delete task: {task_id} - {reason}" if task_id else f"Error delete task: {reason}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.task_id=task_id
        self.reason = reason

class TaskNotFound(BaseAppExeption):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Has not tasks: {user_id}"
        )
        self.user_id=user_id


