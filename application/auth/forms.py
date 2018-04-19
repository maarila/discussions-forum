from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=4)])
    username = StringField("Username", [validators.Length(min=4)])
    password = PasswordField("Password", [validators.Length(min=6)])

    class Meta:
        csrf = False