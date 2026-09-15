from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    owner_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    class Config:
        from_attributes = True

class ProjectStats(BaseModel):
    project_id: int
    project_name: str
    total_tasks: int
    todo_count: int
    in_progress_count: int
    done_count: int

class TaskBase(BaseModel):
    title: str
    status: str = "todo"
    priority: Literal["low", "medium", "high"] = Field(...)
    due_date: Optional[str] = None
    project_id: int
    assigned_to_id: Optional[int] = None

class TaskCreate(TaskBase):
    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Task title cannot be blank or contain only whitespace.")
        return value.strip()

    @field_validator("priority")
    @classmethod
    def validate_priority_set(cls, value: str) -> str:
        return value.lower().strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[str] = None
    assigned_to_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    class Config:
        from_attributes = True

class QuickAddRequest(BaseModel):
    description: str
    project_id: int
    assigned_to_id: Optional[int] = None