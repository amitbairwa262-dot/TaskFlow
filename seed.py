import sys
import os
import random
import time

# Allow importing from the backend/app package
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.database import SessionLocal, engine, Base
from app.models import User, Project, Task

# Create tables if they don't already exist
Base.metadata.create_all(bind=engine)

STATUSES = ["pending", "in_progress", "completed"]
PRIORITIES = [0, 1, 2]  # low, medium, high (integer scale)

SAMPLE_TASK_TITLES = [
    "Submit report", "Fix login bug", "Design homepage", "Write unit tests",
    "Update documentation", "Review pull request", "Prepare presentation",
    "Client call", "Deploy to production", "Refactor database layer",
    "Plan sprint", "Backup database", "Optimize queries", "Team standup",
    "Code review", "Research new library", "Update dependencies",
    "Write blog post", "Fix CSS issue", "Test payment gateway",
]


def seed_users(db, count=5):
    users = []
    for i in range(1, count + 1):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            hashed_password="not_a_real_hash",
            is_active=True,
        )
        db.add(user)
        users.append(user)
    db.commit()
    for u in users:
        db.refresh(u)
    return users


def seed_projects(db, users, count=3):
    projects = []
    for i in range(1, count + 1):
        project = Project(
            name=f"Project {i}",
            description=f"Sample project {i} used for benchmarking",
            owner_id=random.choice(users).id,
        )
        db.add(project)
        projects.append(project)
    db.commit()
    for p in projects:
        db.refresh(p)
    return projects


def seed_tasks(db, users, projects, count=100):
    tasks = []
    for i in range(count):
        title = random.choice(SAMPLE_TASK_TITLES) + f" #{i+1}"
        task = Task(
            title=title,
            description="Auto-generated task for benchmarking",
            status=random.choice(STATUSES),
            priority=random.choice(PRIORITIES),
            due_date=None,
            project_id=random.choice(projects).id,
            assigned_to_id=random.choice(users).id,
        )
        db.add(task)
        tasks.append(task)
    db.commit()
    for t in tasks:
        db.refresh(t)
    return tasks


def main():
    db = SessionLocal()
    try:
        start = time.time()

        print("Seeding users...")
        users = seed_users(db, count=5)
        print(f"  Created {len(users)} users")

        print("Seeding projects...")
        projects = seed_projects(db, users, count=3)
        print(f"  Created {len(projects)} projects")

        print("Seeding tasks...")
        tasks = seed_tasks(db, users, projects, count=100)
        print(f"  Created {len(tasks)} tasks")

        elapsed = time.time() - start
        print(f"\nSeeding complete in {elapsed:.3f} seconds.")
        print(f"Total tasks in DB (approx.): {len(tasks)}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
