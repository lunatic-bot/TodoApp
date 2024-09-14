from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    creation_time = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")))

    # password reset token and its expiration time
    reset_token = Column(String, nullable=True)  
    reset_token_expiration = Column(DateTime, nullable=True)  

    # Relationship with TodoItem
    todos = relationship("TodoItem", back_populates="owner", cascade="all, delete-orphan")