from alarm_system.backend.app import create_app
from config import SECRET_KEY
app = create_app()
app.secret_key = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)