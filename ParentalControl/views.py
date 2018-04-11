from flask import render_template, url_for

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signIn')
def login():
    return render_template('signIn.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')