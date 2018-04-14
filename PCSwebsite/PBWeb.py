from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)


app.config['SECRET_KEY']="secretsecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PBdatabase.db'
db = SQLAlchemy(app)


class Parents(db.Model):
    phone_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20))
    password = db.Column(db.String(40))

    def __int__(self, phone_no, name, email, password):
        self.phone_no = phone_no
        self.name = name
        self.email = email
        self.password = password


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    phone_no = IntegerField('Phone Number', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=40)])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=40)])


class Login(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators={InputRequired(), Length(min=4, max=40)})


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = Parents.query.filter_by(name=form.name.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('dashboard'))
            return "invalid password"
    return render_template("login.html", form=form)


@app.route('/signIn', methods=['POST', 'GET'])
def signIn():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = Parents(phone_no=form.phone_no.data, name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signIn.html", form=form)


if __name__ == '__main__':

    app.run(debug=True)