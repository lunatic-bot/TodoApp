
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import init_db, get_db
from crud import get_todo_by_id, get_todos, create_todo, update_todo, delete_todo, toggle_todo_completed_status
from schemas import TodoResponse, TodoCreate, TodoUpdate
from models import TodoItem

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse


app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the database
init_db()



@app.get("/", response_class=HTMLResponse)
def read_todos(request: Request, db: Session = Depends(get_db)):
    todos = db.query(TodoItem).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


# main.py
# @app.post("/todos/add-todo", response_model=TodoResponse)
# def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)):
#     return create_todo(db=db, title=todo.title, description=todo.description)


@app.post("/todos/add-todo", tags=["Todos"])
async def add_todo(request: Request, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = create_todo(db=db, title=todo.title, description=todo.description)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return db_todo
    
    # return templates.TemplateResponse("index.html", {"request": request, "todo": db_todo})
    # Redirect to the home page
    # return RedirectResponse(url="/", status_code=303)



@app.get("/todos/get-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_todo_by_id(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.get("/todos", response_model=list[TodoResponse], tags=["Todos"])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = get_todos(db, skip=skip, limit=limit)
    return todos


@app.put("/todos/update-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = update_todo(db, todo_id, title=todo.title, description=todo.description, completed=todo.completed)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/delete-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    db_todo = delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.put("/todos/toggle-complete/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    db_todo = toggle_todo_completed_status(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo



@app.get("/about", tags=["About"])
def get_about(request : Request):
    return templates.TemplateResponse("about.html", {"request": request})
