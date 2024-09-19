# Import Pydantic's BaseModel and EmailStr for validation
from pydantic import BaseModel, EmailStr  
# Import Optional for nullable fields, and List for list types
from typing import Optional, List
# Import datetime for time-related fields  
from datetime import datetime  

# Define the base schema for a Todo item
class TodoBase(BaseModel):
    title: str  
    description: str  
    completed: bool = False  

# Schema for creating a new Todo item, extending TodoBase
class TodoCreate(TodoBase):
    user_id: int  

# Schema for updating a Todo item, allowing optional fields for partial updates
class TodoUpdate(BaseModel):
    title: Optional[str] = None  
    description: Optional[str] = None  
    completed: Optional[bool] = None  

# Schema for the response when retrieving a Todo item from the database
class TodoResponse(TodoBase):
    id: int  
    user_id: int  
    creation_time: datetime  
    completion_time: Optional[datetime] = None  

    class Config:
        orm_mode = True  

# Schema for user creation, used during sign-up
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

# Schema for the login response, containing the JWT access token
class Token(BaseModel):
    access_token: str  # The JWT token for authentication
    token_type: str  # Type of the token, typically "Bearer"

# Schema for requesting a password reset
class ResetRequest(BaseModel):
    email: str  

# Schema for resetting the password using a reset token
class PasswordResetForm(BaseModel):
    token: str  # The token sent to the user's email for password reset, required
    new_password: str  
    confirm_password: str  
