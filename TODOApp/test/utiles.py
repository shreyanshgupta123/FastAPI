from sqlalchemy import create_engine, StaticPool,text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..routers.todos import get_db, get_current_user
import pytest
from ..models import Todos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'FastAPI', 'id': 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo=Todos(
        title='learn to code',
        description='learn to code',
        priority=1,
        complete=False,
        owner_id=1,
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
