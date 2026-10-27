# Task Manager API

A simple REST API to manage tasks. Built with **FastAPI + SQLite + SQLAlchemy**.

## What it does

```
  You (browser / Postman)
          |
          v
   [ FastAPI app ]  -->  [ SQLAlchemy ]  -->  [ SQLite: tasks.db ]
```

| Action            | Method | URL           |
|-------------------|--------|---------------|
| Create a task     | POST   | /tasks        |
| View all tasks    | GET    | /tasks        |
| View one task     | GET    | /tasks/{id}   |
| Update / complete | PUT    | /tasks/{id}   |
| Delete a task     | DELETE | /tasks/{id}   |

## Project layout

```
task-manager-api/
├── app/
│   ├── main.py       # API routes
│   ├── models.py     # Database table (Task)
│   ├── schemas.py    # Data checks (Pydantic)
│   ├── crud.py       # Database actions
│   └── database.py   # SQLite connection
├── tests/
│   └── test_tasks.py # Automatic tests
├── requirements.txt
└── README.md
```

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** to try every endpoint in your browser.

## Example

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2 packets"}'

curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## Run tests

```bash
pytest
```

## Ideas to grow it later
- Add user login (JWT)
- Add due dates and priority
- Add a React frontend
- Add Docker
