from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TodoResponse(TodoBase):
    id: int
    creation_time: datetime
    completion_time: Optional[datetime] = None

    class Config:
        orm_mode = True

# TodoItem can be an alias for TodoResponse if both represent the same data structure.
TodoItem = TodoResponse



