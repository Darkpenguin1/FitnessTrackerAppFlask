from werkzeug.security import generate_password_hash, check_password_hash
from myApp import db
from datetime import datetime
from flask_login import UserMixin

# Association table for many-to-many relationship between WorkoutDay and Exercises
workout_day_exercise = db.Table('workout_day_exercise', 
    db.Column('workout_day_id', db.Integer, db.ForeignKey('workout_day._id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise._id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', back_populates='user', lazy=True)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self._id)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.setPassword(password)

class Exercise(db.Model):
    __tablename__ = 'exercise'
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(2), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_pr = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)

    workout_days = db.relationship('WorkoutDay', secondary=workout_day_exercise, lazy='subquery', back_populates='exercises')
    

    def __init__(self, name, description, user_id, weight=None, unit=None, date=None, is_pr=False):
        self.name = name
        self.description = description
        self.weight = weight
        self.unit = unit
        self.date = date or datetime.utcnow()
        self.is_pr = is_pr
        self.user_id = user_id

    def __repr__(self):
        return f'<Exercise {self.name} Description: {self.description}>'

class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plan'
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    cycle_type = db.Column(db.String, nullable=False)
    cycle_length = db.Column(db.Integer, nullable=False)

    workout_days = db.relationship('WorkoutDay', back_populates='workout_plan', lazy=True)
    user = db.relationship('User', back_populates='workout_plans')

    def __init__(self, name, user_id, cycle_type, cycle_length):
        self.name = name
        self.user_id = user_id
        self.cycle_type = cycle_type
        self.cycle_length = cycle_length

    def __repr__(self):
        return f'<WorkoutPlan {self.name}>'

class WorkoutDay(db.Model):
    __tablename__ = 'workout_day'
    _id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(db.Integer, db.ForeignKey('workout_plan._id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)

    exercises = db.relationship('Exercise', secondary=workout_day_exercise, lazy='subquery', back_populates='workout_days')
    workout_plan = db.relationship('WorkoutPlan', back_populates='workout_days')

    def __init__(self, workout_plan_id, day_number):
        self.workout_plan_id = workout_plan_id
        self.day_number = day_number

    def __repr__(self):
        return f'<WorkoutDay Plan ID: {self.workout_plan_id}, Day Number {self.day_number}>'
