from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, jsonify
from flask import current_app as app
from myApp import db
from myApp.models import User, Exercise, WorkoutPlan, WorkoutDay, PR
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/")
def home():
    return render_template("home.html")



@user_bp.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_email = request.form.get("email")
        password = request.form.get('password')
        
        user = User.query.filter_by(email=user_email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash("Login Successful!")
            return redirect(url_for("user_bp.user"))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("user_bp.login"))    
    else:
        if current_user.is_authenticated:
            flash("Already logged in!")
            return redirect(url_for("user_bp.user"))

        return render_template("login.html")

    

@user_bp.route("/signup/", methods=["POST", "GET"])
def signup():
    if request.method == "POST":    ## if the user enters there info ie a POST method
        name = request.form.get("username")     ## init the name and email var to the info entered on the html form
        email = request.form.get("email")
        password = request.form.get("password")

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
@login_required
def user():
    user = current_user
    return render_template("user.html", user=user)


@user_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("You have succesfully logged out!")
    return redirect(url_for("user_bp.login"))

@user_bp.route("/view/")    ## views login info for all users the password for all users is 'pass'
def view():
    users = User.query.all()
    return render_template("view.html", users=users)

# myApp/user/routes.py

@user_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} deleted successfully.", "success")
    else:
        flash(f"User not found.", "error")
    return redirect(url_for("user_bp.view"))


@user_bp.route("/create_workoutPlan/", methods=["GET", "POST"])
@login_required
def create_workoutPlan():
    if request.method == "POST":
        name = request.form.get("name")
        cycle_type = request.form.get("cycle_type")
        cycle_length_str = request.form.get("cycle_length")
        
        if not name or not cycle_type or not cycle_length_str:
            flash("Please fill out the form in its entirety!")
            return redirect(url_for("user_bp.create_workoutPlan"))

        try:
            cycle_length = int(cycle_length_str)

        except ValueError:
            flash("Invalid cycle length")
            return redirect(url_for("user_bp.create_workoutPlan"))

        user_id = current_user._id
        
        new_workoutPlan = WorkoutPlan(name, user_id,cycle_type, cycle_length)
        db.session.add(new_workoutPlan)
        db.session.commit()
        
        for day_number in range(1, cycle_length + 1):
            workout_day = WorkoutDay(workout_plan_id=new_workoutPlan._id, day_number=day_number)
            db.session.add(workout_day)
        db.session.commit()
        flash("WorkoutPlan succesfully Created!")
        
    return render_template("create_workoutPlan.html")

@user_bp.route("/view_workoutPlan/", methods=["GET", "POST"])
@login_required
def view_workoutPlan():
    user_id = current_user._id
    plans = WorkoutPlan.query.filter_by(user_id=user_id).all() 
    return render_template("view_workoutPlans.html", plans=plans)

@user_bp.route("/edit_workoutPlans/<int:plan_id>", methods=["GET", "POST"])
@login_required
def edit_workoutPlans(plan_id):
    user_id = current_user._id
    plan = WorkoutPlan.query.get_or_404(plan_id)
    if request.method == "POST":
        if 'update' in request.form:
            plan.name = plan.request.form.get('name', plan.name)
            plan.cycle_type = plan.request.form.get('cycle_type', plan.cycle_type)
            plan.cycle_length = plan.request.form.get('cycle_length', plan.cycle_length)
            db.session.commit()
        elif 'delete' in request.form:
            db.session.delete(plan)
            db.session.commit()
            return redirect(url_for('view_workoutPlans'))
    return render_template("edit_workoutPlans", plan=plan)


@user_bp.route("/edit_workoutPlan/<int:plan_id>", methods=["GET", "POST"])
@login_required
def edit_workoutPlan(plan_id):
    workout_plan = WorkoutPlan.query.get_or_404(plan_id)
    if workout_plan.user_id != current_user._id:
        flash("You do not have permission to edit this workout plan.")
        return redirect(url_for("user_bp.view_workoutPlan"))
    
    return render_template("workout_planEdit.html", workout_plan=workout_plan)

