from werkzeug.security import generate_password_hash, check_password_hash
from myApp import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.setPassword(password)
    