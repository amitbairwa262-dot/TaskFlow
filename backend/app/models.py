from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    projects = relationship(
        "Project",
        back_populates="owner"
    )

    tasks = relationship(
        "Task",
        back_populates="assigned_to"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  
    description = Column(String, nullable=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    owner = relationship(
        "User",
        back_populates="projects"
    )

    tasks = relationship(
        "Task",
        back_populates="project"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)

    status = Column(
        String,
        default="pending"
    )

    priority = Column(
        Integer,
        default=0
    )

    due_date = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    assigned_to_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )

    assigned_to = relationship(
        "User",
        back_populates="tasks"
    )