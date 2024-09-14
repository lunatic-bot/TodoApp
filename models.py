from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from database import Base

class TodoItem(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    creation_time = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")))
    completion_time = Column(DateTime, nullable=True)
    # New field to reference the User who owns this todo
    user_id = Column(Integer, ForeignKey("users.id"))

    # Establish a relationship with the User model
    owner = relationship("User", back_populates="todos")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    creation_time = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")))

    # password reset token and its expiration time
    reset_token = Column(String, nullable=True)  
    reset_token_expiration = Column(DateTime, nullable=True)  

    # Relationship with TodoItem
    todos = relationship("TodoItem", back_populates="owner", cascade="all, delete-orphan")












# # models.py
# from sqlalchemy import Column, Integer, String, Boolean, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# from pytz import timezone 

# Base = declarative_base()

# class TodoItem(Base):
#     __tablename__ = 'todos'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String)
#     completed = Column(Boolean, default=False)
#     creation_time = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")))
#     completion_time = Column(DateTime, nullable=True)
