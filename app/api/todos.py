# Importing necessary modules from FastAPI, SQLAlchemy, Starlette, and local application components.
from fastapi import Depends, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

# Importing templates, database connection, CRUD operations, Pydantic schemas, models, and authentication functions.
from app.core.templates import templates
from app.db.database import get_db
import app.crud.todos as crud
import app.crud.users as crud_users
from app.schemas.schemas import TodoResponse, TodoUpdate
from app.models.users import User
from app.core.auth import get_current_user

# Creating an API Router for defining routes
from fastapi import APIRouter
router = APIRouter()

# Route to read todos (GET method)
@router.get("/read-todos", response_class=HTMLResponse)
def read_todos(request: Request, skip: int = 0, limit: int = 10, 
               db: Session = Depends(get_db), 
               current_user: str = Depends(get_current_user)):
    # If the user is not authenticated, redirect them to the login page
    if not current_user:
        return RedirectResponse(url='/users/login?message=Please%20log%20in%20to%20continue', status_code=302)
    
    # Fetch user information based on the logged-in user's email
    user = crud_users.get_user_by_mail(db, email=current_user.email)
    
    # Get the user's todos with pagination (skip and limit)
    todos, total_todos = crud.get_all_todos_for_user(db, skip, limit, user_id=user.id)
    
    # Render the template with todos data and user details
    return templates.TemplateResponse("index.html", {
            "request": request,
            "todos": todos,
            "total": total_todos,
            "skip": skip,
            "limit": limit,
            'current_user': current_user
        })

# Route to add a new todo (POST method)
@router.post("/todos/add-todo", response_model=TodoResponse, tags=["Todos"])
async def add_todo(
    title: str = Form(...),  # Collect title from form data
    description: str = Form(...),  # Collect description from form data
    db: Session = Depends(get_db),  # Inject the database session
    current_user: User = Depends(get_current_user)  # Inject the current user from auth
):
    # Fetch user data using the logged-in user's email
    user = crud.get_user_by_mail(db, current_user.email)
    
    # If user is not found, raise a 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Try creating a new todo for the user
    try:
        db_todo = crud.create_todo_for_user(db=db, title=title, description=description, user_id=current_user.id)
        return db_todo
    # Raise an exception if there's an error during creation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route to update an existing todo (PUT method)
@router.put("/todos/update-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    # Update the todo using the CRUD function
    db_todo = crud.update_todo(db, todo_id, todo)
    
    # If the todo is not found, raise a 404 error
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Return the updated todo
    return db_todo

# Route to delete a todo (DELETE method)
@router.delete("/todos/delete-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    # Delete the todo using the CRUD function
    db_todo = crud.delete_todo(db, todo_id)
    
    # If the todo is not found, raise a 404 error
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Return the deleted todo
    return db_todo

# Route to toggle the completion status of a todo (PUT method)
@router.put("/todos/toggle-complete/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    # Toggle the completed status of the todo
    db_todo = crud.toggle_todo_completed_status(db, todo_id)
    
    # If the todo is not found, raise a 404 error
    if db_todo is None:
        print(f"Todo with ID {todo_id} not found.")
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Return the updated todo with toggled completion status
    return db_todo