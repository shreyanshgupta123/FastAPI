from fastapi import  HTTPException, Depends, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import SessionLocal
from ..models import Todos
from starlette import status
from .auth import get_current_user
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):

    title: str =Field(min_length=3)
    description: str=Field(min_length=3,max_length=50)
    priority: int=Field(gt=0, le=5)
    complete: bool



@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,
                      todo_request: TodoRequest,
                      db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    todo_model=Todos(**todo_request.model_dump(),owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.put("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        user:user_dependency,
        todo_request: TodoRequest,
        db: db_dependency,
        todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete


    db.add(todo_model)
    db.commit()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency,user:user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    # Alternatively, you can use the following line to delete the todo_model directly:
   # db.delete(todo_model)
    db.commit()
    return {"message": "Todo deleted successfully"}