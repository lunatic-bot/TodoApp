# crud.py
from sqlalchemy.orm import Session
from models import TodoItem, User
from datetime import datetime
import schemas
from auth import verify_password
from pytz import timezone 

def get_user_by_mail(db: Session, email: str):
    return db.query(User).filter(User.email ==  email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_mail(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user




# Create a new todo associated with a user
def create_todo_for_user(db: Session, title: str, description: str, user_id: int):
    # Create an instance of the SQLAlchemy model
    db_todo = TodoItem(
        title=title,
        description=description,
        user_id=user_id
    )
    
    # Add the model instance to the session
    db.add(db_todo)
    
    # Commit the transaction
    db.commit()
    
    # Refresh the instance to get any auto-generated fields like ID
    db.refresh(db_todo)
    
    # Convert the model instance to a Pydantic schema
    return db_todo

# Get todos for a specific user
def get_todos_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(TodoItem).filter(TodoItem.user_id == user_id).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()

def get_all_todos_for_user(db: Session, skip: int = 0, limit: int = 10, user_id: int = 0):
    todos = db.query(TodoItem).filter(TodoItem.user_id == user_id).offset(skip).limit(limit).all()
    total_todos = db.query(TodoItem).filter(TodoItem.user_id == user_id).count()
    return todos, total_todos


# def request_password_reset(db: Session, ):
def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.reset_token == token).first()
    
    



def create_todo(db: Session, title: str, description: str):
    db_todo = TodoItem(title=title, description=description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


def toggle_todo_completed_status(db: Session, todo_id: int):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo:
        completed = db_todo.completed 
        print("Current comletion status : ", completed)
        if completed:
            db_todo.completed = not completed
            db_todo.completion_time = None
        else:
            db_todo.completed = not completed
            db_todo.completion_time = datetime.now(timezone("Asia/Kolkata"))

        print("Updated status : ", db_todo.completed)
        db.commit()
        db.refresh(db_todo)
    return db_todo



