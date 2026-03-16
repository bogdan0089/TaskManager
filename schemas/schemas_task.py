from pydantic import BaseModel
from core.enum import TaskStatus


class CreateTask(BaseModel):
    title: str
    status: TaskStatus

class ResponseTask(CreateTask):
    id: int



class TaskUpdateStatus(BaseModel):
    title: str
    status: TaskStatus
    


class TaskUpdate(BaseModel):
    title: str
    status: TaskStatus


