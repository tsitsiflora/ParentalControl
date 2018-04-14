from flask import Flask, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signIn')
def signIn():
    return render_template('signUp.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/macros')
def macros():
    return render_template('macros.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)