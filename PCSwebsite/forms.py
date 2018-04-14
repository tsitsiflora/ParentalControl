import datetime

from flask_wtf import FlaskForm 
from wtforms.fields import SelectField, FloatField, TextAreaField, StringField, PasswordField, FileField, BooleanField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired])

class SignUpForm(FlaskForm):
    name = StringField('name' , validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phonenumber = StringField('phonenumber', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    confirmpassword = StringField('password', validators=[DataRequired()])











