import datetime
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException,Request
from pydantic import BaseModel
from sqlalchemy.sql.functions import user
from starlette import status
from ..database import SessionLocal
from ..models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from fastapi.templating import Jinja2Templates
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
SECRET_KEY = '4d68b85ee27a10f49b3b0c44051ffc757a4e7c36ef08fdbb99d5e278c84e1970'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Pydantic model for user creation request
class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str
    phone_number: str

class UpdateUserRequest(BaseModel):
    email: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    phone_number: str | None = None
    role: str | None = None
    is_active: bool | None = None

class TokenData(BaseModel):
    access_token: str
    token_type: str
# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates=Jinja2Templates(directory="TodoApp/templates")

###pages###
@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})





###Endpoints####
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    print(user)
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(username:str,user_id:int,role:str,expire_delta:timedelta):
    encode = {'sub':username,'id':user_id,'role':role}
    expire = datetime.datetime.now(datetime.timezone.utc) + expire_delta
    encode.update({'exp':expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None or user_role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

        return {
            'username': username,
            'id': user_id,
            'role': user_role   # ✅ Include role in returned user dict
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate User')



@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency, current_user: Annotated[dict, Depends(get_current_user)]):
    # Optional: Only allow admin users to access this endpoint
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can view all users."
        )

    users = db.query(User).all()
    return users

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,
                      db: db_dependency):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.firstname,
        last_name=create_user_request.lastname,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

@router.post("/token",response_model=TokenData)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials')

    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=10)
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    update_data: UpdateUserRequest,
    db: db_dependency,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    # Optional: Only admin can update users
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update users."
        )

    user_model = db.query(User).filter(User.id == user_id).first()
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Update fields if provided
    if update_data.email is not None:
        user_model.email = update_data.email
    if update_data.firstname is not None:
        user_model.first_name = update_data.firstname
    if update_data.lastname is not None:
        user_model.last_name = update_data.lastname
    if update_data.phone_number is not None:
        user_model.phone_number = update_data.phone_number
    if update_data.role is not None:
        user_model.role = update_data.role
    if update_data.is_active is not None:
        user_model.is_active = update_data.is_active

    db.commit()
    db.refresh(user_model)
    return {"message": "User updated successfully", "user": user_model}
