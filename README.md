# TaskFlow — Full-Stack Task Management Platform

TaskFlow is a full-stack task management application built with **FastAPI**, **SQLAlchemy**, and a **vanilla JavaScript** frontend. It includes a custom-built algorithms engine for sorting and searching tasks, along with a rule-based AI parser for natural-language quick-add of tasks.

---

## 🚀 Features

- **User Management** — Create and manage users
- **Project Management** — Organize tasks under multiple projects
- **Task Management** — Full CRUD (Create, Read, Update, Delete) operations on tasks
- **Custom Algorithms Engine**
  - Insertion Sort — sort tasks by priority/due date
  - Binary Search — fast lookup on sorted task data
  - Linear Search — search tasks by keyword/title
- **AI Quick-Add Parser** — Rule-based natural language parser that converts plain text input (e.g. *"Submit report by tomorrow high priority"*) into structured task fields
- **RESTful API** built with FastAPI and documented via Swagger UI
- **SQLite Database** using SQLAlchemy ORM

---

## 🛠️ Tech Stack

**Backend**
- FastAPI
- SQLAlchemy
- Pydantic (data validation)
- SQLite (database)
- Uvicorn (ASGI server)

**Frontend**
- HTML5
- CSS3
- Vanilla JavaScript (Fetch API)

---

## 📁 Project Structure

```
TaskFlow1/
├── backend/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── routers/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   ├── projects.py       # Project endpoints
│   │   │   ├── tasks.py          # Task endpoints
│   │   │   └── users.py          # User endpoints
│   │   ├── __init__.py
│   │   ├── ai_parser.py          # Rule-based quick-add parser
│   │   ├── algorithms.py         # Sorting & searching algorithms
│   │   ├── database.py           # DB connection & session
│   │   ├── dependencies.py       # Shared dependencies
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── models.py             # SQLAlchemy models
│   │   └── schemas.py            # Pydantic schemas
│   ├── venv/                     # Backend virtual environment
│   ├── requirements.txt
│   └── taskflow.db
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── venv/                         # Root virtual environment
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd TaskFlow
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Run the Backend Server
```bash
uvicorn app.main:app --reload
```
Backend will run at: `http://127.0.0.1:8000`
Swagger API docs: `http://127.0.0.1:8000/docs`

### 4. Run the Frontend
Open `frontend/index.html` using **VS Code Live Server** extension.
> ⚠️ Do not open `index.html` directly via `file://` — this will cause CORS/fetch errors. Always use Live Server.

Frontend will run at: `http://127.0.0.1:5500` (or similar)

---

## 📡 API Endpoints (Overview)

| Method | Endpoint              | Description             |
|--------|------------------------|--------------------------|
| GET    | `/users/`              | Get all users            |
| POST   | `/users/`              | Create a new user         |
| GET    | `/projects/`           | Get all projects         |
| POST   | `/projects/`           | Create a new project      |
| GET    | `/tasks/`              | Get all tasks             |
| POST   | `/tasks/`              | Create a new task          |
| PUT    | `/tasks/{id}`          | Update a task              |
| DELETE | `/tasks/{id}`          | Delete a task              |

*(Full endpoint list available in Swagger docs at `/docs`)*

---

## 🧠 Algorithms Engine

Implemented from scratch (no built-in sort/search functions used):

- **Insertion Sort** — Used to sort tasks by priority or due date
- **Binary Search** — Used for fast lookups on sorted task lists
- **Linear Search** — Used for keyword-based task search

## 🤖 AI Quick-Add Parser

A rule-based natural language parser (`ai_parser.py`) that extracts structured task data (title, due date, priority) from plain text input — without relying on any external LLM API.

---

## 👨‍💻 Author

**Amit**
Software Engineering Student — Masai School
Backend Focus: FastAPI, SQLAlchemy, PostgreSQL/SQLite

---

## 📄 License

This project was built as part of a college/course assignment for educational purposes.
