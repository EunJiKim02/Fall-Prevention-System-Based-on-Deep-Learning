from flask import Flask
from fall_detection_system.routes.main_routes import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp, url_prefix='/')

    return app