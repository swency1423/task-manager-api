from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Use a fresh in-memory database for tests
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_get_task():
    res = client.post("/tasks", json={"title": "Learn FastAPI", "description": "Build an API"})
    assert res.status_code == 201
    task_id = res.json()["id"]
    assert res.json()["completed"] is False

    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Learn FastAPI"


def test_list_tasks():
    client.post("/tasks", json={"title": "Second task"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.json()) >= 2


def test_update_and_complete_task():
    task_id = client.post("/tasks", json={"title": "Old title"}).json()["id"]
    res = client.put(f"/tasks/{task_id}", json={"title": "New title", "completed": True})
    assert res.status_code == 200
    assert res.json()["title"] == "New title"
    assert res.json()["completed"] is True


def test_delete_task():
    task_id = client.post("/tasks", json={"title": "Delete me"}).json()["id"]
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_missing_task_returns_404():
    assert client.get("/tasks/99999").status_code == 404


def test_empty_title_is_rejected():
    assert client.post("/tasks", json={"title": ""}).status_code == 422
