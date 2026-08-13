import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

from app.routers import users, projects, tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("taskflow_middleware")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API", version="1.0.0")


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.middleware("http")
async def log_request_execution_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(f"Method: {request.method} | Path: {request.url.path} | Duration: {process_time_ms}ms | Status: {response.status_code}")
    return response

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])