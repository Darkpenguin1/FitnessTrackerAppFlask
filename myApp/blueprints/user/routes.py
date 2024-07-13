from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from flask import current_app as app
from myApp import db
from myApp.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/")
def home():
    return render_template("home.html")


@user_bp.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        user_email = request.form["email"]
        password = request.form['password']
        
        user = User.query.filter_by(email=user_email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user'] = user.email
            flash("Login Successful!")
            return redirect(url_for("user_bp.user"))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("user_bp.user"))    
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user_bp.user"))

        return render_template("login.html")
    

@user_bp.route("/signup/", methods=["POST", "GET"])
def signup():
    if request.method == "POST":    ## if the user enters there info ie a POST method
        name = request.form["username"]     ## init the name and email var to the info entered on the html form
        email = request.form["email"]
        password = request.form["password"]

        #checkif user already exists
        existing_user = User.query.filter_by(email=email).first()      

        if existing_user:
            flash("User already exists. PLease log in or use a different email")
            return redirect(url_for("user_bp.signup"))
        new_user = User(name, email, password)       ## once we have all the info we need to create a user obj we init it as a new user
        
        try:

            db.session.add(new_user)        ## push the user into the db
            db.session.commit() 
            flash("Signup Succesful please login with your new credentials!")
            return redirect(url_for("user_bp.login"))
        except IntegrityError:
            db.session.rollback()
            flash("ERROR: Unable to create user. Please try again later!")
            return redirect(url_for("user_bp.signup"))

    return render_template("signup.html")       ## if the request is just a get ie when a user just goes to the site (A GET request) we just render the html page

@user_bp.route("/user/", methods=["POST", "GET"])
def user():
    if "user" in session:
        user_email = session["user"]      # init the user in the list of users in the session
        user = User.query.filter_by(email=user_email).first()
        if user:
            return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("user_bp.login"))

@user_bp.route("/logout/")
def logout():
    flash("You have succesfully logged out!", "info")
    if "user" in session:
        user = session["user"]
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("user_bp.login"))

@user_bp.route("/view/")
def view():
    return render_template("view.html", values=User.query.all())




@user_bp.route("/create_exercise/", methods=["GET", "POST"])
def create_exercise():
    return render_template("createExercise.html") 
