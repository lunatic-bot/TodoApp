
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import init_db, get_db
from crud import get_todo_by_id, get_todos, create_todo, update_todo, delete_todo
from schemas import TodoResponse, TodoCreate, TodoUpdate
from models import TodoItem

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")

# Initialize the database
init_db()



@app.get("/", response_class=HTMLResponse)
def read_todos(request: Request, db: Session = Depends(get_db)):
    todos = db.query(TodoItem).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


# main.py
@app.post("/todos/", response_model=TodoResponse)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db=db, title=todo.title, description=todo.description)

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_todo_by_id(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.get("/todos/", response_model=list[TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = get_todos(db, skip=skip, limit=limit)
    return todos

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = update_todo(db, todo_id, title=todo.title, description=todo.description, completed=todo.completed)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    db_todo = delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
