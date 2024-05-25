from flask import Flask
from alarm_system.backend.routes.main_routes import main_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_bp, url_prefix='/')

    return app