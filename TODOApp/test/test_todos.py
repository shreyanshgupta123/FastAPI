from fastapi import status
from .utiles import *

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

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': test_todo.id,
            'title': 'learn to code',
            'description': 'learn to code',
            'priority': 1,
            'complete': False,
            'owner_id': 1
        }
    ]


def test_read_one_authenticated(test_todo):
    response=client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            'id': test_todo.id,
            'title': 'learn to code',
            'description': 'learn to code',
            'priority': 1,
            'complete': False,
            'owner_id': 1
        }

def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code==404
    assert response.json() == {
        "detail": 'Todo not found'
    }
def test_create_todo(test_todo):
    request_data={
        'title': 'learn to code',
        'description': 'learn to code',
        'priority': 5,
        'complete': False,
    }
    response = client.post("/todos", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data={
        'title':'changed title',
        'description':'changed description',
        'priority':1,
        'complete':False,
    }
    response=client.put('/todo/1',json=request_data)
    assert response.status_code == 204
    db=TestingSessionLocal()
    model=db.query().filter(Todos.id==1).first()
    assert model.title=='changed title'

def test_update_todo_not_found(test_todo):
    request_data={
        'title':'changed title',
        'description':'changed description',
        'priority':1,
        'complete':False,
    }
    response=client.put('/todo/99',json=request_data)
    assert response.status_code == 404
    assert response.json()=={
        'detail':'Todo not found.'
    }

def test_delete_todo(test_todo):
    response=client.delete('/todo/1')
    assert response.status_code==204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 404
    assert response.json() == {
        'detail': 'Todo not found.'
    }

