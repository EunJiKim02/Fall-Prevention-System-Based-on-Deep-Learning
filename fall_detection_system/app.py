from fastapi import FastAPI
from fall_detection_system.routes.routes import main_bp

def create_app():
    app = FastAPI()
    app.include_router(main_bp, prefix='')

    return app