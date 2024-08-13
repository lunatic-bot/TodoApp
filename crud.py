# crud.py
from sqlalchemy.orm import Session
from models import TodoItem
from datetime import datetime

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TodoItem).offset(skip).limit(limit).all()

def create_todo(db: Session, title: str, description: str):
    db_todo = TodoItem(title=title, description=description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, title: str, description: str, completed: bool):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo:
        db_todo.title = title
        db_todo.description = description
        db_todo.completed = completed
        if completed and db_todo.completion_time is None:
            db_todo.completion_time = datetime.utcnow()
        elif not completed:
            db_todo.completion_time = None
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
