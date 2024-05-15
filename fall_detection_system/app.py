from fastapi import FastAPI
from fall_detection_system.routes.main_routes import main_routers
from fall_detection_system.routes.monitor_routes import monitor_routes

# router를 Fast API에 연결

def create_app():
    app = FastAPI()
    app.include_router(main_routers, prefix='')
    app.include_router(monitor_routes)

    return app