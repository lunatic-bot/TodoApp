from sqlalchemy.orm import Session
from models import User
from app.core.auth import verify_password
from app.core.auth import get_password_hash


def create_user_in_db(db: Session, username: str, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_mail(db: Session, email: str):
    return db.query(User).filter(User.email ==  email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_mail(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.reset_token == token).first()
    






