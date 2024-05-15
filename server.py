from fall_detection_system.app import create_app
import uvicorn

app = create_app()

# FastAPI 서버 작동
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)