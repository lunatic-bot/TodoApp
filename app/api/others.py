from fastapi import APIRouter  # Importing APIRouter for routing
from starlette.requests import Request  # Importing Request to handle incoming HTTP requests

from app.core.templates import templates  # Importing templates to render HTML templates

# Create an instance of APIRouter for defining routes
router = APIRouter()

# Define a route for the "/about" page
@router.get("/about")
def get_about(request: Request):
    # Render the "about.html" template and pass the request object to it
    return templates.TemplateResponse("about.html", {"request": request})
