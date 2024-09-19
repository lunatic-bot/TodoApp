from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey  # Import required column types and relationships
from sqlalchemy.orm import relationship  # Import relationship for ORM associations
from datetime import datetime  # Import datetime to manage time-related fields
from pytz import timezone  # Import timezone for setting specific time zones
from app.db.database import Base  # Import the base class for SQLAlchemy models

# Define the TodoItem model, representing the 'todos' table in the database
class TodoItem(Base):
    __tablename__ = 'todos'  # Specify the table name as 'todos'

    # Define the columns for the 'todos' table
    id = Column(Integer, primary_key=True, index=True)  # Primary key for the table, automatically incrementing
    title = Column(String, index=True)  # Title of the todo item, with an index for faster search
    description = Column(String)  # Description of the todo item
    completed = Column(Boolean, default=False)  # Boolean field to indicate whether the todo is completed, defaults to False
    creation_time = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")))  # Creation time with a default of the current time in the 'Asia/Kolkata' timezone
    completion_time = Column(DateTime, nullable=True)  # Completion time, nullable if the todo is not yet completed

    # ForeignKey column linking to the 'users' table, representing the user who owns the todo
    user_id = Column(Integer, ForeignKey("users.id"))

    # Establish a relationship between the TodoItem and the User models
    owner = relationship("User", back_populates="todos")  # This relationship allows easy access to the associated user, linking the TodoItem to the User model
