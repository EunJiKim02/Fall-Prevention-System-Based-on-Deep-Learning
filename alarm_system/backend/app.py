from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
from backend.routes.main_routes import main_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_bp, url_prefix='/')

    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
    socketio.init_app(app)
    
    return app, socketio