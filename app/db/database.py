from sqlalchemy import create_engine  # Import function to create the SQLAlchemy engine
from sqlalchemy.orm import sessionmaker  # Import sessionmaker to handle database sessions
from sqlalchemy.ext.declarative import declarative_base  # Import base class for models

# Base class for all database models. All models will inherit from this.
Base = declarative_base()


import os

if os.getenv("WEBSITE_SITE_NAME"):  # running in Azure
    db_path = "/home/db/db.sqlite3"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
else:  # local dev
    db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

# URL for connecting to the SQLite database (file-based)
# SQLALCHEMY_DATABASE_URL = "sqlite:////home/site/wwwroot/app/db.sqlite3"#"sqlite:///C:/Users/atalb/Documents/Coding/FastAPI/ToDoApp/todo.db"  # Path to your SQLite database file

# Create the SQLAlchemy engine with the provided database URL.
# 'check_same_thread=False' is required for SQLite in multi-threaded environments.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "SessionLocal" class. Each instance of SessionLocal will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function that provides a database session for FastAPI routes.
def get_db():
    """
    Dependency that provides a SQLAlchemy database session.
    Ensures that the session is properly closed after the request is handled.
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the caller
    finally:
        db.close()  # Ensure the session is closed after the request is complete
