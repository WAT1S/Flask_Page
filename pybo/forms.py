from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired("Subject is require field")])
    content = TextAreaField("Content", validators=[DataRequired("Content is require field")])
    
class AnswerForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired("Content is require field")])
    
class UserCreateForm(FlaskForm):
    username = StringField("username", validators=[DataRequired("Username is require field"), Length(min=3, max=25)])
    password1 = PasswordField("password", validators=[DataRequired("password is require field"), EqualTo("password2","The password is different.")])
    password2 = PasswordField("password", validators=[DataRequired("password is require field")])
    email = EmailField("email", [DataRequired(), Email()])
    
class UserLoginForm(FlaskForm):
    email = EmailField("email", [DataRequired("Email is require field"), Email()])
    password = PasswordField("password", validators=[DataRequired("password is require field")])
    