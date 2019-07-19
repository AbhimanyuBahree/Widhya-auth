from flask import Blueprint, render_template,redirect,url_for,request
from flask_login import login_required
student = Blueprint('student',__name__)
@student.route("/")
def browse_missions():
    return redirect(url_for('auth.index'))
@student.route("/solvemicrotasks")
def solvemicrotasks():
    return render_template('solvemicrotask.html')
@student.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')
@student.route("/dashboardstudent")
@login_required
def dashboardstudent():
    return render_template('dashboard.html',firstname=request.args.get('firstname'))
@student.route("/signout")
def home():
    return redirect(url_for('auth.index'))