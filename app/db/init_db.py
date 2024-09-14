from app.db.database import engine, Base

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
