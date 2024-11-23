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
    stored_view=db.Column(db.Integer,default=0)

class Pet(db.Model,UserMixin):
    __tablename__='pet'
    id=db.Column(db.Integer,primary_key=True)
    stored_name=db.Column(db.String(64),nullable=False)
    stored_category=db.Column(db.String(64),nullable=False)
    stored_breed=db.Column(db.String(64),nullable=False)
    stored_gender=db.Column(db.String(64),nullable=False)
    stored_age=db.Column(db.Integer)
    stored_desc=db.Column(db.String(64),nullable=False,default="No details about the pet!!")
    photo=db.Column(db.String(64))
    added_by=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"))
    adopted_by=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"))
    flag=db.Column(db.Integer,default=0)


    