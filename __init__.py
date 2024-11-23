from flask import Flask,session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
DB_NAME = "prcapp.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "gveghwijlmrkb"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "apps.login"
    from models import User
    @login_manager.user_loader
    def load_user(id):
        record = User.query.get(int(id))
        return record
    from myapp import myapplication
    app.register_blueprint(myapplication,url_prefix='/')
    if not path.exists("instance/"+DB_NAME):
        with app.app_context():
            db.create_all()
            create_initial_data(db)
    return app
def create_initial_data(db):
    from models import User
    admin = User(
        stored_name="Admin",
        stored_email="admin@prc.org",
        stored_password=generate_password_hash("admin"),
        role="admin",
    )
    db.session.add(admin)
    db.session.commit()