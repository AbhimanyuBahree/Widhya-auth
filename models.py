from app import db
import datetime
from flask_login import UserMixin
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    urole=db.Column(db.String(1000))
    confirmed=db.Column(db.Boolean,nullable=False,default=False)
    confirmed_on=db.Column(db.DateTime,nullable=True)
