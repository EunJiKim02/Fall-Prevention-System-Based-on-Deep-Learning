from flask import render_template, request, redirect, url_for, Blueprint, session, jsonify
from backend.database.db import Mysqldb
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main', __name__)

mysql = Mysqldb()

@main_bp.route('/')
def index():

    return jsonify(
        {
            "users": [
                "a",
                "b",
                "c"
            ]
        }
    )

@main_bp.route('/signup')
def signup():
    return render_template('signup.html')

@main_bp.route('/signup_request', methods=['POST'])
def signup_request():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        info = [email, password, name]

        if mysql.signup(info):
            return redirect(url_for("main.index"))
        else:
            return redirect(url_for("main.signup"))
    else:
        return "invalid access"
    




@main_bp.route('/add_patients', methods=['POST'])
def add_patients():

    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        name = request.form.get('name')
        room = request.form.get('loc')
        nurse = request.form.get('nurse')
        significant = request.form.get('significant')
        risk = request.form.get('risk')

        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(os.getcwd())
                file.save(os.path.join("./frontend/public/assets/PatientsImg", filename))
                img = filename
            else:
                img = None
        else:
            img = None

        info = [name, room, nurse, significant, img ,risk]

        if mysql.insert_patients(info):
            return jsonify({"res": True})
        else:
            return jsonify({"res": False})
    else:
        return jsonify({"res": False})


@main_bp.route('/patients')
def patients():
    # 환자 데이터를 불러와서 json 파일로 전송
    info = mysql.selectall("select * from PATIENT")
    print(info)
    return jsonify({"patients": info})


@main_bp.route('/patient/<int:id>', methods=['GET'])
def get_patient(id):
    patient = mysql.get_patient_info(id)
    if patient:
        return jsonify({"patient": {
            "name": patient[1],
            "loc": patient[2],
            "nurse": patient[3],
            "significant": patient[4],
            "img": patient[5],
            "risk": patient[6]
        }})
    else:
        return jsonify({"error": "Patient not found"}), 404


@main_bp.route('/patient_delete', methods=['POST'])
def patient_delete():
    if request.method == 'POST':
        id = request.json.get('id')
    # 환자 데이터를 불러와서 json 파일로 전송
    info = mysql.delete_patients(id)
    return jsonify({"res": info})



@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/signin_request', methods=['POST'])
def signin_request():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        
        print(email, password)
        if mysql.authenticate_manager(email, password):
            session['userid'] = email
            return jsonify({"res": True})
        else:
            return jsonify({"res": False})
    else:
        return "invalid access"