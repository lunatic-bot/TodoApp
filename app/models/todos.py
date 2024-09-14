from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from app.db.database import Base

class TodoItem(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    creation_time = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")))
    completion_time = Column(DateTime, nullable=True)
    # New field to reference the User who owns this todo
    user_id = Column(Integer, ForeignKey("users.id"))

    # Establish a relationship with the User model
    owner = relationship("User", back_populates="todos")