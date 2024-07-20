from werkzeug.security import generate_password_hash, check_password_hash
from myApp import db
from datetime import datetime
from flask_login import UserMixin

# Association table to declare the many to many relationship between (Workout Day and Exercises) A workoutday can use multiple exercises and exercises can be on many days
workout_day_exercise = db.Table('workout_day_exercise', 
    db.Column('workout_day_id', db.Integer, db.ForeignKey('workout_day._id'), primaryKey=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise._id'), primaryKey=True)
)




class User(UserMixin, db.Model):
    __tablename__ = 'user'
    _id = db.Column(db.Integer, primary_key=True)           # Do I have to assign all these values to nullable equals false even though my html form doesnt allow them
    username = db.Column(db.String(100), nullable=False)    # -- to be null when submitted?
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    exercises = db.relationship('Exercise', backref='user', lazy=True)
    workout_plan = db.relationship('WorkoutPlan', backref='user', lazy=True)


    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    ## Since i keep getting an error trying to migrate my db into using "id" i have to override the get_id method to take _id var
    def get_id(self):
        return str(self._id)

    def __repr__(self):
        return f'<User {self.username}>'

    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.setPassword(password)
    
    def __str__(self):
        return self.email


class Exercise(db.Model):       ## A new model to represent the properties of exercise (what will be logged)
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)    
    weight = db.Column(db.Integer, nullable=True)      ## In the future I want the user to be able to input the number of sets and the weight.  
    unit = db.Column(db.String(2), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)     ## I thought about bw exercises and weight should be nullable 
    is_pr = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), name='exercise_user_fk', nullable=False)

    workout_days = db.relationship('WorkoutDay', secondary=workout_day_exercise, lazy='subquery', backref=db.backref('exercises', lazy=True))

    def __init__(self, name, description, user_id, weight=None, unit=None, date=None, is_pr=False):
        self.name = name
        self.description = description
        self.weight = weight
        self.unit = unit
        if date is None:
            self.date = datetime.utcnow()
        else:
            self.date = date
        self.is_pr = is_pr
        self.user_id = user_id
             

    def __repr__(self):
        return f'<Exercise {self.name} Description: {self.description}>'
    
class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plan'
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), name='exercise_user_fk', nullable=False)
    cycle_type = db.Column(db.String, nullable=False)
    cycle_length = db.Column(db.Integer, nullable=False)

    def __init__(self, name, user_id, cycle_type, cycle_length):   # okay so most often times workout plans are in cycle EXAMPLE: Push Pull Legs
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
    exercises = db.relationship('Exercise', secondary=workout_day_exercise, lazy='subquery', backref=db.backref('workout_days', lazy=True))
    
    def __init__(self, workout_plan_id, day_number):
        self.workout_plan_id = workout_plan_id
        self.day_number = day_number

    def __repr__(self):
        return f'<WorkoutDay Plan ID: {self.workout_plan_id}, Day Number {self.day_number}'