from extensions import db
from app import app  # Import your Flask app and db instance
from models import UserSubjectScores, Quizes, Questions # Import the table model

with app.app_context():  # Ensures we are in an app context
    # Drop the table
    quizes=Quizes.query.all()
    for quiz in quizes:
        db.session.delete(quiz)
    db.session.commit()
