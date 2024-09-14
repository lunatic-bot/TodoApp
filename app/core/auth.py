# auth.py
from passlib.context import CryptContext
from app.db.database import get_db
from fastapi import Depends, HTTPException, status
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.models.users import User
from datetime import datetime, timedelta
from pytz import timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "57168498522b9b42531f34be15dcd8d7e1a5fe14261c7d80e82cb9cdac26bd6b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def get_current_user(request: Request, db: Session = Depends(get_db)):
    print("GET CURRENT USER : ")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.cookies.get("access_token")
        if token:
            token = token.replace("Bearer ", "")
        else:
            raise credentials_exception
        
        print("Token from cookie:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload:", payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone("Asia/Kolkata")) + expires_delta
    else:
        expire = datetime.now(timezone("Asia/Kolkata")) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
