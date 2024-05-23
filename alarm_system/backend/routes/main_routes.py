from flask import render_template, request, redirect, url_for, Blueprint, session
from alarm_system.backend.database.db import Mysqldb

from config import SECRET_KEY

main_bp = Blueprint('main', __name__)


mysql = Mysqldb()

@main_bp.route('/')
def index():
    return render_template('index.html')

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
    

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/signin_request', methods=['POST'])
def signin_request():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        if mysql.authenticate_manager(email, password):
            session['userid'] = email
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.login'))
    else:
        return "invalid access"