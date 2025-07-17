from fastapi import  HTTPException, Depends, Path, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import SessionLocal
from ..models import Todos
from starlette import status
from .auth import get_current_user
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    print(user.get('role'))

    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')

    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')  # Corrected

    db.delete(todo_model)
    db.commit()
    return  # 204 means no content, so no return body



