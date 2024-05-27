from flask import render_template, request, redirect, url_for, Blueprint, session, jsonify
from alarm_system.backend.database.db import Mysqldb

from flask_socketio import SocketIO, emit
import time


alarm_route = Blueprint('alarm', __name__)

def monitor_patients(socketio):
    monitor_query = "SELECT id, name FROM PATIENT WHERE current_status = TRUE"
    while True:
        mysql_socket = Mysqldb()
        patients = mysql_socket.selectall(monitor_query)
        print(patients)
        if len(patients) > 0:
            for patient in patients:
                socketio.emit('warning', {'patient_id': patient[0], 'message': f'Patient {patient[1]} needs attention!'})
        time.sleep(5)  # Check every 5 seconds
