from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


#  Define the schemas
class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoCreate(TodoBase):
    user_id: int

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    user_id: int
    creation_time: datetime
    completion_time: Optional[datetime] = None

    class Config:
        orm_mode = True




## schemas for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for user response after successful sign-up or retrieval
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    creation_time: datetime

    class Config:
        orm_mode = True

# Schema for login response with JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

## user password reset 
class ResetRequest(BaseModel):
    email: str

class PasswordResetForm(BaseModel):
    token: str
    new_password: str
    confirm_password: str