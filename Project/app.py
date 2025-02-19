from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from extensions import db
from models import *
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.secret_key = 'quizzify'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///IQ_Vault.db'
app.config['SQLALCHEMY_BINDS'] = {
    'IQ_Vault_db': 'sqlite:///IQ_Vault.sqlite3',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

upload_folder="static/images"
app.config['UPLOAD_FOLDER'] = upload_folder
ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
# def tempInput():
#     return render_template('tempInput.html', activePage='tempInput')
def index():
    if "user_id" in session and "username" in session and User.query.get(session["user_id"]):
        quizes=Quizes.query.all()
        print(User.query.get(session["user_id"]))
        return render_template('index.html', activePage='index', quizes=quizes, user=User.query.get(session["user_id"]))
    else:
        return redirect(url_for('auth'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form['action']  # Check if it's login or register

        if action == 'login':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session["user_id"] = user.id
                session["username"]=user.username
                return redirect(url_for('index'))
            else:
                flash("Invalid login credentials", "error")

        elif action == 'register':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash("Username already exists", "error")
            else:
                email=request.form['email']
                new_user = User(email=email, username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful! Please log in.", "success")
                initializeSubjectScore(new_user.id)
                return redirect(url_for('auth'))
    return render_template('auth.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# @app.route("/quizInput")
# def quizInput():
#     if request.method == 'POST':
#         quizSubject=request.form['subject']
#         quizTitle = request.form['quizName']
#         maxMarks=request.form['MaxMarks']
#         topics="|".join(request.form.getlist('topics[]'))
#         # thumbnail=
#         if quizSubject and quizTitle and maxMarks:
#             quiz=Quizes(subject=quizSubject, title=quizTitle,maxMarks=int(maxMarks), topicsCovered=topics)
#             db.session.add(quiz)
#             db.session.commit()
#     return "<h1>HIIIII</h1>"

#CHECK USERSUBJECTSCORES AFTER DOING USER LOGIN AND AUTH
@app.route("/quizDetails/<int:quiz_id>")
def quizDetails(quiz_id):
    quiz=Quizes.query.get(quiz_id)
    questions=Questions.query.filter_by(quiz_id=quiz_id).all()
    return render_template('quizdetails.html', activePage='quizDetails', quiz=quiz, questions=questions, subjectScore=UserSubjectScores.query.filter_by(subject=quiz.subject).first() if UserSubjectScores.query.filter_by(subject=quiz.subject).first() else None, user=User.query.get(session["user_id"]))

@app.route("/quizAttempt/<int:quiz_id>")
def quizAttempt(quiz_id):
    quiz=Quizes.query.get(quiz_id)
    print(quiz)
    questions=Questions.query.filter_by(quiz_id=quiz_id).all()
    questions_data = [
        {
            "id": q.id,
            "question": q.question,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct": q.correct,
            "marks": q.marks
        } for q in questions
    ]
    quiz_data={
        "id": quiz.id,
        "subject": quiz.subject,
        "title": quiz.title,
        "maxMarks": quiz.maxMarks,
        "duration" : quiz.quizDuration
    }
    return render_template('quizAttempt.html', activePage='quizAttempt', quiz=quiz_data, questions=questions_data)

@app.route("/about")
def about():
    return render_template('about.html', activePage='about', user=User.query.get(session["user_id"]))

@app.route("/myQuizes")
def myQuizes():
    user_id = session['user_id']
    user = User.query.get(user_id)
    quizes = UserQuizes.query.filter_by(user_id=user_id).all()
    recent_quizes= UserQuizes.query.filter_by(user_id=user_id).order_by(UserQuizes.id.desc()).limit(3)
    return render_template('myQuizes.html', activePage="myQuizes", user=user, user_quizes=quizes, recent_quizes=recent_quizes)
#WORKING
@app.route("/create_quiz/quizDetails", methods=["GET", "POST"])
def create_quizDetails():
    if request.method == "POST":
        quizSubject = request.form['subject']
        quizTitle = request.form['title']
        quizDifficulty=request.form['difficulty']
        quizDuration=request.form['duration']
        thumbnail=request.files['thumbnail']
        filename=secure_filename(thumbnail.filename)
        if quizSubject and quizTitle and quizDifficulty:
            thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            quiz=UserQuizes(subject=quizSubject, title=quizTitle, user_id=session.get("user_id"), username=session.get("username"), difficulty=quizDifficulty, quizDuration=quizDuration, thumbnail=filename)
            db.session.add(quiz)
            db.session.commit()
            return redirect(url_for('create_quizQuestions', quiz_id=quiz.id))
        else:
            return "Please fill all the fields", 400
    return render_template('addQuiz.html', activePage='addQuiz', user=User.query.get(session["user_id"]))

@app.route("/create_quiz/<int:quiz_id>/questions", methods=["GET", "POST"])
def create_quizQuestions(quiz_id):
    if request.method == "POST":
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct = request.form['correct']
        marks = request.form['marks']
        explanation= request.form['explanation']
        if question and option1 and option2 and option3 and option4 and correct and marks:
            question = UserQuestions(question=question, option1=option1, option2=option2, option3=option3, option4=option4, correct=correct, marks=marks, quiz_id=quiz_id , explanation=explanation)
            db.session.add(question)
            db.session.commit()
    return render_template('addQuestions.html', activePage='addQuestions', quiz_id=quiz_id, questions=UserQuestions.query.filter_by(quiz_id=quiz_id).all(), quiz=UserQuizes.query.get(quiz_id), user_id=session.get("user_id"))

@app.route("/create_quiz/finished/<int:quiz_id>")
def create_quizFinished(quiz_id):
    quiz= UserQuizes.query.get(quiz_id)
    questions= UserQuestions.query.filter_by(quiz_id=quiz_id).all()
    maxMarks=0
    for q in questions:
        maxMarks+=int(q.marks)
    quiz.maxMarks=maxMarks
    db.session.commit()
    return redirect(url_for('myQuizes'))

@app.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    quiz = UserQuizes.query.filter_by(id=quiz_id, user_id=session["user_id"]).first()
    print(quiz)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
    return redirect(url_for('myQuizes'))

@app.route("/userQuizDetails/<int:quiz_id>")
def userQuizDetails(quiz_id):
    quiz=UserQuizes.query.get(quiz_id)
    questions=UserQuestions.query.filter_by(quiz_id=quiz_id).all()
    # return render_template('quizdetails.html', activePage='quizDetails', quiz=quiz, questions=questions)
    return render_template('quizdetails.html', activePage='quizDetails', quiz=quiz, questions=questions, subjectScore=UserSubjectScores.query.filter_by(subject=quiz.subject).first() if UserSubjectScores.query.filter_by(subject=quiz.subject).first() else None, user=User.query.get(session.get("user_id")))

@app.route("/userQuizAttempt/<int:quiz_id>")
def userQuizAttempt(quiz_id):
    quiz=UserQuizes.query.get(quiz_id)
    questions=UserQuestions.query.filter_by(quiz_id=quiz_id).all()
    questions_data = [
        {
            "id": q.id,
            "question": q.question,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct": q.correct,
            "marks": q.marks
        } for q in questions
    ]
    quiz_data={
        "id": quiz.id,
        "user_id":quiz.user_id,
        "subject": quiz.subject,
        "title": quiz.title,
        "maxMarks": quiz.maxMarks,
        "duration" : quiz.quizDuration
    }
    print(questions_data)
    return render_template('quizAttempt.html', activePage='quizAttempt', quiz=quiz_data, questions=questions_data)

def initializeSubjectScore(user_id):
    quizes=Quizes.query.all()
    subjects=[]
    for quiz in quizes:
        subject=quiz.subject
        if subject not in subjects:
            subjects.append(subject)

    for subject in subjects:
        if not UserSubjectScores.query.filter_by(user_id=user_id, subject=subject).first():
            subject_score = UserSubjectScores(user_id=user_id, subject=subject, score=0, maxMarks=0)
            db.session.add(subject_score)
            db.session.commit()


@app.route('/result', methods=['POST'])
def result():
    user_id=session["user_id"]
    score = int(request.form['score'])
    total_score = Quizes.query.filter_by(id=request.form['quizID']).first().maxMarks
    correct_count = request.form['correctCount']
    wrong_count= request.form['wrongCount']
    quiz = Quizes.query.get(request.form['quizID'])

    score_percent = (score / total_score)*100
    badge="none"
    if score_percent == 100:
        badge = "Gold"
    elif score_percent >= 90:
        badge = "Silver"
    elif score_percent >= 75:
        badge = "Bronze"

    subject = quiz.subject
    print("User ID :", user_id)

    if not UserScore.query.filter_by(user_id=user_id, quiz_id=request.form['quizID']).first():
            if UserSubjectScores.query.filter_by(user_id=user_id, subject=subject).first():
                subject_score = UserSubjectScores.query.filter_by(user_id=user_id, subject=subject).first()
                if score/total_score >= 0.75:
                    subject_score.topicsMastered+="|"+quiz.title
            else:
                subject_score = UserSubjectScores(user_id=user_id, subject=subject, score=0, maxMarks=0, topicsMastered=quiz.title)
                db.session.add(subject_score)
            if subject_score:
                subject_score.score += score
                subject_score.maxMarks += total_score
            db.session.commit()

    #Adding Quiz Score
    if UserScore.query.filter_by(user_id=user_id, quiz_id=request.form['quizID']).first():
        user_score = UserScore.query.filter_by(user_id=user_id, quiz_id=quiz.id).first()
        user_score.score=score
        user_score.maxMarks=total_score
    else:
        quiz_score = UserScore(user_id=user_id, quiz_id=request.form['quizID'], score=score, badges=badge)
        db.session.add(quiz_score)
    db.session.commit()
    return render_template('result.html', score=score, total_score=total_score, correct_count=correct_count, wrong_count=wrong_count, badge=badge, subject=subject, score_percentage=score_percent)

@app.route("/resultUserQuizes", methods=['GET', 'POST'])
def resultUserQuizes():
    user_id=session["user_id"]
    score = int(request.form['score'])
    total_score = UserQuizes.query.filter_by(id=request.form['quizID']).first().maxMarks
    correct_count = request.form['correctCount']
    wrong_count= request.form['wrongCount']
    quiz = UserQuizes.query.get(request.form['quizID'])

    score_percent = (score / total_score)*100
    badge="none"
    if score_percent == 100:
        badge = "Gold"
    elif score_percent >= 90:
        badge = "Silver"
    elif score_percent >= 75:
        badge = "Bronze"

    subject = quiz.subject
    print("Score :", score, "Total Score :", total_score)
    return render_template('result.html', score=score, total_score=total_score, correct_count=correct_count, wrong_count=wrong_count, badge=badge, subject=subject, score_percentage=score_percent, user=User.query.get(session.get("user_id")))

@app.route("/achievements")
def achievements():
    user_id = session["user_id"]
    initializeSubjectScore(user_id)
    userSubjectScores=UserSubjectScores.query.filter_by(user_id=user_id).all()
    return render_template('achievements.html', userSubjectScores=userSubjectScores, user=User.query.filter_by(id=user_id), activePage="achievements")

@app.route('/subjectPage/<subject>')
def subject_page(subject):
    quizes=Quizes.query.filter_by(subject=subject).all()
    subjectScore=UserSubjectScores.query.filter_by(subject=subject, user_id=session["user_id"]).first()
    return render_template('subjectPage.html', subject=subject, quizes=quizes, activePage="subjectPage", user=User.query.filter_by(id=session["user_id"]).first(), subjectScore=subjectScore)

@app.route("/settings")
def settings():
    return render_template('settings.html', user=User.query.filter_by(id=session["user_id"]).first(), activePage="settings")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)