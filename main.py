from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI()

# In-memory storage for todos
todos = []

# Pydantic model for todo
class Todo(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    completed: bool = False
    creation_datetime: datetime = datetime.now()
    completion_datetime: Optional[datetime] = None
    

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    todos.append(todo.dict())
    return todo

@app.get("/todos/", response_model=List[Todo])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            updated_todo.creation_datetime = todo["creation_datetime"]  # Keep original creation date
            if updated_todo.completed and not todo["completed"]:
                updated_todo.completion_datetime = datetime.now()
            todos[index] = updated_todo.dict()
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            del todos[index]
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
