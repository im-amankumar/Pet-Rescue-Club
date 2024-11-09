from flask import Blueprint,request, redirect, flash, url_for, session,Response, jsonify
from flask import render_template,send_file
from flask_login import login_required, current_user
from __init__ import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date,timedelta, datetime
from sqlalchemy import or_,and_
from pytz import timezone
myapplication=Blueprint('apps',__name__)


@myapplication.route("/")
def home():
    user=current_user
    if user.is_anonymous:
        user=None
    else:
        user=User.query.filter(User.id==user.id).first()
    return render_template("index.html",user=user)

@myapplication.route("/about")
def about():
    return render_template("about.html")
@myapplication.route("/discover")
def discover():
    return render_template("discover.html")
@myapplication.route("/contact")
def contact():
    return render_template("contact.html")

@myapplication.route("/register",methods=['POST','GET'])
def register():
    if request.method == "POST":
        input_email = request.form.get("email")
        input_name = request.form.get("name")
        input_password = request.form.get("password")
        input_confirm_password = request.form.get("confirm_password")
        input_role=request.form['role']
        email_exists = User.query.filter(User.stored_email==input_email).first()
        username_exists = User.query.filter(User.stored_name==input_name).first()
        
        if email_exists:
            flash('Email is already registered with us. Try to login', category='error')
        elif username_exists:
            flash('Username is already registered with us. Try to use different username', category='error')
        elif input_password != input_confirm_password:
            flash('Password don\'t match! ', category='error')
        elif len(input_name) < 2:
            flash('Username length should be atleast 2', category='error')
        elif len(input_password) < 6:
            flash('Password length should be atleast 6', category='error')
        elif len(input_email) < 4:
            flash('Email address is invalid', category='error')
        else:
            new_user = User(stored_email=input_email, stored_name=input_name, stored_password=generate_password_hash(input_password), role=input_role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User account has been successfully created','success')
            return redirect(url_for('apps.login'))
    return render_template("signup.html")

    

@myapplication.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        input_email = request.form.get("email")
        input_password = request.form.get("password")
        user = User.query.filter(User.stored_email==input_email).first()
        if user:
            if check_password_hash(user.stored_password, input_password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('apps.home'))
            else:
                flash("Password is incorrect!", category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template('login.html')

@myapplication.route('/log-out',methods=['GET'])
@login_required
def sign_out():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect("/")

@myapplication.route("/findpet")
@login_required
def findpet():
    user = current_user
    user_role=User.query.filter(User.id==user.id).first().role
    print(user_role)
    if user_role=='rescue':
        return render_template("shelter.html")
    if user_role=='user':
        return render_template("findpet.html")
    