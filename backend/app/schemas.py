from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
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
    priority: str
    due_date: Optional[str] = None
    project_id: int

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
        normalized = value.lower().strip()
        if normalized not in ["low", "medium", "high"]:
            raise ValueError("Priority must be explicitly set to 'low', 'medium', or 'high'.")
        return normalized

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    class Config:
        from_attributes = True

class QuickAddRequest(BaseModel):
    text: str
    project_id: int