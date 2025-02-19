from models import Quizes, Questions
from extensions import db
from flask import Flask
from app import app

with app.app_context():
    db.create_all()
    