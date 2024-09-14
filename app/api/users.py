from fastapi import Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from app.schemas.schemas import UserResponse, Token
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pytz import timezone
from email_validator import validate_email, EmailNotValidError

import app.crud as crud
from app.core.templates import templates
from app.db.database import get_db
from app.core.auth import create_access_token, get_current_user, get_password_hash
from app.utlis.utils import generate_reset_token, send_email
from app.models.users import User

from fastapi import APIRouter
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/users/signup", response_model=UserResponse)
async def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...),
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
    
    new_user = crud.create_user_in_db(db, username, email, password)

    # Email content
    subject = "Welcome to the Todo App!"
    body = f"""Hello {username},

                We are excited to have you join our growing community at the Todo App! Your new account has been successfully created, and you are now part of a platform that helps you organize your tasks and achieve your goals effortlessly.

                ### What can you do with the Todo App?

                - **Create and Manage Tasks**: Easily create new tasks and keep track of your progress.
                - **Set Deadlines and Priorities**: Stay on top of your tasks by setting due dates and priority levels.
                - **Organize your Workflow**: Use categories and tags to organize your tasks in the way that works best for you.
                - **Collaborate with Others**: Share tasks and collaborate with teammates, friends, or family members on group projects.

                ### Getting Started

                Here are a few quick steps to help you get started:
                1. Log in to your account using the email and password you provided during registration.
                2. Create your first task by clicking the 'Add Task' button on your dashboard.
                3. Explore the settings section to customize the app based on your personal preferences.

                ### Need Help?

                If you need any assistance or have questions, feel free to reach out to our support team at support@todoapp.com. We’re here to help you make the most out of your experience.

                Thank you once again for choosing the Todo App. We are committed to helping you stay organized and productive.

                Best regards,
                The Todo App Team

                ---

                Follow us on social media for updates and productivity tips:
                - Twitter: @TodoApp
                - Facebook: facebook.com/todoapp
                - Instagram: @todoappofficial
                """

    # Send welcome email
    await send_email(email, subject, body)

    # return new_user
    #  Redirect to the login page after successful signup
    return RedirectResponse(url='/users/login', status_code=302)


@router.get('/users/signup')
def get_login_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})    


@router.post("/token", response_model=Token)
def login_for_access_token(request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # print("form dtaa", form_data.username, form_data.password)
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        error_message = "Incorrect username or password"
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "message": error_message, "message_type": "danger"}
        )
    
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    response = RedirectResponse(url='/redirect-to-home', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    print("Access token set in cookie:", access_token)
    return response
    # return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users/login")
def get_login_page(request: Request):
    # Get the message from query parameters, if any
    message = request.query_params.get("message", "")
    return templates.TemplateResponse("login.html", {"request": request, "message": message, "message_type": "info"})
    # return templates.TemplateResponse("login.html", {"request": request})    

@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url='/users/login?message=You%20have%20been%20logged%20out')
    response.delete_cookie("access_token")
    return response

@router.get("/", response_class=HTMLResponse)
def read_todos(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    print("getting todos : ")
    print("Current user:", current_user)

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




@router.post("/request-password-reset")
async def request_password_reset(request: Request, email: str = Form(...), db:Session = Depends(get_db)):
    print("This 1")
    try:
        email = validate_email(email).email
    except EmailNotValidError as es:
        # raise HTTPException(status_code=400, detail="Invalid email address")
        error_message = "Invalid email address. Please enter a valid email."
        return templates.TemplateResponse("request_password_reset.html", {"request": request, "error_message": error_message})

    print("This 2")
    db_user = crud.get_user_by_mail(db, email)
    if not db_user:
        # raise HTTPException(status_code=404, detail="User not found")
        error_message = "Email not found. Please check the email address you entered."
        return templates.TemplateResponse("request_password_reset.html", {"request": request, "error_message": error_message})
    
    print("This 3")
    
    
    token = generate_reset_token()
    expiration_time = datetime.now(timezone("Asia/Kolkata")) + timedelta(minutes=30)  # Set token to expire in 1 hour
    
    db_user.reset_token = token
    db_user.reset_token_expiration = expiration_time
    
    # Save user changes to the database
    db.commit()

    # Send reset email
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    await send_email(email, "Password Reset", f"Click the link to reset your password: {reset_link}")
    
    # return {"message": "Password reset link has been sent to your email."}
    return templates.TemplateResponse("password_reset_response.html", {"request": request})


@router.get("/request-password-reset", response_class=HTMLResponse)
async def request_password_reset_form(request: Request):
    return templates.TemplateResponse("request_password_reset.html", {"request": request})

@router.get("/reset-password/", response_class=HTMLResponse)
async def get_reset_password_form(token: str, request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@router.post("/reset-password/")
async def reset_password(request: Request, token: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...), db: Session = Depends(get_db)):
    #
    if new_password != confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    # Find the user by the token
    db_user = crud.get_user_by_token(db, token)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Update the user's password and invalidate the token
    db_user.hashed_password = get_password_hash(new_password)
    db_user.reset_token = None 
    db_user.reset_token_expiration = None
    
    # Send confirmation email
    await send_email(db_user.email, "Password Changed", "Your password has been successfully changed. You can now login with your new password.")
    
    # return {"message": "Password has been successfully reset."}
    return templates.TemplateResponse("password_reset_success.html", {"request": request})

