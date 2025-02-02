from datetime import datetime
from extensions import db

class User(db.Model):
    __bind_key__ = 'users_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1000), unique=True, nullable=False)
    hash_password = db.Column(db.String(1000), nullable=False, unique=True)
    
class Quizes(db.Model):
    __bind_key__ = 'quizes_db'
    id = db.Column(db.Integer, primary_key=True)
    subject=db.Column(db.String(100), nullable=False)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(1000), nullable=True)
    maxMarks=db.Column(db.Integer, nullable=False)
    thumbnail=db.Column(db.String(100), nullable=True)
    questions=db.relationship('Questions', backref='quiz', lazy=True)

class Questions(db.Model):
    __bind_key__ = 'questions_db'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question=db.Column(db.String(1000), nullable=False)
    #Options
    option1=db.Column(db.String(1000), nullable=False)
    option2=db.Column(db.String(1000), nullable=False)
    option3=db.Column(db.String(1000), nullable=False)
    option4=db.Column(db.String(1000), nullable=False)
    #Correct
    correct=db.Column(db.String(1000), nullable=False)
    marks=db.Column(db.Integer, nullable=False)

class UserQuizes(db.Model):
    __bind_key__ = 'userquizes_db'
    id = db.Column(db.Integer, primary_key=True)