@user_bp.route("/create_exercise/<int:workoutday_id>", methods=["GET", "POST"])
@login_required
def create_exercise(workoutday_id):
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        weight = request.form.get("weight", None)
        unit = request.form.get("unit", None)

        if not name or not description:
            flash("Name and Description are required.")
            return redirect(url_for("user_bp.create_exercise", workoutday_id=workoutday_id))
        
        user_id = current_user._id
        
        new_exercise = Exercise(name=name, description=description, weight=weight, unit=unit, user_id=user_id)
        workout_day = WorkoutDay.query.get(workoutday_id)
        if workout_day:
            workout_day.exercises.append(new_exercise)
            db.session.add(new_exercise)
            db.session.commit()
            flash("Exercise logged")
            
            plan_id = workout_day.workout_plan_id
            return redirect(url_for("user_bp.edit_workoutPlan", plan_id=plan_id))   
        
        flash("Workout day not found")
        return redirect(url_for("user_bp.create_exercise", workoutday_id=workoutday_id))


@user_bp.route("/edit_exercise/<int:workoutday_id>", methods=["GET", "POST"])
@login_required
def edit_exercise(workoutday_id):
    workout_day = WorkoutDay.query.get_or_404(workoutday_id)
    workout_plan = WorkoutPlan.query.get_or_404(workout_day.workout_plan_id)
    if request.method == "POST":
        exercise_id = request.form.get('exercise_id')
        exercise = Exercise.query.get_or_404(exercise_id)
        
        if 'update' in request.form:    
            if exercise in workout_day.exercises:
                exercise.name = request.form.get("name", exercise.name)
                exercise.description = request.form.get("description", exercise.description)
                exercise.weight = request.form.get("weight", exercise.weight)
                exercise.unit = request.form.get("unit", exercise.unit)
                db.session.commit()
                flash("Exercise Succesfully Updated!", 'success')
        elif 'delete' in request.form:
            if exercise in workout_day.exercises:
                workout_day.exercises.remove(exercise)
                db.session.delete(exercise)
                db.session.commit()
                flash("Exercise Deleted Successfully!", 'success')
        
    
    return render_template("workout_planEdit.html", workout_plan=workout_plan)


@user_bp.route("/log_pr/", methods=["GET", "POST"]) ## blank for now
@login_required
def log_pr():
    if request.method == "POST":
        exercise_name = request.form.get("name")
        weight = request.form.get("weight")
        unit = request.form.get("unit")
        date_str = request.form.get("date")
        
        if not exercise_name:
            flash("Name is a required field!")
            return redirect(url_for("user_bp.log_pr"))

        user_id = current_user._id
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format!")
            return redirect(url_for("user_bp.log_pr"))

        pr = PR(user_id=user_id ,exercise_name=exercise_name, weight=weight, unit=unit, date=date)

        db.session.add(pr)
        db.session.commit()

        flash("PR Logged")
        return redirect(url_for("user_bp.user"))
    return render_template("log_pr.html")

@user_bp.route("/view_prs/", methods=["GET", "POST"])
@login_required
def view_prs():
    user_id = current_user._id
    prs = PR.query.filter_by(user_id=user_id).all()
    return render_template("view_prs.html", prs=prs)

@user_bp.route("/api/exercises/", methods=["GET"])
@login_required
def get_exercises():
    user_id = current_user._id
    exercises = db.session.query(PR.exercise_name).filter_by(user_id=user_id).distinct().all()
    exercise_names = [exercise[0] for exercise in exercises]  
    return jsonify(exercise_names)

@user_bp.route("/api/getPRS/", methods=["GET"])
@login_required
def get_prs():
    user_id = current_user._id
    
    # Query to fetch PRs grouped by exercise_name and ordered by date
    prs = db.session.query(
        PR.exercise_name,
        PR.date,
        PR.weight
    ).filter_by(user_id=user_id).order_by(PR.exercise_name, PR.date).all()

    pr_data = {}
    for pr in prs:
        exercise_name = pr.exercise_name
        if exercise_name not in pr_data:
            pr_data[exercise_name] = []
        pr_data[exercise_name].append({
            "date": pr.date.strftime("%Y-%m-%d"),
            "weight": pr.weight
        })
    
    return jsonify(pr_data)


@user_bp.route("/pr_chart/")
@login_required
def view_PRChart():
    return render_template("pr_chart.html")