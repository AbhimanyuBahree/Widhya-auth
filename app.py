from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_mail import Mail, Message
import sendgrid
import os
#import pymongo
#import dns
from forms import *
#from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
def send_mail(users, name, email, ph_num, field):
	sg = sendgrid.SendGridAPIClient(apikey = os.environ.get("SG_API_KEY"))
	from_email = sendgrid.helpers.mail.Email("widhya.org@gmail.com", name="Widhya Org")
	#print(subject_given.split("-")[0])
	to_email = sendgrid.helpers.mail.Email("rahuldravid313@gmail.com")
	#print(to_email)
	subject = "Subscribers List "
	mail_content = "Name : <b>%s</b> <br>Email ID : <b>%s</b> <br>Number : <b>%s</b> <br>Field Of Interest : <b>%s</b> <br>"%(name, email, ph_num, field)
	content = sendgrid.helpers.mail.Content("text/html", "<html><body><p>Thanks for actually using this particular thingy. I hope you're doing good! Thank those who actually agreed to use this particular website.</p> <br> <pre>%s</pre></body></html>"%(mail_content))
	mail = sendgrid.helpers.mail.Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	return response


DEBUG = True
app = Flask(__name__)	#initialising flask
app.config.from_object(__name__)	#configuring flask
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SECURITY_PASSWORD_SALT']='djkwendfjknnin'
#@app.teardown_request is important for db to update password in password reset
@app.teardown_request
def teardown(res_or_exc):
    db.session.remove()
    return res_or_exc
#app.config['MONGOALCHEMY_DATABASE'] = 'widhyadb'
#app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://admin:1234@widhyadb-hhg3l.mongodb.net/test?retryWrites=true'
#db=MongoAlchemy(app)

#client = pymongo.MongoClient("mongodb+srv://admin:1234@widhyadb-hhg3l.mongodb.net/test?retryWrites=true&w=majority")
#print(client)
#db = client.widhyadb

#print(db.ddede)
#print('yo\n')
#print(type(db.efef))
#db.test.insert_one({"item": "canvas"})
db=SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'

db.init_app(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_USERNAME']='nidhi.bahree@gmail.com'
app.config['MAIL_PASSWORD']='babubabu2611'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_SUPPRESS_SEND']=False
mail=Mail(app)



login_manager = LoginManager()
login_manager.login_view='auth.index'
login_manager.init_app(app)


from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#app = Flask(__name__)




from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from student import student as student_blueprint
app.register_blueprint(student_blueprint)

from company import company as company_blueprint
app.register_blueprint(company_blueprint)




'''@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")
'''
@app.errorhandler(500)
def application_error(e):
	return 'Sorry, unexpected error: {}'.format(e), 500

if(__name__ == "__main__"):
	app.run(debug=True)
