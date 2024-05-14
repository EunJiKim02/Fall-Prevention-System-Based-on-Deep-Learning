from flask import render_template, request, redirect, url_for, Blueprint


main_bp = Blueprint('index', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')