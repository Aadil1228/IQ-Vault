from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from extensions import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users_db': 'sqlite:///users_db.sqlite3',
    'quiz_db': 'sqlite:///quiz_db.sqlite3'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

@app.route("/")
def index():
    
    return render_template('index.html', activePage='index')

@app.route("/about")
def about():
    return render_template('about.html', activePage='about')

if __name__ == "__main__":
    app.run(debug=True)
