from fastapi import APIRouter, Depends, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
from app.core.config import oauth  # import oauth from your config
from app.crud.users import create_user_in_db
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

# Redirect user to Google OAuth login page
@router.get("/auth/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# OAuth callback endpoint
@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    
    # Do something with the user information (store in DB or session)
    user_info = { "email": user['email'], "name": user['name'] }
    print("Google user info : ", user_info)

    user = create_user_in_db(db, user_info["name"], user_info["email"], "test")
    # jwt_token = jwt.encode({"sub": user_info['email']}, SECRET_KEY, algorithm="HS256")
    # return RedirectResponse(url=f"/dashboard?token={jwt_token}")
    
    return RedirectResponse(url="/")  # Redirect to the home page after login
