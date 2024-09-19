from sqlalchemy.orm import Session
from app.models.todos import TodoItem  # Importing the SQLAlchemy model for todos
from datetime import datetime
import app.schemas.schemas as schemas  # Importing Pydantic schemas for data validation
from pytz import timezone  # Importing timezone support for date and time handling


# Create a new todo associated with a user
def create_todo_for_user(db: Session, title: str, description: str, user_id: int):
    # Create an instance of the SQLAlchemy model for a new Todo item
    db_todo = TodoItem(
        title=title,
        description=description,
        user_id=user_id  # Link the todo to the given user by user_id
    )
    
    # Add the new todo item to the session (pending state)
    db.add(db_todo)
    # Commit the transaction to save the new todo in the database
    db.commit()
    # Refresh the instance to reflect any auto-generated fields (like ID)
    db.refresh(db_todo)
    # Return the created todo item
    return db_todo

# Get todos for a specific user
def get_todos_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    # Query the database for todos that belong to a specific user
    return db.query(TodoItem).filter(TodoItem.user_id == user_id).offset(skip).limit(limit).all()

# Get a specific todo by its ID
def get_todo_by_id(db: Session, todo_id: int):
    # Query the database for a todo item with the specified ID
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()

# Get all todos for a user with pagination (skip and limit)
def get_all_todos_for_user(db: Session, skip: int = 0, limit: int = 10, user_id: int = 0):
    # Query for todos of a specific user with pagination
    todos = db.query(TodoItem).filter(TodoItem.user_id == user_id).offset(skip).limit(limit).all()
    # Get the total count of todos for that user
    total_todos = db.query(TodoItem).filter(TodoItem.user_id == user_id).count()
    # Return both the todos and the total count
    return todos, total_todos

# Create a new todo without associating it with a user
def create_todo(db: Session, title: str, description: str):
    # Create a new todo without a user
    db_todo = TodoItem(title=title, description=description)
    # Add the new todo to the session and commit
    db.add(db_todo)
    db.commit()
    # Refresh to get auto-generated fields
    db.refresh(db_todo)
    return db_todo

# Update an existing todo item
def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    # Query the todo item by its ID
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    # If the todo exists, update its title and description
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        # Commit the changes to the database
        db.commit()
        # Refresh the instance to get updated fields
        db.refresh(db_todo)
    return db_todo

# Delete a todo item by its ID
def delete_todo(db: Session, todo_id: int):
    # Query the todo item by its ID
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    # If the todo exists, delete it from the database
    if db_todo:
        db.delete(db_todo)
        db.commit()  # Commit the transaction to remove the todo
    return db_todo

# Toggle the completed status of a todo item
def toggle_todo_completed_status(db: Session, todo_id: int):
    # Query the todo item by its ID
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    # If the todo exists, toggle the completion status
    if db_todo:
        completed = db_todo.completed  # Check current completion status
        print("Current completion status : ", completed)
        # If the todo is completed, unmark it and reset the completion time
        if completed:
            db_todo.completed = not completed
            db_todo.completion_time = None
        else:
            # If the todo is not completed, mark it as completed and set the completion time
            db_todo.completed = not completed
            db_todo.completion_time = datetime.now(timezone("Asia/Kolkata"))  # Set the time to current time

        print("Updated status : ", db_todo.completed)
        # Commit the changes and refresh the instance
        db.commit()
        db.refresh(db_todo)
    return db_todo
