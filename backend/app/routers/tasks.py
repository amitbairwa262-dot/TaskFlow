from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# एब्सोल्यूट इम्पोर्ट्स - डॉट (.) का उपयोग न करें
from app.dependencies import get_db
from app.models import Task, Project
from app.schemas import TaskCreate, TaskResponse, TaskUpdate, QuickAddRequest
from app.algorithms import AlgorithmsEngine
from app.ai_parser import MockAIParser

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Target project scope does not exist")
    db_task = Task(
        title=task.title, status=task.status, priority=task.priority,
        due_date=task.due_date, project_id=task.project_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskResponse])
def list_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# Sorted endpoint - insertion sort use karo
@router.get("/sorted", response_model=List[TaskResponse])
def get_priority_sorted_tasks(project_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    task_dicts = [
        {"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "due_date": t.due_date, "project_id": t.project_id}
        for t in tasks
    ]
    sorted_dicts = AlgorithmsEngine.insertion_sort_tasks(task_dicts)
    return [TaskResponse(**t) for t in sorted_dicts]

# Search endpoint - linear search use karo (SIRF EK BAAR DEFINE, duplicate hataya)
@router.get("/search", response_model=List[TaskResponse])
def search_tasks_by_title(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    all_tasks = db.query(Task).all()
    task_dicts = [
        {"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "due_date": t.due_date, "project_id": t.project_id}
        for t in all_tasks
    ]
    matched = AlgorithmsEngine.linear_search(task_dicts, q)
    return [TaskResponse(**t) for t in matched]

# Find-exact endpoint - binary search use karo
@router.get("/find-exact", response_model=TaskResponse)
def find_task_by_exact_title(title: str, project_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    task_dicts = sorted(
        [
            {"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "due_date": t.due_date, "project_id": t.project_id}
            for t in tasks
        ],
        key=lambda x: x["title"].lower()
    )
    result = AlgorithmsEngine.binary_search(task_dicts, title)
    if not result:
        raise HTTPException(status_code=404, detail="No exact title match found")
    return TaskResponse(**result)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task record not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_record(task_id: int, updates: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task record not found")

    data = updates.model_dump(exclude_unset=True)
    for key, val in data.items():
        setattr(db_task, key, val)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task_record(
    task_id: int,
    updates: TaskUpdate,
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task record not found"
        )

    # Only supplied fields will be updated
    data = updates.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for key, value in data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_record(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task record not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task record deleted successfully"}

@router.post("/quick-add", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def quick_add_task_ai(payload: QuickAddRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Target operational project scope not found")

    extracted_data = MockAIParser.parse_natural_language(payload.text)

    db_task = Task(
        title=extracted_data["title"],
        priority=extracted_data["priority"],
        due_date=extracted_data["due_date"],
        status="todo",
        project_id=payload.project_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
