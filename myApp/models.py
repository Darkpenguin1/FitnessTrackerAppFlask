from werkzeug.security import generate_password_hash, check_password_hash
from myApp import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    _id = db.Column(db.Integer, primary_key=True)           # Do I have to assign all these values to nullable equals false even though my html form doesnt allow them
    username = db.Column(db.String(100), nullable=False)    # -- to be null when submitted?
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    exercises = db.relationship('Exercise', backref='user', lazy=True)


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
    

class Exercise(db.Model):       ## A new model to represent the properties of exercise (what will be logged)
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)    
    weight = db.Column(db.Integer, nullable=True)      ## In the future I want the user to be able to input the number of sets and the weight.  
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)     ## I thought about bw exercises and weight should be nullable 
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), name='exercise_user_fk', nullable=False)

    def __init__(self, name, description, user_id, weight=None, date=None):
        self.name = name
        self.description = description
        self.weight = weight
        if date is None:
            self.date = datetime.utcnow()
        else:
            self.date = date
        self.user_id = user_id
             

    def __repr__(self):
        return f'<Exercise {self.name} Description: {self.description}>'
    
