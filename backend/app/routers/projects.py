from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.dependencies import get_db
from app.models import Project, Task
from app.schemas import ProjectCreate, ProjectResponse, ProjectStats

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(name=project.name, owner_id=project.owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.get("/statistics", response_model=List[ProjectStats])
def get_project_statistics(db: Session = Depends(get_db)):
    stats_query = db.query(
        Project.id.label("project_id"),
        Project.name.label("project_name"),
        func.count(Task.id).label("total_tasks"),
        func.count(func.nullif(Task.status != "todo", True)).label("todo_count"),
        func.count(func.nullif(Task.status != "in_progress", True)).label("in_progress_count"),
        func.count(func.nullif(Task.status != "done", True)).label("done_count")
    ).join(Task, Project.id == Task.project_id, isouter=True).group_by(Project.id).all()
    
    return [
        ProjectStats(
            project_id=row.project_id,
            project_name=row.project_name,
            total_tasks=row.total_tasks,
            todo_count=row.todo_count,
            in_progress_count=row.in_progress_count,
            done_count=row.done_count
        ) for row in stats_query
    ]

@router.get("/{project_id}/stats")
def get_single_project_stats(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    by_status = {"todo": 0, "in_progress": 0, "done": 0}
    for task in tasks:
        if task.status in by_status:
            by_status[task.status] += 1

    return {
        "total_tasks": len(tasks),
        "by_status": by_status
    }