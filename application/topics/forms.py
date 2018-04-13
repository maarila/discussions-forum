from flask_wtf import FlaskForm
from wtforms import StringField, validators


class TopicForm(FlaskForm):
    title = StringField("Topic", [validators.Length(min=2)])

    class Meta:
        csrf = False
