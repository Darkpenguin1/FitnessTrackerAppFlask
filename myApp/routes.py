from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import current_app as app
from myApp import db
from myApp.models import User
from sqlalchemy.exc import IntegrityError

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        user = request.form["nm"]
        session["user"] = user

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")
    

@app.route("/signup/", methods=["POST", "GET"])
def signup():
    if request.method == "POST":    ## if the user enters there info ie a POST method
        name = request.form["username"]     ## init the name and email var to the info entered on the html form
        email = request.form["email"]
        password = request.form["password"]

        #checkif user already exists
        existing_user = User.query.filter_by(email=email).first()      

        if existing_user:
            flash("User already exists. PLease log in or use a different email")
            return redirect(url_for("signup"))
        new_user = User(name, email, password)       ## once we have all the info we need to create a user obj we init it as a new user
        
        try:

            db.session.add(new_user)        ## push the user into the db
            db.session.commit() 
            flash("Signup Succesful please login with your new credentials!")
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("ERROR: Unable to create user. Please try again later!")
            return redirect(url_for("signup"))

    return render_template("signup.html")       ## if the request is just a get ie when a user just goes to the site (A GET request) we just render the html page

@app.route("/user/", methods=["POST", "GET"])
def user():
    email = None        # init the email to Null
    if "user" in session:
        user = session["user"]      # init the user in the list of users in the session
        if request.method == "POST":    ## if the request is post meaning secure info like logging in 
            email = request.form["email"]   # init email to the email we get from the request form
            session["email"] = email
            flash("Submission successful!")
        else:
            if "email" in session:      # if the session is a GET meaning just a endpoint to the page but they are still logged in save there session email
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    flash("You have succesfully logged out!", "info")
    if "user" in session:
        user = session["user"]
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route("/view/")
def view():
    return render_template("view.html", values=User.query.all())
