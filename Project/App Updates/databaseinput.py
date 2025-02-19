from models import Quizes, Questions
from extensions import db
from flask import Flask

# Create Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IQ_Vault.db'  # Update your DB URI
app.config['SQLALCHEMY_BINDS']={

'IQ_Vault_db': 'sqlite:///IQ_Vault.sqlite3',}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the database

# Start the application context
with app.app_context():
    db.create_all()
    for i in range(1):
        subject = input("Enter Subject: ")
        title = input("Enter Title: ")
        maxMarks = int(input("Enter Max Marks: "))
        thumbnail = input("Enter Thumbnail: ")
        topicsCovered = input("Enter Topics Covered: ")

        # Step 1: Add Quiz to DB First
        quiz = Quizes(subject=subject, title=title, maxMarks=maxMarks, thumbnail=thumbnail, topicsCovered=topicsCovered)
        db.session.add(quiz)
        db.session.commit()  # Commit to generate the ID

        # Step 2: Now Add Questions with quiz_id
        n = int(input("No. of questions: "))
        for j in range(n):
            question = input("Enter Question: ")
            option1 = input("Enter Option 1: ")
            option2 = input("Enter Option 2: ")
            option3 = input("Enter Option 3: ")
            option4 = input("Enter Option 4: ")
            correct = input("Enter Correct Answer: ")
            marks = int(input("Enter Marks: "))

            question_entry = Questions(
                quiz_id=quiz.id,  # Assign quiz_id after quiz is added
                question=question,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct=correct,
                marks=marks
            )
            db.session.add(question_entry)

        db.session.commit()  # Commit all questions
        print("Quiz Added Successfully")
