from flask import Blueprint, render_template,redirect,url_for, request,flash
from app import db
from app import mail
from models import User
from project.token import generate_confirmation_token
from project.token import confirm_token
from flask_mail import Mail,Message
import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user
auth = Blueprint('auth',__name__)
@auth.route("/newpassword/<token>",methods=['POST'])
def newpassword_post(token):
    password=request.form.get('password')
    confirm_password=request.form.get('confirm_password')
    print("Password is "+password)
    print("Confirmed password is "+confirm_password)
    email=confirm_token(token)
    user=User.query.filter_by(email=email).first()
    if password==confirm_password:
        user.password=generate_password_hash(password)
        db.session.add(user)
        db.session.commit() 
        flash('Password has been successfully reset','success')
    else:
        flash('Make sure confirm password and password are same','danger')
        return render_template('newpassword.html')
    return redirect(url_for('auth.index'))
@auth.route("/newpassword/<token>")
def newpassword(token):
    return render_template('newpassword.html')
@auth.route("/reset")
def reset():
    print(url_for('auth.reset', _external=True))
    return render_template('resetpassword.html')
@auth.route("/reset",methods=['POST'])
def reset_post():
    email=request.form.get('email')
    user=User.query.filter_by(email=email).first()
    if user==None:
        flash("Email is not registered. Go to Signup page",'danger')
    else:
        token=generate_confirmation_token(email)
        confirm_url = url_for('auth.newpassword', token=token, _external=True)
        html = render_template('resetmail.html', confirm_url=confirm_url)
        subject="Password Reset"
        msg=Message(subject=subject,sender="nidhi.bahree@gmail.com",recipients=[email,'abhimanyu.bahree@gmail.com'],html=html)
        mail.send(msg)
        flash("Reset password email successfully sent. Go check your email",'success')
    return render_template('resetpassword.html')

@auth.route("/confirm/<token>")
def confirm_email(token):
    try:
        email=confirm_token(token)
    except:
        flash("The confirmation link is invalid or expired",'danger')
    user=User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed",'success')
    else:
        user.confirmed=True
        user.confirmed_on=datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!",'success')
    return redirect(url_for('auth.browse_missions'))
@auth.route("/browse_missions")
def browse_missions():
    #msg=Message(subject="Welcome to Widhya Tech",sender="nidhi.bahree@gmail.com",recipients=["abhimanyu.bahree@gmail.com"])
    #msg.body="successfully registered"
    #mail.send(msg)
    return render_template('browse_missions.html') 
@auth.route("/")
def index():
    return render_template('browse_missions.html')    
@auth.route("/login")
def login():
    return render_template('login.html')
@auth.route("/login",methods=['POST'])
def login_post():
    email=request.form.get('email')
    password=request.form.get('password')
    user=User.query.filter_by(email=email).first()
    if user==None:
        flash('Invalid username or password. Try again','danger')
    else:
        if not user or not check_password_hash(user.password,password):
            flash('Invalid username or password. Try again','danger')
        elif not user.confirmed:
            flash('Please confirm your email id','danger')
        else:
            flash('Successfully logged in!','success')
            print(user.name)
            print(user.urole)
            print(user.password)
            print(user.email)
            login_user(user)
            return redirect(url_for("auth.index"))
    return redirect(url_for('auth.login'))
@auth.route("/signup")
def signup():
    return render_template('signup.html')
@auth.route("/signup",methods=['POST'])
def signup_post():
    email=request.form.get('email')
    name=request.form.get('name')
    password=request.form.get('password')
    urole=request.form.get('urole')
    user=User.query.filter_by(email=email).first()
    if user:
        # Go to <a href="{{url_for('auth.login')}}">Login page</a>
        flash('Email address already exists. ','danger')
    elif urole!="student" and urole!="company":
        flash('Please select role as student or company','danger')
    else:
        new_user=User(email=email,name=name,password=generate_password_hash(password),urole=urole,confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        token=generate_confirmation_token(email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject="Please confirm your email"
        msg=Message(subject=subject,sender="nidhi.bahree@gmail.com",recipients=[email,'abhimanyu.bahree@gmail.com'],html=html)
        mail.send(msg)
        flash('You are successfully registered!','success')
        msg=Message(subject="Welcome to Widhya Tech",sender="nidhi.bahree@gmail.com",recipients=[email,'abhimanyu.bahree@gmail.com'])
        msg.body="Hi "+name+" you are successfully registered"+" as a "+urole+". Your password is "+password
        mail.send(msg)
    return render_template('signup.html')
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.index'))