from flask import Blueprint, render_template,redirect,url_for
company = Blueprint('company',__name__)
@company.route("/")
def browse_missions():
    return redirect(url_for('auth.index'))
@company.route("/companydashboard")
def dashboard():
    return render_template('companydashboard.html')
@company.route("/opportunity")
def opportunity():
    return render_template('opportunity.html')
@company.route("/uploadmicrotask",methods=['POST','GET'])
def uploadmicrotask():
    return render_template('uploadmicrotask.html')
@company.route("/signout")
def home():
    return redirect(url_for('auth.index'))
