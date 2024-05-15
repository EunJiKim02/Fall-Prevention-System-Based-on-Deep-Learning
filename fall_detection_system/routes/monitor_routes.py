from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

'''
환자 모니터링 정보 받아오는 router
'''


# templates 위치 지정
templates = Jinja2Templates(directory="fall_detection_system/templates")

# 환자의 기본 정보를 계속 받아오는 router
monitor_routes = APIRouter()


# alarm_bp router 연결

# 환자 모니터링 정보 class
class PatientInfo(BaseModel):
    name : str # 이름
    loc : str # 환자 병실 정보
    picture : str # 환자 이미지 url
    nurse : str # 담당 간호사
    info : str # 환자 특이사항


@monitor_routes.post("/send")
def get_data(data : PatientInfo):
    return '전송완료'