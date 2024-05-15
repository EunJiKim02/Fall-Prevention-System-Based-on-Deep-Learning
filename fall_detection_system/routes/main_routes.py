from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


# templates 위치 지정
templates = Jinja2Templates(directory="fall_detection_system/templates")

# router 정의
# 기본 web page router (로그인, 메인 화면)
main_routers = APIRouter()


@main_routers.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@main_routers.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})