from backend.app import create_app
from config import SECRET_KEY
import threading
from backend.routes.alarm_routes import monitor_patients

app, socketio = create_app()
app.secret_key = SECRET_KEY


if __name__ == '__main__':
    
    threading.Thread(target=monitor_patients, args=(socketio,)).start()
    #socketio.run(app, debug=True)
    socketio.run(app)


