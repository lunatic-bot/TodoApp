from fastapi import Depends, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.templates import templates
from app.db.database import get_db
import app.crud.todos as crud
from app.schemas.schemas import TodoResponse, TodoUpdate
from app.models.users import User
from app.core.auth import get_current_user

from fastapi import APIRouter
router = APIRouter()

@router.get("/read-todos", response_class=HTMLResponse)
def read_todos(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user:
        # Redirect to login page if not authenticated
        return RedirectResponse(url='/users/login?message=Please%20log%20in%20to%20continue', status_code=302)
    
    user = crud.get_user_by_mail(db, email=current_user.email)
    todos, total_todos = crud.get_all_todos_for_user(db, skip, limit, user_id=user.id)
    # return {"todos": todos, "total": total_todos, "skip": skip, "limit": limit}
    return templates.TemplateResponse("index.html", {
            "request": request,
            "todos": todos,
            "total": total_todos,
            "skip": skip,
            "limit": limit,
            'current_user': current_user
        })


## add todo in database
@router.post("/todos/add-todo", response_model=TodoResponse, tags=["Todos"])
async def add_todo(
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = crud.get_user_by_mail(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        db_todo = crud.create_todo_for_user(db=db, title=title, description=description, user_id=current_user.id)
        return db_todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 


@router.put("/todos/update-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/todos/delete-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/todos/toggle-complete/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.toggle_todo_completed_status(db, todo_id)
    if db_todo is None:
        print(f"Todo with ID {todo_id} not found.")
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo