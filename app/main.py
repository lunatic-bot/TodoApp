import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utlis.exception_handlers import http_exception_handler
from starlette.middleware.sessions import SessionMiddleware
from app.db.database import Base, engine
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

# from config import settings
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# print("base dir: ", BASE_DIR)
# print("Python path:", sys.path)
# print("Current working directory:", os.getcwd())
# print("Files in cwd:", os.listdir(os.getcwd()))
# print("Files in app folder:", os.listdir(os.path.join(os.getcwd(), "app")))

# Static Files Configuration
# Serves static files (CSS, JavaScript, images) from the app/static directory
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Global Exception & Middleware Configuration
# Handle HTTP exceptions across the application
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
# Enable session handling with secret key from environment variables

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Checking database schema...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


session_secret = os.getenv("SESSION_SECRET_KEY")
if not session_secret:
    raise RuntimeError("SESSION_SECRET_KEY environment variable not set!")
app.add_middleware(SessionMiddleware, secret_key=session_secret)

# Import API Routers
# Each router handles a specific domain of the application
from app.api.users import router as users_router
from app.api.todos import router as todos_router
from app.api.others import router as others_router
from app.api.auth_routes import router as auth_router

# Router Registration
# Group API endpoints by domain for better organization
app.include_router(users_router, tags=["Users"])
# Todo management endpoints
app.include_router(todos_router, tags=["Todos"])
# Miscellaneous endpoints
app.include_router(others_router, tags=["Others"])
# Authentication endpoints (no explicit tag for auth routes)
app.include_router(auth_router)




























































# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request: Request, exc: StarletteHTTPException):
#     if exc.status_code == status.HTTP_404_NOT_FOUND:
#         return HTMLResponse(content=templates.get_template('404.html').render(), status_code=status.HTTP_404_NOT_FOUND)
#     # return await request.app.default_exception_handler(request, exc)
#     return {"request": request, "exception": exc}

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return HTMLResponse(content="Invalid request", status_code=status.HTTP_400_BAD_REQUEST)



# upload_directory = r"C:\Users\atalb\Documents\Coding\FastAPI\ToDoApp\UploadedFiles"

# @app.post("/uploadfile")
# async def upload_file(file: UploadFile, current_user: User = Depends(get_current_user)):
#     uploadFilename = f"User_{current_user.id}_{file.filename}"
#     file_location = f"{upload_directory}/{uploadFilename}"
#     with open(file_location, "wb+") as file_object:
#         shutil.copyfileobj(file.file, file_object)
#     return {"info": f"file '{uploadFilename}' saved at '{file_location}'"}





# @app.get("/todos/add-from-file")
# async def add_todos_from_file(
#     db: Session = Depends(get_db), 
#     current_user: User = Depends(get_current_user)
# ):
#     # Get the most recent file uploaded by the user (assuming only one file is uploaded at a time)
#     # user_filename = f"{current_user.id}_uploaded_file.csv"
#     # uploadFilename = f"User_{current_user.id}_{file.filename}"
#     userFile = None
#     UserFilePrefix = f"User_{current_user.id}"
#     for filename in os.listdir(upload_directory):
#         if filename.startswith(UserFilePrefix):
#             userFile = os.path.join(upload_directory, filename)
#             break
    

#     # Check if the file exists
#     if not userFile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail="No uploaded file found for the user"
#         )

#     # Read the file using pandas
#     try:
#         df = pd.read_csv(userFile)
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail=f"Error reading the file: {str(e)}"
#         )

#     # Validate the dataframe (assuming it has 'title' and 'description' columns)
#     if 'title' not in df.columns or 'description' not in df.columns:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="The file must contain 'title' and 'description' columns"
#         )

#     # Iterate over each row and create a Todo for the current user
#     for _, row in df.iterrows():
#         title=row['title'], 
#         description=row['description']
#         if title and description:
#             todo = TodoCreate(
#                 title=title,
#                 description=description
#             )

#             ## create todo
#             created_todo = crud.create_todo_for_user(db=db, todo=todo, user_id=current_user.id)         

#     # return JSONResponse(content={"status":"Todos added from file"}, status_code=200)
#     return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
