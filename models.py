from datetime import datetime
from __init__ import db
from flask_login import UserMixin
from pytz import timezone 

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id =db.Column(db.Integer, primary_key=True)
    stored_email =db.Column(db.String(64), unique=True, nullable=False)
    stored_name=db.Column(db.String(64),nullable=False)
    stored_password =db.Column(db.String(64), unique=True, nullable=False)
    role = db.Column(db.String(32), nullable=False, default="user")
    def to_dict(self):
        return{
            "id":self.id,
            "email":self.stored_email,
            "name":self.stored_name,
            "role":self.role,
        }
class Message(db.Model, UserMixin):
    __tablename__ = 'message'
    id=db.Column(db.Integer,primary_key=True)
    stored_name=db.Column(db.String(64),nullable=False)
    stored_email =db.Column(db.String(64), nullable=False)
    stored_message=db.Column(db.String(256),nullable=False)
    