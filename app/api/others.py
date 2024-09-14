from fastapi import APIRouter
from starlette.requests import Request

from app.core.templates import templates

router = APIRouter()

@router.get("/about")
def get_about(request : Request):
    return templates.TemplateResponse("about.html", {"request": request})
