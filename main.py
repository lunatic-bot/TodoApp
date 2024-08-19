
import os
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from database import init_db, get_db
import crud
from schemas import TodoResponse, TodoCreate, TodoUpdate, UserCreate, UserResponse, Token
from models import TodoItem, User

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse

from pytz import timezone



from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from auth import verify_password, get_password_hash
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

import pandas as pd
from io import StringIO
import shutil



# from config import settings


app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the database
init_db()

## USER ROUTES
##################################################################

# JWT settings
SECRET_KEY = "57168498522b9b42531f34be15dcd8d7e1a5fe14261c7d80e82cb9cdac26bd6b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class TokenMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         token = request.cookies.get("access_token")
#         if token:
#             try:
#                 token = token.replace("Bearer ", "")
#                 payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#                 request.state.user = payload.get("sub")
#             except jwt.ExpiredSignatureError:
#                 request.state.user = None
#             except jwt.InvalidTokenError:
#                 request.state.user = None
#         else:
#             request.state.user = None
        
#         try:
#             response = await call_next(request)
#         except Exception as e:
#             # Log the exception and optionally return a response
#             print(f"Error in call_next: {e}")
#             response = JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
#         # response = await call_next(request)
#         return response

# app.add_middleware(TokenMiddleware)

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        if token:
            try:
                token = token.replace("Bearer ", "")
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user = payload.get("sub")
            except jwt.ExpiredSignatureError:
                request.state.user = None
            except jwt.InvalidTokenError:
                request.state.user = None
            except Exception as e:
                request.state.user = None
                print(f"Error decoding JWT: {e}")
        else:
            request.state.user = None

        try:
            response = await call_next(request)
        except Exception as e:
            print(f"Error in call_next: {e}")
            response = JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
        
        return response

app.add_middleware(TokenMiddleware)
#####################################################################################
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


@app.post("/users/signup", response_model=UserResponse)
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...),
    confirm_password: str = Form(...), db: Session = Depends(get_db)):

    if password != confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    # Check if user already exists
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # hashed_password = pwd_context.hash(user.password)
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return new_user
    #  Redirect to the login page after successful signup
    return RedirectResponse(url='/users/login', status_code=302)


@app.get('/users/signup')
def get_login_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})    



@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print("form dtaa", form_data.username, form_data.password)
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print("Login failed: Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    response = RedirectResponse(url='/redirect-to-home', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    print("Access token set in cookie:", access_token)
    return response
    # return {"access_token": access_token, "token_type": "bearer"}



@app.get("/redirect-to-home")
async def redirect_to_home(request: Request):
    # This endpoint handles redirection after setting the cookie
    return RedirectResponse(url='/')



@app.get("/users/login")
def get_login_page(request: Request):
    # Get the message from query parameters, if any
    message = request.query_params.get("message", "")
    return templates.TemplateResponse("login.html", {"request": request, "message": message})
    # return templates.TemplateResponse("login.html", {"request": request})    


# @app.get("/logout")
# def logout(request: Request):
#     response = RedirectResponse(url="/users/login")
#     response.delete_cookie("access_token")  # Remove the access token cookie
#     return response

@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url='/users/login?message=You%20have%20been%20logged%20out')
    response.delete_cookie("access_token")
    return response




@app.get("/", response_class=HTMLResponse)
def read_todos(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    print("getting todos : ")
    print("Current user:", current_user)
    # if isinstance(current_user, RedirectResponse):
    #     print("Current user : ", current_user)
    #     return current_user

    if not current_user:
        # Redirect to login page if not authenticated
        return RedirectResponse(url='/users/login?message=Please%20log%20in%20to%20continue', status_code=302)
    
    user = crud.get_user_by_mail(db, email=current_user.email)
    todos, total_todos = crud.get_all_todos_for_user(db, skip, limit, user_id=user.id)
    # return {"todos": todos, "total": total_todos, "skip": skip, "limit": limit}
    return templates.TemplateResponse("index.html", {
            "request": request,
            "todos": todos,
            "total": total_todos,
            "skip": skip,
            "limit": limit,
            'current_user': current_user
        })



@app.post("/todos/add-todo", tags=["Todos"])
async def add_todo(request: Request, todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # print("Create todo was called.")
    user = crud.get_user_by_mail(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_todo = crud.create_todo_for_user(db=db, todo=todo, user_id=current_user.id)
    return db_todo



@app.put("/todos/update-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/delete-todo/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.put("/todos/toggle-complete/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    print(f"Received request to toggle completion status for todo ID: {todo_id}")
    db_todo = crud.toggle_todo_completed_status(db, todo_id)
    if db_todo is None:
        print(f"Todo with ID {todo_id} not found.")
        raise HTTPException(status_code=404, detail="Todo not found")
    
    print(f"Todo with ID {todo_id} status toggled successfully.")
    return db_todo



@app.get("/about", tags=["About"])
def get_about(request : Request):
    return templates.TemplateResponse("about.html", {"request": request})




@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return HTMLResponse(content=templates.get_template('404.html').render(), status_code=status.HTTP_404_NOT_FOUND)
    # return await request.app.default_exception_handler(request, exc)
    return {"request": request, "exception": exc}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return HTMLResponse(content="Invalid request", status_code=status.HTTP_400_BAD_REQUEST)



upload_directory = r"C:\Users\atalb\Documents\Coding\FastAPI\ToDoApp\UploadedFiles"

@app.post("/uploadfile")
async def upload_file(file: UploadFile, current_user: User = Depends(get_current_user)):
    uploadFilename = f"User_{current_user.id}_{file.filename}"
    file_location = f"{upload_directory}/{uploadFilename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"info": f"file '{uploadFilename}' saved at '{file_location}'"}





@app.get("/todos/add-from-file")
async def add_todos_from_file(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Get the most recent file uploaded by the user (assuming only one file is uploaded at a time)
    # user_filename = f"{current_user.id}_uploaded_file.csv"
    # uploadFilename = f"User_{current_user.id}_{file.filename}"
    userFile = None
    UserFilePrefix = f"User_{current_user.id}"
    for filename in os.listdir(upload_directory):
        if filename.startswith(UserFilePrefix):
            userFile = os.path.join(upload_directory, filename)
            break
    

    # Check if the file exists
    if not userFile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No uploaded file found for the user"
        )

    # Read the file using pandas
    try:
        df = pd.read_csv(userFile)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error reading the file: {str(e)}"
        )

    # Validate the dataframe (assuming it has 'title' and 'description' columns)
    if 'title' not in df.columns or 'description' not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="The file must contain 'title' and 'description' columns"
        )

    # Iterate over each row and create a Todo for the current user
    for _, row in df.iterrows():
        title=row['title'], 
        description=row['description']
        if title and description:
            todo = TodoCreate(
                title=title,
                description=description
            )

            ## create todo
            created_todo = crud.create_todo_for_user(db=db, todo=todo, user_id=current_user.id)         

    # return JSONResponse(content={"status":"Todos added from file"}, status_code=200)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
