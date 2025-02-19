import pandas as pd
from models import *
from extensions import db
from app import app

# Path to the downloaded file
file_path = "C://Users//Aadil Goyal//OneDrive//Desktop//Languages//Python Framework//Flask//Project//QuzAura (1).xlsx"

# Read the Excel file
df_quizes=pd.read_excel(file_path, sheet_name='Quizes', engine="openpyxl")
df_questions = pd.read_excel(file_path, sheet_name="Questions", engine="openpyxl")
df_quizes = df_quizes.dropna(subset=["Subject"])
df_questions = df_questions.dropna(subset=["Question"])



# Display first few rows
print(df_quizes.head())
quizes_list = df_quizes.to_dict(orient="records")
questions_list = df_questions.to_dict(orient="records")


# # Example: Print the first question in a structured format
print(quizes_list)
with app.app_context():
    for row in range(len(quizes_list)):
        quiz=Quizes(
            subject=quizes_list[row]["Subject"],
            title=quizes_list[row]["Title"],
            difficulty=quizes_list[row]["Difficulty"],
            quizDuration=quizes_list[row]["Duration"])
        print(quiz.subject)
        db.session.add(quiz)
        i=0
        maxMarks=0
        for row2 in range(len(questions_list)):
            i+=1
            if row+1==questions_list[row2]["Quiz ID"]:
                maxMarks+=questions_list[row2]["Marks"]
                question=Questions(
                    quiz_id=row+1,
                    question=questions_list[row2]["Question"],
                    option1=questions_list[row2]["Option 1"],
                    option2=questions_list[row2]["Option 2"],
                    option3=questions_list[row2]["Option 3"],
                    option4=questions_list[row2]["Option 4"],
                    correct=questions_list[row2]["Correct"],
                    explanation=questions_list[row2]["Explain"],
                    marks=questions_list[row2]["Marks"]
                )
                db.session.add(question)
        quiz.maxMarks=maxMarks
        db.session.commit()


with app.app_context():
    quizes=Quizes.query.all()
    for quiz in quizes:
        if quiz.subject=="Python":
            quiz.thumbnail="python.jpg"
        elif quiz.subject=="Java":
            quiz.thumbnail="java.jpg"
        elif quiz.subject=="Digital Electronics":
            quiz.thumbnail="DE.png"
        elif quiz.subject=="Applied Soft Computing":
            quiz.thumbnail="asc.jpeg"
        elif quiz.subject=="Javascript":
            quiz.thumbnail="js.jpg"
        elif quiz.subject=="Flask":
            quiz.thumbnail="flask.avif"
        elif quiz.subject=="Azure":
            quiz.thumbnail="azure.avif"
        else:
            quiz.thumbnail="back.jpg"
    db.session.commit()