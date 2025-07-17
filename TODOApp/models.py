from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    email= Column(String,unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role=Column(String)
    phone_number=Column(String)



class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('users.id'))
