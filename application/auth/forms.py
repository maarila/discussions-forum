from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=4, max=48)])
    username = StringField("Username", [validators.Length(min=4, max=24)])
    password = PasswordField("Password", [validators.Length(min=6, max=255)])

    class Meta:
        csrf = False
