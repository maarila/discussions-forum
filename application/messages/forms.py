from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField, validators


class MessageForm(FlaskForm):
    name = TextAreaField("Message", [validators.Length(min=2, max=2000)])

    class Meta:
        csrf = False
