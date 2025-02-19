from datetime import datetime
from extensions import db

#ADD TOPICS COVERED IN QUIZES POSSIBLY AS A STRING AND THEN USING SPLIT INTO A LIST TO DISPLAY

class User(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    # quizzes = db.relationship('Quiz', backref='user', lazy=True)
    scores=db.relationship('UserScore', backref='user',lazy=True)
    subjectScores=db.relationship('UserSubjectScores', backref='user',lazy=True)


class Quizes(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__='quizes'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    maxMarks = db.Column(db.Integer, nullable=False, default=10)
    thumbnail = db.Column(db.String(100), nullable=True, default="gk.png")
    # topicsCovered= db.Column(db.String(1000), nullable=False, default="Surprise")
    difficulty=db.Column(db.String(100), nullable=False, default="Easy")
    quizDuration=db.Column(db.String(1000), nullable=False)
    questions = db.relationship('Questions', backref='quiz', cascade="all, delete", lazy=True)
    scores = db.relationship('UserScore', backref='quiz', lazy=True)
    def __repr__(self):
        return f"<Quizes {self.title} ({self.subject})>"

class Questions(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id', ondelete="CASCADE"), nullable=False)
    question = db.Column(db.String(1000), nullable=False)

    # Options
    option1 = db.Column(db.String(1000), nullable=False)
    option2 = db.Column(db.String(1000), nullable=False)
    option3 = db.Column(db.String(1000), nullable=False)
    option4 = db.Column(db.String(1000), nullable=False)

    # Correct Answer
    correct = db.Column(db.String(1000), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    explanation=db.Column(db.String(1000), nullable=True, default="No Explanation for this question")



class UserScore(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__ = 'user_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id', ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    badges=db.Column(db.String(2000), nullable=True, default="No Badges")
    

    # Unique constraint to prevent duplicate scores for the same quiz attempt
    __table_args__ = (db.UniqueConstraint('user_id', 'quiz_id', name='unique_user_quiz'),)

class UserSubjectScores(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__ = 'user_subject_scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    maxMarks=db.Column(db.Integer, nullable=False)
    topicsMastered=db.Column(db.String(1000), nullable=True, default="No Topics Mastered")

    
class UserQuizes(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__ = 'userquizes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    username = db.Column(db.String(100), db.ForeignKey('users.username', ondelete="CASCADE"), nullable=False)
    
    subject = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=True, default="gk.png")
    difficulty=db.Column(db.String(100), nullable=True, default="Easy")
    quizDuration=db.Column(db.String(1000), nullable=False, default="5")
    maxMarks = db.Column(db.Integer, nullable=False, default=10)

    # Relationship with Questions
    questions = db.relationship('UserQuestions', backref='user_quiz',cascade="all, delete", lazy=True)

class UserQuestions(db.Model):
    __bind_key__ = 'IQ_Vault_db'
    __tablename__ = 'userquestions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('userquizes.id', ondelete="CASCADE"), nullable=False)
    question = db.Column(db.String(1000), nullable=False)

    # Options
    option1 = db.Column(db.String(1000), nullable=False)
    option2 = db.Column(db.String(1000), nullable=False)
    option3 = db.Column(db.String(1000), nullable=False)
    option4 = db.Column(db.String(1000), nullable=False)

    # Correct Answer
    correct = db.Column(db.String(1000), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    explanation=db.Column(db.String(1000), nullable=True, default="No Explanation for this question")