from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    creation_time: datetime
    completion_time: Optional[datetime] = None

    class Config:
        orm_mode = True

class TodoItem(TodoBase):
    creation_time: datetime
    completion_time: Optional[datetime] = None

    class Config:
        orm_mode = True


