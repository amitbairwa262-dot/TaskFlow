# TaskFlow — Full-Stack Task Management Platform

TaskFlow is a full-stack task management application built with **FastAPI**, **SQLAlchemy**, and a **vanilla JavaScript** frontend. It includes a custom-built algorithms engine for sorting and searching tasks, along with a rule-based AI parser for natural-language quick-add of tasks.

---

## 🚀 Features

- **User Management** — Register/login and manage users
- **Project Management** — Organize tasks under multiple projects
- **Task Management** — Full CRUD (Create, Read, Update, Delete) operations on tasks
- **Custom Algorithms Engine**
  - Insertion Sort — sort tasks by priority
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
TaskFlow/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── projects.py       # Project endpoints
│   │   │   ├── tasks.py          # Task endpoints
│   │   │   └── users.py          # User endpoints (register/login)
│   │   ├── __init__.py
│   │   ├── ai_parser.py          # Rule-based quick-add parser
│   │   ├── algorithms.py         # Sorting & searching algorithms
│   │   ├── database.py           # DB connection & session
│   │   ├── dependencies.py       # Shared dependencies
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── models.py             # SQLAlchemy models
│   │   └── schemas.py            # Pydantic schemas
│   ├── requirements.txt
│   └── taskflow.db
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── benchmark.py                  # Algorithm benchmark script
├── seed.py                       # Sample data seeder
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
python -m uvicorn app.main:app --reload
```
Backend will run at: `http://127.0.0.1:8000`
Swagger API docs: `http://127.0.0.1:8000/docs`

### 4. Seed sample data (optional)
```bash
cd ..
python seed.py
```

### 5. Run the Frontend
Open `frontend/index.html` using **VS Code Live Server** extension.
> ⚠️ Do not open `index.html` directly via `file://` — this will cause CORS/fetch errors. Always use Live Server.

Frontend will run at: `http://127.0.0.1:5500` (or similar)

---

## 📡 API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register` | Register a new user |
| POST | `/api/users/login` | Login with username/password |
| GET | `/api/users/` | List all users |

**Example — Register**
Request: `POST /api/users/register`
```json
{ "username": "amit", "email": "amit@example.com", "password": "secret123" }
```
Response `201`:
```json
{ "id": 1, "username": "amit", "email": "amit@example.com" }
```

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/projects/` | Create a project |
| GET | `/api/projects/` | List all projects |
| GET | `/api/projects/statistics` | Stats for all projects (SQL GROUP BY) |
| GET | `/api/projects/{id}/stats` | Stats for a single project |

**Example — Single Project Stats**
Request: `GET /api/projects/1/stats`
Response `200`:
```json
{ "total_tasks": 34, "by_status": { "pending": 12, "in_progress": 9, "completed": 13 } }
```

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/?assigned_to_id={id}` | List tasks (optionally filtered by user) |
| GET | `/api/tasks/sorted?project_id={id}` | Priority-sorted tasks (Insertion Sort) |
| GET | `/api/tasks/search?q={query}` | Keyword search (Linear Search) |
| GET | `/api/tasks/find-exact?title={t}&project_id={id}` | Exact title lookup (Binary Search) |
| GET | `/api/tasks/{id}` | Get one task |
| PUT | `/api/tasks/{id}` | Full update |
| PATCH | `/api/tasks/{id}` | Partial update |
| DELETE | `/api/tasks/{id}` | Delete a task |
| POST | `/api/tasks/quick-add` | AI Quick-Add (natural language) |

**Example — Create Task**
Request: `POST /api/tasks/`
```json
{ "title": "Fix login bug", "priority": "high", "due_date": "tomorrow", "project_id": 1, "assigned_to_id": 3 }
```
Response `201`:
```json
{ "id": 42, "title": "Fix login bug", "status": "todo", "priority": "high", "due_date": "tomorrow", "project_id": 1, "assigned_to_id": 3 }
```

**Example — AI Quick-Add**
Request: `POST /api/tasks/quick-add`
```json
{ "description": "Fix broken inventory pipeline calculations by tomorrow afternoon with high priority", "project_id": 1, "assigned_to_id": 3 }
```
Response `201`:
```json
{ "id": 43, "title": "Fix broken inventory pipeline calculations afternoon", "status": "todo", "priority": "high", "due_date": "tomorrow", "project_id": 1 }
```

*(Full interactive docs at `/docs`)*

---

## 🧠 Algorithms Engine — Complexity & Benchmarks

All three algorithms are implemented from scratch (no built-in `sort()`/`bisect` used).

| Algorithm | Time Complexity | Used For |
|-----------|-----------------|----------|
| Insertion Sort | O(n²) worst/avg case | Sorting tasks by priority |
| Linear Search | O(n) | Keyword/substring search across all tasks |
| Binary Search | O(log n) | Exact title lookup on a pre-sorted list |

**Why sort-first for binary search:** Binary Search requires the input to already be sorted. Sorting from scratch costs O(n log n), so binary search only pays off when the same sorted list is reused across multiple lookups rather than re-sorted every time.

**Benchmark results** (comparison counts from `benchmark.py`, run on n = 10 / 500 / 3000 randomly generated tasks):

| n | Insertion Sort comparisons | Linear Search comparisons | Binary Search comparisons |
|---|---|---|---|
| 10 | 30 | 10 | 3 |
| 500 | 45,903 | 500 | 9 |
| 3000 | 1,535,774 | 3,000 | 11 |

**Analysis:** Insertion Sort comparisons grow roughly quadratically — going from n=500 to n=3000 (6x the input) increases comparisons by ~33x, consistent with O(n²). Linear Search grows exactly linearly with n, as expected for O(n). Binary Search grows logarithmically — comparisons only go from 3 to 11 across a 300x increase in n, matching O(log n).

---

## 🤖 AI Quick-Add — Prompting Technique & Examples

`MockAIParser` simulates an LLM-based extraction pipeline without making real network calls. Its `build_prompt()` method constructs a role-structured prompt (a `system`/`user` message pair) documenting what a real LLM integration would receive; the parser then applies deterministic rule-based extraction to stand in for the model's response.

**System prompt (fixed):**
> "You are a task-parsing assistant. Extract three fields from the user's natural language statement: title, priority (low/medium/high), and due_date (or null if not mentioned)..."

**Worked Examples**

| # | Input | Extracted Title | Priority | Due Date |
|---|-------|------------------|----------|----------|
| 1 | "Fix broken inventory pipeline calculations by tomorrow afternoon with high priority" | Fix broken inventory pipeline calculations afternoon | high | tomorrow |
| 2 | "Submit report today" | Submit report | medium | today |
| 3 | "Research new library whenever" | Research new library | low | null |
| 4 | "Deploy hotfix asap" | Deploy hotfix | high | null |
| 5 | "Team standup next monday" | Team standup | medium | next monday |

---

## 👨‍💻 Author

**Amit**
Software Engineering Student — Masai School
Backend Focus: FastAPI, SQLAlchemy, PostgreSQL/SQLite

---

## 📄 License

This project was built as part of a college/course assignment for educational purposes.